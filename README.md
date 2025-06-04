# Course AutoNote Generator

Transform your course transcripts into beautiful, structured study notes using AI-powered processing with Google's Gemini API.

## 🌟 Features

- **AI-Powered Processing**: Uses Google's Gemini AI to intelligently structure raw transcripts into organized study notes
- **Multiple Output Formats**: Export notes as Markdown (.md), HTML (.html), or PDF (.pdf)
- **Batch Processing**: Upload and process multiple transcript files simultaneously
- **Drag & Drop Interface**: User-friendly web interface with drag-and-drop file upload
- **REST API**: Programmatic access for developers
- **Responsive Design**: Modern, mobile-friendly interface
- **File Management**: Automatic cleanup and organized output generation

## 📋 Prerequisites

Before running the application, ensure you have:

- Python 3.8 or higher
- Google Gemini API key
- wkhtmltopdf (for PDF generation)

### Installing wkhtmltopdf

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install wkhtmltopdf
```

**macOS:**
```bash
brew install wkhtmltopdf
```

**Windows:**
Download and install from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html)

## 🚀 Installation

1. **Clone the repository:**
```bash
git clone <github.com/Surjeet4146/course-autonote-generator>
cd course-autonote-generator
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
```

Edit the `.env` file and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
SECRET_KEY=your-secret-key-change-this-in-production
```

5. **Create required directories:**
```bash
mkdir uploads output
```

## 🔑 Getting a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key
5. Add it to your `.env` file

## 🏃‍♂️ Running the Application

1. **Start the Flask development server:**
```bash
python app.py
```

2. **Access the application:**
Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

```
course-autonote-generator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your environment variables (create this)
├── templates/
│   └── index.html        # Main web interface
├── uploads/              # Temporary file storage (auto-created)
├── output/               # Generated notes output (auto-created)
└── README.md            # This file
```

## 🖥️ Usage

### Web Interface

1. **Upload Files**: 
   - Drag and drop transcript files (.txt or .md) onto the upload area
   - Or click "Choose Files" to browse and select files

2. **Configure Settings**:
   - Enter course name (optional)
   - Enter topic/chapter (optional)
   - Select output format (Markdown, HTML, or PDF)

3. **Generate Notes**:
   - Click "Generate Notes"
   - Download will start automatically when processing completes

### API Usage

Send POST requests to `/api/process` with JSON payload:

```bash
curl -X POST http://localhost:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "Your transcript content here...",
    "course_name": "Introduction to Psychology",
    "topic": "Cognitive Behavioral Therapy",
    "format": "markdown"
  }'
```

**Response:**
```json
{
  "success": true,
  "notes": "# Introduction to Psychology\n\n## Cognitive Behavioral Therapy\n\n...",
  "format": "markdown"
}
```

## 📝 Supported File Formats

### Input Files
- `.txt` - Plain text transcripts
- `.md` - Markdown formatted transcripts

### Output Formats
- **Markdown (.md)**: Clean, structured text format
- **HTML (.html)**: Styled web page with professional formatting
- **PDF (.pdf)**: Print-ready document format

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `SECRET_KEY` | Flask secret key for sessions | Change in production |
| `FLASK_ENV` | Flask environment | development |
| `FLASK_DEBUG` | Enable debug mode | True |
| `MAX_CONTENT_LENGTH` | Max file upload size in bytes | 16777216 (16MB) |
| `UPLOAD_FOLDER` | Temporary upload directory | uploads |
| `OUTPUT_FOLDER` | Generated files directory | output |

### Application Settings

You can modify these settings in `app.py`:

- `MAX_CONTENT_LENGTH`: Maximum file upload size
- `ALLOWED_EXTENSIONS`: Supported file extensions
- File storage directories

## 🔧 Development

### Running in Development Mode

```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python app.py
```

### Code Structure

- **`app.py`**: Main Flask application with routes and logic
- **`process_transcript_with_gemini()`**: AI processing function
- **`markdown_to_html()`**: HTML conversion with styling
- **Templates**: Jinja2 templates for web interface

## 🐳 Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

# Install wkhtmltopdf
RUN apt-get update && apt-get install -y wkhtmltopdf && apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN mkdir -p uploads output

EXPOSE 5000
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t course-autonote-generator .
docker run -p 5000:5000 --env-file .env course-autonote-generator
```

## 🚨 Troubleshooting

### Common Issues

1. **PDF Generation Fails**:
   - Ensure wkhtmltopdf is installed and in PATH
   - Check file permissions for output directory

2. **API Key Errors**:
   - Verify your Gemini API key is correct
   - Check API quota and billing status

3. **File Upload Issues**:
   - Check file size limits (default 16MB)
   - Ensure file extensions are .txt or .md

4. **Memory Issues**:
   - Large files may cause memory issues
   - Consider processing files in smaller batches

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Commit changes: `git commit -am 'Add feature'`
5. Push to branch: `git push origin feature-name`
6. Submit a pull request

## 🙏 Acknowledgments

- Google Gemini AI for intelligent text processing
- Flask framework for web application structure
- Bootstrap-inspired styling for modern UI
- Community contributors and testers

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Create a new issue with detailed information
3. Include error logs and system information

---

**Happy Note Taking! 📚✨**