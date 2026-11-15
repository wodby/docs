# Wodby documentation

`2.0/` is the Wodby 2 documentation and `1.0/` is the Wodby 1 documentation. They are separate sites with separate
builds; a change to one does not apply to the other.

## Page titles and descriptions (Wodby 2)

- The first heading of a page is its browser and search title. Write it so it makes sense on its own: "Cluster
  updates", not "Updates". Use sentence case.
- Head a catalog stack guide "<Product> stack guide", or "<Product> (buildable) stack guide", and a provider page
  "<Product> provider".
- Keep the navigation label in `2.0/mkdocs.yml` short. It does not affect the title.
- Add a `title` to the front matter only when the title should say more than the heading.
- Give every page a `description` in its front matter: one or two plain sentences, 110 to 160 characters, no Markdown.
  Update it when the page's subject changes, for example when a list in it gains a new item.

The details are in [`2.0/scripts/README.md`](2.0/scripts/README.md).

## Before pushing

```sh
python3 -m unittest discover -s 2.0/scripts -p 'test_*.py'
cd 2.0 && mkdocs build --strict
```

The tests fail when two pages share a title, a page is titled with a menu label such as "Overview", a stack or
provider page does not say what it is, or a description is missing or outside the length limits.
