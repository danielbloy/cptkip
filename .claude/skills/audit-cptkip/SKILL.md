---
name: audit-cptkip
description: Run a full project-wide code-quality audit of the cptkip repo (bugs, missing test coverage, missing/unclear docs, obvious missing functionality, clarity, memory/CPU performance) and remediate what's safe to fix. Use when asked to audit, review, or analyse the whole cptkip project — not for scoped memory/perf work on cptkip/ only (see optimise-cptkip for that).
---

# CPTKIP Code-Quality Audit

A recurring, manually-invoked audit of the whole repo. Each run produces a
fresh `claude-analysis.md` report, then remediates what's safe to fix,
tracked in a `claude-plan.md` checklist. This skill was distilled from the
first full run (2026-07-25, branch `claude_optimise`) — treat the lessons
below as load-bearing, not optional colour.

## Scope

Whole repo: `cptkip/`, `tests/`, `examples/`, `validate/`, and top-level docs
(`README.md`, `development_environment.md`, `changelog.md`, `roadmap.md`,
`validate/validation.md`). Do not touch `CircuitPython/` (vendored) or
`.idea/` — both are "do not touch" per `CLAUDE.md`.

## Finding categories

Tag every finding with one of these (matches what the user asks for each
time this is invoked):

1. Bugs
2. Missing test coverage
3. Missing or unclear documentation
4. Obvious missing functionality — **catalogue only, never implement** (see
   Step 2)
5. Code that could be clearer **without increasing memory usage**
6. Code that could use better patterns for usability
7. CPU-cycle perf optimisations that don't increase memory
8. Memory optimisations that may cost a little CPU

## Step 1 — Always regenerate `claude-analysis.md` first

This is the mandatory first deliverable of every run. Write it fresh from a
full re-analysis every time — **never diff against or append to a previous
version**, even if one already exists in the repo (overwrite it). Do this
entirely before touching any code.

1. Split the codebase into module groups matching the dependency order in
   `CLAUDE.md` (`core` → `config`/`cpu`/`pin`/`task` → `device` → `animation`),
   plus one more group for `examples/`, `validate/`, and docs.
2. Spawn one **general-purpose** research agent per group, in parallel,
   foreground (not `Explore` — it's read-only/location-finding and explicitly
   disclaims open-ended analysis/code review). Brief each with the finding
   categories above and instruct: read full files (not partial views), quote
   exact code with file:line, and verify non-obvious claims (execute the
   code, check the actual library source a bug depends on, grep the whole
   repo for real call sites) rather than inferring from a partial read.
3. For anything flagged as high-risk, hardware-affecting, or where the root
   cause isn't obviously correct, verify it yourself directly before trusting
   it — see the `pixels.py` lesson below for why this matters.
4. Synthesize into `claude-analysis.md` at repo root:
   - **TL;DR** with counts.
   - **Critical/hardware-affecting bugs** called out first, bold/blockquote.
   - **Bugs** found, with a proposed fix per item.
   - **Breaking-change candidates**, each with explicit payoff-vs-risk
     reasoning and a suggested changelog line — see the bar in Step 2.
   - **Documentation fixes**, **clarity improvements**, **missing test
     coverage** — each with a proposed fix.
   - **Missing functionality** — catalogued with rationale, explicitly never
     implemented.
   - A status column per fixable item (`proposed` initially; update to
     `fixed` / `left-alone` / `corrected` once Step 2 finishes).
5. This report **is** the plan. Present it before implementing anything
   non-trivial, unless the user has already granted blanket authorization for
   this run (e.g. "go ahead with the remaining batches").

## Step 2 — Implement in dependency-ordered batches

- Batch by module, in the same dependency order used for research groups, so
  later batches can rely on earlier fixes (e.g. a `core/memory.py` fix should
  land before batches that add regression tests depending on its corrected
  values).
- Track batches in `claude-plan.md` at repo root (checklist + context,
  regenerated/updated each run — don't let it reference a stale prior run).
- **Breaking changes**: only make one if the payoff is large and clearly
  outweighs a narrow, well-understood blast radius (e.g. "this is the only
  place in the codebase that doesn't follow convention X, and grep confirms
  nothing depends on the old behaviour"). Always flag it explicitly in the
  report, even if you decide to make it.
- **Never implement missing-functionality items.** Catalogue only, regardless
  of how easy they'd be.
- Run the module's test subdirectory after each batch, not just at the end.

## Step 3 — Verify and close the loop

- Full verification pass after all batches:
  ```
  pytest tests/
  PYTHONPATH=../.. pytest examples/
  flake8 cptkip --count --select=E9,F63,F7,F82 --show-source --statistics
  ```
  `validate/` can't run without hardware — substitute an `ast.parse()` syntax
  check of every `validate/**/*.py` file plus a grep for usage of every API
  touched this run, to catch stale references to removed/changed behaviour.
- Update `claude-analysis.md`'s status column to reflect what actually
  happened — including any correction made mid-run (see below).

## Hard-won lessons (apply these, don't relearn them)

- **A guard that "can never fire" isn't automatically a bug.** The first run
  made the dead `pin is None` guard in `cptkip/device/pixels.py`'s desktop
  stub unconditional — looked like a clean fix, passed the full unit suite,
  but broke two real examples that pass `config.PIXELS_PIN` (legitimately
  `None` on desktop) straight into the constructor. The stub's entire purpose
  is to accept anything, including `None`, when hardware isn't present.
  Grepping for literal `Foo(None, ...)` call sites is **not enough** —
  config-driven `None` values (`config.*_PIN`) flow in indirectly. **Always
  run the full `examples/` suite, not just `tests/`, before trusting any
  validation/guard fix that touches a pin/device constructor examples wire up
  via `config.py`.**
- **Match the existing test style.** Default to simple, direct in-process
  assertions. Only reach for subprocess isolation (spawning a fresh
  interpreter, copying the package into a `tmp_path`) when there's genuinely
  no simpler way to prove a fix works around shared import-time global state
  (e.g. `cptkip.config.configuration` mutating `cptkip.core.logging.LEVEL` at
  import time) — and even then, expect the simpler version to be preferred.
- **`flake8` is not preinstalled** in the project's `.venv` even though CI
  installs it fresh each run — `pip install flake8` before relying on the
  lint gate locally.
- The `examples/` suite takes ~2 minutes; budget for it and consider running
  it in the background while doing other verification/writing in the
  meantime.

## Verification commands (canonical, from `CLAUDE.md`)

```
pytest tests/
PYTHONPATH=../.. pytest examples/
flake8 cptkip --count --select=E9,F63,F7,F82 --show-source --statistics
```
