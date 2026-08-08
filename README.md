# GigFee — public site

The public pages for [GigFee](https://play.google.com/store/apps/details?id=com.stagefee.stagefee),
served by GitHub Pages.

**This repository is public on purpose, and holds no application code.** The
app itself lives in a separate private repository. Nothing here should ever
be more than static HTML.

## What is here

| File | What it is |
|---|---|
| `index.html` | Landing page — what the app is, and links to the rest |
| `privacy-policy.html` | The privacy policy, including the data deletion section |

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
| Store listing → Privacy policy | `<pages-url>/privacy-policy.html` |
| App content → Data deletion → Delete account URL | `<pages-url>/privacy-policy.html#delete-my-data` |

Both must stay reachable without an app install or a login — that is a Play
requirement, not a preference.

## Publishing

Push to `main`. GitHub Pages serves it from the repository root; there is no
build step, and adding one would only create a way for the published page to
differ from the file in the repo.
