from feedgen.feed import FeedGenerator
from pathlib import Path
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

        for item in self.source_path.rglob("*.md"):
            parse = ParseMarkdown(item)
            filename = item.stem                             # filename without extension

            entry = fg.add_entry()
            entry.id(f"https://ngonella.com/feed/{filename}")    # unique ID
            entry.title(parse.meta["title"][0])                             # title
            entry.link(href=f"https://ngonella.com/{filename}")  # link
            entry.content(parse.content_html, type='html') 

        fg.rss_file(self.output_file)