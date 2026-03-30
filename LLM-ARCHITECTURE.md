---
tags:
  - claude/instructions
  - claude/centre-controle
  - architecture
  - llm
version: 1.0.0
created: 2026-03-30
---

# LLM Architecture — Collaboration Multi-Modeles

> Version: 1.0.0 | Derniere MAJ: {{DATE}}

Ce document decrit l'architecture de collaboration entre plusieurs LLMs utilises en parallele
pour le developpement et la gestion de projets complexes avec Claude Code.

---

## 1. Architecture generale

```
                          +---------------------+
                          |     OPERATEUR       |
                          |   {{OPERATOR_NAME}} |
                          |   (human in loop)   |
                          +----------+----------+
                                     |
              +-----------------------+-----------------------+
              |                       |                       |
   +----------v----------+ +---------v---------+ +-----------v----------+
   |  Claude Opus 4.6    | | Claude Sonnet 4.6 | |  Claude Haiku 4.5   |
   |                     | |                   | |                      |
   |  - Code critique    | |  - Documentation  | |  - Recherche rapide  |
   |  - Audit securite   | |  - Refactoring    | |  - Navigation vault  |
   |  - Architecture     | |  - Cours / slides | |  - Questions simples |
   |  - Debug complexe   | |  - Organisation   | |  - Lecture seule     |
   +---------------------+ +-------------------+ +----------------------+
                                     |
                          +----------v----------+
                          |  Perplexity / Gemini |
                          |                      |
                          |  - Veille techno     |
                          |  - Recherche web     |
                          |  - Docs a jour       |
                          |  - CVE / advisories  |
                          +---------------------+
```

---

## 2. Modeles et responsabilites

### Claude Opus 4.6 — Architecte et Auditeur

| Dimension | Detail |
|-----------|--------|
| **Cas d'usage principal** | Code de production, audit securite, decisions d'architecture |
| **Quand l'utiliser** | Taches critiques : auth, crypto, infra prod, composants complexes |
| **Quand ne PAS l'utiliser** | Recherche rapide, navigation, taches simples (sur-cout tokens) |
| **Permissions** | Lecture/ecriture sur tous les fichiers non-LOCK |
| **Droits LOCK** | Seul modele autorise a proposer des modifications LOCK (avec accord operateur) |
| **Paradigme** | Zero-Trust, Secure-by-Design, audit systematique |

### Claude Sonnet 4.6 — Redacteur et Refactoreur

| Dimension | Detail |
|-----------|--------|
| **Cas d'usage principal** | Documentation, refactoring, supports pedagogiques, slides |
| **Quand l'utiliser** | Taches de moyenne criticite, fichiers non-LOCK, ecriture |
| **Quand ne PAS l'utiliser** | Code critique, systemes auth/crypto, audit securite |
| **Permissions** | Lecture/ecriture sur fichiers non-LOCK |
| **Droits LOCK** | Lecture uniquement sur fichiers LOCK |
| **Paradigme** | Clarte, structure, coherence du style |

### Claude Haiku 4.5 — Lecteur et Navigateur

| Dimension | Detail |
|-----------|--------|
| **Cas d'usage principal** | Recherche rapide, navigation vault, questions simples |
| **Quand l'utiliser** | Mode DISCUSSION, delegation agents simples, lectures |
| **Quand ne PAS l'utiliser** | Toute tache d'ecriture, audit, architecture |
| **Permissions** | Lecture seule (strictement) |
| **Droits LOCK** | Lecture uniquement |
| **Paradigme** | Economie de tokens, rapidite, precision |

### Perplexity / Gemini — Veille et Recherche externe

| Dimension | Detail |
|-----------|--------|
| **Cas d'usage principal** | Veille technologique, recherche de documentation a jour, CVE |
| **Quand l'utiliser** | Avant de coder une fonctionnalite (verifier l'existant), recherche de precedents |
| **Quand ne PAS l'utiliser** | Code de production, decisions architecturales (pas de tracabilite) |
| **Permissions** | Aucune permission sur le workspace |
| **Integration** | Resultats synthetises par l'orchestrateur avant integration dans un artefact |
| **Paradigme** | Acces Internet, informations recentes, sources multiples |

---

## 3. Workflow type d'un cycle de developpement

