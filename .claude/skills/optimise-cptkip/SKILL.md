---
name: optimise-cptkip
description: Analyse and optimise Python code under cptkip/ for CircuitPython — memory first, speed second, readability preserved. Use when asked to optimise, reduce memory/RAM footprint, cut allocations, or improve performance of code in the cptkip library (not examples/, tests/, validate/, or CircuitPython/).
---

# Optimise cptkip for CircuitPython

Analyse and optimise Python source **only under `cptkip/`**. Do not modify
`examples/`, `tests/`, `validate/`, `CircuitPython/` (vendored, do-not-touch per
CLAUDE.md), or `.idea/`. If a change would require touching a test or example to
keep it passing, that's fine — but the optimisation target itself is `cptkip/` code.

## Priority order

1. **Memory** — this is the primary goal. CPTKIP targets memory-constrained
   microcontrollers (Pico-class boards); this is a stated project goal, not a
   style preference.
2. **Speed** — secondary. Only pursue speed wins that don't cost memory, unless
   the user says otherwise.
3. **Readability** — must be preserved. Don't obscure logic for a marginal gain.
   If an optimisation makes code meaningfully harder to follow, flag it as an
   option rather than applying it silently.

## Memory optimisation techniques to look for

- **Reduce allocations in loops / hot paths** (animation frame updates, task
  scheduler ticks, device polling): reuse buffers/objects instead of creating
  new ones each call; hoist object creation out of loops where correctness
  allows.
- **Prefer generators/iterators over materialised lists** where the full list
  isn't needed at once.
- **Avoid string-heavy operations in hot paths** — repeated f-strings/`.format`/
  concatenation each allocate; avoid in code that runs every frame/tick, fine in
  one-shot setup/logging paths.
- **`__slots__`** on classes with a fixed, known set of instance attributes
  (especially in `device` and `animation`) to cut per-instance overhead —
  but only where it doesn't conflict with subclassing patterns already in use.
- **Avoid gratuitous abstraction layers** (extra wrapper classes, indirection)
  that add per-object overhead without earning it.
- **Lazy/minimal imports** — avoid importing more of a module than needed;
  watch for imports that pull in heavy dependency chains.
- **Avoid duplicated state** — don't cache/copy data that's already available
  elsewhere (e.g. re-deriving from `core`/`config` instead of storing a second
  copy).

## Speed optimisation techniques (secondary, don't trade memory for them)

- Hoist invariant computation out of loops.
- Avoid repeated attribute/dict lookups in tight loops (local variable
  binding) — only where it doesn't hurt readability.
- Short-circuit early where checks are cheap and skip expensive work.

## Commenting requirement

Every non-obvious optimisation **must** have a short comment explaining the
*why* — e.g. "reused buffer to avoid per-frame allocation" or "__slots__: fixed
attribute set, cuts per-instance memory". This matches the repo's existing
comment convention (comment the non-obvious, not the obvious) but is a hard
requirement here, not just a default. Obvious/idiomatic changes (e.g. swapping
`+` concatenation for `.join()`) don't need a comment if the reason is
self-evident from the diff.

## Workflow

1. Identify the target file(s) — either what the user named, or scan the
   relevant `cptkip/<module>/` if the user gave a module/feature instead of a
   file.
2. For each file, read it fully before proposing changes — don't optimise from
   a partial view.
3. List candidate optimisations with a one-line rationale each (memory impact
   first, then speed) before editing, especially for anything affecting public
   API shape or behaviour.
4. Apply edits, matching existing formatting (double-quoted strings, PEP 8,
   4-space indent — see CLAUDE.md conventions). Add the required comments for
   non-obvious changes.
5. Verify nothing broke:
    - `pytest tests/`
    - `PYTHONPATH=../.. pytest examples/` (only if the touched module has
      example coverage)
    - `flake8 cptkip --count --select=E9,F63,F7,F82 --show-source --statistics`
6. Summarise: what changed, the memory/speed rationale for each non-trivial
   change, and any optimisation considered but rejected for hurting
   readability.
