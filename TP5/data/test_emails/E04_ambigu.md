---
email_id: E04
from: "Yahia Zriga <yahia.zriga@telecom-sudparis.eu>"
date: "2026-01-25"
subject: "Problème avec le truc"
---

CORPS:
<<<
Salut,

J'ai un problème avec le truc de ce matin. Ça marche pas comme prévu.

Tu peux m'aider ?

Yahia
>>>

ATTENDU:
- intent: ask_clarification
- 1-2 points clés attendus: "demander précisions sur 'le truc'", "contexte insuffisant pour répondre"