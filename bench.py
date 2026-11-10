"""Time each solved day by phase: parse, part 1, part 2.

Usage:
    python bench.py              # every day with an input file
    python bench.py 11 13        # just those days
    python bench.py -n 20 11     # 20 repetitions instead of the default

Each day gets one row per implementation: `src` is Matt's src/dayNN.py,
`ai` is Claude's comparison solution in AI_src/dayNN.py when it exists.

Reports **best** and **median** of N runs rather than a single shot.  At this
scale that is not pedantry: most days here finish in well under a
millisecond, and on Windows the ambient noise floor -- timer granularity, GC,
another process taking the core -- is itself a sizeable fraction of a
millisecond.  A single measurement of a 0.6 ms parse can land anywhere in a
range wider than the difference between two implementations you are trying to
compare, so the number would be unactionable.

Best-of-N estimates the floor: interference only ever adds time, so the
fastest observed run is the closest thing to the work itself.  The median
says what a typical run costs with the noise included.  When the two are
close the measurement is trustworthy; when best is far below median,
something on the machine is interfering and the median is mostly about that.

perf_counter is the right clock here -- it is the highest-resolution one
available and, unlike process_time, it counts wall time, which is what you
actually wait for.
"""

import argparse
import importlib
import importlib.util
import statistics
import sys
from pathlib import Path
from time import perf_counter

REPO_ROOT = Path(__file__).resolve().parent
INPUT_DIR = REPO_ROOT / "inputs"
AI_DIR = REPO_ROOT / "AI_src"
DEFAULT_REPS = 5
DAYS = range(13)  # day 00 dry run + AoC 2026's 12 puzzles


def time_call(fn, arg, reps):
    """Return (best_ms, median_ms) for `reps` calls of fn(arg)."""
    samples = []
    for _ in range(reps):
        start = perf_counter()
        fn(arg)
        samples.append((perf_counter() - start) * 1000.0)
    return min(samples), statistics.median(samples)


def implementations(day):
    """[("src", module), ("ai", module)] for whichever of the two exist.

    The AI module shares its file name with Matt's, so it is loaded by path
    under the name ai_dayNN (same scheme as tests/conftest.py).
    """
    found = []
    try:
        found.append(("src", importlib.import_module(f"day{day:02d}")))
    except ModuleNotFoundError:
        pass
    path = AI_DIR / f"day{day:02d}.py"
    if path.exists():
        spec = importlib.util.spec_from_file_location(f"ai_day{day:02d}", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        found.append(("ai", module))
    return found


def bench_module(module, raw, reps):
    """Return per-phase timings for one implementation, or None if it should be skipped.

    Skipped when the day is not fully solved yet.  An unsolved part raises
    NotImplementedError, and a half-timed row next to real measurements
    would only mislead.
    """
    parsed = module.parse_input(raw)
    try:
        module.part1(parsed)
        module.part2(parsed)
    except NotImplementedError:
        return None

    return {
        "parse": time_call(module.parse_input, raw, reps),
        "part1": time_call(module.part1, parsed, reps),
        "part2": time_call(module.part2, parsed, reps),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("days", nargs="*", type=int, help="days to bench (default: all)")
    parser.add_argument("-n", "--reps", type=int, default=DEFAULT_REPS, help="repetitions per phase")
    args = parser.parse_args(argv)

    sys.path.insert(0, str(REPO_ROOT / "src"))
    days = args.days or DAYS

    header = f"{'day':>3}  {'impl':<4}  {'parse best/med':>18}  {'part1 best/med':>18}  {'part2 best/med':>18}  {'total':>9}"
    print(f"best and median of {args.reps} runs, milliseconds\n")
    print(header)
    print("-" * len(header))

    grand = 0.0
    for day in days:
        path = INPUT_DIR / f"day{day:02d}.txt"
        if not path.exists():  # inputs are gitignored
            continue
        raw = path.read_text()
        for label, module in implementations(day):
            timings = bench_module(module, raw, args.reps)
            if timings is None:
                continue
            cells = []
            for phase in ("parse", "part1", "part2"):
                best, med = timings[phase]
                cells.append(f"{best:8.3f} /{med:8.3f}")
            total = sum(best for best, _ in timings.values())
            if label == "src":
                grand += total
            print(f"{day:>3}  {label:<4}  {'  '.join(cells)}  {total:8.3f} ")

    print("-" * len(header))
    print(f"{'src':>3}  {'all':<4}  {'':>18}  {'':>18}  {'':>18}  {grand:8.3f} ")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
