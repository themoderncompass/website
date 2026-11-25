"""Import one public Modern Compass Beehiiv issue without rewriting its article."""
import argparse
from datetime import datetime, time, timedelta
from email.utils import parsedate_to_datetime
from hashlib import sha256
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import subprocess
import tempfile
import textwrap
from urllib.parse import parse_qsl, urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, build_opener
from xml.etree import ElementTree as ET
from zoneinfo import ZoneInfo

FEED = "https://rss.beehiiv.com/feeds/1yfrlTASgD.xml"
SOURCE = "newsletter.themoderncompass.io"
CENTRAL = ZoneInfo("America/Chicago")
ROOT = Path(__file__).resolve().parents[1]
POSTS = Path("src/content/blog")
ART = Path("public/blog-thumbnails")
CONTENT = "{http://purl.org/rss/1.0/modules/content/}encoded"
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
SIGNED = re.compile(r"^(?:x-amz-|x-goog-|signature$|expires$|token$|policy$|key-pair-id$)", re.I)
VOID = set("br hr img source wbr col".split())
TAGS = set(("p div span h1 h2 h3 h4 h5 h6 b strong i em u s del sub sup br hr ol ul li "
            "a img picture source figure figcaption blockquote pre code table caption "
            "thead tbody tfoot tr th td colgroup col dl dt dd mark small cite abbr wbr").split())
ATTR = {
    "a": {"href", "title", "download"},
    "img": {"src", "srcset", "alt", "width", "height", "title", "sizes"},
    "source": {"src", "srcset", "media", "type", "sizes"},
    "ol": {"start", "reversed", "type"}, "li": {"value"},
    "th": {"colspan", "rowspan", "scope"}, "td": {"colspan", "rowspan"},
    "col": {"span"}, "colgroup": {"span"}, "abbr": {"title"},
}
TAXONOMY = {
    "Growth": r"\b(grow\w*|learn\w*|confidence|strengths|personal development|self[- ]\w+|health)\b",
    "Life Transition": r"\b(direction|transition|change careers|life change|starting over|turning point|uncertainty|next chapter)\b",
    "Relationships": r"\b(relationship\w*|marriage|parent\w*|daughters|son|family|friend\w*|spouse|connection\w*)\b",
    "Productivity": r"\b(productivit\w*|time management|habit\w*|discipline|focus|routine\w*|schedule\w*)\b",
    "Career": r"\b(career\w*|job\w*|workplace|profession\w*|manager\w*|employ\w*)\b",
    "Building": r"\b(build\w*|creat\w*|entrepreneur\w*|business|launch\w*|founder|newsletter growth)\b",
    "Book Frameworks": r"\b(framework\w*|self awareness|calibrated trust|mutual influence|minimum requirements|affinity|resonance|timeos)\b",
}
MOTIFS = {
    "direction": ('A route splitting into three paths', '<path d="M-160 132 Q-98 42 0 34 Q105 20 151 -104 M0 34 Q60 -2 87 -134 M0 34 Q-4 -34 -65 -97"/><circle cx="-160" cy="132" r="9"/><circle cx="151" cy="-104" r="10"/><circle cx="87" cy="-134" r="10"/><circle cx="-65" cy="-97" r="10"/>'),
    "Growth": ('Shoots growing from a seed', '<path d="M0 141V-10 Q0 -120 98 -132 Q94 -32 0 -10 Q-11 -104 -117 -104 Q-112 -22 0 16 M-111 146H111"/><circle cx="0" cy="48" r="15"/>'),
    "Life Transition": ('An open doorway and a path beyond it', '<path d="M-85 110V-130H77V110 M-85 -130L23 -99V129L-85 110 M25 109L150 74 M76 110L150 135"/><circle cx="0" cy="21" r="4"/>'),
    "Relationships": ('Two intersecting paths', '<path d="M-145 123C-26 116 -42 -108 135 -112 M-141 -110C11 -106 4 113 143 116"/><circle cx="-145" cy="123" r="12"/><circle cx="135" cy="-112" r="12"/><circle cx="-141" cy="-110" r="12"/><circle cx="143" cy="116" r="12"/>'),
    "Productivity": ('A clock and a marked interval', '<circle r="117"/><path d="M0 -117A117 117 0 0 1 117 0 M0 -73V0L59 30 M0 96v19 M-117 0h19 M96 0h19"/>'),
    "Career": ('A sequence of steps climbing toward a horizon', '<path d="M-145 120H-69V62H3V0H75V-61H151 M75 -61V-111H149L120 -87H75"/>'),
    "Building": ('Three offset building blocks', '<path d="M-132 110v-62h89v62z M-45 110V-9H44v119z M43 110v-180h89v180z M-132 130h264"/>'),
    "Book Frameworks": ('Four points aligned on a simple grid', '<path d="M0 -126L126 0 0 126 -126 0ZM-126 0H126M0 -126V126"/><circle r="25"/><circle cy="-126" r="8"/><circle cy="126" r="8"/><circle cx="-126" r="8"/><circle cx="126" r="8"/>'),
}


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def read_feed(fixture):
    limit = 6_000_000
    if fixture:
        with fixture.open("rb") as source:
            data = source.read(limit + 1)
    else:
        with build_opener(NoRedirect).open(FEED, timeout=25) as source:
            data = source.read(limit + 1)
    if len(data) > limit or b"<!doctype" in data.lower() or b"<!entity" in data.lower():
        raise ValueError("Unsafe or oversized feed")
    return ET.fromstring(data.decode("utf-8-sig")).findall("./channel/item")


