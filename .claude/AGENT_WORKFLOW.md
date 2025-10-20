# Modern Compass Agent Workflow

This document explains how to use the custom Claude agents for content creation and optimization.

## Available Agents

### 1. **content-scout** (Purple)
Researches trending topics and struggles across the web (Reddit, Quora, forums, etc.)

**Use for:**
- Researching what people are struggling with on specific topics
- Identifying common advice patterns and gaps
- Finding emotional language and real examples for blog content
- Understanding where Modern Compass frameworks can add value

**Example prompts:**
- "Research what people are struggling with regarding feeling stuck in their jobs"
- "What are common questions and failures around building habits?"
- "Research trending struggles with career decisions and AI impact"

### 2. **blog-writer** (Green)
Writes SEO-optimized blog posts in Josh's authentic voice.

**Use for:**
- Converting Reddit insights into full blog posts
- Writing new blog content based on topics or research
- Creating preview/teaser versions of newsletter content

**Example prompts:**
- "Write a blog post based on this Reddit discussion about [topic]"
- "Create a blog about decision-making frameworks for college"
- "Turn this newsletter into a blog preview that drives signups"

### 3. **website-marketing-strategist** (Red)
Optimizes website content, SEO, and conversion rates.

**Use for:**
- Analyzing landing page performance (especially newsletter signups)
- SEO audits and keyword research
- Meta ad conversion optimization
- Content strategy and editorial calendars

**Example prompts:**
- "Analyze the newsletter landing page and suggest improvements"
- "Audit the blog for SEO opportunities"
- "Help me optimize for Meta ad traffic conversion"

---

## Content Creation Workflow

### Option 1: Research → Blog Pipeline

**Step 1: Research Topic**
```
Research what people are struggling with regarding [topic]
```

The content-scout agent will return:
- Common struggles and emotional language
- Existing advice patterns
- Gaps Modern Compass can fill
- Suggested blog angles
- Framework alignment

**Step 2: Create Blog Post**
```
Write a blog post about [topic] based on this research: [paste summary]
```

**OR skip research and write directly:**
```
Write a blog post about [topic]
```

The blog-writer agent will create:
- Full markdown blog post (1,200-1,800 words)
- SEO-optimized with keywords
- Internal links to related content
- Newsletter CTA linking to https://themoderncompass.io/newsletter/
- Thumbnail SVG in matching style

**Step 3: Optimize for SEO (Optional)**
```
Use website-marketing-strategist agent to review this blog post for SEO
```

The agent will provide:
- SEO score and improvements
- Keyword opportunities
- Technical optimizations
- Content expansion suggestions

---

### Option 2: Direct Blog Creation

**Step 1: Write Blog**
```
Use blog-writer agent to write a blog about [topic]
```

Provide context like:
- Target audience
- Key points to cover
- Related Modern Compass frameworks
- Any research or sources

**Step 2: SEO Review**
```
Use website-marketing-strategist agent to audit this blog for SEO
```

---

### Option 3: Newsletter → Blog Preview

**Step 1: Create Preview**
```
Use blog-writer agent to create a blog preview from this newsletter:
[paste newsletter content]

Make it a teaser that drives newsletter signups without giving away the full content.
```

**Step 2: Optimize Landing Page**
```
Use website-marketing-strategist agent to optimize the newsletter signup flow
```

---

## Agent Output Locations

### Blog Posts
- **Markdown file:** `/src/content/blog/[slug].md`
- **Thumbnail:** `/public/blog-thumbnails/[slug].svg`

### Agent Reports
- Agents provide analysis and recommendations directly in chat
- Save important insights to documentation as needed

---

## Best Practices

### Content Scout
✅ **Do:**
- Research across multiple sources (Reddit, Quora, forums)
- Look for recurring themes and emotional language
- Identify what advice already exists and what's missing
- Connect findings to Modern Compass framework
- Note specific phrases people use

❌ **Don't:**
- Rely on single-source research
- Copy content directly (use for understanding)
- Research topics too narrow or generic
- Ignore advice gaps Modern Compass can fill

### Blog Writer
✅ **Do:**
- Provide clear context and target audience
- Reference existing blog posts for cross-linking
- Review output for Josh's authentic voice
- Test newsletter CTAs for specificity

❌ **Don't:**
- Accept generic or platitude-heavy content
- Skip the SEO optimization steps
- Forget to create the thumbnail SVG
- Use em dashes or smart quotes (standard ASCII only)

### Website Marketing Strategist
✅ **Do:**
- Request specific metrics (SEO score, keyword volume)
- Ask for prioritized action lists
- Get 12-month content calendars
- Focus on conversion optimization for Meta ads

❌ **Don't:**
- Implement changes without testing
- Ignore mobile-first optimization
- Forget to track KPIs after changes

---

## Example End-to-End Workflow

**Goal:** Create a blog post about feeling stuck in your job

1. **Research (Optional):** "Research what people are struggling with regarding feeling stuck in their jobs"
   - Agent searches web for common themes
   - Identifies advice gaps and emotional language
   - Suggests blog angles

2. **Write:** "Write a blog post about feeling stuck in your job with golden handcuffs"
   - Agent creates full blog post with SEO
   - Generates thumbnail SVG
   - Includes internal links and newsletter CTA

3. **Review:** Read the blog post, give feedback:
   - "Make the opening more narrative"
   - "Remove sentences starting with And or But"
   - "This section sounds too AI-generated, rewrite it"

4. **Optimize (Optional):** "Review this blog for SEO improvements"
   - Agent provides SEO score and recommendations
   - Implement critical fixes

5. **Publish:** Blog post is ready to go live!

---

## Tips for Success

1. **Be specific with prompts:** Instead of "find Reddit content," say "find trending posts about career decisions in r/careerguidance from the last 30 days"

2. **Iterate:** If blog output doesn't sound like Josh, ask agent to "rewrite this section with more optimism and builder mentality"

3. **Cross-reference:** Always check existing blog posts to avoid duplicate topics and maximize internal linking

4. **Track results:** After publishing, monitor which topics drive newsletter signups and create more of that content

5. **Batch work:** Use reddit-content-scout weekly to build a backlog of blog ideas, then write 2-3 posts at once

---

## Questions or Issues?

If an agent isn't working as expected:
- Check the agent definition in `.claude/agents/[agent-name].md`
- Ensure you're using the right tools (WebSearch, WebFetch, etc.)
- Provide more context in your prompt
- Try breaking complex requests into smaller steps

**Always... follow your compass!**

*- Josh*
