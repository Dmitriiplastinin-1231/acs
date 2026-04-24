"""small_angle_linearization_method.py

Метод линеаризации для первой задачи: Δy ≈ H * tan(theta0).
"""
from __future__ import annotations
import math


def linearized_displacement(height_m: float, theta0_rad: float) -> float:
    """Возвращает верхнюю оценку бокового смещения."""
    return height_m * math.tan(theta0_rad)
