"""plot_task1_comparison.py

График для первой задачи:
сравнение линеаризации и численного интегрирования RK2 на высоте 10 км.

Параметр --theta0-deg позволяет менять начальный наклон ракеты.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import math
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt

from project_configuration import launch_model_parameters as P
from numerical_methods.heun_rk2_integration_method import simulate_rk2
from numerical_methods.small_angle_linearization_method import linearized_displacement


def main() -> None:
    parser = argparse.ArgumentParser(
        description="График сравнения линеаризации и RK2 для задачи 1"
    )

    parser.add_argument(
        "--theta0-deg",
        type=float,
        default=2.0,
        help="Начальный наклон ракеты, градусы",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="calculation_results/figures/task1_linearization_vs_rk2.png",
        help="Файл для сохранения графика",
    )

    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    theta0_rad = math.radians(args.theta0_deg)
    omega0_rad_s = 0.0
    phi0 = 0.0

    result_rk2 = simulate_rk2(
        phi0,
        target_height_m=P.H_10KM,
        amplitude=P.A_ROLL,
        period=P.T_ROLL,
        tau=P.TAU,
        a_ctrl=P.A_CTRL,
        dt=P.DT,
        a_z=P.A_Z,
        save_history=False,
        initial_theta_rad=theta0_rad,
        initial_omega_rad_s=omega0_rad_s,
    )

    y_linear_signed = linearized_displacement(P.H_10KM, theta0_rad)
    y_rk2_signed = result_rk2.y_m

    y_linear_abs = abs(y_linear_signed)
    y_rk2_abs = abs(y_rk2_signed)

    labels = [
        "Линеаризация\nбез учёта управления",
        "RK2\nс учётом управления",
    ]

    values = [y_linear_abs, y_rk2_abs]

    fig, ax = plt.subplots(figsize=(10.5, 7.2))

    bars = ax.bar(labels, values, width=0.55)

    ax.axhline(
        1000,
        linestyle="--",
        linewidth=1.4,
        label="допуск 1000 м",
    )

    ax.set_title(
        f"Смещение на высоте 10 км при начальном наклоне θ₀ = {args.theta0_deg:.1f}°",
        fontsize=14,
        pad=14,
    )

    ax.set_ylabel("Модуль бокового смещения |Δy|, м", labelpad=10)
    ax.set_ylim(0, max(1150, max(values) * 1.35))

    ax.grid(axis="y", alpha=0.3)
    ax.legend(loc="upper right")

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + max(20, max(values) * 0.03),
            f"{value:.1f} м",
            ha="center",
            va="bottom",
            fontsize=11,
        )

    if max(values) < 1000:
        conclusion = "Оба результата меньше допуска 1000 м"
    else:
        conclusion = "Смещение превышает допуск 1000 м"

    ax.text(
        0.5,
        0.62,
        conclusion,
        transform=ax.transAxes,
        ha="center",
        fontsize=12,
        bbox={
            "boxstyle": "round,pad=0.35",
            "facecolor": "white",
            "edgecolor": "gray",
            "alpha": 0.9,
        },
    )

    initial_data_text = (
        f"Начальные данные: "
        f"θ₀ = {args.theta0_deg:.1f}°, "
        f"H = 10 км, "
        f"A = {math.degrees(P.A_ROLL):.1f}°, "
        f"τ = {P.TAU:.1f} с, "
        f"h = {P.DT:.2f} с"
    )

    fig.text(
        0.5,
        0.12,
        initial_data_text,
        ha="center",
        fontsize=10.5,
        bbox={
            "boxstyle": "round,pad=0.35",
            "facecolor": "white",
            "edgecolor": "gray",
            "alpha": 0.9,
        },
    )

    explanation_text = (
        "На графике сравниваются две оценки бокового смещения на высоте 10 км. "
        "Линеаризация показывает грубую верхнюю оценку, а RK2 учитывает работу системы управления. "
        "Сравнение ведётся по модулю смещения."
    )

    fig.text(
        0.5,
        0.045,
        explanation_text,
        ha="center",
        fontsize=9.5,
        wrap=True,
    )

    fig.subplots_adjust(left=0.11, right=0.96, top=0.88, bottom=0.28)

    plt.savefig(output_path, dpi=220)

    print("=" * 72)
    print("График задачи 1: сравнение линеаризации и RK2")
    print("=" * 72)
    print(f"Начальный наклон theta0: {args.theta0_deg:.3f}°")
    print(f"Линеаризация: Δy = {y_linear_signed:.3f} м, |Δy| = {y_linear_abs:.3f} м")
    print(f"RK2:           Δy = {y_rk2_signed:.3f} м, |Δy| = {y_rk2_abs:.3f} м")
    print(f"Файл графика: {output_path}")


if __name__ == "__main__":
    main()
