import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from pydantic import BaseModel
from models.generator import generate_responses
from backend.metrics import compute_bertscore, compute_rouge
from backend.analysis import metric_agreement,evaluate_dataset
from backend.analysis import evaluate_dataset
from backend.database import create_tables, save_prompt, save_responses,get_responses_by_prompt,select_best_response,get_all_prompts


app = FastAPI()
create_tables()
@app.get("/")
def home():
    return {"message": "API is running"}
class PromptRequest(BaseModel):
    prompt: str
@app.post("/generate")
def generate(request: PromptRequest):
    prompt_id = save_prompt(request.prompt)
    responses = generate_responses(request.prompt)
    bert_scores = compute_bertscore(request.prompt, responses)
    rouge_scores = compute_rouge(request.prompt, responses)
    save_responses(prompt_id, responses, bert_scores, rouge_scores)
    response_data = []
    for i, r in enumerate(responses):
        response_data.append({
            "text": r,
            "bert_score": bert_scores[i],
            "rouge_score": rouge_scores[i]
        })
    return {
        "prompt_id": prompt_id,
        "responses": response_data
    }
class SelectionRequest(BaseModel):
    response_id: int
@app.get("/responses/{prompt_id}")
def get_responses(prompt_id: int):
    responses = get_responses_by_prompt(prompt_id)
    return {"responses": responses}
@app.post("/select")
def select(request: SelectionRequest):
    success = select_best_response(request.response_id)
    if not success:
        return {"error": "Response not found"}
    return {"message": "Best response saved"}
@app.get("/analysis/{prompt_id}")
def analyze(prompt_id: int):
    responses = get_responses_by_prompt(prompt_id)
    result = metric_agreement(responses)
    return {
        "prompt_id": prompt_id,
        "analysis": result
    }
@app.get("/evaluate")
def evaluate():
    prompt_ids = get_all_prompts()
    result = evaluate_dataset(prompt_ids, get_responses_by_prompt)
    return result
