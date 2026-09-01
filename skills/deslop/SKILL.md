---
name: deslop
description: Clean up LLM-style comments and docstrings in the current branch's changes. Use when the user says "deslop", "clean up the comments", "de-slop this", or before opening a PR on AI-written code.
allowed-tools: Bash(git *), Read, Edit, Grep, Glob
argument-hint: "[files...]"
---

# Deslop

Strip the tells of LLM-written code from the current change. Right now this is
scoped to **comments and docstrings only** — never change code behavior. (The
scope will grow as other consistent patterns show up; add them below as they do.)

## What to operate on

- If files are given as arguments, those files.
- Otherwise, the current branch's changes: `git diff main...HEAD --name-only`
  plus anything uncommitted (`git diff --name-only`, `git ls-files --others
  --exclude-standard`). If you wrote the code earlier in this session you
  already know the files — still run the diff so you don't miss any.

Only touch comments in hunks this branch added or changed. Leave pre-existing
comments alone even if they're bad; that's a separate cleanup.

## The test

For every comment or docstring in the change, ask: **would this be useful to
someone reading the file cold, with no knowledge of this PR or the conversation
that produced it?** If not, delete it. If yes, make it as short as it can be
while still being useful.

## What to delete

**Narration of what the code does.** The code already says it.

```python
# Iterate over the users and send each one an email
for user in users:
    send_email(user)
```
→ no comment.

**History and process.** Anything that only makes sense relative to the PR,
the conversation, or a previous version of the code. Watch for "previously",
"now", "updated to", "replaced", "no longer", "instead of", "this was".

```python
# Previously this used a raw SQL query, but we now use the ORM
# to handle the filtering, which also fixes the timezone issue.
qs = Event.objects.filter(start__gte=now)
```
→ no comment. (If the timezone fix is genuinely non-obvious, keep *that*:
`# filter in DB so start is compared in UTC`.)

**Section banners and restated names.**

```python
# ---- Helper functions ----

def get_user_email(user):
    """Get the user's email."""
    return user.email
```
→ no banner, no docstring.

**Docstrings that enumerate the obvious.** A three-line function does not need
Args/Returns sections. If the parameter names already say what they are, don't
repeat them.

## What to keep (but shorten)

**Why comments** — constraints, workarounds, non-obvious behavior, "must stay
in sync with X", links to issues or docs. These earn their place, but they are
almost always too long. A *why* is usually five to ten words. If it's three
lines, it's either explaining the code (delete) or wrapping a short reason in
narrative (cut to the reason).

The most common bloat: **stating the reason, then walking through the failure
mechanism.** Keep the reason. Drop the chain of what-would-go-wrong-otherwise —
if someone needs it, they'll remove the line and find out.

```
- # Tracebacks are stored up to 100 KB. That is far too much to repeat for every run in a list, and
- # the root error is at the end, so the tail is what gets kept.
+ # Tracebacks are stored up to 100 KB. Keep the tail, where the root error is.
```

```
- // Keep the resume cache in memory. Backed by localStorage it throws QuotaExceededError from
- // inside a promise callback once storage is near its cap, stranding the upload with no error.
+ // Keep the resume cache in memory so uploads work even when localStorage is nearly full
```

```
- // Before openTab, which matches on tab id: repointing first lets follow mode select the tab
- // this just moved onto the draft instead of opening a second one for the same notebook.
+ // point at the new draft before opening the tab
```

```
- # Unlike Create, a stored job can have a null trigger_condition (e.g. carried over from a
- # cron schedule) — it just means the job never actually runs.
+ # legacy jobs can have a null trigger_conditions so allow them (unlike Create)
```

Notice the rewrites are sometimes *less precise* than the originals. That's
fine. A comment is a pointer, not a proof.

**Docstrings that describe everything the function doesn't do.** Say what it
does. Leave out the list of things it leaves alone.

```
-  * Repoint every open tab for one notebook at the draft the agent just edited, so the edit is
-  * visible where the user is already looking. Pins are cleared, since a version or snapshot view
-  * would keep showing cells the edit did not touch. Tabs for other notebooks, the selection, and
-  * the tab count are all left alone — a notebook that is not open stays closed.
+  * Repoint every open tab for a notebook at a specific draft ID.
```

```
-         A cell that reads from a source needs a job's window to translate at all.
-
-         Without one its wrapper rejects the translation for a missing start_datetime, and
-         steps_to_cells answers a rejected step with an empty cell — so the preview would execute
-         nothing, succeed, and return no output.
+         A cell that reads from a source needs a job's window to translate at all,
+         since it can be dependent on variables provided by the job.
```

**Docstrings on public/non-trivial functions** — keep a one-line summary. Add
detail only for things the signature doesn't tell you (side effects, raised
exceptions, surprising return shapes).

**Match the surrounding file.** If the code around the change (not from this
branch) has no docstrings, new functions in it probably shouldn't either. If
the module uses full Google-style docstrings everywhere, follow that.

## Never touch

- `TODO` / `FIXME` / `HACK` markers (shorten the text if bloated, but keep the marker)
- Tooling directives: `# noqa`, `# type: ignore`, `# pragma:`, `# fmt:`, `eslint-disable`, etc.
- License headers
- Comments containing a URL or ticket reference
- Anything in a file the branch didn't change

## Language

Plain, short, lowercase-after-`#` is fine. Cut these on sight: "in order to",
"note that", "this function is responsible for", "ensures that", "handles the
case where", "it is important to", "we use X here to". Say the thing.

## Workflow

1. Get the file list (above). Read each changed hunk.
2. Apply the edits directly. Don't ask per-comment — the user wants the cleanup
   done, not a review.
3. When unsure whether a *why* comment is load-bearing, keep it (shortened).
   Deleting a real reason costs more than leaving a short comment.
4. Don't commit. Finish with a short summary: files touched, roughly how many
   comments removed vs. rewritten, and call out any you kept because you weren't
   sure — those are the ones worth a human glance.
