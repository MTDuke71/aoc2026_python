"""Day 0: The Tyranny of the Rocket Equation (tutorial dry run) -- Claude's version.

Comparison solution for src/day00.py.  Same five names, same answers; the
difference is style.  Part 2's "fuel for the fuel" is a generator that
yields each positive fuel step, so the answer is a sum of sums and the stop
condition lives in one place.
"""

from collections.abc import Iterator
from pathlib import Path

INPUT = Path(__file__).resolve().parent.parent / "inputs" / "day00.txt"


def parse_input(raw: str) -> list[int]:
    return [int(line) for line in raw.split()]


def fuel(mass: int) -> int:
    return mass // 3 - 2


def fuel_chain(mass: int) -> Iterator[int]:
    """Fuel for the mass, then fuel for that fuel, ... while each step is positive."""
    while (mass := fuel(mass)) > 0:
        yield mass


def part1(masses: list[int]) -> int:
    return sum(map(fuel, masses))


def part2(masses: list[int]) -> int:
    return sum(sum(fuel_chain(m)) for m in masses)


def solve(raw: str) -> tuple[int, int]:
    parsed = parse_input(raw)
    return part1(parsed), part2(parsed)


def main() -> None:
    parsed = parse_input(INPUT.read_text())
    print(f"part1={part1(parsed)}")
    print(f"part2={part2(parsed)}")


if __name__ == "__main__":
    raise SystemExit(main())
