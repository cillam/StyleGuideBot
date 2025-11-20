# StyleGuideBot

RAG-based style guide assistant with FastAPI backend and React frontend, deployed on AWS.

## Architecture

[Architecture diagram here]

## Tech Stack

**Backend:** FastAPI, LangChain, OpenAI, Chroma
**Frontend:** React, Vite, TailwindCSS
**Deployment:** AWS Lambda, S3, CloudFront, API Gateway

## Project Structure

- `/backend` - FastAPI API and RAG pipeline
- `/frontend` - React web application
- `/data_processing` - Scripts for ingesting style guides
- `/infrastructure` - Deployment scripts and IaC

## Local Development

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Deployment

See `/infrastructure/README.md` for deployment instructions.

## Demo

[Link to live demo]
[Demo video/GIF]
