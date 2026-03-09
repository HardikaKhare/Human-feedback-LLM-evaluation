from bert_score import score
from rouge_score import rouge_scorer
def compute_bertscore(reference, candidates):
    P, R, F1 = score(candidates, [reference]*len(candidates), lang="en", verbose=False)
    return F1.tolist()

def compute_rouge(reference, candidates):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)

    scores = []
    for candidate in candidates:
        s = scorer.score(reference, candidate)
        scores.append(s["rougeL"].fmeasure)

    return scores