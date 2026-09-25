import { defineCollection, z } from 'astro:content';
import { author } from '../data/author';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishedDate: z.date(),
    author: z.string().default(author.name),
    keywords: z.array(z.string()).optional(),
    image: z.string().optional(),
    socialImage: z.string().optional(),
    sourceUrl: z.string().url().optional(),
    draft: z.boolean().default(false),
    hideFooterCta: z.boolean().default(false),
    hideDescription: z.boolean().default(false),
    categories: z.array(z.enum(['Book Frameworks', 'Productivity', 'Growth', 'Life Transition', 'Relationships', 'Career', 'Building'])).default([]),
  }),
});

export const collections = {
  blog,
};
