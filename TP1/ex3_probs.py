import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import math

model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

phrase = "Artificial intelligence is fascinating."
inputs = tokenizer(phrase, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits  # (1, seq_len, vocab)

# TODO: convertir en probabilités (softmax)
probs = torch.softmax(logits, dim=-1)

# On affiche P(token_t | tokens_) pour t>=1
input_ids = inputs["input_ids"][0]
for t in range(1, len(input_ids)):
    tok_id = input_ids[t].item()
    p = probs[0, t-1, tok_id].item()
    tok_txt = tokenizer.decode([tok_id])
    print(t, repr(tok_txt), f"{p:.3e}")

log_probs = torch.log_softmax(logits, dim=-1)
input_ids = inputs["input_ids"][0]

total_logp = 0.0
n = 0

for t in range(1, len(input_ids)):
    tok_id = input_ids[t].item()
    lp = log_probs[0, t-1, tok_id].item()
    total_logp += lp
    n += 1

avg_neg_logp = - total_logp / n
ppl = math.exp(avg_neg_logp)

print("total_logp:", total_logp)
print("avg_neg_logp:", avg_neg_logp)
print("perplexity:", ppl)

def compute_logp_and_ppl(sentence):
    inputs = tokenizer(sentence, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    log_probs = torch.log_softmax(logits, dim=-1)
    input_ids = inputs["input_ids"][0]

    total_logp = 0.0
    n = 0
    for t in range(1, len(input_ids)):
        tok_id = input_ids[t].item()
        total_logp += log_probs[0, t-1, tok_id].item()
        n += 1

    avg_neg_logp = - total_logp / n
    ppl = math.exp(avg_neg_logp)
    return total_logp, ppl

s1 = "Artificial intelligence is fascinating."
s2 = "Artificial fascinating intelligence is."

logp1, ppl1 = compute_logp_and_ppl(s1)
logp2, ppl2 = compute_logp_and_ppl(s2)

print("Phrase 1:", s1)
print("  logp:", logp1, "perplexity:", ppl1)

print("Phrase 2:", s2)
print("  logp:", logp2, "perplexity:", ppl2)

s3 = "L'intelligence artificielle est fascinante."

logp3, ppl3 = compute_logp_and_ppl(s3)

print("Phrase 3:", s3)
print("  logp:", logp3, "perplexity:", ppl3)

prefix = "Artificial intelligence is"
inp = tokenizer(prefix, return_tensors="pt")

with torch.no_grad():
    out = model(**inp)
    logits2 = out.logits  # (1, seq_len, vocab)

# TODO: récupérer la distribution pour le prochain token (dernier pas de temps)
last_logits = logits2[0, -1, :]
last_probs = torch.softmax(last_logits, dim=-1)

topk = 10
vals, idx = torch.topk(last_probs, k=topk)

print("\nTop 10 tokens suivants pour le préfixe:", repr(prefix))
for p, tid in zip(vals.tolist(), idx.tolist()):
    print(repr(tokenizer.decode([tid])), f"{p:.3e}")