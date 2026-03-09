## Human-in-the-Loop Evaluation System for LLM Responses
This project implements a human-in-the-loop evaluation framework for language model responses. The system generates multiple responses using DistilGPT2 and compares automated evaluation metrics (BERTScore and ROUGE) with human preference.

# Architecture
Prompt
 ↓
LLM generates responses
 ↓
Human selects best response
 ↓
BERTScore + ROUGE evaluation
 ↓
Agreement analysis between human and metrics

# tech stack
Python
FastAPI
Transformers (HuggingFace)
BERTScore
ROUGE
SQLite

# Api endpoints
POST /generate
GET /responses/{prompt_id}
POST /select
GET /analysis/{prompt_id}
GET /evaluate