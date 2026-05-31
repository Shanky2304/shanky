# Git Commit Rules

Follow conventional commits: https://www.conventionalcommits.org/en/v1.0.0/

## Project-specific conventions
- One logical change per commit
- Use `git mv` for renames to preserve history
- Types used in this project: feat, fix, refactor, chore, docs
- Keep subject line under 72 chars
- If bundling multiple changes, separate with `and` in subject and explain each in body

## Examples
feat: add cerebras client with rate limit fallback
fix: retry on malformed llama tool call JSON
refactor: abstract LLMClient config loading from env
chore: rename begin.py to main.py