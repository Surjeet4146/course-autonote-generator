from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import google.generativeai as genai
import os
from werkzeug.utils import secure_filename
import markdown
import pdfkit
from datetime import datetime
import json
import zipfile
import tempfile
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

ALLOWED_EXTENSIONS = {'txt', 'md'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_transcript_with_gemini(transcript_text, course_name="", topic=""):
    """Convert raw transcript to structured notes using Gemini API"""
    prompt = f"""
    Convert this raw course transcript into well-structured study notes in Markdown format.
    
    Course: {course_name}
    Topic: {topic}
    
    Please format the output with:
    1. Clear headings and subheadings
    2. Key concepts highlighted
    3. Important definitions in bullet points
    4. Examples and explanations organized logically
    5. Summary at the end
    
    Make it student-friendly and easy to review for exams.
    
    Transcript:
    {transcript_text}
    
    Output only the formatted Markdown content:
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error processing transcript: {str(e)}"

def markdown_to_html(markdown_text, title="Course Notes"):
    """Convert Markdown to styled HTML"""
    html_content = markdown.markdown(markdown_text, extensions=['extra', 'codehilite'])
    
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f8f9fa;
            }}
            .container {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1, h2, h3 {{
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 5px;
            }}
            h1 {{ font-size: 2.5em; }}
            h2 {{ font-size: 2em; }}
            h3 {{ font-size: 1.5em; }}
            ul, ol {{
                padding-left: 20px;
            }}
            li {{
                margin-bottom: 5px;
            }}
            code {{
                background-color: #f1f2f6;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }}
            pre {{
                background-color: #f1f2f6;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
            }}
            blockquote {{
                border-left: 4px solid #3498db;
                margin: 0;
                padding-left: 20px;
                font-style: italic;
                color: #555;
            }}
            .timestamp {{
                color: #7f8c8d;
                font-size: 0.9em;
                text-align: right;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {html_content}
            <div class="timestamp">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
    </body>
    </html>
    """
    return styled_html

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        flash('No files selected')
        return redirect(url_for('index'))
    
    files = request.files.getlist('files')
    course_name = request.form.get('course_name', '')
    topic = request.form.get('topic', '')
    output_format = request.form.get('output_format', 'markdown')
    
    if not files or all(file.filename == '' for file in files):
        flash('No files selected')
        return redirect(url_for('index'))
    
    processed_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Read and process the transcript
            with open(filepath, 'r', encoding='utf-8') as f:
                transcript_text = f.read()
            
            # Process with Gemini
            processed_notes = process_transcript_with_gemini(transcript_text, course_name, topic)
            
            # Generate output filename
            base_name = os.path.splitext(filename)[0]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            if output_format == 'html':
                output_filename = f"{base_name}_notes_{timestamp}.html"
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                html_content = markdown_to_html(processed_notes, f"{course_name} - {topic}")
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            
            elif output_format == 'pdf':
                output_filename = f"{base_name}_notes_{timestamp}.pdf"
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                html_content = markdown_to_html(processed_notes, f"{course_name} - {topic}")
                
                try:
                    pdfkit.from_string(html_content, output_path)
                except Exception as e:
                    flash(f'PDF generation failed: {str(e)}')
                    continue
            
            else:  # markdown
                output_filename = f"{base_name}_notes_{timestamp}.md"
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(processed_notes)
            
            processed_files.append({
                'original': filename,
                'output': output_filename,
                'path': output_path
            })
            
            # Clean up uploaded file
            os.remove(filepath)
    
    if len(processed_files) == 1:
        return send_file(processed_files[0]['path'], as_attachment=True)
    elif len(processed_files) > 1:
        # Create zip file for multiple outputs
        zip_filename = f"course_notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = os.path.join(app.config['OUTPUT_FOLDER'], zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_info in processed_files:
                zipf.write(file_info['path'], file_info['output'])
        
        return send_file(zip_path, as_attachment=True)
    
    flash('No files were processed successfully')
    return redirect(url_for('index'))

@app.route('/api/process', methods=['POST'])
def api_process():
    """API endpoint for processing transcript text directly"""
    data = request.get_json()
    
    if not data or 'transcript' not in data:
        return jsonify({'error': 'No transcript provided'}), 400
    
    transcript = data['transcript']
    course_name = data.get('course_name', '')
    topic = data.get('topic', '')
    output_format = data.get('format', 'markdown')
    
    try:
        processed_notes = process_transcript_with_gemini(transcript, course_name, topic)
        
        response_data = {
            'success': True,
            'notes': processed_notes,
            'format': output_format
        }
        
        if output_format == 'html':
            response_data['html'] = markdown_to_html(processed_notes, f"{course_name} - {topic}")
        
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)