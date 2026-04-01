# docs/0-inputs/ — Documents client

Ce repertoire est le **point de depot unique** pour tous les documents fournis par le client ou le sponsor du projet. Les agents y lisent leurs inputs client ; ils n'y ecrivent jamais.

## Convention de nommage des repertoires

Chaque sous-repertoire suit la convention `{domaine}/{systeme}/` correspondant a l'agent destinataire. Les agents savent automatiquement ou chercher leurs documents client grace a cette convention.

### Structure

```
docs/0-inputs/
  ba/
    source/                      # Documents bruts initiaux (CdC, notes, PPT, mails, CR...)
    0-audit/                     # Documents de l'existant a auditer (brownfield)
    1-scoping/                   # Complements pour vision, glossaire, acteurs, exigences
    2-spec/                      # Complements pour modele domaine, regles metier
    3-design/                    # Complements pour le design fonctionnel
      ft-NNN-slug/               # Par feature (crees au scaffold apres decouverte des epics)
  tech/
    source/                      # Documents techniques existants (schemas archi, code, infra...)
    0-audit/                     # Documentation technique de l'existant (brownfield)
    1-archi/                     # Complements pour decisions d'architecture
    2-design/                    # Complements pour design technique (API, data model...)
  steer/                         # Decisions COPIL, arbitrages, changements de perimetre
```

## Regles

1. **Les agents lisent, vous ecrivez.** Les agents ne deposent jamais de fichiers ici. Seul l'utilisateur (vous) y ajoute des documents.
2. **Nommez vos dossiers de facon descriptive.** A l'interieur de chaque sous-repertoire systeme, vous pouvez creer librement des sous-dossiers pour organiser vos documents (par date, par atelier, par theme...).
3. **Tous les formats sont acceptes.** Markdown, PDF, Word, PowerPoint, images, CSV... Les agents s'adaptent au format fourni.
4. **Un repertoire vide ne bloque rien.** Si aucun document client n'est disponible pour un agent, il continue avec ses seuls upstream agents.

## Quel repertoire pour quel agent ?

| Repertoire | Agents destinataires | Quand deposer |
|------------|---------------------|---------------|
| `ba/_source/` | `ba-discovery` | Avant le lancement du pipeline BA — cahier des charges, notes d'ateliers, presentations |
| `ba/0-audit/` | `ba-0.1`, `ba-0.2` | Avant le pipeline S0 (brownfield) — specs existantes, manuels, captures d'ecran |
| `ba/1-scoping/` | `ba-1.1` a `ba-1.4` | Complements apres la discovery — CR de reunions, precisions du sponsor |
| `ba/2-spec/` | `ba-2.1` a `ba-2.3` | Complements pour la specification — documents regles metier, schemas entites |
| `ba/3-design/ft-NNN/` | `ba-3.1` a `ba-3.6` | Documents cibles par feature — maquettes, retours client, CR d'ateliers ecrans. Pour cibler une US specifique, nommer le fichier avec le numero d'US (ex: `retour-us-003-validation.pdf`) |
| `tech/_source/` | `tech-t0.1` | Avant le pipeline Tech — schemas archi, code source, config infra |
| `tech/0-audit/` | `tech-t0.1`, `tech-t0.2` | Documentation technique de l'existant |
| `tech/1-archi/` | `tech-t1.1` a `tech-t1.4` | Contraintes techniques, docs securite, decisions existantes |
| `tech/2-design/` | `tech-t2.1` a `tech-t2.6` | Complements pour design technique — schemas BDD, specs API existantes |
| `steer/` | `steer-p0.1` a `steer-p3.2` | Decisions de COPIL, arbitrages, changements de perimetre |

## Exemples concrets

```
docs/0-inputs/
  ba/
    source/
      cahier-des-charges-v2.pdf
      notes-atelier-cadrage-2025-03-10.md
      presentation-sponsor.pptx
    0-audit/
      spec-fonctionnelle-v3.docx
      captures-ecran-appli-existante/
    1-scoping/
      cr-reunion-2025-03-15-precision-perimetre.md
    3-design/
      ft-001-gestion-reservations/
        maquettes-figma-export/
        retour-us-003-validation-ecran.pdf
      ft-002-moteur-disponibilite/
        cr-atelier-regles-calcul.md
  tech/
    source/
      schema-archi-si-2024.pdf
      docker-compose-prod.yml
    1-archi/
      contraintes-securite-dsi.pdf
  steer/
    pv-copil-2025-03-20.md
```

## Scaffold automatique

L'arborescence de base (`ba/_source/`, `ba/0-audit/`, `tech/_source/`, etc.) est creee automatiquement par le tool scaffold au debut de chaque pipeline. Les sous-repertoires par feature (`ba/3-design/ft-NNN/`) sont crees dynamiquement apres la decouverte des epics et features.