```
PHASE 1 — RESEARCH
  Perplexity/Gemini
  └─ Recherche : librairies, CVE, best practices, documentation officielle
  └─ Sortie : synthese markdown dans .claude/context/research-YYYYMMDD.md
      |
      v
PHASE 2 — ARCHITECTURE
  Claude Opus (John)
  └─ Conception du systeme sur la base de la recherche
  └─ Production : ADR + diagrammes C4 + RBAC
      |
      v
PHASE 3 — IMPLEMENTATION
  Claude Opus (Barry/Winston)
  └─ Code de production, tests unitaires, integration
  └─ Validation : tests + lint + audit (adapter a votre stack)
      |
      v
PHASE 4 — DOCUMENTATION
  Claude Sonnet (Paige)
  └─ README, docs inline, changelog, supports pedagogiques
      |
      v
PHASE 5 — REVUE SECURITE
  Claude Opus (Quinn/Bob)
  └─ Audit du code produit, threat model, validation RBAC
  └─ Sortie : rapport audit avec score de risque
      |
      v
PHASE 6 — VALIDATION OPERATEUR
  {{OPERATOR_NAME}} (human)
  └─ Revue des livrables, validation des decisions LOCK
  └─ Declenchement des actions git (commit, push, merge)
```

---

## 4. Regles de collaboration inter-LLM

### Isolation des contextes
- Chaque LLM recoit le contexte minimal necessaire a sa tache (least privilege)
- Les resultats Perplexity/Gemini sont toujours synthetises par Claude avant integration
- Aucun output externe n'est commite brut dans le depot

### Handoff entre agents
Quand un agent termine et passe la main :
1. Il produit un livrable explicite (fichier ou rapport)
2. Il logue son travail dans `.claude/logs/agents/`
3. L'orchestrateur valide le livrable avant de passer a la phase suivante
4. Le log orchestrateur enregistre la transition

### Conflits de fichiers
- Deux agents ne peuvent pas ecrire sur le meme fichier en parallele
- L'orchestrateur reserve les fichiers avant delegation
- En cas de conflit : l'agent a plus haute criticite (Opus > Sonnet > Haiku) a priorite

### Secrets et credentials
- Aucun LLM ne recoit de credentials, tokens, ou secrets en clair
- Les fichiers `.env` et les secrets sont exclus via `.claudeignore`
- Les audits securite travaillent sur le code, jamais sur les secrets

---

## 5. AI-Assisted Development — Principes

Ce systeme applique les principes de l'AI Fluency Framework d'Anthropic
(https://anthropic.skilljar.com/ai-fluency-framework-foundations) selon quatre axes :

### 5.1 Pratique
Chaque interaction LLM produit un artefact concret :
- Code = fichier source + tests
- Architecture = diagramme + ADR
- Documentation = fichier markdown structure
- Recherche = synthese dans `.claude/context/`

### 5.2 Efficace
Le routage par modele optimal evite le sur-cout :
- Opus n'est pas sollicite pour une simple navigation vault
- Haiku ne produit pas de code critique
- Perplexity/Gemini ne remplace pas la decision architecturale (elle l'informe)

### 5.3 Ethique
Transparence totale sur l'usage des LLMs :
- Chaque session est loguee (qui a fait quoi, avec quel modele)
- Les commits mentionnent la collaboration LLM
- Aucune automatisation cachee : l'operateur valide toujours les actions importantes

### 5.4 Sur
Zero-Trust par defaut sur les outputs LLM :
- Tout code produit est revu avant integration
- Les fichiers LOCK ne peuvent pas etre modifies sans accord humain explicite
- Les actions git sont toujours declenchees par l'operateur, jamais autonomement
- Les credentials ne transitent jamais par un LLM

---

## 6. Metriques de suivi (optionnel)

Pour les workspaces avec fort volume d'utilisation, surveiller :

| Metrique | Objectif | Outil |
|----------|----------|-------|
| Taux de succes des delegations agent | > 90% | Logs orchestrateur |
| Ratio Opus/Sonnet/Haiku | Equilibre selon charge | Logs sessions |
| Fichiers LOCK modifies sans accord | 0 | Audit git |
| Anomalies ouvertes > 7 jours | 0 | ORCHESTRATEUR.md section 7 |
| Backlogs synchronises | 100% | .claude/backlogs/ |

---

## 7. References

- **AI Fluency Framework** : https://anthropic.skilljar.com/ai-fluency-framework-foundations
- **Claude Code Documentation** : https://docs.anthropic.com/claude/docs/claude-code
- **Anthropic Model Overview** : https://docs.anthropic.com/claude/docs/models-overview
- **CLAUDE.md ROOT** : `CLAUDE.md` (racine du workspace)
- **Routage agents** : `00-control-center/ORCHESTRATEUR.md`
