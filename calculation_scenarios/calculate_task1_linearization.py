"""calculate_task1_linearization.py

Сценарий запуска первой задачи методом линеаризации.

Для первой задачи можно задавать начальный наклон ракеты напрямую:
    --theta0-deg 2.0

Если этот параметр не указан, начальный угол считается через фазу качки phi0.
"""

from __future__ import annotations

import math

from project_configuration import launch_model_parameters as P
from numerical_methods.small_angle_linearization_method import linearized_displacement


def main() -> None:
    parser = P.build_parser("Задача 1: линеаризация на высоте 10 км")

    parser.add_argument(
        "--phi0",
        type=float,
        default=0.0,
        help="Фаза качки в момент старта, рад",
    )

    parser.add_argument(
        "--theta0-deg",
        type=float,
        default=None,
        help="Начальный наклон ракеты для задачи 1, градусы",
    )

    args = parser.parse_args()

    if args.theta0_deg is not None:
        theta0 = math.radians(args.theta0_deg)
        omega0 = 0.0
        source = "задан напрямую"
    else:
        theta0, omega0 = P.initial_conditions(args.phi0, args.A, args.T)
        source = "вычислен через фазу качки"

    y = linearized_displacement(P.H_10KM, theta0)

    print("=" * 72)
    print("Задача 1: линеаризация")
    print("=" * 72)
    print(f"Начальный угол theta0: {math.degrees(theta0):.3f}° ({source})")
    print(f"Начальная угловая скорость omega0: {math.degrees(omega0):.3f}°/с")
    print("Высота H: 10 км")
    print(f"Δy(10 км) ≈ H * tan(theta0) = {y:.3f} м")
    print("Это верхняя оценка без учёта выравнивания траектории системой управления.")


if __name__ == "__main__":
    main()
