from transformers import GPT2Model
import plotly.express as px
from sklearn.decomposition import PCA

model = GPT2Model.from_pretrained("gpt2")

# TODO: récupérer la matrice des embeddings positionnels
position_embeddings = model.wpe.weight

print("Shape position embeddings:", position_embeddings.size())

# TODO: afficher quelques infos de config utiles
print("n_embd:", model.config.n_embd)
print("n_positions:", model.config.n_positions)

# TODO: extraire les 50 premières positions (tensor -> numpy)
positions = position_embeddings[:50].detach().cpu().numpy()

pca = PCA(n_components=2)
reduced = pca.fit_transform(positions)

fig = px.scatter(
    x=reduced[:, 0],
    y=reduced[:, 1],
    text=[str(i) for i in range(len(reduced))],
    color=list(range(len(reduced))),
    title="Encodages positionnels GPT-2 (PCA, positions 0-50)",
    labels={"x": "PCA 1", "y": "PCA 2"}
)

# TODO: sauver dans TP1/positions_50.html
fig.write_html("TP1/positions_50.html")
print("Saved: TP1/positions_50.html")

positions_200 = position_embeddings[:200].detach().cpu().numpy()

pca_200 = PCA(n_components=2)
reduced_200 = pca_200.fit_transform(positions_200)

fig_200 = px.scatter(
    x=reduced_200[:, 0],
    y=reduced_200[:, 1],
    text=[str(i) for i in range(len(reduced_200))],
    color=list(range(len(reduced_200))),
    title="Encodages positionnels GPT-2 (PCA, positions 0-200)",
    labels={"x": "PCA 1", "y": "PCA 2"}
)

fig_200.write_html("TP1/positions_200.html")
print("Saved: TP1/positions_200.html")