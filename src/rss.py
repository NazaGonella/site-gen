from feedgen.feed import FeedGenerator
from pathlib import Path
import markdown
from typing import List, Dict, Optional
from src.parser import ParseMarkdown

class MarkdownRSS:
    def __init__(
        self,
        source_path: Path,
        output_file: str,
    ):
        self.source_path = source_path
        self.output_file = output_file

    def build(self):
        fg = FeedGenerator()
        fg.id('http://ngonella.com/feed')
        fg.title('Naza Gonella Blog')
        fg.link( href='http://ngonella.com', rel='alternate' )
        fg.link( href='http://ngonella.com/feed.xml', rel='self' )
        fg.subtitle('Hello and welcome to my feed!!')
        fg.author( {'name':'Nazareno Gonella','email':'nazagonella2@gmail.com'} )
        # fg.logo('http://icon.jpg')
        fg.language('en')

        # for item in self.source_path.rglob("*.html"):
        #     content = item.read_text(encoding="utf-8")     # read HTML
        #     filename = item.stem                             # filename without extension

        #     entry = fg.add_entry()
        #     entry.id(f"https://ngonella.com/feed/{filename}")    # unique ID
        #     entry.title(filename)                             # title
        #     entry.link(href=f"https://ngonella.com/{filename}")  # link
        #     entry.content(content, type='html')              # feed content

        for item in self.source_path.rglob("*.md"):
            # content = item.read_text(encoding="utf-8")      # read Markdown
            parse = ParseMarkdown(item)
            # html = markdown.markdown(content)               # convert to HTML
            filename = item.stem                             # filename without extension

            entry = fg.add_entry()
            entry.id(f"https://ngonella.com/feed/{filename}")    # unique ID
            entry.title(parse.meta["title"][0])                             # title
            entry.link(href=f"https://ngonella.com/{filename}")  # link
            entry.content(parse.content_html, type='html') 

        # fe = fg.add_entry()
        # fe.id('http://ngonella.com/feed/1')
        # fe.title('The First Episode')
        # fe.content("this is some first content <h1> HEY YOU </h1>")
        # fe.link(href="http://lernfunk.de/feed")

        # fe = fg.add_entry()
        # fe.id('http://ngonella.com/feed/2')
        # fe.title('The Second Episode')
        # fe.content("this is some content <h1> HEY YOU </h1>")
        # fe.link(href="http://lernfunk.de/feed")

        fg.rss_file(self.output_file) # Write the RSS feed to a file

        # fg.title(self.blog_title)
        # fg.link(href=self.blog_link, rel="alternate")
        # fg.description(self.blog_description)
        # author_data = {'name': self.author_name}
        # if self.author_email:
        #     author_data['email'] = self.author_email
        # fg.author(author_data)

        # markdown_files = list(self.source_path.rglob("*.md"))

        # for md_file in markdown_files:
        #     content = md_file.read_text(encoding="utf-8")
        #     html_content = markdown.markdown(content)
        #     filename = md_file.stem

        #     entry = fg.add_entry()
        #     entry.title(filename)
        #     entry.link(href=f"{self.blog_link}/{filename}")
        #     entry.description(html_content)

        # fg.rss_file(self.output_file, encoding="utf-8")
