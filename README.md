# StyleGuideBot

RAG-based style guide assistant with FastAPI backend and React frontend, deployed on AWS.

## Architecture

[Architecture diagram here]

## Tech Stack

**Backend:**
- FastAPI
- LangChain
- OpenAI API (embeddings)
- Claude API (generation)
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

## Data Source

This project uses content from the [Wikipedia Manual of Style](https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style), retrieved via the [MediaWiki API](https://www.mediawiki.org/wiki/API:Main_page).

**License:** [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)

**Attribution:** Wikipedia contributors

**API Endpoint:** https://en.wikipedia.org/w/api.php

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


This project is for portfolio and educational purposes.
