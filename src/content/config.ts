import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishedDate: z.date(),
    author: z.string().default('Josh Imholte'),
    keywords: z.array(z.string()).optional(),
    image: z.string().optional(),
    draft: z.boolean().default(false),
    categories: z.array(z.enum(['Book Frameworks', 'Productivity', 'Growth', 'Life Transition', 'Relationships', 'Career', 'Building'])).default([]),
  }),
});

export const collections = {
  blog,
};
