"""phase_sweep_method.py

Параметрический sweep по фазе качки платформы.
"""
from __future__ import annotations
import csv
import math
from typing import Iterable
from project_configuration import launch_model_parameters as P
from mathematical_model.simulation_result_model import SimulationResult
from numerical_methods.heun_rk2_integration_method import simulate_rk2


def sweep_phases(
    num_phases: int,
    *,
    target_height_m: float,
    amplitude: float = P.A_ROLL,
    period: float = P.T_ROLL,
    tau: float = P.TAU,
    a_ctrl: float = P.A_CTRL,
    dt: float = P.DT,
    a_z: float = P.A_Z,
) -> list[SimulationResult]:
    """Равномерно перебирает фазы от 0 до 2π и запускает simulate_rk2."""
    results: list[SimulationResult] = []
    for i in range(num_phases):
        phi0 = 2.0 * math.pi * i / num_phases
        results.append(simulate_rk2(phi0, target_height_m=target_height_m, amplitude=amplitude, period=period, tau=tau, a_ctrl=a_ctrl, dt=dt, a_z=a_z))
    return results


def max_abs_displacement(results: Iterable[SimulationResult]) -> float:
    """Максимальное по модулю боковое смещение среди всех прогонов."""
    return max(abs(r.y_m) for r in results)


def save_sweep_csv(results: Iterable[SimulationResult], filename: str) -> None:
    """Сохраняет сводную таблицу по sweep в CSV."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['phi0_deg', 'theta0_deg', 'omega0_deg_s', 'y_m'])
        for r in results:
            writer.writerow([f'{math.degrees(r.phi0_rad):.6f}', f'{math.degrees(r.theta0_rad):.6f}', f'{math.degrees(r.omega0_rad_s):.6f}', f'{r.y_m:.6f}'])
