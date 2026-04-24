# Запуск ракеты с морской платформы

Проект решает задачу оценки бокового смещения ракеты при старте с подвижной морской платформы.

Платформа качается с амплитудой до 2° и периодом 8 секунд. Система управления ракетой компенсирует отклонение, но имеет задержку 0.3 секунды между измерением угла и управляющим воздействием.

## Постановка задачи

Нужно ответить на два вопроса:

1. Насколько сместится траектория ракеты на высоте 10 км из-за наклона платформы в момент старта?
2. Можно ли пренебречь этим смещением при выводе спутника на орбиту, если точность выведения составляет ±1 км?

Для второго вопроса в проекте принята расчётная высота 160 км.

---

## Используемые методы

### Задача 1: высота 10 км

Используются два подхода:

1. **Линеаризация** — простая верхняя оценка смещения:

\[
\Delta y \approx H \cdot \tan(\theta_0)
\]

2. **Численное интегрирование RK2** — расчёт с учётом управления и задержки.

Итог: даже грубая верхняя оценка меньше 1000 м, поэтому на высоте 10 км смещением можно пренебречь.

---

### Задача 2: высота 160 км

Используется связка методов:

1. **Метод Хойна / RK2** — численное интегрирование уравнений движения.
2. **Параметрический sweep по фазе качки** — перебор возможных моментов старта.

Фаза качки в момент запуска заранее неизвестна, поэтому программа перебирает разные значения фазы:

\[
\varphi_0 \in [0, 2\pi)
\]

Для каждой фазы вычисляются начальные условия:

\[
\theta_0 = A \cdot \cos(\varphi_0)
\]

\[
\omega_0 = -A \cdot \Omega \cdot \sin(\varphi_0)
\]

После этого для каждой фазы запускается численное интегрирование, а итогом считается максимальное смещение по модулю.

---

## Структура проекта

```text
offshore_launch_simulation_named_files/
├── project_launcher.py
├── README.md
├── requirements.txt
│
├── project_configuration/
│   └── launch_model_parameters.py
│
├── mathematical_model/
│   ├── rocket_motion_equations.py
│   └── simulation_result_model.py
│
├── numerical_methods/
│   ├── small_angle_linearization_method.py
│   ├── heun_rk2_integration_method.py
│   └── phase_sweep_method.py
│
├── calculation_scenarios/
│   ├── calculate_task1_linearization.py
│   ├── calculate_task1_rk2.py
│   └── calculate_task2_phase_sweep.py
│
├── graph_scripts/
│   ├── plot_task1_comparison.py
│   ├── plot_task2_phase_sweep.py
│   └── plot_task2_grid_comparison.py
│
├── user_interface/
│   └── desktop_app.py
│
├── calculation_results/
│   ├── csv/
│   └── figures/
│
└── project_documentation/
    ├── project_structure_documentation.md
    ├── mathematical_model_documentation.md
    └── code_explanation_documentation.md

---

## Установка зависимостей

На Linux можно установить зависимости так:

```bash
sudo apt install python3-matplotlib python3-tk python3-pil python3-pil.imagetk
