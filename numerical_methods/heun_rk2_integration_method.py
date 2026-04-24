"""heun_rk2_integration_method.py

Численное интегрирование методом Хойна, то есть RK2.

Файл отвечает за один численный прогон:
для заданных начальных условий считается движение ракеты до нужной высоты.

Для задачи 2 начальные условия обычно берутся из фазы качки phi0.
Для задачи 1 можно задать начальный наклон ракеты напрямую через initial_theta_rad.
"""

from __future__ import annotations

import math
from collections import deque

from project_configuration import launch_model_parameters as P
from mathematical_model.rocket_motion_equations import rocket_equations_rhs
from mathematical_model.simulation_result_model import SimulationResult


def simulate_rk2(
    phi0: float,
    *,
    target_height_m: float,
    amplitude: float = P.A_ROLL,
    period: float = P.T_ROLL,
    tau: float = P.TAU,
    a_ctrl: float = P.A_CTRL,
    dt: float = P.DT,
    a_z: float = P.A_Z,
    save_history: bool = False,
    initial_theta_rad: float | None = None,
    initial_omega_rad_s: float | None = None,
) -> SimulationResult:
    """Считает одну траекторию методом Хойна RK2.

    Параметры:
    - phi0 — фаза качки в момент старта;
    - target_height_m — высота, до которой идёт расчёт;
    - amplitude — амплитуда качки платформы;
    - period — период качки;
    - tau — задержка управления;
    - a_ctrl — коэффициент управления;
    - dt — шаг интегрирования;
    - a_z — вертикальное ускорение;
    - save_history — сохранять ли временной ряд;
    - initial_theta_rad — начальный угол ракеты, если задаётся напрямую;
    - initial_omega_rad_s — начальная угловая скорость, если задаётся напрямую.

    Если initial_theta_rad и initial_omega_rad_s не переданы,
    начальные условия вычисляются через фазу качки phi0.
    """

    # 1. Начальные условия.
    #
    # Для задачи 2:
    # начальный угол и начальная угловая скорость вычисляются по фазе качки.
    #
    # Для задачи 1:
    # начальный угол можно задать напрямую через initial_theta_rad.
    if initial_theta_rad is None or initial_omega_rad_s is None:
        theta0, omega0 = P.initial_conditions(phi0, amplitude, period)
    else:
        theta0 = initial_theta_rad
        omega0 = initial_omega_rad_s

    # 2. Время, за которое ракета достигает целевой высоты.
    target_time = P.time_to_height(target_height_m, a_z)

    # 3. Количество шагов интегрирования.
    n_steps = math.ceil(target_time / dt)

    # 4. Задержка управления в шагах.
    #
    # Например:
    # tau = 0.3 c, dt = 0.01 c
    # значит задержка равна 30 шагам.
    n_delay = max(1, round(tau / dt))

    # 5. Начальное состояние системы.
    #
    # state = (y, theta, omega)
    # y — боковое смещение;
    # theta — угол отклонения;
    # omega — угловая скорость.
    state = (0.0, theta0, omega0)

    # 6. Буфер для значения theta(t - tau).
    #
    # Пока прошлых значений ещё нет, считаем, что до старта угол был равен theta0.
    history = deque([theta0] * (n_delay + 2), maxlen=n_delay + 2)

    samples: list[tuple[float, float, float, float, float, float]] = []

    t = 0.0

    for _ in range(n_steps + 1):
        height = P.height_at(t, a_z)
        speed = P.vertical_speed_at(t, a_z)
        y, theta, omega = state

        if save_history:
            samples.append((t, height, speed, y, theta, omega))

        if height >= target_height_m:
            break

        # Значение угла с задержкой для первой стадии RK2.
        theta_delayed_k1 = history[0]

        # Значение угла с задержкой для второй стадии RK2.
        theta_delayed_k2 = history[1]

        # Стадия 1: предиктор.
        k1 = rocket_equations_rhs(
            t,
            state,
            theta_delayed_k1,
            a_ctrl,
            a_z,
        )

        predicted_state = tuple(
            state[i] + dt * k1[i]
            for i in range(3)
        )

        # Стадия 2: корректор.
        k2 = rocket_equations_rhs(
            t + dt,
            predicted_state,
            theta_delayed_k2,
            a_ctrl,
            a_z,
        )

        # Формула метода Хойна:
        # x_{n+1} = x_n + h/2 * (k1 + k2)
        state = tuple(
            state[i] + 0.5 * dt * (k1[i] + k2[i])
            for i in range(3)
        )

        # Сохраняем новое значение theta для будущего учёта задержки.
        history.append(state[1])

        t += dt

    return SimulationResult(
        phi0_rad=phi0,
        theta0_rad=theta0,
        omega0_rad_s=omega0,
        target_height_m=target_height_m,
        target_time_s=t,
        y_m=state[0],
        samples=samples,
    )
