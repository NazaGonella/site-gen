import shutil
from pathlib import Path
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from ._site import Site
from .page import Page

class WatchDogHandler(FileSystemEventHandler):
    def __init__(self, site : Site):
        super().__init__()
        self.site : Site = site

    def on_modified(self, event: FileSystemEvent) -> None:
        print("")
        mod_file_path : Path = Path(event.src_path)
        rel_path : Path = mod_file_path.relative_to(self.site.content_path)

        if (mod_file_path.is_dir()):
            return

        # print(mod_file_path)
        # print(rel_path)

        if (mod_file_path.suffix != ".md"):
            output_path: Path = self.site.build_path / rel_path
            shutil.copy2(mod_file_path, output_path)
            print("modified file:", mod_file_path, " -> ", output_path)
            return

        if (mod_file_path in self.site.pages):
            page : Page = self.site.pages[mod_file_path]
            page.parse_fields(mod_file_path)

            self.site.update_indices_for_page(page)

            template_path = self.site.templates_path / f"{page.get_field("template")}.html"
            template_content = template_path.read_text(encoding="utf-8") if template_path.exists() else ""

            output_path : Path = self.site.build_path / rel_path.parent / "index.html"
            output_path.write_text(page.render(template_content), encoding="utf-8")

            print("modified markdown file:", mod_file_path, " -> ", output_path)
        else:
            print("ERROR")  # TODO
            self.site.build()
    
    def on_created(self, event: FileSystemEvent) -> None:
        print("")
        created_file_path = Path(event.src_path)
        rel_path : Path = created_file_path.relative_to(self.site.content_path)
        build_file_path: Path = self.site.build_path / rel_path
        # print(created_file_path)
        # print(rel_path)
        # print(build_file_path)
        if created_file_path.suffix != ".md":
            if created_file_path.is_file():
                shutil.copy2(created_file_path, build_file_path)
                print("created file:", created_file_path, " -> ", build_file_path)
            elif created_file_path.is_dir():
                if build_file_path.exists():
                    print("ERROR")  # TODO
                    # shutil.rmtree(build_file_path)
                shutil.copytree(created_file_path, build_file_path)
                print("created directory:", created_file_path, " -> ", build_file_path)
        else:
            self.site.build()
            print("created markdown file:", created_file_path, "-> rebuilding...")
    
    # TODO: not rebuild when creating or deleting markdown file
    
    def on_deleted(self, event: FileSystemEvent) -> None:
        print("")
        del_file_path : Path = Path(event.src_path)
        rel_path : Path = del_file_path.relative_to(self.site.content_path)

        if del_file_path.suffix == ".md":
            build_file_path: Path = self.site.build_path / rel_path.parent / "index.html"
            if build_file_path.exists():
                # self.site.pages.pop(del_file_path, None)
                # self.site.update_indices()
                self.site.build()
                print("deleted markdown file:", del_file_path, " -> ", build_file_path, ", rebuilding...")
            else:
                print("ERROR")  # TODO
        else:
            build_file_path : Path = self.site.build_path / rel_path
            if build_file_path.exists():
                if build_file_path.is_file():
                    build_file_path.unlink()
                    print("deleted file:", del_file_path, " -> ", build_file_path)
                elif build_file_path.is_dir():
                    shutil.rmtree(build_file_path)
                    self.site.build()
                    print("deleted directory:", del_file_path, " -> ", build_file_path, ", rebuilding...")
    
    def on_moved(self, event: FileSystemEvent) -> None:
        print("")
        src_path = Path(event.src_path)
        src_rel = src_path.relative_to(self.site.content_path)
        old_build_path = self.site.build_path / src_rel

        dest_path = Path(event.dest_path)
        dest_rel = dest_path.relative_to(self.site.content_path)
        build_dest_path = self.site.build_path / dest_rel

        # print(src_path)
        # print(src_rel)
        # print(old_build_path)

        # print(dest_path)
        # print(dest_rel)
        # print(build_dest_path)

        if old_build_path.exists():
            if old_build_path.is_file() and src_path.suffix != ".md":
                old_build_path.unlink()
                print("moved file, removed old file:", old_build_path)
            elif old_build_path.is_dir():
                shutil.rmtree(old_build_path)
                self.site.build()
                print("moved directory, removed old directory:", old_build_path, ", rebuilding...")
            else:
                self.site.build()
                print("moved markdown file:", old_build_path, "\nrebuilding...")
                return

        if dest_path.suffix != ".md":
            if dest_path.is_file():
                # build_dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dest_path, build_dest_path)
                print("moved file:", dest_path, " -> ", build_dest_path)
            elif dest_path.is_dir():
                if build_dest_path.exists():
                    # shutil.rmtree(build_dest_path)
                    print("ERROR")  # TODO
                shutil.copytree(dest_path, build_dest_path)
                print("moved directory:", dest_path, " -> ", build_dest_path)
            else:
                print("ERROR")  # TODO
        else:
            self.site.build()
            print("moved markdown file:", dest_path, " -> ", build_dest_path,"\nrebuilding...")