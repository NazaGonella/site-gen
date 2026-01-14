import json
from _site import Site
from pathlib import Path


def build_default_files():
    # ensure all required folders exist
    for folder in ("content", "build", "deploy", "scripts", "styles", "templates"):
        Path(folder).mkdir(parents=True, exist_ok=True)

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
    <script>
        if (localStorage.getItem('darkmode') === 'active') {
        document.documentElement.classList.add('darkmode');
        }
    </script>
    <link rel="stylesheet" href="/style.css">
    <script type="text/javascript" src="/darkmode.js" defer></script>
    </head>

    <body>
    <header>
        <link rel="icon" href="/assets/favicon.svg" type="image/svg">
        <div style="margin-bottom:1em;"></div>
        <button id="theme-switch">
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M480-120q-150 0-255-105T120-480q0-150 105-255t255-105q14 0 27.5 1t26.5 3q-41 29-65.5 75.5T444-660q0 90 63 153t153 63q55 0 101-24.5t75-65.5q2 13 3 26.5t1 27.5q0 150-105 255T480-120Z"/></svg>
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M480-280q-83 0-141.5-58.5T280-480q0-83 58.5-141.5T480-680q83 0 141.5 58.5T680-480q0 83-58.5 141.5T480-280ZM200-440H40v-80h160v80Zm720 0H760v-80h160v80ZM440-760v-160h80v160h-80Zm0 720v-160h80v160h-80ZM256-650l-101-97 57-59 96 100-52 56Zm492 496-97-101 53-55 101 97-57 59Zm-98-550 97-101 59 57-100 96-56-52ZM154-212l101-97 55 53-97 101-59-57Z"/></svg>
        </button>
        <nav>
        <a class="title" href="/">blog</a>
        <span class="separator"></span>
        <a class="title" href="/about/">about</a>
        <span class="separator"></span>
        <a class="title" href="/resume/es/">resume</a>
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
    <script>
        if (localStorage.getItem('darkmode') === 'active') {
        document.documentElement.classList.add('darkmode');
        }
    </script>
    <link rel="stylesheet" href="/style.css">
    <script type="text/javascript" src="/darkmode.js" defer></script>

    </head>

    <body>
    <header>
        <link rel="icon" href="/assets/favicon.svg" type="image/svg">
        <div style="margin-bottom:1em;"></div>
        <button id="theme-switch">
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M480-120q-150 0-255-105T120-480q0-150 105-255t255-105q14 0 27.5 1t26.5 3q-41 29-65.5 75.5T444-660q0 90 63 153t153 63q55 0 101-24.5t75-65.5q2 13 3 26.5t1 27.5q0 150-105 255T480-120Z"/></svg>
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M480-280q-83 0-141.5-58.5T280-480q0-83 58.5-141.5T480-680q83 0 141.5 58.5T680-480q0 83-58.5 141.5T480-280ZM200-440H40v-80h160v80Zm720 0H760v-80h160v80ZM440-760v-160h80v160h-80Zm0 720v-160h80v160h-80ZM256-650l-101-97 57-59 96 100-52 56Zm492 496-97-101 53-55 101 97-57 59Zm-98-550 97-101 59 57-100 96-56-52ZM154-212l101-97 55 53-97 101-59-57Z"/></svg>
        </button>
        <nav>
        <a class="title" href="/">blog</a>
        <span class="separator"></span>
        <a class="title" href="/about/">about</a>
        <span class="separator"></span>
        <a class="title" href="/resume/es/">resume</a>
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