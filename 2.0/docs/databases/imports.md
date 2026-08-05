# Database Import

From `Databases > [Database] > Import` you can run an import for an individual DB.

The import source can be:

- an archive uploaded from the dashboard
- a public URL where the archive can be downloaded
- an existing backup

For a backup-based import, the source can be an existing completed backup or a fresh backup created from a compatible
source database that has a usable backup preset.

The source must stay within the destination database's [ownership boundary](../sharing.md#creation-import-and-copy-forms):

- the source and destination databases must belong to the same organization
- an organization-owned destination can import only from an organization-owned source
- for a project-owned destination, the source database must be owned by or shared with the destination's owner project, including when the source database is organization-owned

Your access to both databases through separate projects does not combine their resource boundaries. Share the source
database with the destination project before starting the import. You also need permission to view an existing source
backup or to create a fresh one.
