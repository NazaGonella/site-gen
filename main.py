import time
import markdown

from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from parser import parse_markdown


class WatchDogHandler(FileSystemEventHandler):
    def on_modified(self, event: FileSystemEvent) -> None:

        mod_file_path : Path = Path(event.src_path)
        if mod_file_path.suffix == ".md":
            output : str = parse_markdown(mod_file_path)

            output_path : Path = mod_file_path.parent / "index.html"
            output_path.write_text(output, encoding="utf-8")

def main():
    target = "posts"
    watch_path = Path(target)

    event_handler = WatchDogHandler()

    observer = Observer()
    observer.schedule(event_handler, watch_path, recursive=True)
    observer.start()

    handler = lambda *a, **kw: SimpleHTTPRequestHandler(
        *a, directory=target, **kw
    )

    HTTPServer(("127.0.0.1", 8000), handler).serve_forever()

main()