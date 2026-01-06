import markdown
import re
from pathlib import Path

def parse_markdown(md_file : Path) -> str:
    md : markdown.Markdown = markdown.Markdown(extensions=["meta"])

    content_md : str = md_file.read_text(encoding="utf-8")
    content_html : str = md.convert(content_md)

    template : str = (Path("templates") / Path("template.html")).read_text(encoding="utf-8")

    output : str = template.replace("$body$", content_html)

    symbols : set[str] = set(re.findall(r'\$(.*?)\$', output))      # all symbols that are between $
    for sym in symbols:
        if sym in md.Meta:
            output = output.replace(f"${sym}$", md.Meta[sym][0])

    return output