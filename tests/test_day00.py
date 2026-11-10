"""Day 0: The Tyranny of the Rocket Equation (tutorial dry run).

The worked model for a finished 2026 test module.  Every test takes the
`solution` fixture, so it runs once against src/day00.py and once against
AI_src/day00.py.  Tests go through the five public names only (parse_input,
part1, part2, solve, main's INPUT): the statement fixes behaviour, not the
helpers an implementation chooses, so a test written from the statement
gives away nothing about how to solve it.
"""

import pytest

# (part1, part2) once adventofcode.com has accepted both; None until then.
LOCKED = (3481005, 5218616)

EXAMPLE = "12\n14\n1969\n100756\n"


def test_parse_input(solution):
    assert solution.parse_input(EXAMPLE) == [12, 14, 1969, 100756]


@pytest.mark.parametrize(("mass", "fuel"), [(12, 2), (14, 2), (1969, 654), (100756, 33583)])
def test_part1_statement_examples(solution, mass, fuel):
    assert solution.part1(solution.parse_input(f"{mass}\n")) == fuel


@pytest.mark.parametrize(("mass", "fuel"), [(14, 2), (1969, 966), (100756, 50346)])
def test_part2_statement_examples(solution, mass, fuel):
    assert solution.part2(solution.parse_input(f"{mass}\n")) == fuel


def test_parts_sum_over_modules(solution):
    parsed = solution.parse_input(EXAMPLE)
    assert solution.part1(parsed) == 2 + 2 + 654 + 33583
    assert solution.part2(parsed) == 2 + 2 + 966 + 50346


@pytest.mark.parametrize("mass", [1, 2, 6, 8])
def test_part2_small_masses_need_no_fuel(solution, mass):
    """mass // 3 - 2 is <= 0 for these; part 2 must count nothing, not a negative amount."""
    assert solution.part2(solution.parse_input(f"{mass}\n")) == 0


def test_crlf_input(solution):
    """Windows-downloaded inputs carry \r; parse_input must not keep it."""
    assert solution.parse_input(EXAMPLE.replace("\n", "\r\n")) == solution.parse_input(EXAMPLE)


def test_real_input_locked(solution, check_locked):
    check_locked(solution, LOCKED)
