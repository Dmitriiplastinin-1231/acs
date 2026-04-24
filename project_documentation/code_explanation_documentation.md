# Краткое объяснение кода

1. launch_model_parameters.py хранит исходные параметры.
2. rocket_motion_equations.py задаёт систему уравнений.
3. heun_rk2_integration_method.py считает одну траекторию методом Хойна.
4. phase_sweep_method.py перебирает фазы качки.
5. calculation_scenarios содержит файлы, которые запускают конкретные расчёты.

Рекомендуемый порядок показа на защите:
1. launch_model_parameters.py
2. rocket_motion_equations.py
3. heun_rk2_integration_method.py
4. phase_sweep_method.py
5. calculation_scenarios/calculate_task2_phase_sweep.py
