// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://themoderncompass.io',
  trailingSlash: 'never',
  build: {
    format: 'file',
  },
  integrations: [
    sitemap({
      // /newsletter-signup is a no-distractions ad-landing duplicate of
      // /newsletter (no nav, nothing to do but subscribe or leave) — keep
      // it out of the sitemap so it isn't offered as an organic result.
      filter: (page) => !page.includes('/newsletter-signup'),
    }),
  ],
});
