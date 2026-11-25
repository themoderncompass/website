# Beehiiv newsletter imports

The setup PR includes the November 20 issue, “Finding Direction From an Unlikely Place,” as the pilot. Merging it publishes the pilot through the ordinary website deployment and adds the workflow to the default branch. No other historical issues are backfilled.

The workflow checks the public feed at approximately 9:23 a.m. Central on the third Saturday. GitHub cron starts a lightweight calendar job on Saturdays; otherwise there is no checkout, feed request, or import. The importer looks for the published issue from the preceding Friday. A delayed issue can be picked up manually in **Actions → Prepare monthly newsletter PR → Run workflow** using its slug. Manual runs default to dry run. After merge, running against the pilot reports that it already exists; use a new published issue for a full remote test.

The importer keeps authored text, order, semantic markup, links, inline image URLs, original URL and publication timestamp. It removes Beehiiv styling and footer chrome. Existing URL, slug, and title matches are skipped. The blog entry gets one or two existing categories, a search description, a topic-based 1200×630 SVG for the blog and article, and PNG social art. Check these in review. If RSS omits a component present in the web issue, add it before merging. Unrecognized embeds, unresolved personalization, and detected signed URLs stop the run for manual review. Save expiring public attachments under public/downloads/ when completing those imports manually, as in the existing discipline post.

For write-enabled runs, GitHub Actions must be allowed to push an issue branch and create a pull request. If blocked, check **Settings → Actions → General → Workflow permissions → Allow GitHub Actions to create and approve pull requests**. The workflow never approves, merges or pushes to the default branch. No Beehiiv account, API key or email access is needed.

Local test (Python 3 and Inkscape required), from a clean checkout without the pilot:

    python -m unittest discover -s scripts -p 'test_*.py'
    python scripts/import_newsletter.py --slug finding-direction-from-an-unlikely-place
    npm ci
    npm run build
    python scripts/verify_newsletter.py finding-direction-from-an-unlikely-place

Pass --feed-file to run against a local RSS fixture. A successful local test or setup PR does not verify that remote schedules or PR permissions have run.
