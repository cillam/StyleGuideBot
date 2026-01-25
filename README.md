# StyleGuideBot

A RAG chatbot that answers questions about the Wikipedia Manual of Style with cited sources.

**Live:** Available upon request

## Overview

StyleGuideBot uses semantic search and AI generation to provide accurate, cited answers to style guide questions. The system retrieves relevant sections from the Wikipedia Manual of Style and uses Claude to synthesize comprehensive answers.

## Architecture

```
User Query
    ↓
[React Frontend] → reCAPTCHA verification
    ↓
[API Gateway] → Rate limiting
    ↓
[Main Lambda (in VPC)]
    ├→ [Embedding Lambda] → OpenAI embeddings
    ├→ [Chroma Vector DB] → Semantic search (S3)
    ├→ [Bedrock Claude] → Answer generation (VPC endpoint)
    └→ [PostgreSQL RDS] → Conversation state (VPC)
```

## Tech Stack

### Backend
- **Framework:** FastAPI with Mangum adapter for Lambda
- **LLM:** AWS Bedrock (Claude Sonnet 4.5)
- **Embeddings:** OpenAI text-embedding-3-small
- **Vector Database:** Chroma
- **Conversation Memory:** PostgreSQL
- **Agent Framework:** LangGraph with checkpointing

### Frontend
- **Framework:** React 18 with Vite
- **Styling:** TailwindCSS
- **Security:** reCAPTCHA v3
- **HTTP Client:** Axios

### Infrastructure (AWS)
- **Compute:** Lambda (main app + embedding function)
- **API:** API Gateway
- **Storage:** S3 (vector database storage)
- **Frontend Hosting:** AWS Amplify
- **Database:** RDS PostgreSQL (conversation state)
- **Networking:** VPC with security groups and endpoints
- **Secrets:** Secrets Manager
- **AI:** Bedrock (Claude access)

### Security Features
- **reCAPTCHA v3:** Bot protection 
- **Rate Limiting:** 
  - 40 requests/hour per IP
  - 20 requests/hour per session
  - 500 requests/day global limit
- **VPC Isolation:** Lambda runs in private VPC
- **Secrets Management:** AWS Secrets Manager
- **HTTPS:** All traffic encrypted via Amplify and API Gateway

## Project Structure

```
StyleGuideBot/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── style_guide.py       # RAG pipeline & agent logic
│   ├── requirements.txt     # Python dependencies
│   ├── requirements-lambda.txt  # Lambda-specific dependencies
│   └── Dockerfile           # Lambda container image
├── embedding_lambda/
│   ├── embedding_lambda.py  # OpenAI embedding + reCAPTCHA handler
│   └── requirements.txt     # Embedding Lambda dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API client
│   │   └── utils/           # Session management
│   ├── package.json
│   └── vite.config.js
├── data_processing/
│   ├── scrape_wikipedia.py  # Wikipedia API scraper
│   ├── chunk_documents.py   # Document chunking
│   └── create_vectorstore.py # Chroma database creation
└── deploy-lambda.sh         # Deployment script
```

## Data Source

This project uses content from the [Wikipedia Manual of Style](https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style), retrieved via the [MediaWiki API](https://www.mediawiki.org/wiki/API:Main_page).

- **License:** [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)
- **Attribution:** Wikipedia contributors
- **API Endpoint:** https://en.wikipedia.org/w/api.php


## Features

- ✅ **Semantic Search:** Finds relevant style guide sections using vector similarity
- ✅ **Cited Answers:** Every response includes source sections from the Manual of Style
- ✅ **Conversation Memory:** Maintains context across multiple questions
- ✅ **Rate Limiting:** Prevents abuse with multi-tier rate limits
- ✅ **Security:** reCAPTCHA verification and VPC isolation
- ✅ **Responsive Design:** Works on desktop, tablet, and mobile

## Limitations & Future Enhancements

**Current Limitations:**
- Single style guide (Wikipedia MOS only)
- No user authentication
- No conversation export/history

**Potential Enhancements:**
- [ ] Multi-style guide support (AP, Chicago, etc.)
- [ ] User accounts with saved conversations
- [ ] Conversation history/export
- [ ] A/B testing for prompt improvements

## License

This project is for portfolio and educational purposes. The Wikipedia Manual of Style content is used under CC BY-SA 4.0 license with proper attribution.


---

**Built as part of a learning project to demonstrate RAG architecture, AWS deployment, and full-stack development skills.**
