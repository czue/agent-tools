---
name: morning-review
description: Walk through your GitHub PR review queue one PR at a time as a thinking aid. Use when the user says things like "let's do the morning review", "let's go through my review queue", "let's do code reviews", or "show me what I need to review". Pulls open review-requested PRs from a configured repo, skips ones already reviewed since the last push or stale beyond a configurable age, and walks through the rest one-by-one — printing the URL for the user to open in their browser, then producing an independent review for discussion. Appends a session log to a local markdown journal. Does NOT post anything to GitHub.
allowed-tools: Bash(gh *), Read, Write, Edit, Skill
---

# Morning Review

Walk through the user's open PR review queue one PR at a time. For each PR, print the link so the user can open it in their browser, then independently produce a code review for them to read and discuss. Append a one-line entry per PR to a local markdown journal so future sessions have continuity.

This is a **thinking aid only**. NEVER post anything to GitHub — no comments, no reviews, no approvals, no requested changes. Do not call `gh pr review`, `gh pr comment`, `gh api ... -X POST`, or anything else that writes to GitHub. The user handles all GitHub actions themselves in their browser.

## Defaults

Users can customize these defaults. If a default is set, use it without prompting.

- `default_repo`: `peregrine-io/peregrine`
- `default_journal_path`: `~/.claude/morning-review.md`
- `default_stale_after_days`: `14` — PRs whose `updatedAt` is older than this are auto-skipped as stale/dead

## Workflow

### 1. Read the journal tail

Read the last ~100 lines of the journal at `default_journal_path` (create the file if it doesn't exist). This gives continuity — you can mention "last session was 3 days ago, you covered N PRs" if relevant. Don't belabor it; one short sentence at most.

### 2. Fetch the review queue

Use `gh pr list` (not `gh search prs` — the latter does not support `additions`/`deletions`/`headRefOid`):

```bash
gh pr list --repo <default_repo> --search "review-requested:@me" --state open \
  --json number,title,author,url,isDraft,additions,deletions,updatedAt,headRefOid
```

This returns everything needed for the queue display AND the already-reviewed check (`headRefOid` is the head commit SHA, used in step 3) in a single call.

### 3. Filter out PRs that don't need review attention

A PR is **skipped** if any of:

- **already reviewed** — user has submitted a review with `submitted_at` newer than the latest commit on the head ref
- **stale** — `updatedAt` is older than `default_stale_after_days` days ago (these are typically abandoned PRs the author never came back to; if the user does want to look at a stale PR, they can open it directly)
- **previously skipped, no change** — the journal's most recent entry for this PR number contains "skip" (case-insensitive) AND the PR's `updatedAt` is older than that journal session's date. If we already skipped it and nothing has changed, skip it again. Reason label: `previously skipped (YYYY-MM-DD)`.

For the already-reviewed check:

```bash
gh api repos/<owner>/<repo>/pulls/<number>/reviews --jq '[.[] | select(.user.login == "<user-login>")] | sort_by(.submitted_at) | last'
gh api repos/<owner>/<repo>/commits/<head_sha> --jq .commit.committer.date
```

A PR is "already reviewed" if the user has a review with `submitted_at` newer than that commit date.

Get the user's login once at the start: `gh api user --jq .login`. The PR's `headRefOid` (head SHA) and `updatedAt` come from the `gh pr list` query in step 2.

### 4. Present the queue

Output a single message with two sections:

```
**Skipped (N):**
- #NNNN title — _author_ — already reviewed
- #NNNN title — _author_ — stale (45d)

**Queue (M):**
1. #NNNN title — _author_ — +X/-Y [draft]
2. #NNNN title — _author_ — +X/-Y
...

Starting with #NNNN. Open it: <url>
Tell me when you're ready for my notes.
```

If the queue is empty, say so and stop. If the skipped list is empty, omit that section.

### 5. Per-PR loop

For each PR in the queue, in order:

1. **Announce the PR**: print `#NNNN — <title>` and the URL on its own line so it's clickable. Include +X/-Y and `[draft]` tag if applicable. A "tell me when you're ready" prompt is fine here — the user needs a moment to open the PR in their browser. **Then stop.**

2. **Wait for the user's reply.** Any natural-language reply means "go" (e.g. "ok", "ready", "go ahead", or even "this looks small, just summarize it"). If the user instead says something like "skip this one" or "not now", treat that as a skip — go to step 4 with the skip note.

3. **Produce the review.** Invoke the existing `review` skill via the `Skill` tool, passing the PR number as the argument. (If the `Skill` tool isn't available in this harness, follow the `review` skill's workflow inline: `gh pr view <n>`, `gh pr diff <n>`, then a sectioned review.)

   When the review output is complete, **stop without a closing prompt** — no "ready for the next one?", no "let me know when to move on", no "anything else on this one?". The user will read your notes and reply in their own time. The user may ask follow-up questions about the PR; answer them in line. They will eventually signal they're done with this PR (e.g. "next", "ok moving on", "done with this one", or just a note like "approved" / "I'll comment on the X point").

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

Finally, suggest a session rename the user can copy-paste. Generate a short, distinctive title from the PRs actually reviewed (not skipped) — pick 2-4 keywords from their titles that capture the theme. Examples:

- 3 PRs about `list_bolt_items`, `find_bolt_item folder id`, `supersede plan on stop` → `/rename morning review 2026-05-22 — bolt items, plan supersede`
- 1 PR `feat(embeddings): partial update mode` → `/rename morning review 2026-05-22 — embeddings partial update`
- 0 PRs reviewed (all skipped) → skip the rename suggestion entirely; nothing distinctive to title with

Format the suggestion as a single fenced code block so it's one-click selectable. Prefix with one line: `💡 Rename this session:` Don't elaborate further — the user pastes or ignores.

**Note on `/rename` itself:** The agent cannot invoke `/rename` directly in most harnesses (the `SlashCommand` tool typically isn't available). This is why we suggest a copy-paste line at the end rather than running it programmatically. Do not attempt to call `/rename` via any tool — print the suggested line and stop.

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
- **Once the review is produced, never end a message with a "ready for the next one?" / "shall I move on?" / "let me know when" prompt.** While discussing the code, stopping is the signal — the user will reply when they're done with that PR. Trailing prompts during code discussion are noise. (Exception: the initial announce step *may* end with "tell me when you're ready for my notes" since the user needs a moment to open the PR in their browser.)
- **Don't re-fetch the queue mid-session** unless the user asks — if a new PR comes in during the session, that's tomorrow's problem.
- **Use the existing `review` skill** for the actual review pass — don't reimplement that logic here. This skill is the orchestrator, not the reviewer.
