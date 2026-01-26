import os
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DOCS_ROOT = os.path.join(ROOT, "docs")

class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            for (name, value) in attrs:
                if name.lower() == "href" and value:
                    self.links.append(value)


def is_external(href: str) -> bool:
    href_lower = href.lower()
    if href_lower.startswith(("http://", "https://", "mailto:", "tel:", "javascript:")):
        return True
    # protocol-relative
    if href_lower.startswith("//"):
        return True
    return False


def resolve_local_path(source_html_path: str, href: str) -> str | None:
    # Strip query and fragment for file existence checks
    parsed = urlparse(href)
    path = parsed.path
    if not path:
        return None

    # If anchor-only or empty, ignore
    if href.startswith("#"):
        return None

    # Absolute path relative to site root
    if path.startswith("/"):
        rel = path[1:]
        # If ends with '/', assume index.html inside that folder
        if rel.endswith("/"):
            rel = os.path.join(rel, "index.html")
        return os.path.join(DOCS_ROOT, rel.replace("/", os.sep))

    # Relative path
    source_dir = os.path.dirname(source_html_path)
    rel = path
    # If ends with '/', assume index.html
    if rel.endswith("/"):
        rel = os.path.join(rel, "index.html")
    full = os.path.normpath(os.path.join(source_dir, rel.replace("/", os.sep)))
    return full


def collect_html_files(root: str):
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def main() -> int:
    if not os.path.isdir(DOCS_ROOT):
        print(f"ERROR: docs/ not found at {DOCS_ROOT}")
        return 2

    broken = []
    total_links = 0
    checked_links = 0

    for html_path in collect_html_files(DOCS_ROOT):
        try:
            with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            print(f"WARN: Cannot read {html_path}: {e}")
            continue
        parser = LinkCollector()
        try:
            parser.feed(content)
        except Exception as e:
            # If parser fails, skip but note
            print(f"WARN: HTML parse error in {html_path}: {e}")
            continue

        for href in parser.links:
            total_links += 1
            if not href or is_external(href):
                continue
            target = resolve_local_path(html_path, href)
            if target is None:
                continue
            checked_links += 1
            # Allow both file and directory with index.html
            if not os.path.exists(target):
                # Special case: if the resolved target is .../index.html, allow directory check
                if target.endswith("index.html"):
                    if os.path.isdir(os.path.dirname(target)):
                        # directory exists but missing index.html
                        broken.append((html_path, href, target))
                    else:
                        broken.append((html_path, href, target))
                else:
                    # Try also index.html when href ends with folder-like string
                    dirname, basename = os.path.split(target)
                    if basename == "" and os.path.isdir(dirname):
                        idx = os.path.join(dirname, "index.html")
                        if not os.path.exists(idx):
                            broken.append((html_path, href, idx))
                    else:
                        broken.append((html_path, href, target))

    print(f"Scanned HTML files in: {DOCS_ROOT}")
    print(f"Total hrefs found: {total_links}")
    print(f"Internal links checked: {checked_links}")

    if broken:
        print("\nBROKEN LINKS:")
        for src, href, target in broken:
            rel_src = os.path.relpath(src, ROOT)
            rel_target = os.path.relpath(target, ROOT)
            print(f"- Page: {rel_src} | href: {href} | missing: {rel_target}")
        print(f"\nTotal broken: {len(broken)}")
        return 1
    else:
        print("\nNo broken internal links detected.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
