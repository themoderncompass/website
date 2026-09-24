# Modern Compass website rules

## Newsletter imports

- Source: https://newsletter.themoderncompass.io. Check issue pages and user-supplied links; the archive can be stale. Compare article content, not just titles, to avoid duplicates.
- Port the approved newsletters word for word. Preserve titles, paragraphs, punctuation, spelling, personal stories, emphasis, lists, links, images, attachments, book updates, and sign-offs. Do not rewrite, summarize, correct grammar, add conclusions, or remove sections for SEO. Existing emojis and sentences are part of the source even if original-writing guidelines advise against them.
- Appearance is the only acceptable variation: use the existing blog layout, typography, spacing, semantic heading levels, and shared components. Exclude Beehiiv site navigation, comments, and other platform controls, not authored newsletter content. Use the public page's resolved greeting.
- Preserve the original publication date (and exact timestamp/offset if the source provides one). Never substitute the import date or invent a publication time. Record the original issue URL in `sourceUrl`.
- Each new post belongs in `src/content/blog/`, with relevant existing categories and a topic-specific SVG in `public/blog-thumbnails/`. Use the same artwork for the article header and blog card. Match the site's established minimalist gradient illustration style and 1200×630 canvas. Supply a PNG copy via `socialImage` for social cards and article structured data; keep the SVG for visible page artwork.
- SEO/AEO improvements belong in accurate metadata and structured data. Preserve the visible title and body. Use `hideDescription: true` to keep newly written metadata out of the imported article and `hideFooterCta: true` when the source already includes its own subscription call to action. Do not invent FAQs, claims, or keyword-stuffed prose.
- Verify rendered article text against the source, including links and embedded content. Expiring attachment URLs must be replaced with a durable copy of the same public attachment, not committed as expiring links.

## Shared appearance

- Reuse global styles in `src/layouts/Layout.astro`. Filled buttons use `mc-button`, secondary buttons use `mc-button-ghost`, and buttons on colored backgrounds use `mc-button-inverse`. Do not introduce a competing button style for an imported article.
- Reuse the existing blog page and index layouts. Keep category navigation card dimensions unchanged when resizing their icons; enlarge the artwork inside the available space and check desktop and mobile layouts.

## Validation and delivery

- Run `npm ci` and `npm run build`, verify new routes, metadata, dates, images, links, and category/latest-post placement, and visually check desktop and mobile pages.
- Deliver changes through a pull request unless Josh explicitly requests merging or publishing. Do not merge or enable automatic merging as part of preparing a PR.
- These import rules override generic original-blog-writing guidance in `.claude/agents/blog-writer.md` for newsletter ports. They apply to Codex and Claude Code alike.