def identity(url):
    u = urlsplit(url)
    if u.scheme != "https" or u.netloc.lower() != SOURCE or not re.fullmatch(r"/p/[a-z0-9-]+/?", u.path):
        raise ValueError("Unexpected Beehiiv article URL")
    slug = u.path.rstrip("/").split("/")[-1]
    if not SLUG.fullmatch(slug) or len(slug) > 150:
        raise ValueError("Unexpected slug")
    return f"https://{SOURCE}/p/{slug}", slug


def url_for(value, base, image=False):
    if value.startswith("#") and not image:
        return value
    result = urljoin(base, value)
    u = urlsplit(result)
    if (u.scheme not in ({"https"} if image else {"https", "mailto", "tel"})
            or (u.scheme == "https" and (not u.hostname or u.username or u.password))
            or any(ch in result for ch in "\r\n\t\\")):
        raise ValueError("Unsupported link or image URL; review the source manually")
    if any(SIGNED.search(key) for key, _ in parse_qsl(u.query)):
        raise ValueError("A signed attachment needs a verified durable copy before import")
    return result


class Article(HTMLParser):
    """Whitelist article markup; fail closed rather than silently losing embeds."""
    def __init__(self, url):
        super().__init__(convert_charrefs=True)
        self.url = url
        self.stack = []
        self.parts = []
        self.words = []
        self.body_count = 0
        self.images = []
        self.links = []
        self.semantics = []

    @property
    def inside(self):
        return any(mode == "body" for _, mode in self.stack) and not any(mode == "skip" for _, mode in self.stack)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_starttag(self, tag, attrs):
        attrs = {k: v for k, v in attrs}
        classes = set((attrs.get("class") or "").split())
        mode = ""
        if tag == "style" or "beehiiv__footer" in classes:
            mode = "skip"
        elif tag == "div" and "beehiiv__body" in classes and not self.inside:
            mode = "body"
            self.body_count += 1
        elif self.inside:
            if tag not in TAGS:
                raise ValueError("Unsupported article markup; review the source manually")
            mode = "render"
            keys = ATTR.get(tag, set()) | {"id", "lang", "dir"}
            out = []
            for k, v in attrs.items():
                if k not in keys:
                    continue
                if k in {"href", "src"}:
                    if not v or not v.strip():
                        raise ValueError("Empty article link or image")
                    v = url_for(v, self.url, image=(k == "src"))
                    if k == "href":
                        self.links.append(v)
                    elif tag == "img":
                        self.images.append(v)
                elif k == "srcset":
                    # The comma-delimited syntax also allows commas in CDN URLs.
                    # Preserve simple candidate sets; don't misread ambiguous ones.
                    vals = re.split(r",\s+(?=\S)", v or "")
                    if not vals or any(not x.split() for x in vals):
                        raise ValueError("Unsupported responsive image markup")
                    v = ", ".join(" ".join([url_for(p[0], self.url, image=True), *p[1:]]) for p in map(str.split, vals))
                out.append(f' {k}="{escape(v, quote=True)}"' if v is not None else f" {k}")
            if tag == "img" and not attrs.get("src"):
                raise ValueError("Image needs an original source URL")
            self.parts.append(f"<{self.output_tag(tag)}{''.join(out)}>")
            if tag not in {"div", "span"}:
                self.semantics.append(self.output_tag(tag))
        if tag not in VOID:
            self.stack.append((tag, mode))

    @staticmethod
    def output_tag(tag):
        return "h2" if tag == "h1" else tag

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1][0] != tag:
            raise ValueError("Article HTML is not balanced; review the source manually")
        _, mode = self.stack.pop()
        if mode == "render":
            self.parts.append(f"</{self.output_tag(tag)}>")

    def handle_data(self, data):
        if self.inside:
            data = re.sub(r"\{\{\s*name\s*\|\s*there\s*\}\}", "there", data)
            if "{{" in data or "{%" in data:
                raise ValueError("Unresolved publication personalization needs a public-page check")
            self.words.append(data)
            # Literal linefeeds keep their HTML text semantics without breaking a Markdown HTML block.
            self.parts.append(escape(data, quote=False).replace("\r", "&#13;").replace("\n", "&#10;"))

    def parse(self, raw):
        self.feed(raw)
        self.close()
        if self.body_count != 1 or self.stack or len(" ".join(self.words).split()) < 100:
            raise ValueError("Expected one complete article body; no teaser-only import")
        return "<div>\n" + "".join(self.parts) + "\n</div>\n"


