---
name: commit
description: >
  Prepare a safe, high-quality Git commit. Use when the user asks to commit,
  save, wrap up work, checkpoint progress, or create a Git commit. Never push
  changes unless explicitly instructed.
---

# Commit Skill

## Goal

Create a clean, meaningful Git commit while minimizing the risk of committing
broken code or unintended files.

## Workflow

1. Understand what the user wants committed.
   - If the scope is unclear, ask which files or features should be included.

2. Check the repository status.
   - Run `git status`.
   - Identify modified, deleted, new, and staged files.

3. Review the changes.
   - Run `git diff`.
   - If files are already staged, also inspect `git diff --staged`.
   - Look for suspicious changes before committing.

4. Verify the project.
   - If the project has an obvious test suite, run it.
   - If tests fail, stop immediately.
   - Explain the failures and do not commit until the user decides how to proceed.

5. Stage files carefully.
   - Never assume every file should be committed.
   - Ask before using `git add -A`.
   - Prefer staging only the files relevant to the requested work.

6. Create a commit message.
   - Use Conventional Commits whenever appropriate.
   - Keep the summary under 72 characters.
   - Use the imperative mood.
   - Examples:
     - feat(search): add recursive grep
     - fix(parser): handle empty YAML
     - docs: update Week 5 submission

7. Before committing, summarize:
   - Files to be committed.
   - Commit message.
   - Any warnings or unusual observations.

8. Commit only after approval.

9. Never push to a remote repository unless the user explicitly asks.

## Safety Rules

- Never hide failing tests.
- Never fabricate test results.
- Never rewrite Git history unless explicitly requested.
- Never commit secrets such as API keys, tokens, passwords, or `.env` files.
- If uncertain, stop and ask.
