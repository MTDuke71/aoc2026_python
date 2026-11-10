# aoc2026_python

Advent of Code 2026, in Python. Twelve puzzles, December 1–12.

Matt writes the solutions in `src/`. After a day is solved, Claude writes its
own version in `AI_src/` for a side-by-side comparison. The layout and
conventions otherwise match [aoc2021_python](https://github.com/MTDuke71/aoc2021_python).

## Layout

| Path | What it is |
|---|---|
| `src/dayNN.py` | Matt's solutions — `parse_input` / `part1` / `part2` / `solve` / `main` |
| `AI_src/dayNN.py` | Claude's comparison solutions, same five names, written after Matt solves the day |
| `tests/test_dayNN.py` | one pytest module per day; each test runs against both implementations |
| `tests/conftest.py` | the `solution`, `real_input` and `check_locked` fixtures |
| `bench.py` | per-phase timings, best and median of N runs, one row per implementation |
| `Problem_Statements/days/` | puzzle text, function guides, and `summary_2026.md` |
| `inputs/dayNN.txt` | puzzle inputs (gitignored — AoC asks they not be redistributed) |
| `scripts/` | PowerShell helpers that download statements and inputs and convert the HTML to Markdown |

Days 01–12 start as stubs whose `part1` / `part2` raise `NotImplementedError`.
The tests and the bench both key on that, so an unsolved day shows up as a
skip, never as an answer or a timing. Statements and inputs arrive as each day
unlocks (midnight US Eastern).

## Setup

Windows, no WSL. Virtualenv executables live in `Scripts\`, not `bin/`:

```
python -m venv .venv
.venv\Scripts\python.exe -m pip install pytest ruff
```

## Each morning

```
$env:AOC_SESSION = "your_session_cookie"
.\scripts\download_aoc2026_problems.ps1 -StartDay 1 -EndDay 1
.\scripts\convert_aoc2026_html_to_md.ps1 -StartDay 1 -EndDay 1 -RemoveHtml
```

Part 2 of a statement only exists once part 1 is accepted. To pick it up,
re-download the statement and convert with `-Overwrite`:

```
.\scripts\download_aoc2026_problems.ps1 -StartDay 1 -EndDay 1 -ProblemsOnly
.\scripts\convert_aoc2026_html_to_md.ps1 -StartDay 1 -EndDay 1 -Overwrite -RemoveHtml
```

## Run a day

```
.venv\Scripts\python.exe src\day01.py
.venv\Scripts\python.exe AI_src\day01.py
```

`INPUT` is resolved from `__file__`, so this works from any directory. Parts
print one at a time: part 1's answer is on screen to submit while part 2 is
still a stub.

## Test

```
.venv\Scripts\python.exe -m pytest
.venv\Scripts\python.exe -m pytest tests\test_day01.py
.venv\Scripts\python.exe -m pytest -k src      # Matt's implementations only
```

A test that takes the `solution` argument runs once per implementation that
exists, with ids `[src]` and `[ai]`. Until `AI_src/dayNN.py` exists, only
`[src]` runs. `pyproject.toml` puts `src/` on the path, so a test can also
`import day03` directly; the AI module loads by path as `ai_day03`.

Inputs are gitignored, so a fresh clone has none. Tests that need one **skip**
rather than fail.

Each test module carries a `LOCKED` tuple of the day's real-input answers:

- `LOCKED = (part1, part2)` — asserted, for both implementations. A refactor
  that changes an answer fails.
- `LOCKED = (part1, None)` — part 1 asserted; part 2 reported, then skipped.
  The normal state between the two stars.
- `LOCKED = None` — everything reported, then skipped.

An answer goes into `LOCKED` only after adventofcode.com has accepted it. An
answer nobody has submitted never gets asserted against itself, so a green
suite never implies more confidence than somebody actually has.

## Format

```
.venv\Scripts\ruff.exe format .
.venv\Scripts\ruff.exe check .
```

Line length 110.

## Bench

```
.venv\Scripts\python.exe bench.py          # every solved day with an input
.venv\Scripts\python.exe bench.py -n 20 5  # 20 reps, day 5 only
```

Reports best and median per phase, one row for `src` and one for `ai`.

## Solved

Day 0 is a tutorial dry run (AoC 2019 day 1), not an AoC 2026 puzzle; it is
here to prove the pipeline end to end, including a comparison module. See
[Problem_Statements/days/summary_2026.md](Problem_Statements/days/summary_2026.md)
for the day-by-day table.
