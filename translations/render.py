#!/usr/bin/env python3
"""Render translation markdown into the shared guide HTML chrome."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CSS_HREF = "guide.css"


def slugify(text: str) -> str:
    raw = re.sub(r"<[^>]+>", "", text)
    slug = re.sub(r"[^\w\-]+", "-", raw, flags=re.UNICODE).strip("-").lower()
    return slug or "section"


def inline(text: str) -> str:
    parts: list[str] = []
    i = 0
    pattern = re.compile(
        r"(`[^`]+`)|(\*\*[^*]+\*\*)|(\[[^\]]+\]\([^)]+\))"
    )
    for match in pattern.finditer(text):
        if match.start() > i:
            parts.append(html.escape(text[i : match.start()]))
        token = match.group(0)
        if token.startswith("`"):
            parts.append(f"<code>{html.escape(token[1:-1])}</code>")
        elif token.startswith("**"):
            parts.append(f"<strong>{html.escape(token[2:-2])}</strong>")
        else:
            label, url = re.match(r"\[([^\]]+)\]\(([^)]+)\)", token).groups()
            parts.append(
                f'<a href="{html.escape(url, quote=True)}">{html.escape(label)}</a>'
            )
        i = match.end()
    parts.append(html.escape(text[i:]))
    return "".join(parts)


def render_blocks(md: str) -> tuple[str, list[tuple[str, str]]]:
    lines = md.splitlines()
    out: list[str] = []
    toc: list[tuple[str, str]] = []
    i = 0
    used: dict[str, int] = {}

    def unique(slug: str) -> str:
        n = used.get(slug, 0) + 1
        used[slug] = n
        return slug if n == 1 else f"{slug}-{n}"

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            lang = line[3:].strip() or "text"
            i += 1
            body: list[str] = []
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            code = html.escape("\n".join(body) + ("\n" if body else ""))
            out.append(
                '<div class="code-block"><div class="code-toolbar">'
                f"<span>{html.escape(lang)}</span>"
                '<button type="button" class="copy-button" aria-label="このコードをコピー">コピー</button>'
                "</div>"
                f'<pre tabindex="0"><code class="language-{html.escape(lang)}">{code}</code></pre></div>'
            )
            continue
        if line.startswith("> "):
            quote: list[str] = []
            while i < len(lines) and lines[i].startswith("> "):
                quote.append(lines[i][2:])
                i += 1
            joined = "<br>".join(inline(item) for item in quote)
            out.append(f"<blockquote><p>{joined}</p></blockquote>")
            continue
        if re.match(r"^[-*] ", line):
            items: list[str] = []
            while i < len(lines) and re.match(r"^[-*] ", lines[i]):
                items.append(f"<li>{inline(lines[i][2:])}</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        if re.match(r"^\d+\. ", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                items.append(f"<li>{inline(re.sub(r'^\d+\. ', '', lines[i]))}</li>")
                i += 1
            out.append("<ol>" + "".join(items) + "</ol>")
            continue
        heading = re.match(r"^(#{2,3})\s+(.*)$", line)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2).strip()
            hid = unique(slugify(title))
            if level == 2:
                toc.append((hid, title))
            out.append(f'<h{level} id="{hid}">{inline(title)}</h{level}>')
            i += 1
            continue
        if not line.strip():
            i += 1
            continue
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
            r"^(#{2,3}\s|```|[-*] |\d+\. |> )", lines[i]
        ):
            para.append(lines[i])
            i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out), toc


def split_front(md: str) -> tuple[dict[str, str], str]:
    if not md.startswith("---\n"):
        raise SystemExit("expected YAML front matter")
    end = md.find("\n---\n", 4)
    raw = md[4:end]
    body = md[end + 5 :]
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')
    return meta, body


def toc_html(toc: list[tuple[str, str]]) -> str:
    items = "".join(
        f'<li><a href="#{html.escape(hid, quote=True)}">{inline(title)}</a></li>'
        for hid, title in toc
    )
    return f'<ol>{items}</ol>'


def page(meta: dict[str, str], body: str, toc: list[tuple[str, str]]) -> str:
    nav = toc_html(toc)
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%23246653'/%3E%3Ctext x='18' y='45' fill='white' font-family='sans-serif' font-size='43'%3Ep%3C/text%3E%3C/svg%3E">
<meta name="description" content="{html.escape(meta['description'], quote=True)}">
<title>{html.escape(meta['title_ja'])}</title>
<link rel="stylesheet" href="{CSS_HREF}">
</head>
<body>
<a class="skip-link" href="#article">本文へ移動</a>
<div class="masthead"><a href="../../README.md">ENGINEERING NOTES / PSTACK</a><span>UNOFFICIAL JA TRANSLATION</span></div>
<div class="layout">
<aside class="desktop-toc"><p class="nav-title">CONTENTS / 目次</p><nav aria-label="章の目次">{nav}</nav></aside>
<main class="main-column" id="top">
<header>
<p class="eyebrow">{html.escape(meta['eyebrow'])}</p>
<h1>{html.escape(meta['title_ja'])}</h1>
<p class="subtitle">{html.escape(meta['subtitle'])}</p>
<div class="meta"><span>取得 {html.escape(meta['fetched_on'])}</span><span>原文 {html.escape(meta['published_at'])}</span><span>Lauren Tan (@poteto)</span><span>非公式訳</span></div>
<div class="downloads"><a href="{html.escape(meta['source_url'], quote=True)}">X の原文</a><a href="{html.escape(Path(meta['md_name']).name, quote=True)}">Markdown</a><a href="../../pstack-guide-ja.html">実践入門（別資料）</a></div>
</header>
<details class="mobile-toc"><summary>目次を開く</summary><nav aria-label="モバイル用の章の目次">{nav}</nav></details>
<article id="article">
{body}
</article>
<footer>
<p>Lauren Tan（@poteto）の非公式日本語訳です。このリポジトリ独自の実践入門ではありません。</p>
<p>原文: <a href="{html.escape(meta['source_url'], quote=True)}">{html.escape(meta['source_url'])}</a></p>
<p>取得日: {html.escape(meta['fetched_on'])}。status id: {html.escape(meta['status_id'])}。</p>
</footer>
</main>
</div>
<p id="copy-status" class="sr-only" aria-live="polite"></p>
<script>
document.querySelectorAll('.copy-button').forEach(button => {{
  button.addEventListener('click', async () => {{
    const code = button.closest('.code-block').querySelector('code');
    try {{
      await navigator.clipboard.writeText(code.textContent);
      button.textContent = 'コピーしました';
      document.getElementById('copy-status').textContent = 'コードをコピーしました';
    }} catch {{
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      button.textContent = '選択しました';
      document.getElementById('copy-status').textContent = 'コードを選択しました。コピーのショートカットキーを使ってください';
    }}
    setTimeout(() => {{button.textContent = 'コピー';}}, 2500);
  }});
}});
if ('IntersectionObserver' in window) {{
  const observer = new IntersectionObserver(entries => {{
    for (const entry of entries) if (entry.isIntersecting) {{
      document.querySelectorAll('.desktop-toc a').forEach(link => {{
        if (link.hash === '#' + entry.target.id) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      }});
    }}
  }}, {{rootMargin:'-5% 0px -70% 0px'}});
  document.querySelectorAll('article h2').forEach(heading => observer.observe(heading));
}}
</script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    meta, md_body = split_front(args.markdown.read_text(encoding="utf-8"))
    meta["md_name"] = args.markdown.name
    body, toc = render_blocks(md_body.lstrip("\n"))
    dest = args.output or args.markdown.with_suffix(".html")
    dest.write_text(page(meta, body, toc), encoding="utf-8")
    print(dest)


if __name__ == "__main__":
    main()
