---
name: review
description: >
  Perform a thorough code review. Use when the user asks for a review, bug hunt,
  quality check, architecture critique, or improvement suggestions before
  merging or committing changes.
---

# Code Review Skill

## Goal

Produce a thoughtful review that improves correctness, readability,
maintainability, and long-term quality.

## Review Checklist

Inspect the code for:

### Correctness

- Logic errors
- Incorrect assumptions
- Missing edge cases
- Off-by-one mistakes
- Race conditions
- Resource leaks

### Robustness

- Missing error handling
- Missing input validation
- Dangerous assumptions
- Poor exception handling

### Readability

- Clear naming
- Appropriate function length
- Unnecessary nesting
- Duplicate code
- Dead code
- Confusing comments

### Design

- Separation of responsibilities
- Reusable abstractions
- Unnecessary complexity
- Hardcoded values that should become configuration

### Security

- Secrets committed to source
- Unsafe shell commands
- Path traversal
- Dangerous file operations

### Performance

- Repeated expensive work
- Unnecessary filesystem access
- Excessive API calls
- Inefficient algorithms where they matter

## Reporting

For every issue found:

1. Explain the problem.
2. Explain why it matters.
3. Suggest a concrete improvement.

Prioritize findings by severity:

- Critical
- High
- Medium
- Low
- Style

If no issues are found, say so clearly instead of inventing problems.

## Editing

Do not modify code automatically.

Only suggest improvements unless the user explicitly requests edits.

## Review Philosophy

Prefer constructive feedback.

Avoid nitpicks that do not improve the code.

Focus on changes that make the software more correct, maintainable, or easier to understand.
