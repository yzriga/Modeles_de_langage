import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

SEED = 42  # TODO
torch.manual_seed(SEED)

model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

prompt = "The future of artificial intelligence is"
inputs = tokenizer(prompt, return_tensors="pt")

outputs = model.generate(
    **inputs,
    max_length=50,
)

text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(text)

def generate_once(seed):
    torch.manual_seed(seed)
    out = model.generate(
        **inputs,
        max_length=50,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
    )
    return tokenizer.decode(out[0], skip_special_tokens=True)

for s in [1, 2, 3, 4, 5]:
    print("SEED", s)
    print(generate_once(s))
    print("-" * 40)

def generate_with_penalty(seed, penalty):
    torch.manual_seed(seed)
    out = model.generate(
        **inputs,
        max_length=50,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        repetition_penalty=penalty,
    )
    return tokenizer.decode(out[0], skip_special_tokens=True)

seed_test = 3
print("\n[REPETITION PENALTY COMPARISON] seed =", seed_test)

print("\nSans pénalité (repetition_penalty=1.0):")
print(generate_with_penalty(seed_test, 1.0))

print("\nAvec pénalité (repetition_penalty=2.0):")
print(generate_with_penalty(seed_test, 2.0))

def generate_with_temp(seed, temp):
    torch.manual_seed(seed)
    out = model.generate(
        **inputs,
        max_length=50,
        do_sample=True,
        temperature=temp,
        top_k=50,
        top_p=0.95,
    )
    return tokenizer.decode(out[0], skip_special_tokens=True)

seed_temp = 2
print("\n[TEMPERATURE COMPARISON] seed =", seed_temp)

print("\nTempérature basse (0.1):")
print(generate_with_temp(seed_temp, 0.1))

print("\nTempérature élevée (2.0):")
print(generate_with_temp(seed_temp, 2.0))

out_beam = model.generate(
    **inputs,
    max_length=50,
    num_beams=5,
    early_stopping=True
)
txt_beam = tokenizer.decode(out_beam[0], skip_special_tokens=True)

print("\n[BEAM SEARCH num_beams=5]")
print(txt_beam)

import time

for nb in [5, 10, 20]:
    start = time.time()
    out = model.generate(
        **inputs,
        max_length=50,
        num_beams=nb,
        early_stopping=True
    )
    elapsed = time.time() - start
    txt = tokenizer.decode(out[0], skip_special_tokens=True)

    print(f"\n[BEAM SEARCH num_beams={nb}]")
    print(f"Temps de génération: {elapsed:.3f} secondes")
    print(txt)