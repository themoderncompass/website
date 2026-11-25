"""Compare a generated Astro article with the import recorded in Markdown."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys


class Content(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tokens = []
        self.text = []
        self.urls = []
        self.has_body = False
        self.active = False
        self.depth = 0

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "div" and "post-content" in attrs.get("class", "").split():
            self.has_body = self.active = True
            self.depth = 1
            return
        if not self.active:
            return
        if tag == "div":
            self.depth += 1
        if tag not in {"div", "span"}:
            self.tokens.append(tag)
        if tag in {"img", "a"}:
            self.urls.append((tag, attrs.get("src" if tag == "img" else "href")))

    def handle_endtag(self, tag):
        if self.active and tag == "div":
            self.depth -= 1
            if self.depth == 0:
                self.active = False

    def handle_data(self, data):
        if self.active:
            self.text.append(data)

    def result(self):
        return (" ".join("".join(self.text).split()), self.tokens, self.urls)


def check(slug):
    post = Path(f"src/content/blog/{slug}.md").read_text()
    front, body = post.split("---", 2)[1:]
    route = Path(f"dist/blog/{slug}.html")
    built_html = route.read_text()
    source, built = Content(), Content()
    source.feed(f'<div class="post-content">{body}</div>')
    built.feed(built_html)
    assert built.has_body, "Rendered article body not found"
    assert source.result() == built.result(), "Rendered text, structure, links, or images differ"
    categories = json.loads(re.search(r"^categories:\s*(.*)$", front, re.M)[1])
    assert 1 <= len(set(categories)) <= 2, "Expected one or two categories"
    assert f"/blog-thumbnails/{slug}.svg" in built_html and f"/blog-thumbnails/{slug}.png" in built_html
    assert f'/blog/{slug}' in Path("dist/blog.html").read_text(), "Missing from blog index"
    print(f"Verified rendered article, categories and thumbnail paths: {slug}")


if __name__ == "__main__":
    check(sys.argv[1])
