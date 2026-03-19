# Contributing to snip

Thanks for taking the time to contribute. Bug fixes, new features, and improvements are all welcome.

## Getting started

```bash
git clone https://github.com/phlx0/snip
cd snip
make dev        # creates .venv and installs with dev extras
make run        # launch the app
make test       # run the test suite
make lint       # check for style and correctness issues
```

## Commit messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/). Every commit message should follow this format:

```
<type>(<scope>): <short description>
```

The description should be lowercase and not end with a period. Keep it under ~72 characters.

### Types

| Type | When to use |
|------|-------------|
| `feat` | A new feature or user-visible behaviour |
| `fix` | A bug fix |
| `docs` | Documentation only (README, CHANGELOG, docstrings) |
| `test` | Adding or updating tests, no production code change |
| `refactor` | Code change that isn't a fix or feature |
| `chore` | Build system, dependencies, tooling, release housekeeping |
| `style` | Whitespace, formatting — no logic change |
| `perf` | A performance improvement |
| `ci` | CI/CD pipeline changes |

### Examples

```
feat(themes): add support for 256-colour palettes
fix(clipboard): fall back to xclip when xsel is unavailable
docs: document fzf integration options
test(import): cover malformed JSON edge case
chore: bump textual to 0.52
refactor(storage): extract _resolve_path helper
```

### Breaking changes

If your change breaks backwards compatibility, add `!` after the type and include a `BREAKING CHANGE:` footer:

```
feat!: rename --config flag to --config-file

BREAKING CHANGE: --config is no longer accepted; use --config-file instead
```

## Before opening a PR

- Run `make lint` — fix any issues it reports before pushing
- Run `make test` — all tests must pass
- Keep changes focused — one fix or feature per PR
- If you're adding a CLI flag, update the `--help` output in `__main__.py`
- If it's a user-facing change, add an entry to `CHANGELOG.md` under `[Unreleased]`

## Code style

The goal is code that is easy to read and easy to change. A few principles:

**Clarity over cleverness.** If a simpler, more explicit version exists, prefer it. The next person reading the code (including future you) should not need to pause to decode it.

**Small, focused functions.** A function should do one thing. If you find yourself writing `# step 1 ... # step 2` inside a function body, that is a sign it wants to be split up.

**Meaningful names.** Variables, functions, and classes should say what they are or do. Single-letter names are fine for loop indices; avoid them elsewhere.

**No dead code.** Don't comment out old code and leave it in — if it's gone, delete it. Git history is there if you need it back.

**No magic numbers.** If a literal value has a specific meaning, give it a name.

**Consistent style.** Match the conventions of the surrounding code. If the file uses double quotes, use double quotes. If it snake_cases, snake_case.

**No unnecessary abstractions.** Don't create a helper for something used once. Don't design for hypothetical future requirements. The right amount of complexity is the minimum needed for what the code does today.

**No external dependencies** beyond what's already in `pyproject.toml` without a strong reason and prior discussion.

## Linting

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and import sorting.

```bash
make lint          # report issues
make lint-fix      # auto-fix what ruff can fix safely
```

Ruff runs automatically as part of CI. PRs with lint errors will not be merged. Most issues are auto-fixable — run `make lint-fix` first, then review the diff.

The ruff configuration lives in `pyproject.toml` under `[tool.ruff]`. The rule set is intentionally conservative (a subset of flake8 + isort). If you think a rule is wrong for this project, open an issue rather than adding a per-line `# noqa` suppression.

## Reporting bugs

Use the [bug report template](https://github.com/phlx0/snip/issues/new?template=bug_report.yml). Include your OS, Python version, and `snip --version` output.

## Suggesting features

Use the [feature request template](https://github.com/phlx0/snip/issues/new?template=feature_request.yml).

## License

By contributing you agree that your changes will be licensed under the [MIT License](LICENSE).
