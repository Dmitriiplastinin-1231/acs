"""plot_task2_phase_sweep.py

График для второй задачи:
зависимость бокового смещения ракеты от фазы качки платформы.

График показывает, при каких фазах старта смещение выходит
за допустимые пределы ±1000 м.
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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="График смещения от фазы качки для задачи 2"
    )

    parser.add_argument(
        "--input",
        type=str,
        default="calculation_results/csv/task2_phase_sweep_N72.csv",
        help="CSV-файл с результатами sweep",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="calculation_results/figures/task2_phase_sweep.png",
        help="Файл для сохранения графика",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    phases_deg, displacements_m = read_sweep_csv(input_path)

    if not phases_deg:
        raise ValueError(f"CSV-файл пустой: {input_path}")

    max_index = max(range(len(displacements_m)), key=lambda i: abs(displacements_m[i]))
    max_phase = phases_deg[max_index]
    max_displacement = displacements_m[max_index]

    plot_phases, plot_displacements = close_period(phases_deg, displacements_m)

    fig, ax = plt.subplots(figsize=(11.5, 6.8))

    # Допустимая зона ±1000 м.
    ax.axhspan(
        -1000,
        1000,
        alpha=0.14,
        label="допустимая зона ±1000 м",
    )

    # Границы допуска.
    ax.axhline(1000, linestyle="--", linewidth=1.2, label="граница +1000 м")
    ax.axhline(-1000, linestyle="--", linewidth=1.2, label="граница -1000 м")

    # Нулевая линия — показывает смену направления смещения.
    ax.axhline(0, linewidth=1, alpha=0.6)

    # Основная кривая.
    ax.plot(
        plot_phases,
        plot_displacements,
        marker="o",
        linewidth=1.8,
        markersize=3,
        label="смещение Δy",
    )

    # Худший случай.
    ax.scatter(
        [max_phase],
        [max_displacement],
        s=90,
        zorder=3,
        label="худший случай",
    )

    # Вертикальная линия через фазу максимума.
    ax.axvline(max_phase, linestyle=":", linewidth=1.2)

    # Подпись худшего случая. Сдвинута выше, чтобы не мешать оси X.
    ax.annotate(
        f"максимум |Δy| ≈ {abs(max_displacement):.0f} м\nφ₀ ≈ {max_phase:.0f}°",
        xy=(max_phase, max_displacement),
        xytext=(87, -1500),
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
        "Зависимость бокового смещения ракеты от фазы качки платформы",
        fontsize=14,
        pad=12,
    )

    ax.set_xlabel("Фаза качки φ₀, градусы", labelpad=12)
    ax.set_ylabel("Боковое смещение Δy на высоте 160 км, м", labelpad=8)

    ax.set_xlim(0, 360)
    ax.set_xticks(range(0, 361, 45))

    # Небольшой запас по вертикали, чтобы элементы не прижимались к краям.
    y_min = min(plot_displacements)
    y_max = max(plot_displacements)
    margin = 0.12 * (y_max - y_min)
    ax.set_ylim(y_min - margin, y_max + margin)

    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left")

    # Увеличиваем нижний отступ, чтобы подпись оси X не залезала на график.
    fig.subplots_adjust(left=0.10, right=0.98, top=0.90, bottom=0.16)

    plt.savefig(output_path, dpi=220)

    print("=" * 72)
    print("График задачи 2: смещение от фазы качки")
    print("=" * 72)
    print(f"Входной CSV: {input_path}")
    print(f"Файл графика: {output_path}")
    print(f"Максимум по модулю: {abs(max_displacement):.3f} м")
    print(f"Фаза максимума: {max_phase:.1f}°")
    print(f"Смещение в этой фазе: {max_displacement:.3f} м")

    if abs(max_displacement) > 1000:
        print("Вывод по графику: кривая выходит за допустимую зону ±1000 м.")
    else:
        print("Вывод по графику: кривая остаётся внутри допустимой зоны ±1000 м.")


if __name__ == "__main__":
    main()
