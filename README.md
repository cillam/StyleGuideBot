# StyleGuideBot

RAG-based style guide assistant with FastAPI backend and React frontend, deployed on AWS.

## Architecture

[Architecture diagram here]

## Tech Stack

**Backend:**
- FastAPI
- LangChain
- OpenAI API (GPT-4 + embeddings)
- Chroma Vector DB

**Frontend:**
- React (Vite)

**Deployment:**
- AWS Lambda (backend)
- AWS S3 + CloudFront (frontend)
- AWS API Gateway

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

Coming soon.....

## Demo

Coming soon.....
