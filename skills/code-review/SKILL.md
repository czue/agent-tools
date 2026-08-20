---
name: code-review
description: Personal, no-fan-out override of code review. Reviews a GitHub PR by number/URL directly in the current conversation — no subagents. Use when the user says "code review PR #NNNN", "review this PR", or when invoked by /morning-review's per-PR review step.
allowed-tools: Bash(gh *), Read, Grep, Glob
argument-hint: "<PR number or URL>"
---

# Code Review (inline, no fan-out)

Review a single GitHub PR yourself, in the current conversation. Do not spawn any
`Agent` or `Skill` subagent for this — the whole point is keeping the PR diff and
your reasoning in context so follow-up questions don't require re-reading anything.

**Never post anything to GitHub.** No `gh pr comment`, `gh pr review`, or any other
write operation. Output is for the user to read in chat only.

## Workflow

1. **Check eligibility.** Run `gh pr view <n> --json state,isDraft,title,body,url`.
   Skip (say why, and stop) if the PR is closed, or is a draft the user didn't
   explicitly ask about.

2. **Gather context.**
   - `gh pr diff <n>` for the change itself.
   - Find any `CLAUDE.md` files covering the directories the diff touches (root,
     plus any nested ones under changed paths).

3. **Summarize first.** Before any findings, write a short plain-language summary
   of what the PR does and why (a few sentences). Assume the user is walking in
   cold — they may not have read the code yet.

4. **Review the diff**, checking for:
   - **Correctness bugs** — real bugs, not nitpicks. Trace through the actual
     logic; don't flag something as broken without confirming it. Includes
     things like unparametrized SQL, open redirects, SSRF via user-controlled
     URLs, and swallowed exceptions/silent fallbacks.
   - **CLAUDE.md compliance** — only flag violations the relevant CLAUDE.md
     actually calls out, not general best-practice opinions.
   - **In-file comment compliance** — read existing comments in the touched files
     (e.g. "do not change without updating X", "must stay in sync with Y") and
     check whether the diff violates guidance already written there.

5. **Filter before you say anything.** A finding survives only if the author
   would fix it once aware of it, and its impact is provable — not speculated.
   Drop:
   - Pre-existing issues (not introduced by this diff)
   - Nitpicks a senior engineer wouldn't bother raising
   - Anything a linter/typechecker/CI would already catch
   - Issues on lines the PR didn't touch
   - Changes that are clearly intentional and related to the PR's stated purpose
   - Speculative "this might break X" claims where X isn't actually traced through

6. **Report in chat** — no heading needed beyond the summary. Call out things
   done well, not just problems; this version of the review is meant to be a
   read for someone who wants the full picture, not just a bug list. For each
   issue, tag it with a priority ([P0] drop everything / [P1] urgent / [P2]
   normal / [P3] nice to have), state what's wrong and why it matters, with a
   file:line reference. End with an overall verdict: **Correct** (no blocking
   issues) or **Needs attention** (has P0/P1/P2 findings).

   After the verdict, add a **Human reviewer callouts** section for anything
   non-blocking the user should still know about before approving: new or
   changed dependencies, database migrations, auth/permission changes,
   backwards-incompatible schema/API changes, or irreversible/destructive
   operations. Only include callouts that apply; omit the section entirely if
   none do.

7. **If there's nothing to flag**, say so plainly after the summary — don't
   manufacture a finding to have something to say.

## Answering follow-ups

Since nothing was forked to a subagent, the diff and your review are already in
context — just answer directly. No need to re-fetch anything unless the user
asks about a part of the PR you didn't already pull in (e.g. a file outside the
diff, or current `main` for comparison).
