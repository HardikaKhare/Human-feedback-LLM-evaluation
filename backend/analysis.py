def metric_agreement(responses):
    """
    responses = list of dicts containing:
    response_id
    bert_score
    rouge_score
    is_selected
    """
    human_best = None
    bert_best = None
    rouge_best = None
    max_bert = -1
    max_rouge = -1
    for r in responses:
        if r["is_selected"] == 1:
            human_best = r["response_id"]

        if r["bert_score"] > max_bert:
            max_bert = r["bert_score"]
            bert_best = r["response_id"]

        if r["rouge_score"] > max_rouge:
            max_rouge = r["rouge_score"]
            rouge_best = r["response_id"]
    return {
        "bert_agreement": human_best == bert_best,
        "rouge_agreement": human_best == rouge_best
    }
def evaluate_dataset(prompt_ids, get_responses_by_prompt):
    total = 0
    bert_matches = 0
    rouge_matches = 0
    for pid in prompt_ids:
        responses = get_responses_by_prompt(pid)
        human_selected = any(r["is_selected"] == 1 for r in responses)
        if not human_selected:
            continue
        result = metric_agreement(responses)
        total += 1
        if result["bert_agreement"]:
            bert_matches += 1
        if result["rouge_agreement"]:
            rouge_matches += 1
    if total == 0:
        return {"error": "No evaluated prompts yet"}
    return {
        "total_prompts": total,
        "bert_agreement_rate": bert_matches / total,
        "rouge_agreement_rate": rouge_matches / total
    }