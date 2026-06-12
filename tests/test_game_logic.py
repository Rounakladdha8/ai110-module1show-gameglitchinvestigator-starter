"""Pytest tests for the fixed Game Glitch Investigator logic.

The game logic currently lives in app.py (logic_utils.py is still stubbed with
NotImplementedError), so these tests import the functions from app. app.py
imports cleanly in Streamlit's "bare mode" -- the module-level UI calls just emit
warnings and the button branches are skipped, so importing it has no side effects
that affect these unit tests.
"""

import os
import sys

import pytest

# Make the project root importable so `import app` resolves when pytest runs
# from the tests/ directory.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import check_guess, parse_guess, update_score  # noqa: E402

# Valid guess range enforced by app.py's submit handler.
VALID_LOW, VALID_HIGH = 1, 100


def _is_valid_guess(raw):
    """Mirror app.py's two-step input validation: parse, then range-check.

    NOTE: the range check (1 <= guess <= 100) currently lives inline in app.py's
    submit handler rather than in a standalone function, so it cannot be imported
    directly. This helper reproduces that exact logic so it can be unit-tested.
    Replace it by importing a real validation function once that logic is
    extracted from the handler.
    """
    ok, value, _err = parse_guess(raw)
    if not ok:
        return False
    return VALID_LOW <= value <= VALID_HIGH


# --- Correct guess ---------------------------------------------------------

def test_correct_guess_is_a_win():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


# --- Too-high guess (should tell the player to go LOWER) -------------------

def test_too_high_guess_tells_player_to_go_lower():
    # Regression guard for the original swapped-hint bug (secret 63, guess 70).
    outcome, message = check_guess(70, 63)
    assert outcome == "Too High"
    assert "LOWER" in message.upper()
    assert "HIGHER" not in message.upper()


# --- Too-low guess (should tell the player to go HIGHER) -------------------

def test_too_low_guess_tells_player_to_go_higher():
    outcome, message = check_guess(40, 63)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()
    # "HIGHER" contains the substring of "LOWER"? No -- guard the exact word.
    assert "GO LOWER" not in message.upper()


def test_comparison_is_numeric_not_lexicographic():
    # Regression guard for the str()-cast bug: "9" > "63" lexicographically but
    # 9 < 63 numerically. A single-digit guess below a two-digit secret must be
    # reported as Too Low.
    outcome, _message = check_guess(9, 63)
    assert outcome == "Too Low"


# --- Invalid / out-of-range input ------------------------------------------

@pytest.mark.parametrize("raw", ["0", "-1", "-50", "101", "150", "1000"])
def test_out_of_range_guess_is_rejected(raw):
    assert _is_valid_guess(raw) is False


@pytest.mark.parametrize("raw", ["1", "50", "100"])
def test_in_range_guess_is_accepted(raw):
    assert _is_valid_guess(raw) is True


@pytest.mark.parametrize("raw", ["abc", "", "   ", "3.x", None])
def test_non_numeric_input_is_rejected(raw):
    ok, value, err = parse_guess(raw)
    assert ok is False
    assert value is None
    assert err  # a non-empty error message is returned


# --- Score behavior --------------------------------------------------------

def test_win_awards_points():
    # 100 - 10 * (attempt_number + 1); attempt 1 -> 80
    assert update_score(0, "Win", 1) == 80


def test_win_points_floor_at_10():
    # Late wins never award fewer than 10 points.
    assert update_score(0, "Win", 20) == 10


def test_too_low_always_subtracts_5():
    assert update_score(100, "Too Low", 3) == 95
    assert update_score(100, "Too Low", 4) == 95


def test_too_high_depends_on_attempt_parity():
    assert update_score(100, "Too High", 2) == 105  # even attempt -> +5
    assert update_score(100, "Too High", 3) == 95   # odd attempt  -> -5


def test_unknown_outcome_leaves_score_unchanged():
    assert update_score(42, "Something Else", 1) == 42
