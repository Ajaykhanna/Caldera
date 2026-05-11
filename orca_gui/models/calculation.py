"""Calculation-mode model types."""

from typing import Literal

CalculationMode = Literal["static", "dynamics"]
StaticJobType = Literal["energy", "opt", "freq"]
StateType = Literal["ground", "excited"]
