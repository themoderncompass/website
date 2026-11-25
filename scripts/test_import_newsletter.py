from datetime import date
import unittest
import xml.etree.ElementTree as ET

from import_newsletter import Article, TAXONOMY, already_imported, identity, make_svg, tags_for, third_saturday

ISSUE = "https://newsletter.themoderncompass.io/p/finding-direction-from-an-unlikely-place"


class NewsletterTest(unittest.TestCase):
    def test_third_saturday_each_month(self):
        for year in range(2026, 2031):
            for month in range(1, 13):
                self.assertEqual(sum(third_saturday(date(year, month, day)) for day in range(1, 29)), 1)
        self.assertTrue(third_saturday(date(2026, 12, 19)))
        self.assertFalse(third_saturday(date(2026, 12, 12)))

    def test_duplicate_with_different_filename(self):
        url, slug = identity("https://newsletter.themoderncompass.io/p/reclaim-your-time")
        self.assertTrue(already_imported(slug, url, "An unrelated alias"))
        url, slug = identity("https://newsletter.themoderncompass.io/p/vice-city-vices-bad-habits-and-breaking-both")
        self.assertTrue(already_imported(slug, url, "Vice City"))

    def test_content_and_platform_chrome(self):
        fixture = ("<div class='beehiiv'><style>platform style</style><div class='beehiiv__body'>"
                   "<p>Hello {{ name | there }},</p><h2 id='heading'>A heading</h2>"
                   "<ol start='3'><li><b>Original</b> &amp; <i>emphasis</i></li></ol>"
                   "<p>" + "Original words. " * 70 + "</p>"
                   "<img alt='Caption' src='https://media.beehiiv.com/photo.png' onerror='untrusted()'>"
                   "<a href='https://example.org/example?x=1&amp;y=2'>Original link</a>"
                   "</div><div class='beehiiv__footer'>Powered by beehiiv</div></div>")
        article = Article(ISSUE)
        body = article.parse(fixture)
        self.assertIn("<p>Hello there,</p>", body)
        self.assertIn('<ol start="3"><li><b>Original</b> &amp; <i>emphasis</i></li></ol>', body)
        self.assertEqual(article.images, ["https://media.beehiiv.com/photo.png"])
        self.assertEqual(article.links, ["https://example.org/example?x=1&y=2"])
        for excluded in ("onerror", "Powered by beehiiv", "platform style"):
            self.assertNotIn(excluded, body)

    def test_unsupported_material_needs_review(self):
        for fragment in ("<iframe></iframe>",
                         '<a href="https://example.org/file?X-Amz-Signature=abc">PDF</a>',
                         '<a href="javascript:void(0)">unsafe link</a>'):
            with self.subTest(fragment=fragment), self.assertRaises(ValueError):
                Article(ISSUE).parse(f'<div class="beehiiv__body">{fragment}</div>')

    def test_thumbnail_and_existing_categories(self):
        title = "Finding Direction From an Unlikely Place"
        tags = tags_for(title, "direction learn grow strengths")
        self.assertIn("Life Transition", tags)
        self.assertLessEqual(len(tags), 2)
        self.assertTrue(set(tags) <= TAXONOMY.keys())
        art = ET.fromstring(make_svg(title, tags, "finding-direction"))
        self.assertEqual((art.get("width"), art.get("height")), ("1200", "630"))
        self.assertNotEqual(make_svg(title, tags, "finding-direction"),
                            make_svg("Breaking a Bad Habit", ["Productivity"], "break-a-habit"))


if __name__ == "__main__":
    unittest.main()
