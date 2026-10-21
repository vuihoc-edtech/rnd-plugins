"""Helpers for numbers written the Vietnamese way inside question text."""

from __future__ import annotations

import re
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction

# Needs sympy: `pip install sympy` when the Python environment does not have it.
from sympy import Rational


def num(text: str) -> Rational:
    """An exact number from Vietnamese notation: '60.000' -> 60000, '0{,}175' -> 7/40."""
    s = text.strip().replace("{,}", ",").replace(" ", "").replace(" ", "")
    s = s.strip("$")
    if re.fullmatch(r"-?\d{1,3}(\.\d{3})+(,\d+)?", s):
        s = s.replace(".", "")
    s = s.replace(",", ".")
    return Rational(Fraction(s))


def rnd(value, digits: int = 0) -> Decimal:
    """`value` rounded half up to `digits` decimals, as Vietnamese textbooks round."""
    exp = Decimal(1).scaleb(-digits)
    return Decimal(str(float(value))).quantize(exp, rounding=ROUND_HALF_UP)
