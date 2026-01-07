import shutil
from parser import ParseMarkdown
from pathlib import Path

class Page:
    def __init__(self, parse : ParseMarkdown):
        self.__fields = {
            "title"     : parse.meta["title"],
            "date"      : parse.meta["date"],
            "content"   : parse.content_html,
            # "summary"   : parse.,
            # "url"       : "",
            "tags"       : parse.meta["tags"],
            "section"   : parse.meta["section"],
        }
    
    def update_fields(self, new_fields : dict):
        self.__fields = new_fields
    
    def get_field(self, key : str) -> list | None:
        if not key in self.__fields:
            return None
        return self.__fields[key]
    
    def has_field(self, key : str) -> bool:
        return key in self.__fields

class Site:
    def __init__(self, content_path : str, build_path : str, deploy_path : str, templates_path : str):
        self.content_path : Path = Path(content_path)
        self.build_path : Path = Path(build_path)
        self.deploy_path : Path = Path(deploy_path)
        self.templates_path : Path = Path(templates_path)
        self.sections = {}
        self.tags = {}
    
    def build(self):
        # delete pre-existing build folder
        if self.build_path.exists() and self.build_path.is_dir():
            shutil.rmtree(self.build_path)
        
        self.sections.clear()
        self.tags.clear()

        for item in self.content_path.rglob("*"):
            target = self.build_path / item.relative_to(self.content_path)
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            elif item.suffix == ".md":
                target.parent.mkdir(parents=True, exist_ok=True)

                parse : ParseMarkdown = ParseMarkdown(item)

                page : Page = Page(parse)
                if page.has_field("tags"):
                    for tag in page.get_field("tags"):
                        self.tags.setdefault(tag, []).append(page)
                if page.has_field("section"):
                    section_meta = page.get_field("section")
                    assert len(section_meta) == 1, f"section should only have one value. section_meta={section_meta}."
                    self.sections.setdefault(section_meta[0], []).append(page)

                output_path : Path = target.parent / "index.html"
                output_path.write_text(parse.content_html, encoding="utf-8")

    def deploy_path(self):
        pass

