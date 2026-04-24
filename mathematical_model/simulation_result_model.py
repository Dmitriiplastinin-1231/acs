"""simulation_result_model.py

Структура для хранения результата одного численного прогона.
Здесь нет алгоритма расчёта — только формат данных, который возвращает симулятор.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class SimulationResult:
    """Результат одного численного прогона."""
    phi0_rad: float
    theta0_rad: float
    omega0_rad_s: float
    target_height_m: float
    target_time_s: float
    y_m: float
    samples: list[tuple[float, float, float, float, float, float]]
