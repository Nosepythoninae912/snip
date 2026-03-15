# Contributing to snip

Thanks for taking the time to contribute. Bug fixes, new features, and improvements are all welcome.

## Getting started

```bash
git clone https://github.com/phlx0/snip
cd snip
make dev        # creates .venv and installs with dev extras
make run        # launch the app
make test       # run the test suite
```

## Before opening a PR

- Run `make test` and make sure everything passes
- Keep changes focused — one fix or feature per PR
- If you're adding a CLI flag, update the `--help` output in `__main__.py`
- If it's a user-facing change, add an entry to `CHANGELOG.md` under `[Unreleased]`

## Reporting bugs

Use the [bug report template](https://github.com/phlx0/snip/issues/new?template=bug_report.yml). Include your OS, Python version, and `snip --version` output.

## Suggesting features

Use the [feature request template](https://github.com/phlx0/snip/issues/new?template=feature_request.yml).

## Code style

- Standard Python, no formatter enforced — just keep it consistent with the surrounding code
- Prefer clarity over cleverness
- No external dependencies beyond what's already in `pyproject.toml` unless there's a strong reason

## License

By contributing you agree that your changes will be licensed under the [MIT License](LICENSE).
