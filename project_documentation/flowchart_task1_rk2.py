"""flowchart_task1_rk2.py

Визуализация блок-схемы Задачи 1 методом Рунга-Кутты второго порядка (RK2).
Соответствует логике в calculate_task1_rk2.py

Блок-схема:
┌──────────────────────────┐
│       Начало             │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────────────┐
│ Инициализация параметров         │
│ размеры, запасы, начальные       │
└────────────┬────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│ Создание экземпля notebook:      │
│ Управление: Лон. Главное         │
└────────────┬────────────────────┘
             │
             ▼
     ◇─────────────────◇
    ╱                   ╲
   ╱  Расстояние        ╲
  │  расчета < 10 км?    │
   ╲                     ╱
    ╲                   ╱
     ◇─────────────────◇
        Да ↓    ↑ Нет
      │         │
      ▼         ▼
  ┌──────────────────────┐  ┌──────────────────┐
  │  Применить метод     │  │ Сохранение       │
  │  RK2 (Heun)          │  │ промежуточных    │
  │  на шаге 0.1         │  │ результатов      │
  └─────┬────────────────┘  └────────┬─────────┘
        │                           │
        └───────────────┬───────────┘
                        │
                        ▼
         ┌──────────────────────────┐
         │ Запись результатов       │
         │ обобщенные угды          │
         └──────────┬───────────────┘
                    │
                    ▼
         ┌──────────────────────────┐
         │ Вывод результатов        │
         │ на экран/файл            │
         └──────────┬───────────────┘
                    │
                    ▼
         ┌──────────────────────────┐
         │      Конец               │
         └──────────────────────────┘
"""

import tkinter as tk
from tkinter import messagebox


def visualize_flowchart():
    """Создает визуальное представление блок-схемы Задачи 1 - RK2."""
    
    root = tk.Tk()
    root.title("Блок-схема Задачи 1: RK2 (Heun) на 10 км")
    root.geometry("1000x1100")
    
    canvas = tk.Canvas(root, bg="white", width=1000, height=1100)
    canvas.pack(fill="both", expand=True)
    
    def draw_box(x, y, width, height, text, canvas):
        canvas.create_rectangle(
            x - width/2, y - height/2,
            x + width/2, y + height/2,
            outline="black", width=2
        )
        lines = text.split('\n')
        line_height = 12
        total_height = len(lines) * line_height
        start_y = y - total_height / 2
        for i, line in enumerate(lines):
            canvas.create_text(x, start_y + i * line_height + line_height/2, 
                             text=line, font=("Arial", 9), justify="center")
    
    def draw_diamond(x, y, width, height, text, canvas):
        points = [
            x, y - height/2,
            x + width/2, y,
            x, y + height/2,
            x - width/2, y
        ]
        canvas.create_polygon(points, outline="black", width=2, fill="lightblue")
        lines = text.split('\n')
        line_height = 11
        total_height = len(lines) * line_height
        start_y = y - total_height / 2
        for i, line in enumerate(lines):
            canvas.create_text(x, start_y + i * line_height + line_height/2, 
                             text=line, font=("Arial", 8), justify="center")
    
    def draw_oval(x, y, width, height, text, canvas):
        canvas.create_oval(
            x - width/2, y - height/2,
            x + width/2, y + height/2,
            outline="black", width=2
        )
        canvas.create_text(x, y, text=text, font=("Arial", 9), justify="center")
    
    def draw_parallelogram(x, y, width, height, text, canvas):
        offset = 20
        points = [
            x - width/2 + offset, y - height/2,
            x + width/2 + offset, y - height/2,
            x + width/2 - offset, y + height/2,
            x - width/2 - offset, y + height/2
        ]
        canvas.create_polygon(points, outline="black", width=2, fill="lightyellow")
        lines = text.split('\n')
        line_height = 11
        total_height = len(lines) * line_height
        start_y = y - total_height / 2
        for i, line in enumerate(lines):
            canvas.create_text(x, start_y + i * line_height + line_height/2, 
                             text=line, font=("Arial", 9), justify="center")
    
    def draw_arrow(x1, y1, x2, y2, canvas, label=""):
        canvas.create_line(x1, y1, x2, y2, arrow="last", width=2)
        if label:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            offset_x = -35 if x2 < x1 else 35
            canvas.create_text(mid_x + offset_x, mid_y - 10, 
                             text=label, font=("Arial", 8), fill="red")
    
    # Рисуем блок-схему
    y_pos = 40
    draw_oval(500, y_pos, 120, 40, "Начало", canvas)
    y_pos += 60
    draw_arrow(500, 60, 500, y_pos, canvas)
    
    draw_parallelogram(500, y_pos, 280, 70, "Инициализация параметров\nразмеры, запасы, начальные", canvas)
    y_pos += 90
    draw_arrow(500, y_pos - 80, 500, y_pos, canvas)
    
    draw_box(500, y_pos, 250, 70, "Создание экземпля notebook:\nУправление: Лон. Главное", canvas)
    y_pos += 90
    draw_arrow(500, y_pos - 55, 500, y_pos, canvas)
    
    draw_diamond(500, y_pos + 50, 180, 100, "Расстояние\nрасчета\n< 10 км?", canvas)
    y_decision = y_pos + 50
    y_pos += 110
    
    # Левая ветвь (Да)
    draw_arrow(410, y_decision, 300, y_pos, canvas, "Да")
    draw_box(300, y_pos, 200, 80, "Применить метод\nRK2 (Heun)\nна шаге 0.1", canvas)
    left_y = y_pos + 70
    draw_arrow(300, y_pos + 40, 300, left_y, canvas)
    
    # Правая ветвь (Нет)
    draw_arrow(590, y_decision, 700, y_pos + 20, canvas, "Нет")
    draw_parallelogram(700, y_pos + 60, 200, 70, "Сохранение\nпромежуточных\nрезультатов", canvas)
    right_y = y_pos + 120
    draw_arrow(700, y_pos + 95, 700, right_y, canvas)
    
    # Слияние
    merge_y = max(left_y, right_y) + 50
    draw_arrow(300, left_y, 500, merge_y - 40, canvas)
    draw_arrow(700, right_y, 500, merge_y - 40, canvas)
    
    draw_box(500, merge_y, 220, 70, "Запись результатов\nобобщенные углы", canvas)
    merge_y += 90
    draw_arrow(500, merge_y - 45, 500, merge_y, canvas)
    
    draw_parallelogram(500, merge_y, 240, 70, "Вывод результатов\nна экран/файл", canvas)
    merge_y += 90
    draw_arrow(500, merge_y - 35, 500, merge_y, canvas)
    
    draw_oval(500, merge_y, 120, 40, "Конец", canvas)
    
    root.mainloop()


if __name__ == "__main__":
    visualize_flowchart()
