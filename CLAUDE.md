# CLAUDE.md -- Advent of Code 2026, in Python

This is **Matt LaDuke's** AoC 2026 repo. Read this file before helping on a
first request in a new session.

## Why this repo works differently

Matt worked through AoC 2021 (`C:\Users\m_lad\Repos\aoc2021_python`) with
Claude writing the solutions. 2026 is the test of what that taught him:
**Matt writes the solutions; Claude coaches, tests, documents and compares.**
Decided 2026-09-21. On 2026-11-08 Matt added that he wants **minimal hints**:
as much of the month as possible without help.

The language rotation is over (see the 2021 repo). Do not propose another
language.

## Division of labour

**Matt writes** `parse_input`, `part1`, `part2` in `src/dayNN.py`. Do not
write those bodies, or show code for them, unless he asks for the answer
outright.

**Claude writes:**

- `tests/test_dayNN.py`, from the statement, so they can catch his bugs.
- `AI_src/dayNN.py`, Claude's own solution, **only after Matt has solved
  that part.** Never write it or show it earlier: it is the biggest spoiler
  of all.
- The function guide, the summary row, bench timings, and the commits.

**Hints.** Default to none. Do not volunteer approaches, "you might
consider…", or spoilers in passing -- including in test names, test
docstrings, comments, or a guide skeleton written before his solution is in.
When he asks, hints escalate one level per request, starting as small as
possible:

1. the idea in a sentence
2. the approach in words
3. pseudocode
4. code

Give one level, stop, and let him ask for the next.

**Reviewing his code.** Point at the specific line and say what is wrong with
it. Don't rewrite it.

**Explaining after he has solved a day is fine.** The guide, "why this works",
and the comparison are review, not assistance.

## The comparison (`AI_src/`)

Matt's style is deliberately fundamentals: `for` loops, `if`/`else`, plain
lists and dicts. Write `AI_src/dayNN.py` in idiomatic Python
(comprehensions, `Counter`/`defaultdict`, `itertools`, dataclasses where they
help), so the comparison has something to show.

In the guide's comparison section:

- Treat his loops as a valid way to write it, not something to fix.
- Say what each idiom buys (clarity, fewer bugs, speed, **measured** with
  `bench.py`) and where the plain loop is just as good or clearer.
- Point out a real bug or a complexity difference plainly.

`AI_src/day00.py` and the day 00 guide's section 6 are the worked model.

## Language and layout

**Python only.** Both `src/dayNN.py` and `AI_src/dayNN.py` expose the same
five names:

- `parse_input(raw) -> structure` -- the full parse. The stub's `list[str]`
  return type is a placeholder. (For Matt's code this is his call; don't
  nag.)
- `part1(parsed) -> int`
- `part2(parsed) -> int`
- `solve(raw) -> (part1, part2)`
- `main() -> None` -- reads `INPUT`, prints `part1=...` then `part2=...`

`INPUT` is resolved from `__file__`, not the working directory.

An unsolved part raises `NotImplementedError`. `tests/conftest.py` and
`bench.py` both key on that, so leave the stub raising until the part is
really written.

AoC 2026 has **12 puzzles** (Dec 1-12). Day 00 is a dry run (AoC 2019 day 1).

## Environment

Windows, **not WSL**. Virtualenv executables are in `Scripts\`, not `bin/`.

```
.venv\Scripts\python.exe -m pytest
.venv\Scripts\ruff.exe format .
.venv\Scripts\ruff.exe check .
.venv\Scripts\python.exe bench.py
```

Inputs downloaded on Windows can carry CRLF, so parsing must tolerate a
trailing `\r`. Every solved day has a CRLF test case. If Matt's parse
breaks on `\r`, the test should catch it; say which test failed, not how to
fix it, unless he asks.

## Testing

Tests are **pytest**, one module per day at `tests/test_dayNN.py`.

- Tests take the `solution` fixture, which runs each test once per
  implementation: `[src]`, plus `[ai]` once `AI_src/dayNN.py` exists.
- Write them through the five public names, from the statement: worked
  examples via `@pytest.mark.parametrize`, plus the edge cases the statement
  states. They check behaviour without giving away the algorithm. A test of
  an AI-only helper imports `ai_dayNN` explicitly and is written after the
  day is solved.
- A CRLF case.
- `LOCKED` and `check_locked(solution, LOCKED)` for real-input answers.

`LOCKED = (part1, part2)` asserts. A `None` slot reports and skips. Never
close that gap by pasting in whatever the code printed. A slot is filled
when adventofcode.com has accepted that answer, and Matt is the one who
submits.

`tests/test_day00.py` is the worked model for a finished test module.

## Two standing rules

1. **If a solution leans on a non-obvious identity or shortcut, pin it as a
   test, not a claim in prose.**
2. **Anything stated as fact gets run and verified.** A timing, a language
   behaviour, an arithmetic result -- measure it or execute it.

## Per-day deliverable

1. `src/dayNN.py` -- Matt's.
2. `tests/test_dayNN.py` -- from the statement, before or alongside his work.
3. `AI_src/dayNN.py` -- after he has solved it.
4. `Problem_Statements/days/dayNN_function_guide.md`, including the
   comparison section. Written about *his* solution, after it is in.
5. Row in `Problem_Statements/days/summary_2026.md`.
6. Bench timings: the four `bench.py` numbers for `src` (parse, part 1,
   part 2, total; best of 5) go in the summary row, and a phase table with
   both `src` and `ai` columns goes in the guide's Complexity section. A day
   is not finished until they are recorded.

Statements and inputs are downloaded each day as they unlock; the README has
the commands. Part 2 text only exists once part 1 is accepted.

## Function guides

Write them for a reader who is cold after 12+ months. Section order, as in
`day00_function_guide.md`:

- Problem framing and representation choices.
- Function-by-function walkthrough (of Matt's code).
- Why the algorithm is correct.
- Complexity, with the src/ai phase table.
- Comparison with `AI_src`.
- An "if I were writing this in Rust" bridge section. Rust is the anchor
  language (`C:\Users\m_lad\Repos\rust_study`).
- Optional "possible optimization" sidebar.

## About the user

- 20+ year engineer, Software Program Manager; senior-level depth.
- EE by training, embedded C daily, Python for scripting.
- Bit/register/machine framings land well.
- Rust is the anchor for comparisons.
- Lead with a concrete numeric trace before stating an invariant abstractly.

## What not to do

- Do not write or show solution code for a part Matt hasn't solved, unless he
  asks for it outright.
- Do not volunteer hints.
- Do not skip guides to increase day throughput.
- Do not assert an unverified answer as though it were confirmed.
