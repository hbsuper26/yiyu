# Yiyu Digital Media - Deployment Guide

This project is a Flask application designed for deployment on standard Python hosting environments (e.g., Heroku, AWS, Google Cloud, DigitalOcean, Render).

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Deployment Instructions

### Option 1: Heroku / Render (PaaS)
1. **Login** to your platform.
2. **Create a new app**.
3. **Connect** your repository or upload the files.
4. The platform will detect `requirements.txt` and `Procfile`.
5. **Deploy**.

### Option 2: Traditional Server (VPS/Dedicated)
1. **Install Python & Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run with Gunicorn (Production Server)**:
   ```bash
   gunicorn wsgi:app --bind 0.0.0.0:8000
   ```
   Or use Nginx as a reverse proxy to forward requests to Gunicorn.

## Local Development
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run Server**:
   ```bash
   python app.py
   ```
   Access at `http://localhost:5001`.

## File Structure
- `app.py`: Main application logic.
- `wsgi.py`: Entry point for WSGI servers (Gunicorn).
- `Procfile`: Startup command for PaaS.
- `requirements.txt`: Python dependencies.
- `templates/`: HTML templates.
