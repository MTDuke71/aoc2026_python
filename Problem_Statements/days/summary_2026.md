# AoC 2026 Summary

**Part 1 / Part 2 columns hold submitted, accepted answers** -- the same values
as `LOCKED` in `tests/test_dayNN.py`. A day whose answers have not been accepted
by adventofcode.com stays blank, whatever the code currently prints.

**Parse / P1 / P2 / Total are milliseconds** from `bench.py`, best of 5 on the
real input, for Matt's `src/dayNN.py`, recorded when the day was finished.
Total is the sum of the three bests. `AI_src` timings go in each guide's
comparison section, not here. `bench.py` skips a day until both parts are
written, so a 🟡 row has no timings.

AoC 2026 has 12 puzzles (Dec 1-12). Day 0 is a tutorial dry run (AoC 2019
day 1), not an AoC 2026 puzzle. It is here to prove the pipeline end to end:
module, comparison module, tests against both, locked answers, bench.

Status: ✅ both answers accepted · 🟡 in progress: code written, not every answer accepted yet · ⬜ not started.

| Day | Puzzle | Status | Part 1 | Part 2 | Parse | P1 | P2 | Total | Notes |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 00 | [The Tyranny of the Rocket Equation](day00.md) | ✅ | 3481005 | 5218616 | 0.010 | 0.007 | 0.067 | 0.085 | Dry run; [guide](day00_function_guide.md). Part 1 sums `mass // 3 - 2`; part 2 iterates that on its own output until a step is no longer positive. `AI_src` version uses a generator for the chain. |
| 01 | (unlocks Dec 1) | ⬜ |  |  |  |  |  |  |  |
| 02 | (unlocks Dec 2) | ⬜ |  |  |  |  |  |  |  |
| 03 | (unlocks Dec 3) | ⬜ |  |  |  |  |  |  |  |
| 04 | (unlocks Dec 4) | ⬜ |  |  |  |  |  |  |  |
| 05 | (unlocks Dec 5) | ⬜ |  |  |  |  |  |  |  |
| 06 | (unlocks Dec 6) | ⬜ |  |  |  |  |  |  |  |
| 07 | (unlocks Dec 7) | ⬜ |  |  |  |  |  |  |  |
| 08 | (unlocks Dec 8) | ⬜ |  |  |  |  |  |  |  |
| 09 | (unlocks Dec 9) | ⬜ |  |  |  |  |  |  |  |
| 10 | (unlocks Dec 10) | ⬜ |  |  |  |  |  |  |  |
| 11 | (unlocks Dec 11) | ⬜ |  |  |  |  |  |  |  |
| 12 | (unlocks Dec 12) | ⬜ |  |  |  |  |  |  |  |
