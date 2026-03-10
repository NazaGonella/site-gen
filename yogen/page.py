import tomllib
import markdown
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup
from yogen.config import load_config
from pathlib import Path
from datetime import date, datetime

class Page():
    def __init__(self, md_file : Path, config_file : Path, content_path : Path, meta_sections : dict[str, set[Page]], meta_tags : dict[str, set[Page]]):
        self.config : Path = load_config(config_file)
        self.content_path : Path = content_path
        self.file : Path = md_file
        rel = md_file.relative_to(content_path).parent.as_posix()
        url = "/" if rel == "." else f"/{rel}/"
        self.__metadata = {
            "page" : {
                "title" : self._define_title(md_file, content_path),
                "author" : "",
                "date" : date.today(),
                "template" : "",
                "section" : "global",
                "tags" : [],
                "url" : url,
            },
            "sections" : meta_sections,
            "tags" : meta_tags,
        }
        meta, self.raw_html = self._md_to_html()
        protected = {"content", "raw"}      # fields users cannot set
        for k, v in meta.items():
            if k == "date":
                self.__metadata["page"][k] = self._parse_date(v)
            elif k not in protected:
                self.__metadata["page"][k] = v
            else:
                raise ValueError(f"metadata field '{k}' is protected and cannot be set")
    
    def __hash__(self):
        return hash(self.file)
    
    def __eq__(self, other):
        if not isinstance(other, Page):
            return NotImplemented
        return self.file == other.file
    
    def __getattr__(self, name):
        if name in self.__metadata["page"]:
            return self.__metadata["page"][name]
        raise AttributeError(name)
    
    def get_meta(self, key : str) -> object | None:
        if not key in self.__metadata["page"]:
            return None
        return self.__metadata["page"][key]

    def has_meta(self, key : str) -> bool:
        return key in self.__metadata["page"]

    def render(self, build_path : Path) -> str:
        content_template : Template = Template(self.raw_html)
        rendered_content = content_template.render(**self.__metadata)

        self.__metadata["page"]["content"] = Markup(rendered_content)

        env = Environment(
            loader=FileSystemLoader(str(build_path)),
            autoescape=select_autoescape()
        )
        template_path : str = str(Path(self.get_meta("template")).relative_to("/"))
        template = env.get_template(template_path)
        output = template.render(**self.__metadata)
        return output
    
    def render_raw(self) -> str:
        content : str = self.get_meta("content")
        # content = self._replace_placeholders(content)
        return content

    def _define_title(self, md_file : Path, content_path : Path) -> str:
        if md_file.stem != "index":
            title = md_file.stem
        elif md_file.parent == content_path:
            title = self.config["site"]["title"]
        else:
            title = md_file.parent.stem
        return title

    def _parse_date(self, value : str) -> date:
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Invalid date format: {value}. Expected ISO YYYY-MM-DD.")
    
    def _md_to_html(self) -> tuple[dict, str]:
        FRONT_MATTER_DELIM = "+++"

        meta = {}
        raw = ""

        md : markdown.Markdown = markdown.Markdown(extensions=["footnotes", "tables", "def_list", "toc", 'markdown_captions', 'fenced_code'])
        md_text : str = self.file.read_text(encoding="utf-8")

        lines = md_text.splitlines()
        if lines and lines[0].strip() == FRONT_MATTER_DELIM:
            # find the closing delimiter
            for i in range(1, len(lines)):
                if lines[i].strip() == FRONT_MATTER_DELIM:
                    fm_lines = lines[1:i]
                    if fm_lines:  # parse front matter if not empty
                        meta = tomllib.loads("\n".join(fm_lines))
                    # skip any blank lines immediately after front matter
                    content_lines = lines[i+1:]
                    while content_lines and content_lines[0].strip() == "":
                        content_lines.pop(0)
                    raw = "\n".join(content_lines)
                    break
            else:
                # no closing delimiter found
                raw = "\n".join(lines)
        else:
            # no front matter
            raw = "\n".join(lines)
        
        raw_html : str = md.convert(raw)

        # self.__metadata["content"] = raw_html
        self.__metadata["page"]["content"] = Markup(raw_html)
        
        return meta, raw_html
