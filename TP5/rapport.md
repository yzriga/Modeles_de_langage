# CI5 : IA agentique
## Exercice 1: Mise en place de TP5 et copie du RAG (base Chroma incluse)
![alt text](img/image-1.png)
---
## Exercice 2: Constituer un jeu de test (8–12 emails) pour piloter le développement
**Liste des fichiers emails créés :**
- **E01** : Demande attestation scolarité *(administratif)*
- **E02** : Question validation UE *(enseignement)*  
- **E03** : Sujets PFE Luca Benedetto *(recherche)*
- **E04** : Email ambigu "problème avec le truc" *(clarification)*
- **E05** : Demande notes tous étudiants *(sensible - escalade)*
- **E06** : Cours en distanciel 07/01 *(enseignement)*
- **E07** : Spam marketing *(ignore)*
- **E08** : Information bourse Erasmus *(administratif)*
- **E09** : Tentative prompt injection *(à risque - ignore)*
- **E10** : Planning détaillé PFE *(enseignement)*

![alt text](img/image-2.png)

**Diversité du jeu de test :**
Le jeu de test couvre les 4 intents principaux (reply, ask_clarification, escalate, ignore) avec des cas représentatifs : emails administratifs classiques, questions pédagogiques liées au corpus existant (validation UE, PFE), un cas ambigu nécessitant clarification, et des emails à risque (données sensibles, prompt injection) pour tester la robustesse de l'agent. Cette diversité permettra d'évaluer toutes les branches de décision de l'agent orchestré.

![alt text](img/image-3.png)
---
## Exercice 3: Implémenter le State typé (Pydantic) et un logger JSONL (run events)
![alt text](img/image-4.png)

![alt text](img/image-5.png)

![alt text](img/image-6.png)
---
## Exercice 4: Router LLM : produire une Decision JSON validée (avec fallback/repair)
![alt text](img/image-7.png)
---
## Exercice 5: LangGraph : routing déterministe et graphe minimal (MVP)
![alt text](img/image-8.png)

![alt text](img/image-9.png)

![alt text](img/image-10.png)
---
## Exercice 6: Tool use : intégrer votre RAG comme outil (retrieval + evidence)
![alt text](img/image-11.png)
---
## Exercice 7: Génération : rédiger une réponse institutionnelle avec citations (remplacer le stub reply)
![alt text](img/image-12.png)

![alt text](img/image-13.png)
**Question 7-a : Nœud draft_reply créé**
Fichier [TP5/agent/nodes/draft_reply.py](TP5/agent/nodes/draft_reply.py) implémenté avec :
- Construction du contexte à partir de state.evidence
- Prompt LLM pour génération JSON avec reply_text + citations
- Validation des citations contre evidence.doc_id disponibles
- Safe mode si evidence vide, citations invalides ou JSON malformé

**Question 7-b : Graphe modifié**
[TP5/agent/graph_minimal.py](TP5/agent/graph_minimal.py) mis à jour :
- Import de draft_reply remplaçant stub_reply
- Node "reply" utilise maintenant draft_reply au lieu du stub

**Question 7-c : Tests et résultats**

**Cas 1 : Reply avec evidence (E01 - attestation scolarité)**
```bash
$ python -m TP5.test_graph_minimal
```

**Réponse générée :**
```
La procédure à suivre pour obtenir une attestation de scolarité pour votre 
demande de logement étudiant est définie dans le Règlement de la scolarité 
de la FISA de Télécom SudParis. Vous pouvez consulter cette information 
sur la page 14 de ce document : [doc_1]
```

**Evidence récupérée :** 5 documents du règlement de scolarité FISA/FISE

**Logs JSONL - draft_reply success :**
```json
{
  "run_id": "a06bf628-dde5-44fd-bd98-263dbcfed5e9", 
  "event": "node_end", 
  "data": {
    "node": "draft_reply", 
    "status": "ok", 
    "n_citations": 1
  }
}
```

**Cas 2 : Safe mode avec evidence vide**
Test avec [TP5/test_safe_mode.py](TP5/test_safe_mode.py) :

**Réponse safe mode :**
```
Merci pour votre demande. Pour vous donner une réponse précise, j'aurais 
besoin de quelques informations complémentaires. Pourriez-vous me contacter 
directement ou préciser votre demande ? Cordialement.
```

**Logs JSONL - draft_reply safe_mode :**
```json
{
  "run_id": "cccd9c0b-f2ce-4411-9e67-ed90e8f6c33d", 
  "event": "node_end", 
  "data": {
    "node": "draft_reply", 
    "status": "safe_mode", 
    "reason": "no_evidence"
  }
}
```

L'agent génère maintenant des réponses institutionnelles avec citations valides ou bascule en mode prudent quand l'evidence est insuffisante. Le système est traçable avec logs détaillés (status ok vs safe_mode).

---
## Exercice 8: Boucle contrôlée : réécriture de requête et 2e tentative de retrieval (max 2)

---
## Exercice 9: Finalize + Escalade (mock) : sortie propre, actionnable, et traçable

---
## Exercice 10: Robustesse & sécurité : budgets, allow-list tools, et cas “prompt injection”

---
## Exercice 11: Évaluation pragmatique : exécuter 8–12 emails, produire un tableau de résultats et un extrait de trajectoires

--
## Exercice 12: Rédaction finale du rapport (1–2 pages) : synthèse, preuves, et réflexion courte