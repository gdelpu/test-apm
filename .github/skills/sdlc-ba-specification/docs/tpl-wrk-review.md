---
id: WRK-001
title: "Review Workshop — [Scope]"
mode: structuring              # prep | structuring
scope: "[ft-xxx-slug | ep-xxx-slug | S1 | S2 | S3]"
date: YYYY-MM-DD
participants:
  - "[Name — Role]"
deliverables_reviewed:
  - "[FT-xxx | US-xxx | EP-xxx | ...]"
status: draft                  # draft | validated
resolved_count: 0
open_count: 0
validation_count: 0
---

# [WRK-001] — Retours Workshop : [Scope]

> **Statut** : `draft` — en attente de relecture BA
> **Scope** : [description du périmètre couvert]
> **Date** : [date du workshop]
> **Livrables présentés** : [liste]

---

## Section A — Contexte du workshop

| Champ | Valeur |
|-------|--------|
| **Type de workshop** | Revue de livrables |
| **Animateur** | [Nom — Rôle] |
| **Participants** | [liste] |
| **Durée** | [HHhMM] |
| **Livrables couverts** | [IDs] |
| **Objectif** | [ex. "Valider les US de la feature FT-003 et recueillir les compléments"] |

---

## Section B — Items résolus (prêts pour `/impact`)

> Ces items représentent des décisions prises pendant le workshop.
> Ils peuvent être soumis directement à `/impact` pour analyse des impacts en aval.

| # | Livrable ref | Type | Description du changement | Urgence | Source (participant) |
|---|-------------|------|--------------------------|---------|---------------------|
| R-001 | [ID ex: US-012 CA-003] | [modification \| ajout \| suppression] | [description précise du changement] | [Blocking \| Important \| Mineur] | [Nom] |
| R-002 | | | | | |

> **Types** :
> - `modification` — un élément existant change
> - `ajout` — un nouvel élément à créer
> - `suppression` — un élément à retirer du périmètre

---

## Section C — Questions ouvertes (bloquantes pour `/impact`)

> Ces items nécessitent une réponse du client avant toute analyse d'impact.
> Une fois résolus, déplacer en Section B avec le type approprié et re-lancer `/impact`.

| # | Livrable ref | Question | Owner réponse | Deadline | Urgence |
|---|-------------|----------|--------------|----------|---------|
| Q-001 | [ID ex: GLO-001] | [question précise] | [Nom] | [YYYY-MM-DD] | [Blocking \| Important] |
| Q-002 | | | | | |

> **Urgence Blocking** : la question concerne un input obligatoire d'un agent en aval — l'analyse d'impact est incomplète sans réponse.
> **Urgence Important** : la question affecte la qualité du livrable mais ne bloque pas l'analyse d'impact sur les autres items.

---

## Section D — Validations explicites

> Ces items sont des confirmations explicites de participants pendant le workshop.
> Ils ne génèrent pas d'impact — ils constituent des preuves de validation pouvant justifier le passage d'un livrable en `status: validated`.

| # | Livrable ref | Élément validé | Participant | Formulation dans le transcript |
|---|-------------|----------------|-------------|-------------------------------|
| V-001 | [ID ex: FT-003] | [description de ce qui a été confirmé] | [Nom] | *"[citation ou paraphrase fidèle]"* |
| V-002 | | | | |

---

## Section E — Récapitulatif de routage

```
Routage — [WRK-xxx]

Prêts pour /impact : [N] items résolus (Section B)
  -> Lancer : /impact --input wrk-{NNN}-{scope-slug}-review.md

Bloqués — clarification requise avant /impact : [N] questions ouvertes (Section C)
  Owners :
  - Q-001 ([Livrable ref]) : [Nom] — deadline [date]
  -> Une fois résolus, déplacer en Section B et re-lancer /impact

Validations enregistrées : [N] items (Section D)
  -> Candidats au passage en `validated` :
  - [Livrable ID] (confirmé par [Noms])
```

---

## Production confidence

| Dimension | Niveau | Commentaire |
|-----------|--------|-------------|
| Complétude du transcript | [Haute \| Moyenne \| Faible] | [ex. "Transcript intégral — enregistrement audio"] |
| Couverture des livrables | [Haute \| Moyenne \| Faible] | [ex. "2 livrables sur 4 couverts — BRL-001 non abordé"] |
| Fiabilité des identifiants | [Haute \| Moyenne \| Faible] | [ex. "3 identifiants inférés — à vérifier avec le BA"] |
| **Niveau global** | [Haute \| Moyenne \| Faible] | |
