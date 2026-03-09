from transformers import pipeline
generator = pipeline("text-generation", model="distilgpt2")
def generate_responses(prompt, num_responses=3):
    outputs = generator(
        prompt,
        max_new_tokens=100,
        num_return_sequences=num_responses,
        do_sample=True,
        temperature=0.8,
        top_k=40,
        top_p=0.9,
        repetition_penalty=1.2
        )
    responses = []
    for output in outputs:
        text = output["generated_text"].replace(prompt, "").strip()
        responses.append(text)
    return responses
if __name__ == "__main__":
    prompt = input("Enter a prompt: ")
    results = generate_responses(prompt)
    print("\nGenerated Responses:\n")
    for i, r in enumerate(results, 1):
        print(f"Response {i}:")
        print(r)
        print()