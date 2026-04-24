# Структура проекта

Названия файлов сделаны так, чтобы по ним было понятно, что именно внутри.

## `project_configuration/`

Параметры постановки задачи и численного расчёта.

- `launch_model_parameters.py` — амплитуда качки, период, задержка TVC, шаг интегрирования, высоты 10 км и 160 км, вспомогательные формулы.

## `mathematical_model/`

Математическая модель движения.

- `simulation_result_model.py` — формат результата одного численного прогона.
- `rocket_motion_equations.py` — правая часть системы уравнений и формула боковой скорости.

## `numerical_methods/`

Методы решения задачи.

- `small_angle_linearization_method.py` — аналитическая верхняя оценка для первой задачи.
- `heun_rk2_integration_method.py` — численное интегрирование методом Хойна RK2.
- `phase_sweep_method.py` — равномерный перебор фаз качки.

## `calculation_scenarios/`

Сценарии запуска конкретных расчётов.

- `calculate_task1_linearization.py` — задача 1 через линеаризацию.
- `calculate_task1_rk2.py` — задача 1 через RK2.
- `calculate_task2_phase_sweep.py` — задача 2 через sweep + RK2.

## `user_interface/`

Будущий графический интерфейс.

- `user_interface_plan.md` — заметка о следующем этапе.

## `graph_scripts/`

Будущие скрипты для построения графиков.

- `graph_scripts_plan.md` — заметка о следующем этапе.

## `calculation_results/`

Готовые результаты расчётов.

- `csv/` — таблицы с результатами;
- `figures/` — будущие изображения графиков.

## `project_documentation/`

Документация для защиты и пояснения структуры проекта.
