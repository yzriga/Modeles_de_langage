from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
phrase = "Artificial intelligence is metamorphosing the world!"

# TODO: tokeniser la phrase
tokens = tokenizer.tokenize(phrase)

print(tokens)

# TODO: obtenir les IDs
token_ids = tokenizer.encode(phrase)
print("\nToken IDs:", token_ids)

print("\nDétails par token:")
for tid in token_ids:
    # TODO: décoder un seul token id
    txt = tokenizer.decode([tid])
    print(tid, repr(txt))

phrase2 = "GPT models use BPE tokenization to process unusual words like antidisestablishmentarianism."

tokens2 = tokenizer.tokenize(phrase2)
print(tokens2)

# TODO: extraire uniquement les tokens correspondant au mot long (optionnel mais recommandé)
long_word = "antidisestablishmentarianism"
long_word_tokens = tokenizer.tokenize(long_word)

print("\nTokens du mot 'antidisestablishmentarianism':", long_word_tokens)

# TODO: compter le nombre de sous-tokens
num_subtokens = len(long_word_tokens)
print("Nombre de sous-tokens:", num_subtokens)