from llama_cpp import Llama

llm = Llama(
    model_path="models/qwen2.5-1.5b-instruct-q4_k_m.gguf",
    n_ctx=2048,
    verbose=False,
)

result = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": "You are a helpful cybersecurity assistant."},
        {"role": "user", "content": "How can I protect my account from phishing?"},
    ],
    max_tokens=150,
    temperature=0.2,
)

print(result["choices"][0]["message"]["content"])