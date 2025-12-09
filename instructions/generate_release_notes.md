## Generating Release Notes

You are helping to generate the release notes for an upcoming version of SaaS Pegasus---a
Django SaaS boilerplate built on top of cookicutter.

You will be given a diff summary file containing a set of changes that have been made in
this release. Your job is to draft the release notes according in the same style used
in the current release notes (`src/content/docs/release-notes.md`).

Important instructions:

- Read the existing release notes to get a feel for the style.
- The general format is: 1-2 sentences describing the release followed by a detailed list of changes.
- If a feature is large you can call it out into its own section at the top, but if there
  aren't any large features there is no need to do this.
- Wherever possible use information from the commit messages to understand the intent of the changes.
- Do NOT EVER mention cookiecutter. If a change only affects cookiecutter markup then translate
  the practical implications of that change in human-readable terms. E.g. "Fixed a bug that only
  applied when teams were enabled".
- For library upgrades there is no need to mention specific libraries unless explicitly called
  out in a commit message.
