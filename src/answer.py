from transformers import pipeline
from .arg_validation import validate_int_input


def answer(query: str, k: int) -> None:

    validate_int_input(k, name="k")

    model_name = "Qwen/Qwen3-0.6B"

    generator = pipeline(
        "text-generation",
        model_name,
        dtype="auto",
        device="cpu",
    )
    print("Successfully loaded model and tokenizer.")

    messages = [
        {"role": "user", "content": f"{query}/no_think"},
    ]
    messages = generator(messages, max_new_tokens=3000)[0]["generated_text"]
    print(messages[-1]["content"])



