---
name: deslop
description: Clean up LLM-style comments and docstrings in the current branch's changes. Use when the user says "deslop", "clean up the comments", "de-slop this", or before opening a PR on AI-written code.
allowed-tools: Bash(git *), Read, Edit, Grep, Glob
argument-hint: "[files...]"
---

# Deslop

Strip the tells of LLM-written code from the current change. Scope is
**comments and docstrings only** — never change code behavior.

## What to operate on

- If called during a coding session, by default operate on the files you just 
  created and edited. The goal is to tidy up the changeset before they reach
  a human review.
- If specified, the changeset of a given pull request / branch diff.
- Otherwise the current branch's changes: `git diff main...HEAD --name-only`,
  `git diff --name-only`, and `git ls-files --others --exclude-standard`.

Only touch comments in hunks the branch added or changed. Leave pre-existing
comments alone.

## The test

**Would this be useful to someone reading the file cold, with no knowledge of
this PR or the conversation that produced it?** If not, delete it. If yes, make
it as short as it can be.

## What to delete

**Narration of what the code does.**

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
→ no comment, or `# filter in DB so start is compared in UTC` if that's non-obvious.


## What to keep (but shorten)

**Why comments** — constraints, workarounds, non-obvious behavior, "must stay
in sync with X", links. A *why* is usually five to ten words.

The most common bloat is **stating the reason, then walking through the failure
mechanism.** Keep the reason. Drop the mechanism.

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

The rewrites lose precision. That's fine — a comment is a pointer, not a proof.

**Docstrings that describe everything the function doesn't do.** Say what it
does.

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


**Match the surrounding file.** If nearby code has no docstrings, new functions
don't need them either. If the module uses full Google-style docstrings, follow
that.

## Never touch

- Files the branch didn't change

## Language

Plain and short. Cut on sight: "in order to", "note that", "this function is
responsible for", "ensures that", "handles the case where", "it is important
to", "we use X here to".

## Workflow

1. Get the file list. Read each changed hunk.
2. Edit directly. Don't ask per-comment.
3. When unsure whether a *why* is load-bearing, keep it, shortened.
4. Don't commit. Finish with a short summary: files touched, roughly how many
   comments removed vs. rewritten, and any you kept because you weren't sure.
