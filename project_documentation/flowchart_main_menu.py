"""flowchart_main_menu.py

Визуализация блок-схемы главного меню проекта.
Соответствует логике в project_launcher.py

Блок-схема:
┌─────────────────────────┐
│  Запуск Desktop GUI     │
└────────────┬────────────┘
             │
             ▼
┌──────────────────────────────┐
│  Вывод параметров платформы  │
│  и информации интеграции     │
└────────────┬─────────────────┘
             │
             ▼
┌──────────────────────────────┐
│  Содание экземпля notebook:  │
│  Управление: Лон. Главное    │
└────────────┬─────────────────┘
             │
             ▼
         ◇─────◇
        ╱       ╲
       ╱ Выберите ╲
      │ сценарий   │
       ╲         ╱
        ╲       ╱
         ◇─────◇
        ╱   │   ╲
       /    │    \
      ▼     ▼     ▼
 [1]  [2]  [3]  [4]  [0]
  │    │    │    │    │
  ▼    ▼    ▼    ▼    ▼
╔═══════════════════════════════════════════════════════════╗
║ 1. RK2 на 10 км  2. Линеаризация  3. Sweep+RK2  4. GUI   ║
╚═══════════════════════════════════════════════════════════╝
              │    │       │         │      │
              └────┴───────┴─────────┴──────┘
                        │
                        ▼
              ┌──────────────────┐
              │ Выполнить расчет │
              │  или загрузить   │
              │   интерфейс      │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │    Конец         │
              └──────────────────┘
"""

import tkinter as tk
from tkinter import messagebox


def visualize_flowchart():
    """Создает визуальное представление блок-схемы главного меню."""
    
    root = tk.Tk()
    root.title("Блок-схема главного меню проекта")
    root.geometry("900x1000")
    
    # Создаем холст для рисования
    canvas = tk.Canvas(root, bg="white", width=900, height=1000)
    canvas.pack(fill="both", expand=True)
    
    # Функции для рисования элементов блок-схемы
    def draw_box(x, y, width, height, text, canvas):
        """Рисует прямоугольник (процесс)."""
        canvas.create_rectangle(
            x - width/2, y - height/2,
            x + width/2, y + height/2,
            outline="black", width=2
        )
        canvas.create_text(x, y, text=text, font=("Arial", 10), justify="center")
    
    def draw_diamond(x, y, width, height, text, canvas):
        """Рисует ромб (решение)."""
        points = [
            x, y - height/2,  # вершина
            x + width/2, y,   # правая точка
            x, y + height/2,  # нижняя точка
            x - width/2, y    # левая точка
        ]
        canvas.create_polygon(points, outline="black", width=2, fill="lightgray")
        canvas.create_text(x, y, text=text, font=("Arial", 10), justify="center")
    
    def draw_oval(x, y, width, height, text, canvas):
        """Рисует овал (начало/конец)."""
        canvas.create_oval(
            x - width/2, y - height/2,
            x + width/2, y + height/2,
            outline="black", width=2
        )
        canvas.create_text(x, y, text=text, font=("Arial", 10), justify="center")
    
    def draw_arrow(x1, y1, x2, y2, canvas, label=""):
        """Рисует стрелку."""
        canvas.create_line(x1, y1, x2, y2, arrow="last", width=2)
        if label:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            canvas.create_text(mid_x + 20, mid_y, text=label, font=("Arial", 9))
    
    # Рисуем блок-схему
    draw_oval(450, 50, 150, 40, "Запуск Desktop GUI", canvas)
    draw_arrow(450, 70, 450, 120, canvas)
    
    draw_box(450, 160, 250, 60, "Вывод параметров платформы\nи информации интеграции", canvas)
    draw_arrow(450, 190, 450, 240, canvas)
    
    draw_box(450, 280, 250, 60, "Содание экземпля notebook:\nУправление: Лон. Главное", canvas)
    draw_arrow(450, 310, 450, 370, canvas)
    
    draw_diamond(450, 420, 150, 100, "Выберите\nсценарий", canvas)
    
    # Варианты выбора
    draw_arrow(320, 420, 150, 520, canvas, "1 - RK2")
    draw_arrow(380, 470, 300, 520, canvas, "2 - Лин.")
    draw_arrow(520, 470, 600, 520, canvas, "3 - Sweep")
    draw_arrow(580, 420, 750, 520, canvas, "4 - GUI")
    draw_arrow(450, 470, 450, 520, canvas, "0 - Exit")
    
    # Варианты обработки
    draw_box(150, 560, 120, 40, "Расчет RK2", canvas)
    draw_box(300, 560, 120, 40, "Линеаризация", canvas)
    draw_box(600, 560, 120, 40, "Phase Sweep", canvas)
    draw_box(750, 560, 120, 40, "GUI Interface", canvas)
    draw_box(450, 560, 80, 40, "Выход", canvas)
    
    # Стрелки вниз к завершению
    for x in [150, 300, 450, 600, 750]:
        draw_arrow(x, 580, 450, 650, canvas)
    
    draw_box(450, 700, 150, 60, "Выполнить расчет\nили загрузить\nинтерфейс", canvas)
    draw_arrow(450, 730, 450, 800, canvas)
    
    draw_oval(450, 850, 150, 40, "Конец", canvas)
    
    root.mainloop()


if __name__ == "__main__":
    visualize_flowchart()
