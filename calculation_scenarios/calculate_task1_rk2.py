"""calculate_task1_rk2.py

Сценарий численного решения первой задачи методом Хойна (RK2).

Для первой задачи можно задавать начальный наклон ракеты напрямую:
    --theta0-deg 2.0

Если этот параметр не указан, начальные условия считаются через фазу качки phi0.
"""

from __future__ import annotations

import math
from pathlib import Path

from project_configuration import launch_model_parameters as P
from mathematical_model.rocket_motion_equations import save_history_csv
from numerical_methods.heun_rk2_integration_method import simulate_rk2
from numerical_methods.small_angle_linearization_method import linearized_displacement


def main() -> None:
    parser = P.build_parser("Задача 1: RK2 до 10 км")

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

    parser.add_argument(
        "--csv",
        type=str,
        default="calculation_results/csv/task1_rk2_time_history.csv",
        help="CSV-файл с временным рядом",
    )

    args = parser.parse_args()

    if args.theta0_deg is not None:
        theta0 = math.radians(args.theta0_deg)
        omega0 = 0.0
        source = "задан напрямую"
        initial_theta_rad = theta0
        initial_omega_rad_s = omega0
    else:
        theta0, omega0 = P.initial_conditions(args.phi0, args.A, args.T)
        source = "вычислен через фазу качки"
        initial_theta_rad = None
        initial_omega_rad_s = None

    result = simulate_rk2(
        args.phi0,
        target_height_m=P.H_10KM,
        amplitude=args.A,
        period=args.T,
        tau=args.tau,
        a_ctrl=args.a,
        dt=args.dt,
        a_z=args.az,
        save_history=True,
        initial_theta_rad=initial_theta_rad,
        initial_omega_rad_s=initial_omega_rad_s,
    )

    Path(args.csv).parent.mkdir(parents=True, exist_ok=True)
    save_history_csv(result, args.csv)

    y_lin = linearized_displacement(P.H_10KM, result.theta0_rad)

    print("=" * 72)
    print("Задача 1: RK2 (метод Хойна) до 10 км")
    print("=" * 72)
    print(f"Начальный угол theta0: {math.degrees(result.theta0_rad):.3f}° ({source})")
    print(f"Начальная угловая скорость omega0: {math.degrees(result.omega0_rad_s):.3f}°/с")
    print(f"Численное интегрирование: Δy(10 км) = {result.y_m:.3f} м")
    print(f"Линеаризация:            Δy(10 км) = {y_lin:.3f} м")
    print(f"CSV сохранён: {args.csv}")


if __name__ == "__main__":
    main()
