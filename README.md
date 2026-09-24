# Global Bridge

The Global Bridge website: VIP business and travel services for principals
moving between Europe, North Africa and the Gulf.

The site is a purchased Framer template, exported as static HTML, rebranded
and rewritten for Global Bridge. There is no build step to deploy: the
repository root is the site. Serve it with any static host.

## Layout

    index.html            home
    about/ services/ contact/
    journal/              six articles, driven by Framer's CMS data
    legal/                privacy policy and terms of service
    404.html
    assets/animate/       the page modules React hydrates from, plus the CMS data
    assets/brand/         the Global Bridge marks
    assets/css|fonts|images|videos|meta
    tools/                the rebranding pipeline
    DESIGN.md             the brand's colours, type and spacing

## Rebranding a fresh export

The template's export is machine-generated: a single 500KB HTML file per
route, with every string repeated once per responsive variant, again in the
hydration payload React re-renders from, again in the page modules, and again
in the search index. Editing that by hand is neither reviewable nor
repeatable, so every change is a rule in `tools/` instead.

Drop a clean export in place and run:

    ./tools/build.sh

    recolor.py          the template's palette -> the DESIGN.md tokens
    logo.py             the template's mark -> the Global Bridge monogram
    rewrite-content.py  the copy, and the maps the other three read
    rewrite-js.py       the same copy inside the page modules
    rewrite-cms.py      ...and inside Framer's CMS records
    rewrite-meta.py     ...and inside the site search index
    photos.py           the template's stock photography -> ours

Each stage expects the untouched template, so always start from a clean
export rather than re-running over an already-rebranded tree.

`framercms.py` is a reader and writer for Framer's `.framercms` format, which
the journal's "Load More" reads at runtime. Its index stores each record's
byte offset, so changing any string there means rewriting both files.

## Still to do

- Replace the template's stock photography. `tools/photos.py` lists every
  slot and its shape; drop a file into `assets/photos/` and re-run it.
- Replace the placeholder statistics, testimonials and prices with real ones.
- Have the legal pages reviewed; they keep the template's structure.
