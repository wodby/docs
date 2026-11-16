# Wodby documentation

`2.0/` is the Wodby 2 documentation and `1.0/` is the Wodby 1 documentation. They are separate sites with separate
builds; a change to one does not apply to the other.

## Page titles and descriptions

These rules apply to both sites.

- The first heading of a page is its browser and search title. Write it so it makes sense on its own: "Cluster
  updates", not "Updates". Use sentence case.
- Wodby 2: head a catalog stack guide "<Product> stack guide", or "<Product> (buildable) stack guide", and a provider
  page "<Product> provider".
- Wodby 1: head a stack page "<Product> stack" and an integration page "<Product> integration".
- Keep the navigation label in `mkdocs.yml` short. It does not affect the title.
- Add a `title` to the front matter only when the title should say more than the heading.
- Give every page a `description` in its front matter: one or two plain sentences, 110 to 160 characters, no Markdown.
  Update it when the page's subject changes, for example when a list in it gains a new item.

The title and description build hooks and their tests are shared in `scripts/`. The details are in
[`2.0/scripts/README.md`](2.0/scripts/README.md).

## Before pushing

```sh
python3 -m unittest discover -s scripts
python3 -m unittest discover -s 2.0/scripts -p 'test_*.py'
(cd 1.0 && sh scripts/check-docs.sh -d ../sites/1.0)
(cd 2.0 && mkdocs build --strict -d ../sites/2.0)
```

The tests fail when two pages share a title, a page is titled with a menu label such as "Overview", a stack or provider
page (or a Wodby 1 stack or integration page) does not say what it is, or a description is missing or outside the length
limits.
