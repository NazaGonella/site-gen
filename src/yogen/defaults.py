import json
from ._site import Site
from pathlib import Path


def build_default_files():
    # ensure all required folders exist
    for folder in ("content", "build", "deploy", "scripts", "styles", "templates"):
        Path(folder).mkdir(parents=True, exist_ok=True)
    
    (Path("content") / "home.md").write_text( """---
title: Welcome to the home page!
author: Your Name
date: 01/01/01
tags: home
template: template-home
section: home
---""", encoding="utf-8")

    # ensure config file exists
    config_file = Path("rss-config.json")
    if not config_file.exists():
        default_config = {
            "title": "Your Feed Title",
            "subtitle": "Your Feed Subtitle",
            "authors": [{
                "name": "author 1 name",
                "email": "author 1 email address"
            }],
            "page_link": "https://example.com",
            "feed_link": "https://example.com/example_feed.xml",
            "logo_path": "/path/to/logo.png",
            "languages": ["en"],
            "entries_path": "/path/to/entries/folder/"
        }
        config_file.write_text(json.dumps(default_config, indent=4), encoding="utf-8")
    
    # base post template file
    base_template = """<!DOCTYPE html>
<html>

<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{page.title}}</title>
<link rel="stylesheet" href="/style.css">
</head>

<body>
<header>
    <div style="margin-bottom:1em;"></div>
    <nav>
    <a class="title" href="/">blog</a>
    <span class="separator"></span>
    <a class="title" href="/about/">about</a>
    <span class="separator"></span>
    <a class="title" href="/feed.xml">RSS</a>
    </nav>
    <div style="margin-bottom:2.5em;"></div>
</header>

<main>
    <article>
    <h2>{{page.title}}</h2>
    <p><em>{{page.dateB}}</em></p>
    {{page.content}}
    </article>
</main>

</body>
</html>"""

    home_template = """<!DOCTYPE html>
<html>

<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{page.title}}</title>
<link rel="stylesheet" href="/style.css">
</head>

<body>
<header>
    <link rel="icon" href="/assets/favicon.svg" type="image/svg">
    <div style="margin-bottom:1em;"></div>
    <nav>
    <a class="title" href="/">blog</a>
    <span class="separator"></span>
    <a class="title" href="/about/">about</a>
    <span class="separator"></span>
    <a class="title" href="/feed.xml">RSS</a>
    </nav>
    <div style="margin-bottom:2.5em;"></div>
</header>

<main>
    <article>
    {{page.content}}
    </article>
</main>

</body>
</html>
"""

    templates_path = Path("templates")
    base_template_path = templates_path / "template-post.html"
    home_template_path = templates_path / "template-home.html"
    base_template_path.write_text(base_template, encoding="utf-8")
    home_template_path.write_text(home_template, encoding="utf-8")