# Contributing to Twitto

Thanks for taking the time to contribute ❣️. Twitto is small by design, which means every contribution — a typo fix, a new feature, a sharper README sentence — has an outsized effect on the project. This document exists so your first PR goes smoothly and the project's history stays something people can actually learn from later.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Development Setup](#development-setup)
- [Branching Strategy](#branching-strategy)
- [Commit Message Convention](#commit-message-convention)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [Reporting Security Issues](#reporting-security-issues)
- [Questions](#questions)

<br>

## Code of Conduct

Be respectful, be direct, assume good faith. Critique the code, not the person who wrote it. Disagreement over implementation is normal and healthy; disrespect toward a contributor is not, and won't be tolerated.

<br>

## Ways to Contribute

You don't need to write code to contribute meaningfully. All of these are welcome:

| Type | Examples |
|---|---|
| 🐛 Bug reports | Something breaks, behaves unexpectedly, or contradicts the docs |
| ✨ Feature proposals | See the [Roadmap](README.md#roadmap) for ideas already on the radar |
| 📝 Documentation | README clarity, code comments, setup instructions that didn't work for you |
| 🧪 Tests | Twitto currently has thin test coverage — this is genuinely high-leverage |
| 🔍 Code review | Thoughtful review on open PRs is as valuable as writing new ones |

### Before opening an issue

Search [existing issues](https://github.com/YOUR_USERNAME/twitto/issues) first — duplicates slow everyone down. If you're reporting a bug, include:

- A clear, specific title (not "it doesn't work")
- Steps to reproduce, in order
- What you expected vs. what actually happened
- Python version, Django version, OS
- A stack trace or screenshot if you have one

If you're proposing a feature, explain the *problem* it solves before the *solution* you have in mind — the best implementation isn't always the first one anyone thinks of, and a clear problem statement gives room to find it.

<br>

## Development Setup

```bash
git clone https://github.com/AhmadHussainRandhawa/twitto.git
cd twitto

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env           # fill in SECRET_KEY, DEBUG, SMTP credentials

python manage.py migrate
python manage.py runserver
```

Confirm the app boots cleanly and the check framework is happy before you start:

```bash
python manage.py check
```

<br>

## Branching Strategy

Twitto uses simple, trunk-based development — no `develop` branch, no long-lived integration branches. `main` is always deployable.

| Prefix | Use for |
|---|---|
| `feature/<short-name>` | New functionality |
| `fix/<short-name>` | Bug fixes |
| `docs/<short-name>` | Documentation-only changes |
| `refactor/<short-name>` | Internal restructuring, no behavior change |
| `test/<short-name>` | Adding or improving test coverage |

Branch from `main`. Keep each branch scoped to a single concern — a branch that fixes a bug *and* adds a feature is two branches wearing a trench coat, and it will be asked to split before merge.

<br>

## Commit Message Convention

Twitto follows **[Conventional Commits](https://www.conventionalcommits.org/)**. This isn't bureaucracy for its own sake — a consistent format makes `git log` skimmable, makes future changelog generation possible, and forces each commit to justify its own existence.

```
<type>(<scope>): <concise summary, imperative mood>

<optional body — explain why, not just what, if it's not obvious>
```

| Type | Use for |
|---|---|
| `feat` | A new feature |
| `fix` | A bug fix |
| `refactor` | Code change with no behavior change |
| `docs` | Documentation only |
| `test` | Adding or correcting tests |
| `build` | Dependencies, packaging, build config |
| `ci` | CI/CD configuration |
| `perf` | Performance improvement |
| `style` | Formatting, whitespace — no logic change |
| `chore` | Maintenance with no production code change |

**Good:**

```
fix(tweet): restrict tweet deletion to the owning user

tweetDelete previously fetched by pk only, allowing any authenticated
user to delete another user's tweet. Scoped the query to
user=request.user, matching the existing pattern in tweetEdit.
```

```
feat(tweet): add pagination to the tweet feed
docs(readme): document required environment variables
```

**Avoid:**

```
update
fix bug
final changes
wip
```

One responsibility per commit. If your commit message needs the word "and" to describe what changed, it's probably two commits.

<br>

## Pull Request Process

1. Fork the repo (or branch directly, if you have write access) from `main`.
2. Make your changes as focused, atomic commits.
3. Run `python manage.py check` and exercise the feature manually — Twitto doesn't have full test coverage yet, so manual verification matters until that changes.
4. Update the README if your change affects setup, routes, environment variables, or user-facing behavior.
5. Open the PR with:
   - A title following the commit convention (e.g. `fix: correct tweet deletion authorization`)
   - A description covering **what** changed and **why**
   - Screenshots or a short clip for any UI change
   - Explicit callouts for anything breaking
   - Linked issues where relevant (`Closes #12`)
6. Expect review comments — they're part of the process, not a verdict on the idea. Small back-and-forth before merge is normal.
7. Once approved, the PR will typically be **squash-merged** to keep `main`'s history one clean commit per change, unless the individual commits are independently meaningful and worth preserving.

<br>

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/).
- Keep views thin. Validation and business logic belong in forms and models, not sprawled across `views.py`.
- Every view that reads or mutates a `Tweet` by ID must scope the query to `request.user` unless there's a deliberate, commented reason not to (e.g. public read access). This is the project's one hard rule — see [Reporting Security Issues](#reporting-security-issues) for why.
- Use Django's ORM idiomatically. Reach for raw SQL only with a clear, stated performance justification.
- Match existing naming conventions for templates, URLs, and view functions rather than introducing a new pattern for one file.
- No secrets, credentials, or `.env` contents in commits, ever — check `git diff` before you push if you've touched settings.

<br>

## Reporting Security Issues

If you find a vulnerability — broken access control, injection, credential exposure, anything that could let one user affect another user's data — **please don't open a public issue.** Email the maintainer directly (see [README contact section](README.md#contact)) with steps to reproduce. You'll get a response, and credit in the fix commit unless you'd prefer otherwise.

<br>

## Questions

Not sure if something's worth an issue or a PR? Open a [discussion or issue](https://github.com/AhmadHussainRandhawa/twitto/issues) and ask — that's what it's there for. No question is too small.
