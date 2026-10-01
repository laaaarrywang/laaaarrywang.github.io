"""Build a dependency-free academic homepage from content.json."""
import json
import shutil
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'content.json').read_text())

def text(value):
    return escape(str(value), quote=True)

def url(value):
    value = str(value)
    parsed = urlsplit(value)
    if parsed.scheme not in ('', 'https', 'http', 'mailto') or value.startswith('//'):
        raise ValueError(f'Unsupported URL: {value}')
    return text(value)

def link(item):
    return f'<a href="{url(item["url"])}">{text(item["label"])}</a>'

name = text(data['name'])
initials = ''.join(word[0] for word in data['name'].split()[:2])
photo = (f'<img class="portrait" src="{url(data["photo"])}" alt="Portrait of {name}" width="220" height="220">'
         if data.get('photo') else f'<div class="portrait initials" aria-label="{name}">{text(initials)}</div>')
links = list(data.get('links', []))
if data.get('email'):
    links.insert(0, {'label': 'Email', 'url': 'mailto:' + data['email']})
bio = ''.join(f'<p>{text(p)}</p>' for p in data.get('bio', []))
news = ''.join(f'<li><time>{text(n["date"])}</time><span>{text(n["text"])}' +
               (f' {link(n["link"])}' if n.get('link') else '') + '</span></li>'
               for n in data.get('news', []))
pubs = []
for p in data.get('publications', []):
    image = f'<a class="publication-image" href="{url(p["image"])}" aria-label="View figure for {text(p["title"])}"><img src="{url(p["image"])}" alt="{text(p.get("image_alt", p["title"]))}" loading="lazy" width="200" height="140"></a>' if p.get('image') else ''
    authors = ', '.join(f'<strong>{text(a)}</strong>' if a.rstrip('*') == data['name'] else text(a) for a in p['authors'])
    abstract = f'<details><summary>Abstract</summary><p>{text(p["abstract"])}</p></details>' if p.get('abstract') else ''
    summary = f'<p class="paper-summary">{text(p["summary"])}</p>' if p.get('summary') else ''
    pubs.append(f'<article class="publication {"with-image" if image else ""}">{image}<div><h3>{text(p["title"])}</h3><p class="authors">{authors}</p><p class="venue">{text(p["venue"])}' + (f' <span class="badge">{text(p["award"])}</span>' if p.get('award') else '') + f'</p>{summary}<div class="paper-links">{" ".join(link(l) for l in p.get("links", []))}</div>{abstract}</div></article>')
experience = ''.join(f'<article class="experience"><div><h3>{text(e["role"])}</h3><p>{text(e["organization"])}</p></div><span>{text(e["dates"])}</span></article>' for e in data.get('experience', []))
experience_section = f'<section id="experience"><h2>Experience</h2>{experience}</section>' if experience else ''
education = ''.join(f'<article class="experience"><div><h3>{text(e["organization"])}</h3><p>{text(e["role"])}</p></div><span>{text(e["dates"])}</span></article>' for e in data.get('education', []))
education_section = f'<section id="education"><h2>Education</h2>{education}</section>' if education else ''
service_section = f'<section id="service"><h2>Academic Service</h2><p>{text(data["service"])}</p></section>' if data.get('service') else ''
html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{text(data['description'])}">
  <meta name="theme-color" content="#fafaf8">
  <meta property="og:title" content="{name}">
  <meta property="og:description" content="{text(data['description'])}">
  <meta property="og:type" content="website">
  <title>{name}</title>
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header"><a class="wordmark" href="#about">{name}</a><nav aria-label="Main navigation"><a href="#about">About</a><a href="#news">News</a><a href="#publications">Publications</a>{'<a href="#experience">Experience</a>' if experience else ''}</nav></header>
  <main id="main">
    <section id="about" class="about"><div class="intro"><h1>{name}</h1>{f'<p class="affiliation">{text(data["affiliation"])}</p>' if data.get('affiliation') else ''}<div class="bio">{bio}</div><div class="profile-links">{'<span aria-hidden="true">/</span>'.join(link(l) for l in links)}</div></div><div class="photo-wrap">{photo}</div></section>
    <section id="news"><h2>News</h2>{f'<ul class="news-list">{news}</ul>' if news else '<p class="empty">Updates will be added here.</p>'}</section>
    <section id="publications"><div class="section-heading"><h2>Publications &amp; Preprints</h2>{f'<a href="{url(data["scholar"])}">All publications ↗</a>' if data.get('scholar') else ''}</div>{'<p class="contribution-note">* Equal contribution.</p>' if any('*' in a for p in data.get('publications', []) for a in p['authors']) else ''}{''.join(pubs) if pubs else '<p class="empty">Publications will be added here.</p>'}</section>
    {experience_section}
    {education_section}
    {service_section}
  </main>
  <footer><span>© {date.today().year} {name}</span><span>Last updated: {date.today().strftime('%B %Y')}</span></footer>
</body>
</html>
'''
(ROOT / 'index.html').write_text(html)
out = ROOT / '_site'
out.mkdir(exist_ok=True)
(out / 'index.html').write_text(html)
shutil.copytree(ROOT / 'assets', out / 'assets', dirs_exist_ok=True)
(out / '.nojekyll').touch()
print('Built index.html and _site/')
