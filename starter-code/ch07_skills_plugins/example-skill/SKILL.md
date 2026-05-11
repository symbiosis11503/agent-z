---
name: agentz-changelog-helper
description: Update CHANGELOG.md when adding a new feature — auto-detect git diff, ask for version, format the new entry.
---

# AgentZ Changelog Helper Skill

This skill helps you add a new entry to `CHANGELOG.md` after making changes, with consistent formatting.

## When to invoke

User says any of:
- "Update changelog"
- "Add changelog entry"
- "Bump version"
- After completing a feature

## What you do

1. **Read current `CHANGELOG.md`** to learn the version format conventions
2. **Run `git diff --stat HEAD~1..HEAD` or `git log --oneline -5`** to learn what just changed
3. **Ask user**:
   - What version is this? (e.g., v1.2, v2.0-alpha)
   - What category? (feat / fix / docs / chore / breaking)
   - One-sentence summary?
4. **Draft the entry** following the existing CHANGELOG format:
   ```markdown
   ## v1.2 — YYYY-MM-DD

   ### {category}
   - **{component}**: {summary}
   - {detail bullet 1}
   - {detail bullet 2}
   ```
5. **Insert at the top** (after `# Changelog` heading, before previous version)
6. **Stage but don't commit** — let user review the diff

## Constraints

- **Never commit** without explicit user approval
- **Use existing format** — don't invent new structure
- **Date in user's timezone** if known, otherwise UTC
- **Detail bullets max 5** per entry — split into sub-entries if longer

## Example

User: "Add changelog entry for Ch 14 starter code"

You:
1. Read `CHANGELOG.md` — see format uses `## vX.Y — date`, sections like `### Starter code 擴充`
2. `git log --oneline -3` — see commit "iter 6: Add ch14_multi_agent starter code"
3. Ask: "Version 1.1? Category 'Starter code 擴充'?"
4. User: "yes"
5. Draft:
   ```markdown
   ## v1.1 — 2026-05-11

   ### Starter code 擴充
   - **`starter-code/ch14_multi_agent/`** — 3 架構：Pipeline / Supervisor / Blackboard
   ```
6. Insert into file, show diff, wait for approval.
