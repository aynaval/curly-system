# 🚀 Text-to-SQL FastAPI Application

This application provides a Text-to-SQL interface using WatsonX.ai and SQLite, built with FastAPI.

## 📦 Prerequisites

- Python 3.13+
- Docker (optional, for containerized deployment)
- WatsonX.ai API credentials

---

## 💠 Local Development Setup

### 1. Environment Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows (CMD):
venv\Scripts\activate

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configuration

1. Create a `.env` file with your WatsonX.ai credentials:
```properties
WX_AI_API_KEY=your_api_key_here
WX_AI_PROJECT_ID=your_project_id_here
```

2. Ensure the database is initialized:
```bash
cd db_scripts
python create_db.py
```

## 🐳 Docker Deployment

### 1. Build the Docker image:
```bash
docker build -t text-to-sql .
```

### 2. Run the container:
```bash
docker run -d \
  --name text-to-sql \
  -p 8000:8000 \
  -v $(pwd)/db_scripts:/app/db_scripts \
  text-to-sql
```

### 3. Stop and remove the container:
```bash
docker stop text-to-sql
docker rm text-to-sql
```

## ▶️ Running the Application

### Local Development:
```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- API Documentation: http://localhost:8000/docs
- ReDoc Documentation: http://localhost:8000/redoc
- Base URL: http://localhost:8000

## 📊 Database Schema

### Tables

- `sca_event`: 10 rows
- `sca_event_detail`: 10 rows
- `sca_site`: 10 rows
- `sca_site_detail`: 10 rows

## 🔒 Security Notes

- Never commit your `.env` file
- Keep your WatsonX.ai credentials secure
- Use proper access controls in production

## 🧹 Cleanup

### Local Development:
```bash
deactivate  # Exit virtual environment
```

### Docker:
```bash
# Stop and remove container
docker stop text-to-sql
docker rm text-to-sql

# Remove image (optional)
docker rmi text-to-sql
```

