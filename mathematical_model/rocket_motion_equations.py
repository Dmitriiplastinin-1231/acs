"""rocket_motion_equations.py

Математическая модель движения ракеты в упрощённой постановке.
Здесь находятся правая часть системы уравнений и сохранение временного ряда.
"""
from __future__ import annotations
import csv
import math
from project_configuration import launch_model_parameters as P
from mathematical_model.simulation_result_model import SimulationResult


def rocket_equations_rhs(
    t: float,
    state: tuple[float, float, float],
    theta_delayed: float,
    a_ctrl: float,
    a_z: float,
) -> tuple[float, float, float]:
    """Правая часть системы: y' = v*sin(theta), theta' = omega, omega' = -a*theta(t-tau)."""
    y, theta, omega = state
    v = P.vertical_speed_at(t, a_z)
    return (v * math.sin(theta), omega, -a_ctrl * theta_delayed)


def save_history_csv(result: SimulationResult, filename: str) -> None:
    """Сохраняет временной ряд одного прогона в CSV."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['t_s', 'H_m', 'v_m_s', 'y_m', 'theta_rad', 'omega_rad_s'])
        for row in result.samples:
            writer.writerow([f'{x:.6f}' for x in row])
