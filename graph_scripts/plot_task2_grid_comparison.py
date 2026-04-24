"""plot_task2_grid_comparison.py

График сравнения двух сеток sweep: N=8 и N=72.

Нужен для защиты:
показывает, зачем мы сначала считаем на 8 фазах,
а потом проверяем результат на более плотной сетке из 72 фаз.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


def read_sweep_csv(csv_path: Path) -> tuple[list[float], list[float]]:
    """Читает CSV sweep и возвращает фазы и смещения."""
    phases_deg: list[float] = []
    displacements_m: list[float] = []

    with open(csv_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            phases_deg.append(float(row["phi0_deg"]))
            displacements_m.append(float(row["y_m"]))

    return phases_deg, displacements_m


def close_period(
    phases_deg: list[float],
    displacements_m: list[float],
) -> tuple[list[float], list[float]]:
    """Добавляет точку 360°, равную точке 0°."""
    if not phases_deg:
        return phases_deg, displacements_m

    closed_phases = phases_deg.copy()
    closed_displacements = displacements_m.copy()

    if phases_deg[-1] < 360.0:
        closed_phases.append(360.0)
        closed_displacements.append(displacements_m[0])

    return closed_phases, closed_displacements


def find_max_abs(
    phases_deg: list[float],
    displacements_m: list[float],
) -> tuple[float, float]:
    """Возвращает фазу и смещение для максимума по модулю."""
    max_index = max(range(len(displacements_m)), key=lambda i: abs(displacements_m[i]))
    return phases_deg[max_index], displacements_m[max_index]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Сравнение sweep-сеток N=8 и N=72"
    )

    parser.add_argument(
        "--input-small",
        type=str,
        default="calculation_results/csv/task2_phase_sweep_N8.csv",
        help="CSV-файл для основной сетки N=8",
    )

    parser.add_argument(
        "--input-large",
        type=str,
        default="calculation_results/csv/task2_phase_sweep_N72.csv",
        help="CSV-файл для контрольной сетки N=72",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="calculation_results/figures/task2_grid_comparison.png",
        help="Файл для сохранения графика",
    )

    args = parser.parse_args()

    input_small = Path(args.input_small)
    input_large = Path(args.input_large)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    phases_8, y_8 = read_sweep_csv(input_small)
    phases_72, y_72 = read_sweep_csv(input_large)

    if not phases_8:
        raise ValueError(f"CSV-файл пустой: {input_small}")

    if not phases_72:
        raise ValueError(f"CSV-файл пустой: {input_large}")

    plot_phases_72, plot_y_72 = close_period(phases_72, y_72)
    plot_phases_8, plot_y_8 = close_period(phases_8, y_8)

    max_phase_8, max_y_8 = find_max_abs(phases_8, y_8)
    max_phase_72, max_y_72 = find_max_abs(phases_72, y_72)

    rel_diff = abs(abs(max_y_8) - abs(max_y_72)) / abs(max_y_72) * 100.0

    fig, ax = plt.subplots(figsize=(11.5, 6.8))

    # Допустимая зона ±1000 м.
    ax.axhspan(
        -1000,
        1000,
        alpha=0.14,
        label="допустимая зона ±1000 м",
    )

    ax.axhline(1000, linestyle="--", linewidth=1.2, label="граница +1000 м")
    ax.axhline(-1000, linestyle="--", linewidth=1.2, label="граница -1000 м")
    ax.axhline(0, linewidth=1, alpha=0.6)

    # Плотная сетка N=72 — показывает более точную форму зависимости.
    ax.plot(
        plot_phases_72,
        plot_y_72,
        linewidth=1.8,
        label="контрольная сетка N=72",
    )

    # Основная сетка N=8 — отдельные крупные точки.
    ax.scatter(
        plot_phases_8,
        plot_y_8,
        s=55,
        zorder=3,
        label="основная сетка N=8",
    )

    # Максимум на N=72.
    ax.scatter(
        [max_phase_72],
        [max_y_72],
        s=95,
        zorder=4,
        label="максимум для N=72",
    )

    ax.annotate(
        f"N=72: |Δy|max ≈ {abs(max_y_72):.0f} м\nφ₀ ≈ {max_phase_72:.0f}°",
        xy=(max_phase_72, max_y_72),
        xytext=(max_phase_72 - 33, max_y_72 * 0.70),
        arrowprops={"arrowstyle": "->"},
        fontsize=10,
        bbox={
            "boxstyle": "round,pad=0.3",
            "facecolor": "white",
            "edgecolor": "gray",
            "alpha": 0.85,
        },
    )

    ax.set_title(
        "Сравнение sweep по фазе качки: N=8 и N=72",
        fontsize=14,
        pad=12,
    )

    ax.set_xlabel("Фаза качки φ₀, градусы", labelpad=12)
    ax.set_ylabel("Боковое смещение Δy на высоте 160 км, м", labelpad=8)

    ax.set_xlim(0, 360)
    ax.set_xticks(range(0, 361, 45))

    y_min = min(plot_y_72 + plot_y_8)
    y_max = max(plot_y_72 + plot_y_8)
    margin = 0.12 * (y_max - y_min)
    ax.set_ylim(y_min - margin, y_max + margin)

    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left")

    # Подпись с главным выводом.
    ax.text(
        0.98,
        0.04,
        f"Расхождение максимумов: {rel_diff:.2f}%",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=10,
        bbox={
            "boxstyle": "round,pad=0.3",
            "facecolor": "white",
            "edgecolor": "gray",
            "alpha": 0.85,
        },
    )

    fig.subplots_adjust(left=0.10, right=0.98, top=0.90, bottom=0.16)

    plt.savefig(output_path, dpi=220)

    print("=" * 72)
    print("График сравнения sweep-сеток N=8 и N=72")
    print("=" * 72)
    print(f"CSV N=8: {input_small}")
    print(f"CSV N=72: {input_large}")
    print(f"Файл графика: {output_path}")
    print(f"Максимум |Δy| для N=8: {abs(max_y_8):.3f} м")
    print(f"Максимум |Δy| для N=72: {abs(max_y_72):.3f} м")
    print(f"Расхождение максимумов: {rel_diff:.2f}%")


if __name__ == "__main__":
    main()
