# CI2 - Fine-tuning a language model for text classification

**Nom / Prénom :** ZRIGA Yahia

## Question 1:

### Environnement / installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r TP2/requirements.txt
```
### Versions

**OS** : Ubuntu 24.04 (kernel 6.14.0-37-generic)

**Python** : 3.12.3

**PyTorch (torch)** : 2.9.1

**Transformers (Hugging Face)** : 4.57.3

**TensorFlow** : 2.20.0

**tiktoken**: 0.12.0

**NumPy** : 2.4.0

**Pandas** : 2.3.3

**Scikit-learn** : 1.8.0

**Matplotlib** : 3.10.8

**JupyterLab** : 4.5.1

### Reproductibilité

**Seed utilisé** : 123

---
## Question 2:
`settings` est un dictionnaire Python (`dict`) contenant 5 clés : `n_vocab`, `n_ctx`, `n_embd`, `n_head`, `n_layer`.
Les valeurs sont des entiers et décrivent la configuration du GPT-2 "small" (124M) : taille du vocabulaire, longueur de contexte max, dimension d’embedding, nombre de têtes d’attention et nombre de couches Transformer.

---
## Question 3:
`params` est un dictionnaire Python contenant les poids du modèle GPT-2.  
Il possède 5 clés principales : `blocks`, `b`, `g`, `wpe`, `wte`.

- `wte` : matrice d’embeddings des tokens (shape = [50257, 768])
- `wpe` : matrice d’embeddings positionnels (shape = [1024, 768])
- `blocks` : liste contenant les paramètres de chaque bloc Transformer
- `b` et `g` : paramètres associés aux normalisations (LayerNorm)

Ces paramètres correspondent aux poids entraînés du modèle et seront chargés dans l’architecture définie par `GPTModel`.

---
## Question 4:
Dans `gpt_utils.py`, `GPTModel.__init__(cfg)` attend un dictionnaire `cfg` avec les clés : `vocab_size`, `emb_dim`, `context_length`, `drop_rate`, `n_layers`.
En pratique, comme `cfg` est aussi utilisé dans `TransformerBlock` / `MultiHeadAttention`, il faut également `n_heads` et `qkv_bias`.

La variable `settings` obtenue via `download_and_load_gpt2` est un dictionnaire mais avec des clés OpenAI (`n_vocab`, `n_ctx`, `n_embd`, `n_head`, `n_layer`).
Elle n’est donc pas directement au bon format : on réalise un mapping vers un dictionnaire `model_config` contenant les clés attendues par `GPTModel`.


---
## Question 5:
### Question 5.1:
- df.sample(frac=1, random_state=123) mélange aléatoirement toutes les lignes du dataset.

- Ça évite que le train/test split prenne des blocs non représentatifs si le fichier est trié (par ex. d’abord beaucoup de ham puis beaucoup de spam).

- random_state=123 rend le mélange reproductible : on obtient exactement le même split à chaque exécution.

- Résultat : on a un train et un test plus fair (distribution plus proche du dataset global).

---
### Question 5.2:
Le jeu de données est clairement **déséquilibré**.

Dans le train set :
- ham : 3860 (~86.6 %)
- spam : 597 (~13.4 %)

Le test set présente une distribution très similaire.

Ce déséquilibre peut poser problème lors du fine-tuning : un modèle peut obtenir une bonne accuracy globale en prédisant majoritairement “ham”, tout en détectant mal les spams (classe minoritaire).  
C’est pourquoi l’utilisation de **class weights** est pertinente afin de pénaliser davantage les erreurs sur la classe spam.

---
## Question 7:
Le train set contient 4457 samples et le batch_size est 16.
Nombre de batches par epoch = ceil(4457 / 16) = 279.
(278 batches de 16 + 1 dernier batch de 9 car drop_last=False)

---
## Question 8:
### Question 8.1:
La tâche de détection de spam est une classification binaire (spam / ham), donc le nombre de classes est fixé à 2.

### Question 8.2:
La tête de sortie originale de GPT-2 est une couche linéaire projetant les embeddings de dimension 768 vers l’espace du vocabulaire (50257 tokens).  
Elle a été remplacée par une nouvelle couche linéaire de dimension (768 -> 2), adaptée à la classification binaire.

Original output head:
Linear(in_features=768, out_features=50257, bias=False)

New output head:
Linear(in_features=768, out_features=2, bias=True)

### Question 8.3:
Les couches internes du modèle sont gelées afin de conserver les connaissances linguistiques apprises lors du pré-entraînement et de limiter le nombre de paramètres à optimiser.  
Cela permet un entraînement plus rapide, plus stable et réduit le risque d’overfitting, tout en adaptant le modèle à la nouvelle tâche via la tête de sortie et la normalisation finale.

---
## Question 10:
Pour vérifier le bon fonctionnement du fine-tuning, l’entraînement a d’abord été lancé avec un seul epoch. La fonction de perte diminue globalement au fil des batches, passant d’une valeur initiale élevée (environ 2.5) à des valeurs plus faibles autour de 0.5–0.8. Malgré un certain bruit, cette tendance décroissante indique que le modèle apprend.

Après un epoch, l’accuracy globale atteint environ 86.5 % sur les ensembles d’entraînement et de test, ce qui montre une bonne cohérence entre les deux et peu de sur-apprentissage à ce stade.

Cependant, l’accuracy sur la classe spam est nulle. Le modèle prédit majoritairement la classe “ham”, ce qui s’explique par le fort déséquilibre du dataset (environ 13 % de spam) et le nombre limité d’epochs. Malgré l’utilisation de class weights, le modèle n’a pas encore appris à reconnaître efficacement la classe minoritaire.

---
## Question 11:
Afin d’évaluer l’impact du nombre d’epochs, l’entraînement a été relancé avec `num_epochs = 3`, en conservant les autres paramètres inchangés.

Par rapport à un seul epoch, les performances s’améliorent nettement. L’accuracy globale atteint environ 89.3 % sur l’ensemble d’entraînement et 91.5 % sur l’ensemble de test. Surtout, l’accuracy sur la classe spam passe de 0 % à environ 66 %, montrant que le modèle commence à apprendre efficacement la classe minoritaire.

Ces résultats montrent que, dans un contexte de données déséquilibrées, plusieurs epochs sont nécessaires pour que le fine-tuning de la tête de classification et des couches finales permette une meilleure reconnaissance du spam.

---
## Question 12:
Lors du test sur des phrases personnalisées, le modèle classe correctement les messages normaux (ham), mais échoue à détecter certains spams pourtant évidents.

Ce comportement s’explique principalement par le fort déséquilibre du jeu de données (environ 86 % de messages ham), qui pousse le modèle à privilégier la classe majoritaire afin de maximiser l’accuracy globale.

De plus, le fine-tuning est limité à la tête de classification, avec un nombre réduit d’époques, ce qui empêche le modèle d’apprendre des motifs lexicaux spécifiques au spam (par exemple : urgent, reward, call now).

Enfin, la prédiction repose uniquement sur la représentation du dernier token, ce qui constitue une approximation simplifiée et peut nuire à la performance sur des tâches de classification de séquences complètes.