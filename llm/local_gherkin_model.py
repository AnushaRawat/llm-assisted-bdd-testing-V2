import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
LORA_PATH = "../llm/gherkin_lora"

_tokenizer = None
_model = None


def _load_model():
    global _tokenizer, _model

    if _model is not None:
        return

    _tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    _tokenizer.pad_token = _tokenizer.eos_token

    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        device_map="cpu",
        torch_dtype=torch.float32
    )

    _model = PeftModel.from_pretrained(base_model, LORA_PATH)
    _model.eval()


def generate_gherkin(requirement: str) -> str:
    _load_model()

    prompt = f"""<|system|>
You are an expert in converting software requirements into BDD Gherkin scenarios.
Always generate a Feature with one successful and one failed scenario.</s>
<|user|>
{requirement}</s>
<|assistant|>
"""

    inputs = _tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        output = _model.generate(
            **inputs,
            max_new_tokens=400,
            temperature=0.2,
            top_p=0.9,
            do_sample=True,
            eos_token_id=_tokenizer.eos_token_id
        )

    return _tokenizer.decode(output[0], skip_special_tokens=True)
