# Human-in-the-Loop Evaluation System for LLM Responses

## Overview
This project implements a **human-in-the-loop evaluation framework** for language model responses.  
The system generates multiple responses using **DistilGPT2** and compares automated evaluation metrics (**BERTScore** and **ROUGE**) with **human preference rankings**.

The goal is to analyze **how well automated metrics align with human judgement** when evaluating LLM outputs.

---

## Architecture

```
User Prompt
    ↓
Generate Multiple Responses (DistilGPT2)
    ↓
Compute Automatic Metrics (BERTScore, ROUGE)
    ↓
Human Selects Best Response
    ↓
Compare Metric Ranking vs Human Preference
    ↓
Dataset-Level Agreement Evaluation
```

---

## Tech Stack

- Python  
- FastAPI  
- HuggingFace Transformers  
- BERTScore  
- ROUGE  
- SQLite  

---

## Project Structure

```
human-feedback-llm/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── metrics.py
│   ├── analysis.py
│
├── models/
│   └── generator.py
│
├── README.md
└── .gitignore
```

---

## API Endpoints

| Method | Endpoint | Description |
|------|------|------|
| GET | `/` | Check if the API is running |
| POST | `/generate` | Generate multiple responses for a prompt |
| GET | `/responses/{prompt_id}` | Retrieve responses for a prompt |
| POST | `/select` | Select the best response (human feedback) |
| GET | `/analysis/{prompt_id}` | Compare human choice vs metric ranking |
| GET | `/evaluate` | Compute dataset-level agreement statistics |

---

## Evaluation Method

The system evaluates generated responses using:

- **BERTScore** – measures semantic similarity using contextual embeddings.
- **ROUGE** – measures lexical overlap between responses.

Human feedback is used to select the best response, and the system analyzes **agreement between automated metrics and human judgement**.

---

## Example Evaluation Output

```
{
  "total_prompts": 5,
  "bert_agreement_rate": 0.4,
  "rouge_agreement_rate": 0.2
}
```

This indicates how often automated metrics select the same response preferred by humans.

---

## Future Improvements

- Async response generation for faster inference  
- Docker containerization for deployment  
- Support for additional LLMs (e.g., Mistral, Llama)

---