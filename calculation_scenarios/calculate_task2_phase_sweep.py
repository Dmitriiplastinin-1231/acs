"""calculate_task2_phase_sweep.py

Сценарий второй задачи: sweep фаз качки + RK2 до высоты 160 км.
"""
from __future__ import annotations
import csv
import math
from pathlib import Path
from project_configuration import launch_model_parameters as P
from numerical_methods.phase_sweep_method import max_abs_displacement, save_sweep_csv, sweep_phases


def main() -> None:
    parser = P.build_parser('Задача 2: sweep фаз + RK2 до 160 км')
    parser.add_argument('--n-small', type=int, default=P.N_PHASES_SMALL, help='Число фаз в основном sweep')
    parser.add_argument('--n-large', type=int, default=P.N_PHASES_LARGE, help='Число фаз в контрольном sweep')
    parser.add_argument('--output-dir', type=str, default='calculation_results/csv', help='Папка для CSV-результатов')
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    res_small = sweep_phases(args.n_small, target_height_m=P.H_160KM, amplitude=args.A, period=args.T, tau=args.tau, a_ctrl=args.a, dt=args.dt, a_z=args.az)
    res_large = sweep_phases(args.n_large, target_height_m=P.H_160KM, amplitude=args.A, period=args.T, tau=args.tau, a_ctrl=args.a, dt=args.dt, a_z=args.az)

    max_small = max_abs_displacement(res_small)
    max_large = max_abs_displacement(res_large)

    save_sweep_csv(res_small, output_dir / f'task2_phase_sweep_N{args.n_small}.csv')
    save_sweep_csv(res_large, output_dir / f'task2_phase_sweep_N{args.n_large}.csv')

    comparison_path = output_dir / 'task2_phase_sweep_grid_comparison.csv'
    with open(comparison_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['N_phases', 'max_abs_y_m'])
        writer.writerow([args.n_small, f'{max_small:.6f}'])
        writer.writerow([args.n_large, f'{max_large:.6f}'])

    print('=' * 72)
    print('Задача 2: sweep фаз + RK2 до 160 км')
    print('=' * 72)
    print(f'Время до 160 км: {P.time_to_height(P.H_160KM, args.az):.3f} с')
    print()
    print(f"{'φ0, град':>10} {'θ0, град':>10} {'ω0, град/с':>12} {'y(160 км), м':>14}")
    print(f"{'-' * 10} {'-' * 10} {'-' * 12} {'-' * 14}")
    for r in res_small:
        print(f'{math.degrees(r.phi0_rad):>10.1f} {math.degrees(r.theta0_rad):>10.3f} {math.degrees(r.omega0_rad_s):>12.3f} {r.y_m:>14.3f}')

    print()
    print(f'Максимум |y| для N={args.n_small}: {max_small:.3f} м')
    print(f'Максимум |y| для N={args.n_large}: {max_large:.3f} м')
    if max_large > 0.0:
        rel_diff = abs(max_small - max_large) / max_large * 100.0
        print(f'Расхождение между N={args.n_small} и N={args.n_large}: {rel_diff:.2f}%')

    max_dev = max(max_small, max_large)
    print()
    print(f'Итоговый максимум |Δy|: {max_dev:.3f} м')
    if max_dev < 1_000.0:
        print('Вывод: смещением можно пренебречь для допуска ±1 км.')
    else:
        print('Вывод: смещением нельзя пренебречь для допуска ±1 км.')


if __name__ == '__main__':
    main()
