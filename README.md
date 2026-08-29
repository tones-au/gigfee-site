# GigFee public site

The public pages for [GigFee](https://play.google.com/store/apps/details?id=com.stagefee.stagefee),
served by GitHub Pages.

**This repository is public on purpose, and holds no application code.** The
app itself lives in a separate private repository. Nothing here should ever
be more than static HTML.

## What is here

Served at **<https://gigfee.tones-au.com>**.

| File | What it is |
|---|---|
| `index.html` | Landing page - what the app is, and links to the rest |
| `guides/` | The long-form pages. One directory per guide, each an `index.html`, so the URLs have no file extension |
| `privacy-policy.html` | The privacy policy, including the data deletion section |
| `terms.html` | Terms of use |
| `assets/site.css` | Tokens, masthead, footer and the guide layout, shared by every page |
| `assets/cards/` | The search and social cards, three aspect ratios per guide |
| `tools/make-cards.py` | Regenerates `assets/cards/`. Not served, and nothing runs it automatically |
| `sitemap.xml` | Every URL on the site. **A new guide is not finished until it is in here.** |
| `CNAME` | The custom domain. Deleting it drops the site back to the `github.io` URL and breaks every link on the Play listing. |

## The guides

`guides/` holds explanatory pages about superannuation, tax and invoicing for
Australian musicians. They exist to be found in search, so a few things are
load-bearing rather than decorative:

- **Every factual claim names its source**, in the disclosure block at the foot
  of the page, with the date the page was checked. These pages talk about tax
  and super. Getting a number wrong is not a typo, it is bad advice to somebody
  who acted on it.
- **Each page carries `Article` structured data** with a three-ratio image
  array (16:9, 4:3, 1:1), which is what Google asks for and what gets a
  thumbnail next to the result. The cards come from `tools/make-cards.py`.
- **The homepage carries `WebSite` and `Organization` nodes.** That is what
  Google reads for the site name in a search result. Without them the homepage
  result gets titled with the bare domain, which is where this started.
- **Pages reference the homepage's `@id`s** (`#website`, `#organisation`)
  rather than redeclaring the organisation. Change the homepage node and every
  page follows.

Adding a guide means: the directory and its `index.html`, three cards, an entry
in `sitemap.xml`, a card on `guides/index.html`, and a related-links card on
the guides it relates to. There is no build step to do any of that for you,
which is the trade for there being no build step at all.

## Why the policy lives here rather than beside the app

It used to sit in the app repo, in `store/`. It moved because the copy that
is actually *served* is the one with legal effect, and two copies of a privacy
policy is how a live page ends up a version behind the truth. This is the
canonical copy; the app repo points at it.

The practical consequence: **if a change to the app changes what data leaves
the device, the policy edit belongs in this repository, in the same sitting.**

## Play Console fields these pages fill

| Console field | URL |
|---|---|
| Store listing → Privacy policy | `https://gigfee.tones-au.com/privacy-policy.html` |
| App content → Data deletion → Delete account URL | `https://gigfee.tones-au.com/privacy-policy.html#delete-my-data` |
| Store presence → Website | `https://gigfee.tones-au.com/` |

Both must stay reachable without an app install or a login. That is a Play
requirement, not a preference.

## Publishing

Push to `main`. GitHub Pages serves it from the repository root; there is no
build step, and adding one would only create a way for the published page to
differ from the file in the repo.
