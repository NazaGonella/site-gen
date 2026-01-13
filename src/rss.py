import json
from feedgen.feed import FeedGenerator
from pathlib import Path
from src.parser import ParseMarkdown

class MarkdownRSS:
    def __init__(
        self,
        source_path: str,
        output_file: str,
        config_file: str,
    ):
        self.source_path = source_path
        self.output_file = output_file
        with open(config_file, "r", encoding="utf-8") as f:
            self.config = json.load(f)

    def build(self):
        fg = FeedGenerator()
        fg.id(self.config["feed_link"])
        fg.title(self.config["title"])
        fg.link(href=self.config["page_link"], rel="alternate")
        fg.link(href=self.config["feed_link"], rel="self")
        fg.subtitle(self.config["subtitle"])
        for author in self.config["authors"]:
            fg.author(author)
        if self.config.get("logo_path"):
            fg.logo(self.config["logo_path"])
        fg.language(self.config.get("languages", ["en"])[0])

        entries_path = Path(self.source_path) / self.config.get("entries_path", "")
        for item in entries_path.rglob("*.md"):
            parse = ParseMarkdown(item)
            parent_name = item.parent.stem                             # filename without extension

            entry = fg.add_entry()
            entry.id(f"{self.config['page_link']}/{parent_name}")
            entry.title(parse.meta["title"][0])
            entry.link(href=f"{self.config['page_link']}/{parent_name}")
            entry.content(parse.content_html, type="html") 

        fg.rss_file(self.output_file)