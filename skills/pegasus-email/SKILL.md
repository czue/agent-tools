---
name: pegasus-email
description: Draft the monthly SaaS Pegasus marketing email summarizing recent release notes, for the prospect and customer mailing lists. Use when asked to draft the Pegasus monthly email/newsletter, or to archive a sent one.
allowed-tools: Read, Write, Edit, AskUserQuestion, Bash(git ls-remote*)
---

# Pegasus Monthly Email

Draft the monthly marketing email Cory sends to SaaS Pegasus's prospect and customer lists. It's a casual, first-person recap of what shipped recently, framed around whatever story/theme Cory is currently telling (not just a bulleted changelog). The two lists currently get the identical email — no free/paid split for now (see Style Guidelines).

This skill has two modes. Figure out which one applies from the user's request:

- **Draft mode** (default): generate a new draft covering releases since the last one sent.
- **Archive mode**: the user has a finished, as-sent (or about-to-be-sent) version of the email and wants it saved as a style reference for next time.

## Arguments

- `$0`: (optional) since_version — the last Pegasus version that was already covered in a previous email (e.g. "2026.6.2"). If omitted, auto-detect (see Draft Mode step 1).

## Defaults

- `default_release_notes_path`: `/home/czue/src/personal/pegasus-docs/src/content/docs/release-notes.mdx`
- `default_release_notes_url`: `https://docs.saaspegasus.com/release-notes/` (the CTA link in the email)
- `history_dir`: `<skill-dir>/history/` — one file per sent email, named `YYYY-MM.md`. Doubles as both the style reference and the archive; there's no separate curated-examples file.
- `default_oss_repo`: `saaspegasus/django-boilerplate` — the public GitHub repo backing the free tier, used for the OSS diff link (see below).

## Draft Mode

1. **Resolve since_version**:
   - If `$0` is provided, use it.
   - Else, look for the most recent file in `history_dir` (sorted by filename, `YYYY-MM.md`) whose `Sent:` header line includes a `covers <since_version> → <latest_version>` clause, and use its `latest_version`. Some early history entries predate version tracking and won't have this clause — skip past those to an older one that does, if any.
   - Else (nothing parseable), use `AskUserQuestion` to ask which version was last covered.

2. **Read the release notes** from `default_release_notes_path`. Collect every `## Version X.Y.Z` section *after* since_version, up to the newest. These are written in reverse-chronological order (newest first), so since_version marks the stopping point going down the file.

3. **Read style references**: the 3-4 most recent files in `history_dir`. These are real, as-sent emails — the most recent are the strongest signal for current voice. With only a handful of emails total, it's fine to just read all of them.

4. **Draft the email** following the Style Guidelines below. Group the release notes by theme/story, not by version number — a single email usually spans several versions.

5. **Generate the OSS diff link**: find the `OSS main SHA:` line in the same history file used for since_version (step 1). Build `https://github.com/<default_oss_repo>/compare/<that_sha>...main` and report it alongside the draft for the user to drop in wherever they want — don't embed it into the email body automatically, since placement is their call. If no history file has this line yet (e.g. the feature is new), say so and skip the link; it'll be available starting next cycle once one email has been archived with a SHA recorded.

6. **Present the draft in chat** for iteration. Don't write it to a file unless the user asks to keep iterating on one — if so, a scratch file outside this skill directory (e.g. a git-ignored `docs/` dir in whatever repo the user's working in) is fine; don't commit it.

7. **Iterate conversationally.** This is a creative/style task — discuss changes in plain prose, not via AskUserQuestion. Apply requested edits directly.

## Archive Mode

Triggered when the user shares a finished/as-sent version of the email (pasted, or "save this one", "log this as sent", etc.).

1. Determine the version range it covers (ask if not obvious from context).
2. Resolve the OSS repo's current `main` SHA: `git ls-remote https://github.com/<default_oss_repo>.git main` (no local clone needed) — this becomes next cycle's diff base, so resolve it fresh at archive time rather than reusing whatever was computed during drafting.
3. Write it to `history_dir/YYYY-MM.md` (month it was sent), using the History File Format below.
4. If the user mentions *why* they changed something from the draft (tone, structure, specific phrasing), treat that as durable style guidance — ask if they want it folded into the Style Guidelines section of this SKILL.md, and edit this file if so.

### History File Format

```markdown
Sent: YYYY-MM-DD — covers <since_version> → <latest_version>
OSS main SHA: <sha resolved at archive time>

<the full as-sent email text>
```

The `Sent:` header line is what draft mode parses to find the next since_version — keep it as the first line. (Entries from before this skill existed use `Sent: YYYY-MM (day unknown; predates version tracking in this skill)` with no `covers` clause — draft mode's since_version lookup skips those.) The `OSS main SHA:` line is what draft mode uses to build the diff link — older entries won't have it either, so the diff link just isn't available until the first email is archived post-feature.

## Style Guidelines

Based on Cory's past emails (see `history/`):

- **Voice**: casual, first-person, contractions throughout. Cory narrating what *he* did/built, not a press release. Sentence-fragment asides are fine ("Tests, linters, etc.").
- **Vary sentence rhythm** — mix short punchy lines with longer ones. Avoid uniform, essay-like paragraphs; that reads as too polished/marketing-y.
- **One story, told once.** If there's an overarching theme for the release (e.g. "verification tooling for agents"), state it once near the top and let the individual sections just describe what happened factually. Don't repeat the tie-back thesis in every section — that reads as repetitive.
- **Structure**: `[Cory's personal intro/blurb — leave as a placeholder, he writes this]`, then the "why"/theme paragraph, then either `#`-headed sections per theme (when there are several distinct threads, like the March 2026 example) or flowing narrative paragraphs without headers (when the content is more story-driven, like the Jan/May 2026 examples). Judge which fits based on how many distinct themes the release notes span.
- **Minor/miscellaneous items** (dependency bumps, small fixes, docs) don't need their own section or a bullet list — compress into a single CTA sentence linking to the full release notes, e.g.: "For the complete release notes — including X, Y, and Z — check out the [full changelog](<default_release_notes_url>)."
- **Sign-off varies** each time ("Hope you're doing well," / "Hope you're having a good start to July!" / etc.) — don't reuse the same line verbatim across emails. A `p.s.` inviting replies/feedback is a nice occasional touch, not mandatory.
- **Continuity**: when there's a natural thread, callback to something from the previous email (a stated goal, an ongoing project, a running bit) rather than starting cold each month — check the most recent `history/` file for something to reference.
- **Free vs. paid tier**: currently not called out separately even though the email goes to both prospect and customer lists — most releases apply to both. Flag it to the user if a release has a meaningfully different impact on free vs. paid users; don't split the email preemptively.
- **Avoid**: generic marketing transitions, corporate phrasing ("guardrails to move fast safely"), restating the same point across multiple sections.

## Additional Resources

- `history/` — every past email, one file per month sent. Also the style reference (see Draft Mode step 3) — most recent files are the strongest signal.
