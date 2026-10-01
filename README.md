# Linxuan Wang — academic homepage

A responsive, English academic homepage inspired by the simple layouts of https://xinyangatk.github.io/ and https://yuchen-zhu-zyc.github.io/. Original implementation; no copied biographies, photos, or publications. No third-party runtime dependencies.

## Before publishing

Content is based on your September 2026 CV and your confirmation that you are a third-year Statistics PhD student at Purdue. Publication statuses follow the CV; UBTree is labeled as a preprint. Add your portrait and Google Scholar URL when available. Your original resume PDF is included as the CV download.

Publication figures: `assets/scdd.png` is the training/inference panel extracted from `Desktop/icml2026/poster-LinxuanWang-ICML2026.pdf`; `assets/ubtree.png` is the architecture panel from `figures/ubtree_diagram.pdf` inside `Downloads/UBTree_Preprint.zip`. Clicking either thumbnail opens the full-size image.

`assets/federated-hmc.png` is the centralized/federated HMC illustration (Figure 1 in `Downloads/adaptiveHMC_ADA___Copy_.pdf`), extracted from its matching source archive at `icml2024/Figures/motivation1.png`.

`assets/se3-meanflow.png` is the few-step inference diagram (Figure 1, page 3) extracted from `Downloads/se3meanflow.pdf`.

Inline institution icons come from Purdue's official favicon (`https://www.purdue.edu/home/wp-content/mu-plugins/boilerup-wp/favicon/favicon-96x96.png`), Duke's official favicon (`https://www.duke.edu/wp-content/uploads/2025/12/cropped-dfavicon-1-192x192.png`), Wuhan University's dark green and navy emblem (`https://upload.wikimedia.org/wikipedia/en/6/68/Wuhan_University_Logo.png`), and the Ant Group mark in `logo/logoantgroup.png` inside `Downloads/UBTree_Preprint.zip`.

Edit `content.json`. Put your portrait in `assets/portrait.jpg` and set `photo` to that path. Put a CV in `assets/cv.pdf` and add a link. Empty experience entries are hidden; empty news and publication sections show a short placeholder.

Example content entries (replace every example value with your own information):

```json
{
  "name": "Your English Name",
  "description": "Your English Name — academic homepage",
  "affiliation": "Your department, your university",
  "bio": ["Your biography.", "Your specific research interests."],
  "email": "you@example.edu",
  "photo": "assets/portrait.jpg",
  "scholar": "https://scholar.google.com/citations?user=YOUR_ID",
  "links": [
    {"label": "Google Scholar", "url": "https://scholar.google.com/citations?user=YOUR_ID"},
    {"label": "GitHub", "url": "https://github.com/laaaarrywang"},
    {"label": "CV", "url": "assets/cv.pdf"}
  ],
  "news": [{"date": "Oct 2026", "text": "Your update."}],
  "publications": [{
    "title": "Your paper title",
    "authors": ["Your English Name", "Coauthor"],
    "venue": "Conference, year",
    "image": "assets/paper.jpg",
    "image_alt": "Description of the paper figure",
    "award": "",
    "abstract": "Your abstract.",
    "links": [{"label": "Paper", "url": "https://arxiv.org/abs/YOUR_ID"}, {"label": "Code", "url": "https://github.com/your/repo"}]
  }],
  "experience": [{"role": "Your role", "organization": "Your institution", "dates": "Start – End"}]
}
```

## Local preview

```bash
python3 scripts/build.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory _site
```

Open http://localhost:8000. Rebuild after editing content. You can also open `index.html` directly.

## Publish to GitHub Pages

1. Create an empty public repository named `laaaarrywang.github.io` under `laaaarrywang`. Do not initialize it with a README.
2. Push this local project:

```bash
git add .
git commit -m "Create academic homepage"
git remote set-url origin git@github.com:laaaarrywang/laaaarrywang.github.io.git
git push -u origin main
```

3. In repository **Settings → Pages → Build and deployment**, choose **GitHub Actions**.
4. If the first workflow failed before Pages was enabled, rerun it in **Actions**, or manually run **Deploy academic website**.
5. The site will be available at https://laaaarrywang.github.io/ after a successful deployment.

Future updates: edit `content.json` or assets, then commit and push. GitHub Actions builds and publishes automatically. Local `index.html` is a preview; the workflow always builds from `content.json`.
