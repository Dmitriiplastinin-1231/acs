"""project_launcher.py

Единая точка входа в проект.

Через этот файл можно запускать:
- расчёт первой задачи методом линеаризации;
- расчёт первой задачи методом RK2;
- расчёт второй задачи через sweep;
- графический интерфейс проекта.
"""

from __future__ import annotations

from calculation_scenarios import (
    calculate_task1_linearization,
    calculate_task1_rk2,
    calculate_task2_phase_sweep,
)
from user_interface import desktop_app


def main() -> None:
    print("Запуск с морской платформы")
    print()
    print("Выберите сценарий:")
    print("1 — Задача 1: линеаризация на 10 км")
    print("2 — Задача 1: RK2 на 10 км")
    print("3 — Задача 2: sweep фаз + RK2 на 160 км")
    print("4 — Графический интерфейс")
    print("0 — выход")
    print()

    choice = input("Введите номер: ").strip()

    if choice == "1":
        calculate_task1_linearization.main()

    elif choice == "2":
        calculate_task1_rk2.main()

    elif choice == "3":
        calculate_task2_phase_sweep.main()

    elif choice == "4":
        desktop_app.main()

    elif choice == "0":
        print("Выход.")

    else:
        print("Неизвестный пункт меню.")


if __name__ == "__main__":
    main()
