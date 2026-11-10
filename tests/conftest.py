"""Shared fixtures for the day test modules.

Three problems this file exists to solve:

1. Puzzle inputs are gitignored (AoC asks that they not be redistributed), so
   a fresh clone has no inputs/ at all.  Tests that need one must *skip*, not
   fail -- otherwise the suite is red for everybody who did not personally
   download every file.  That is `real_input`.

2. An answer nobody has submitted is not an answer.  If a test asserted
   whatever the code happened to print, it would pass by construction and
   prove nothing.  That is `check_locked`: it asserts only against a value a
   human has confirmed, and otherwise reports.  See LOCKED below.

3. Each day can have two implementations: Matt's in src/dayNN.py and
   Claude's comparison solution in AI_src/dayNN.py, written only after Matt
   has solved the day.  A test that takes a `solution` argument runs once per
   implementation that exists (ids `src` and `ai`), so the same statement
   checks hold both to account.  See pytest_generate_tests below.
"""

import importlib
import importlib.util
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = REPO_ROOT / "inputs"
AI_DIR = REPO_ROOT / "AI_src"


def day_of(name: str) -> int:
    """Day number from a module or test-module name: day07, ai_day07, test_day07 -> 7."""
    match = re.search(r"day(\d\d)$", name)
    if match is None:
        raise ValueError(f"no dayNN in {name!r}")
    return int(match.group(1))


def implementations(day: int) -> list[tuple[str, object]]:
    """[("src", module)] plus ("ai", module) when AI_src/dayNN.py exists.

    src/ is on sys.path (pyproject.toml), so Matt's module imports as plain
    `dayNN`.  The AI module has the same file name, so it is loaded by path
    under the distinct name `ai_dayNN` to keep the two apart in sys.modules.
    """
    found = [("src", importlib.import_module(f"day{day:02d}"))]
    path = AI_DIR / f"day{day:02d}.py"
    if path.exists():
        name = f"ai_day{day:02d}"
        if name not in sys.modules:
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
        found.append(("ai", sys.modules[name]))
    return found


def pytest_generate_tests(metafunc):
    """Parametrize any test that takes `solution` over every implementation of its day."""
    if "solution" in metafunc.fixturenames:
        impls = implementations(day_of(metafunc.module.__name__))
        metafunc.parametrize("solution", [module for _, module in impls], ids=[label for label, _ in impls])


@pytest.fixture(scope="session")
def real_input():
    """Return `load(day) -> str`, skipping the test when the input is absent.

    Reads with newline="" left at the default, i.e. universal newlines: a
    CRLF file arrives as \n-separated text.  Solutions must still tolerate a
    stray \r on their own (see the crlf test in every day module) because
    input can also reach parse_input from a string literal or a byte read that
    did no translation.
    """

    def load(day: int) -> str:
        path = INPUT_DIR / f"day{day:02d}.txt"
        if not path.exists():
            pytest.skip(f"no {path.relative_to(REPO_ROOT)} (inputs are gitignored)")
        return path.read_text()

    return load


@pytest.fixture
def check_locked(real_input):
    """Return `check(module, LOCKED)` -- assert confirmed answers, report the rest.

    LOCKED is a (part1, part2) tuple of answers accepted by adventofcode.com.
    Either slot may be None, and LOCKED itself may be None, meaning "not
    accepted yet".  AoC hands out part 2 only after part 1 is accepted, so
    `LOCKED = (1234, None)` is a normal state for a day to be in.

    - A slot holding a value: assert.  A refactor that changes the answer fails.
    - A slot holding None:    report what the code currently produces (or that
                              the part still raises NotImplementedError), then
                              skip.

    The asymmetry is the point.  There is no third path where an unverified
    number gets asserted against itself, so a green suite never implies more
    confidence than somebody actually has.  Turning a day green means pasting
    a real answer into LOCKED by hand.

    Works for either implementation: pass the `solution` fixture as module.
    """

    def attempt(part, parsed):
        try:
            return part(parsed)
        except NotImplementedError:
            return NotImplemented

    def check(module, locked):
        name = module.__name__
        raw = real_input(day_of(name))
        locked = (None, None) if locked is None else tuple(locked)

        parsed = module.parse_input(raw)
        got = (attempt(module.part1, parsed), attempt(module.part2, parsed))

        # Confirmed slots are asserted first, so a regression in an accepted
        # part 1 fails even while part 2 is unfinished.
        for label, want, have in zip(("part1", "part2"), locked, got, strict=True):
            if want is not None:
                assert have == want, f"{name} {label}: expected {want}, got {have}"

        if None not in locked:
            # solve() is the public entry point; make sure it agrees.
            assert module.solve(raw) == locked
            return

        report = []
        for label, want, have in zip(("part1", "part2"), locked, got, strict=True):
            if want is not None:
                report.append(f"{label}={have} (locked)")
            elif have is NotImplemented:
                report.append(f"{label} not implemented")
            else:
                report.append(f"{label}={have} (unconfirmed -- submit it, then set LOCKED)")
        pytest.skip(f"{name}: " + ", ".join(report))

    return check
