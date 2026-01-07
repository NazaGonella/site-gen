import markdown
import re
from pathlib import Path


def parse_content(meta : dict, content_html : str, template : str) -> str:
    content : str = content_html
    matches_with_braces = re.findall(r"(\{\{.*?\}\})", content)
    matches = re.findall(r"\{\{(.*?)\}\}", content)
    for i in range(len(matches)):
        m = matches[i]
        token = m.strip()
        if token in meta:
            print(token)
            print(meta[token])
            # print(matches_with_braces[i])
            content = content.replace(matches_with_braces[i], meta[token][0])

    

    return content


class ParseMarkdown:
    def __init__(self, md_file : Path):
        md : markdown.Markdown = markdown.Markdown(extensions=["meta"])
        content_md : str = md_file.read_text(encoding="utf-8")
        content_html : str = md.convert(content_md)

        # print(md.Meta)
        # parse_content(md.Meta, content_html, md.Meta["template"])
        self.meta : dict = md.Meta
        self.content_md : str = content_md
        self.content_html : str = parse_content(md.Meta, content_html, md.Meta["template"])