def third_saturday(today):
    return today.weekday() == 5 and 15 <= today.day <= 21


def tags_for(title, text):
    scores = [(4 * len(re.findall(p, title, re.I)) + min(5, len(re.findall(p, text, re.I))), k)
              for k, p in TAXONOMY.items()]
    scores.sort(key=lambda pair: -pair[0])
    return [k for n, k in scores[:2] if n >= max(2, scores[0][0] * 0.45)] or ["Growth"]


def normalized(value):
    return re.sub(r"[\W_]+", "", value.casefold())


def already_imported(slug, url, title):
    for file in (ROOT / POSTS).glob("*.md"):
        if file.stem == slug:
            return True
        raw = file.read_text()
        front = raw.split("---", 2)[1] if raw.startswith("---") and raw.count("---") >= 2 else ""
        fields = dict(re.findall(r"^(title|sourceUrl):\s*(.+)$", front, re.M))
        old_url = fields.get("sourceUrl", "").strip("'\"")
        old_title = fields.get("title", "").strip("'\"")
        if old_url.split("?")[0].split("#")[0].rstrip("/") == url or normalized(title) == normalized(old_title):
            return True
        # Some historical posts used a different slug and title. A link to
        # precisely this source in the metadata is already handled above.
    return False


def make_svg(title, categories, slug):
    motif = "direction" if re.search(r"\b(direction|compass|path|crossroads)\b", title, re.I) else categories[0]
    label, art = MOTIFS[motif]
    colors = [("#a23ce0", "#1685db", "#fa724a"), ("#b92890", "#7755dc", "#ef9b3b"),
              ("#7c4be5", "#226ace", "#f57953"), ("#982ea8", "#4381d9", "#f5b444")]
    a, b, c = colors[int(sha256(slug.encode()).hexdigest(), 16) % len(colors)]
    lines = textwrap.wrap(title, width=20, max_lines=4, placeholder="…")
    longest = max(map(len, lines))
    size = min(76, 1180 // max(1, longest))
    y0 = 315 - (len(lines) - 1) * (size + 8) // 2
    text = "".join(f'<text x="76" y="{y0+i*(size+8)}" font-size="{size}">{escape(line)}</text>'
                   for i, line in enumerate(lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(label)}</desc>
<defs><linearGradient id="accent" x1="0%" y1="100%" x2="100%" y2="0%">
<stop stop-color="{a}"/><stop offset=".50" stop-color="{b}"/><stop offset="1" stop-color="{c}"/></linearGradient></defs>
<rect width="1200" height="630" fill="#fbf8f4"/>
<rect x="20" y="20" width="1160" height="590" rx="22" fill="none" stroke="#e7ddd8" stroke-width="2"/>
<g transform="translate(897 316)">
<circle r="192" fill="url(#accent)" opacity=".08"/>
<circle r="160" fill="none" stroke="#272432" stroke-opacity=".14" stroke-width="2" stroke-dasharray="3 9"/>
<g fill="none" stroke="url(#accent)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">{art}</g>
</g>
<path d="M76 136H146" stroke="url(#accent)" stroke-width="5" stroke-linecap="round"/>
<g font-family="DejaVu Sans,sans-serif" fill="#201b2c">
<text x="76" y="113" font-size="23" font-weight="700" letter-spacing="4">MODERN COMPASS</text>
<g font-weight="700" letter-spacing="-1.5">{text}</g>
<text x="76" y="535" font-size="20" letter-spacing="3">{escape(" / ".join(categories).upper())}</text>
</g></svg>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", type=str)
    parser.add_argument("--scheduled", action="store_true")
    parser.add_argument("--feed-file", type=Path, help="Use a local RSS fixture for testing")
    parser.add_argument("--output-file", type=Path, help="Write the imported slug for the workflow")
    args = parser.parse_args()
    if args.scheduled == bool(args.slug) or (args.slug and not SLUG.fullmatch(args.slug)):
        parser.error("Select exactly one of --scheduled or --slug")
    now = datetime.now(CENTRAL)
    if args.scheduled and not third_saturday(now.date()):
        return
    candidates = []
    for item in read_feed(args.feed_file):
        url, slug = identity(item.findtext("link") or "")
        if args.slug and slug != args.slug:
            continue
        date = parsedate_to_datetime(item.findtext("pubDate") or "")
        if date.tzinfo is None or date > now:
            continue
        if args.scheduled and date.astimezone(CENTRAL).date() != now.date() - timedelta(days=1):
            continue
        candidates.append((date, item, url, slug))
    if not candidates:
        if args.slug:
            raise ValueError("Requested slug is not a published issue in the feed")
        print("No issue published on the third Friday; use the manual trigger if it was delayed.")
        return
    date, item, url, slug = max(candidates, key=lambda record: record[0])
    title = item.findtext("title") or ""
    if not title.strip() or any(ord(c) < 32 for c in title):
        raise ValueError("Invalid original issue title")
    if already_imported(slug, url, title):
        print("This issue is already on the blog; no changes made.")
        return
    article = Article(url)
    body = article.parse(item.findtext(CONTENT) or "")
    text = " ".join(" ".join(article.words).split())
    categories = tags_for(title, text)
    description = " ".join((item.findtext("description") or "").split())
    if len(description) < 25 or "<" in description:
        description = f"{title}, from the Modern Compass newsletter by Josh Imholte."
    props = {
        "title": title, "description": description, "author": "Josh Imholte", "sourceUrl": url,
        "image": f"/blog-thumbnails/{slug}.svg", "socialImage": f"/blog-thumbnails/{slug}.png",
        "draft": False, "hideDescription": True, "hideFooterCta": any(
            urlsplit(link).hostname == "themoderncompass.io" and urlsplit(link).path.rstrip("/") == "/newsletter"
            for link in article.links
        ), "categories": categories,
    }
    front = "\n".join(f"{key}: {json.dumps(val, ensure_ascii=False)}" for key, val in props.items())
    with tempfile.TemporaryDirectory() as tmp:
        svg = Path(tmp) / "thumb.svg"
        png = Path(tmp) / "thumb.png"
        svg.write_text(make_svg(title, categories, slug))
        subprocess.run(["inkscape", str(svg), f"--export-filename={png}"], check=True, capture_output=True)
        for src, suffix in [(svg, "svg"), (png, "png")]:
            destination = ROOT / ART / f"{slug}.{suffix}"
            if destination.exists():
                raise ValueError("Thumbnail already exists without a matching post")
        for src, suffix in [(svg, "svg"), (png, "png")]:
            (ROOT / ART / f"{slug}.{suffix}").write_bytes(src.read_bytes())
    (ROOT / POSTS / f"{slug}.md").write_text(f"---\npublishedDate: {date.isoformat()}\n{front}\n---\n\n{body}")
    if args.output_file:
        args.output_file.write_text(slug + "\n")
    print(f"Prepared one post with {len(article.images)} inline images and {len(categories)} categories.")


if __name__ == "__main__":
    main()
