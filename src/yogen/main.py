from .watcher import WatchDogHandler
from http.server import HTTPServer, SimpleHTTPRequestHandler
from watchdog.observers import Observer
from pathlib import Path
from ._site import Site
from .defaults import build_default_files


def main():
    event_handler : WatchDogHandler = WatchDogHandler(site)
    observer = Observer()
    observer.schedule(event_handler, site.content_path, recursive=True)
    observer.start()

    http_handler = lambda *a, **kw: SimpleHTTPRequestHandler(
        *a, directory=str(site.build_path), **kw
    )

    HTTPServer(("127.0.0.1", 8000), http_handler).serve_forever()


build_default_files()
site : Site = Site(content_path="content", build_path="build", deploy_path="deploy", scripts_path="scripts", styles_path="styles", templates_path="templates")
site.build()

main()