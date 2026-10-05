# Migration and Release Versioning

This folder demonstrates the migration and release-control pattern required by the AISYS SOP.

## Structure
- versions/ - numbered migration scripts
- release notes are maintained in the docs directory

## Recommended release pattern
1. Create a new numbered migration script for each schema or data-change release.
2. Back up the database before applying a migration.
3. Validate the migration against the test suite.
4. Store a recovery backup and restore script with the release package.
5. Keep rollback instructions in the release notes.

## Prototype examples
The project currently includes a versioned migration skeleton in the `versions` folder and a backup/restore script in `scripts`.
