Use the versioned image tags supplied in `.env`. When changing a tag, choose a
published tag from the image repository and review its release notes and upgrade
instructions before restarting containers.

For Wodby images that package upstream software, a tag such as
`wodby/mariadb:11.4-r0` combines the application version line (`11.4`) with a Wodby
image revision (`r0`). Major/minor tags use a revision counter per image repository.
Full-version tags, such as `11.4.2-r0`, start at `r0` again for each exact upstream
version. Revisions can include application updates and image changes; the revision
number alone does not indicate compatibility.

Previously published tags remain available. Wodby software such as Backup uses
semantic product versions, and third-party images follow their own tag formats.
See the [image revision policy](https://github.com/wodby/images#image-revisions)
for tag formats and their matching Git tags.
