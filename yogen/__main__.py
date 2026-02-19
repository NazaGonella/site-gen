import argparse
import shutil
from yogen.website import Site
from yogen.page import Page
from yogen.watcher import WatchDogHandler
from importlib import resources
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from watchdog.observers import Observer

CONFIG_PATH = "yogen.toml"

def yogen_folder_check():
    if not Path(CONFIG_PATH).is_file():
        raise SystemExit(
            "not a yogen site. Run 'yogen create <name>'."
        )

def parse_arguments():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    create_p = sub.add_parser("create", help="Create a new site directory")
    create_p.add_argument("name", help="Site name")

    sub.add_parser("build", help="Build the site into the output directory")

    serve_p = sub.add_parser("serve", help="Serve the site locally with live reload enabled by default")
    serve_p.add_argument("port", help="Port to bind (default 8000)", type=int, nargs="?", default=8000)
    serve_p.add_argument("--no-live", help="Disable live reload on file changes", action='store_true', required=False)

    sub.add_parser("deploy", help="Push the build directory to the GitHub Pages branch set in yogen.toml")

    return parser.parse_args()


def cmd_create(name : str):
    root = Path(name)
    defaults = resources.files("yogen").joinpath("defaults")
    if root.exists():
        raise FileExistsError(root)

    with resources.as_file(defaults) as src:
        shutil.copytree(src, root)


def cmd_build():
    site : Site = Site(Path(CONFIG_PATH))
    site.build()
    # print("SECTIONS")
    # for k, v in site.sections.items():
    #     print(k, "->", [str(p.file) for p in v])

    # print("PAGE_SECTIONS")
    # for p, s in site.page_sections.items():
    #     print(str(p.file), "->", s)

    # print("TAGS")
    # for k, v in site.tags.items():
    #     print(k, "->", [str(p.file) for p in v])

    # print("PAGE_TAGS")
    # for p, tags in site.page_tags.items():
    #     print(str(p.file), "->", list(tags))

def cmd_serve(port : int, no_reload : bool):
    site : Site = Site(Path(CONFIG_PATH))
    site.build()

    if not no_reload:
        event_handler : WatchDogHandler = WatchDogHandler()
        event_handler.on_rebuild_all = site.build
        event_handler.on_rebuild_md = site.rebuild_md

        observer = Observer()
        # TODO watch templates folder: on any event, rebuild
        observer.schedule(event_handler, site.content_path, recursive=True)
        observer.start()

    http_handler = lambda *a, **kw: SimpleHTTPRequestHandler(
        *a, directory=str(site.build_path), **kw
    )

    HTTPServer(("127.0.0.1", port), http_handler).serve_forever()

def cmd_deploy():
    site : Site = Site(Path(CONFIG_PATH))
    site.deploy()


def main():
    args = parse_arguments()

    match args.cmd:
        case "create":
            cmd_create(args.name)
        case "build":
            yogen_folder_check()
            cmd_build()
        case "serve":
            yogen_folder_check()
            cmd_serve(args.port, args.no_live)
        case "deploy":
            yogen_folder_check()
            cmd_deploy()


if __name__ == "__main__":
    main()