---
name: morning-review
description: Walk through your GitHub PR review queue one PR at a time as a thinking aid. Use when the user says things like "let's do the morning review", "let's go through my review queue", "let's do code reviews", or "show me what I need to review". Pulls open review-requested PRs from a configured repo, skips ones already reviewed since the last push, and walks through the rest one-by-one — printing the URL for the user to open in their browser, then producing an independent review for discussion. Appends a session log to a local markdown journal. Does NOT post anything to GitHub.
allowed-tools: Bash(gh *), Read, Write, Edit, SlashCommand
---

# Morning Review

Walk through the user's open PR review queue one PR at a time. For each PR, print the link so the user can open it in their browser, then independently produce a code review for them to read and discuss. Append a one-line entry per PR to a local markdown journal so future sessions have continuity.

This is a **thinking aid only**. NEVER post anything to GitHub — no comments, no reviews, no approvals, no requested changes. Do not call `gh pr review`, `gh pr comment`, `gh api ... -X POST`, or anything else that writes to GitHub. The user handles all GitHub actions themselves in their browser.

## Defaults

Users can customize these defaults. If a default is set, use it without prompting.

- `default_repo`: `peregrine-io/peregrine`
- `default_journal_path`: `~/.claude/morning-review.md`

## Workflow

### 1. Read the journal tail

Read the last ~100 lines of the journal at `default_journal_path` (create the file if it doesn't exist). This gives continuity — you can mention "last session was 3 days ago, you covered N PRs" if relevant. Don't belabor it; one short sentence at most.

### 2. Fetch the review queue

```bash
gh search prs --review-requested=@me --state=open --repo <default_repo> \
  --json number,title,author,url,isDraft,additions,deletions,updatedAt
```

### 3. Filter out already-reviewed PRs

For each PR, check whether the user has submitted a review since the latest push:

```bash
gh api repos/<owner>/<repo>/pulls/<number>/reviews --jq '[.[] | select(.user.login == "<user-login>")] | sort_by(.submitted_at) | last'
gh api repos/<owner>/<repo>/pulls/<number> --jq '.head.sha, .updated_at'
```

A PR is "already reviewed" if the user has a review with `submitted_at` newer than the last commit push (`pushed_at` on the head ref, or use the latest commit's date — `gh api repos/<o>/<r>/commits/<head_sha> --jq .commit.committer.date`).

Get the user's login once at the start: `gh api user --jq .login`.

### 4. Present the queue

Output a single message with two sections:

```
**Already reviewed (N):**
- #NNNN title — _author_
- #NNNN title — _author_

**Queue (M):**
1. #NNNN title — _author_ — +X/-Y [draft]
2. #NNNN title — _author_ — +X/-Y
...

Starting with #NNNN. Open it: <url>
Tell me when you're ready for my notes.
```

If the queue is empty, say so and stop. If the "already reviewed" list is empty, omit that section.

### 5. Per-PR loop

For each PR in the queue, in order:

1. **Announce the PR**: print `#NNNN — <title>` and the URL on its own line so it's clickable. Include +X/-Y and `[draft]` tag if applicable. **Then stop** — wait for the user to reply.

2. **Wait for the user's signal to proceed.** Any natural-language reply means "go" (e.g. "ok", "ready", "go ahead", or even "this looks small, just summarize it"). If the user instead says something like "skip this one" or "not now", treat that as a skip — go to step 4 with the skip note.

3. **Produce the review.** Invoke the existing `review` skill via `SlashCommand` with the PR number:
   ```
   /review <number>
   ```
   Then stop — wait for the user to read it and discuss. The user may ask follow-up questions about the PR; answer them in line. They will eventually signal they're done with this PR (e.g. "next", "ok moving on", "done with this one", or just a note like "approved" / "I'll comment on the X point").

4. **Append a journal line** before moving on. Format:
   ```
   - #NNNN <title> — <one-line note from the conversation, or "no notes">
   ```
   If the user gave a substantive remark (e.g. "approved", "asked about caching strategy", "needs more tests"), use that as the note. Otherwise default to "reviewed".

5. **Move to the next PR.** Announce it (step 1).

### 6. End of queue

When the queue is exhausted, write a session footer to the journal:
```
(session ended — N reviewed, M skipped)
```

Then summarize for the user in one sentence: "Done — N reviewed, M skipped, journal updated."

## Journal format

The journal is a plain markdown file, append-only. New sessions start with a date header. Example:

```markdown
## 2026-05-20

- #31896 list_bolt_items tool — approved, looks clean
- #31895 find_bolt_item folder id — asked about caching, will follow up in slack
- #31882 supersede plan on stop — skipped, draft
(session ended — 2 reviewed, 1 skipped)

## 2026-05-19

- #31821 get_data_model_stats — flagged missing agent registration
(session ended — 1 reviewed, 0 skipped)
```

When starting a new session, check whether today's date header already exists at the bottom of the file. If yes, append under it. If no, add a blank line then the new `## YYYY-MM-DD` header.

## Hard rules

- **Never write to GitHub.** Reviews are for the user's eyes only. No `gh pr review`, no `gh pr comment`, no `gh api -X POST`, no comments-on-comments, nothing.
- **Never auto-advance.** Always stop and wait for the user between PRs and between announcing/reviewing a PR.
- **Don't re-fetch the queue mid-session** unless the user asks — if a new PR comes in during the session, that's tomorrow's problem.
- **Use the existing `review` skill** for the actual review pass — don't reimplement that logic here. This skill is the orchestrator, not the reviewer.
