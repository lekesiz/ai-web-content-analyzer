# Slides Reveal.js — AI Web Content Analyzer (Soutenance)

17 slides, ~15 min orales + 10 min Q/R.

## Aperçu local

```bash
# Aucune build step — c'est du HTML statique
open index.html
# ou
python3 -m http.server 8000
# puis http://localhost:8000
```

## Navigation

- **Espace / flèche droite** : slide suivante
- **Flèche gauche** : slide précédente
- **Échap / O** : vue d'ensemble
- **F** : plein écran
- **S** : speaker notes (deuxième fenêtre)
- **B** : noir (pause visuelle)

## Déploiement GitHub Pages

```bash
cd ai-web-content-analyzer
mkdir -p slides
cp /Users/mikail/.../slides-ai-wca/index.html slides/
cp /Users/mikail/.../slides-ai-wca/README.md slides/
git add slides/
git commit -m "docs: add Reveal.js slides for soutenance"
git push
```

Puis sur GitHub :
- Settings → Pages
- Source : Deploy from a branch
- Branch : main, Folder : /docs (ou créer un workflow)

Une fois déployé : `https://lekesiz.github.io/ai-web-content-analyzer/slides/`

## Structure (17 slides)

1. Titre
2. Constat
3. Problématique
4. Solution en image
5. Cahier des charges MoSCoW
6. Architecture
7. Pipeline d'analyse
8. Choix techniques
9. Sécurité OWASP + RGPD
10. Métriques (4 chiffres)
11. Démo (placeholder vidéo)
12. 3 difficultés → 3 commits
13. Apprentissages
14. Perspectives V2/V3
15. Compétences UE 6.5
16. Remerciements
17. Q/R

## Personnalisation

- **Couleurs** dans `<style>` au début du fichier :
  - `--accent: #3b82f6` (bleu principal)
  - `--accent2: #06b6d4` (cyan)
  - `--bg: #0b1220` (fond)
- **Vidéo démo** : remplacer la slide 11 par `<video controls src="demo.mp4"></video>`
- **Speaker notes** : ajouter `<aside class="notes">Ton commentaire ici</aside>` dans n'importe quelle `<section>`

## Test responsive

Resize Chrome de 1920 à 1024 : tout doit rester lisible. La police s'adapte automatiquement via les unités `em` de Reveal.

---

*Produit le 22/05/2026 — Cowork.*
