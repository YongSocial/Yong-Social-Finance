# Yong Social Finance — static Jekyll site

Converted from `theme-7920238479426071999.xml` (a Blogger "Indie" theme) into
a standalone Jekyll site that builds and hosts for free on GitHub Pages.

## What was carried over

- **CSS**: `assets/css/blogger-base.css` is the theme's full base stylesheet
  (normalize + Blogger's Indie theme layout/typography), extracted verbatim
  from the template's `<b:skin>` block. `assets/css/custom.css` holds the
  site-specific styling — crypto ticker, topic-row cards, footer — pulled
  from the theme's HTML/CSS widgets.
- **JS**: `assets/js/crypto-ticker.js` is the live CoinGecko-powered ticker,
  unchanged — it's plain JS with no Blogger dependency.
- **Design**: header, footer, topic rows (Markets / Wealth / AI & Technology),
  sidebar (trending / archive / labels), and the YouTube "Watch" section all
  have Jekyll equivalents in `_includes/`.
- **SEO**: canonical URLs, Open Graph, Twitter Card, and Organization/
  BlogPosting JSON-LD are rebuilt in `_layouts/default.html` and
  `_layouts/post.html` using Jekyll's `jekyll-seo-tag` plugin plus custom
  schema blocks matching the original template's structured data.

## What had to change

Blogger templates don't contain your posts — they only define *how* posts
render. The theme XML you uploaded has zero actual articles in it, so:

- **Posts** now live as Markdown files in `_posts/`, one file per article,
  named `YYYY-MM-DD-slug.md`. Three placeholder posts are included so you
  can see the layout, topic rows, and category pages working.
- **Topic rows** (Markets/Wealth/AI & Technology) no longer fetch Blogger's
  `/feeds/posts/summary/-/<label>` JSON at runtime (that endpoint won't
  exist once you're off Blogger). They're built at *compile time* instead,
  by `_includes/category-sections.html` looping over `site.categories`.
  Configure which categories feed which row in `_config.yml` under
  `home_sections`.
- **Search** no longer hits Blogger's server-side search. `search.json` is
  a build-time index of all posts, and `search/index.html` filters it
  client-side with plain JS.
- **Pages** (About, Editorial Policy, Ads Disclosure, Financial Risk
  Disclaimer, Contact, Privacy) are stubbed out with placeholder copy in
  their own folders — replace the text with your real policy pages.

## Migrating your real posts from Blogger

The theme XML is not your content. To get your actual posts:

1. In Blogger: **Settings → Manage blog → Back up content** → download the
   full export (a different, much larger Atom XML with every post/comment).
2. Run:
   ```bash
   python3 scripts/blogger_export_to_jekyll.py path/to/blog-MM-DD-YYYY.xml
   python3 scripts/generate_category_pages.py
   ```
   This writes one `_posts/*.md` file per article (labels become
   `categories:`) and one page per category under `categories/`.
3. Post bodies come through as raw HTML — Jekyll renders that fine as-is,
   but skim a few for leftover Blogger-specific markup (e.g. old inline ad
   snippets) and clean up as needed.
4. Re-run `scripts/generate_category_pages.py` any time you add a post with
   a brand-new category/label.

## Local preview

Requires Ruby + Bundler (not available in the sandbox that built this, so
this hasn't been build-tested — verify locally or let GitHub Pages build it
for you):

```bash
bundle install
bundle exec jekyll serve
# -> http://localhost:4000
```

## Deploying to GitHub Pages

1. Push this folder to a GitHub repo.
2. Repo **Settings → Pages → Source**: deploy from the `main` branch (root).
3. GitHub builds it automatically using the `github-pages` gem pinned in
   `Gemfile` — no CI config needed.
4. Custom domain: add a `CNAME` file with `www.yongsocial.com` (or your
   domain) and point your DNS per GitHub's custom-domain docs.

## Things worth double-checking before launch

- `_config.yml` → `url:` is set to `https://www.yongsocial.com`; update if
  different.
- AdSense client ID in `_config.yml` (`adsense_client`) was carried over
  from the theme as-is — confirm it's still the right account.
- The original template had per-widget AdSense ad units inline in the post
  loop and sidebar; only the loader script was carried over here. Add your
  `<ins class="adsbygoogle">` ad unit tags wherever you want ads to actually
  render (e.g. inside `_layouts/post.html`).
- Favicon: point `/favicon.ico` at a real file (referenced in
  `_layouts/default.html`).
