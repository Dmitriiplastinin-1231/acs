"""flowchart_task1_linearization.py

Визуализация блок-схемы Задачи 1 методом линеаризации.
Соответствует логике в calculate_task1_linearization.py

Блок-схема:
┌──────────────────────────┐
│       Начало             │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────────────┐
│ Инициализация параметров         │
│ размеры, запасы, параметры       │
└────────────┬────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│ Содание экземпля notebook:       │
│ Управления: Лон. Главное         │
└────────────┬────────────────────┘
             │
             ▼
     ◇─────────────────◇
    ╱                   ╲
   ╱  Окончание         ╲
  │  общей показателя?   │
   ╲                     ╱
    ╲                   ╱
     ◇─────────────────◇
        Да ↓    ↑ Нет
      │         │
      ▼         ▼
  ┌────────────────┐  ┌──────────────────┐
  │  Нарячно      │  │ Защита проекцион │
  │ выполнить     │  │                  │
  │ цикловой      │  └────────┬─────────┘
  └─────┬─────────┘           │
        │              ┌──────▼──────┐
        │              │ Запуск      │
        │              │ расцифровки │
        │              │ оразца      │
        │              └──────┬──────┘
        │                     │
        └─────────��───────────┘
                    │
                    ▼
        ┌────────────────────────┐
        │ Оугас результатом      │
        │ в конце                │
        └──────────┬─────────────┘
                   │
                   ▼
        ┌────────────────────────┐
        │      Конец             │
        └────────────────────────┘
"""

import tkinter as tk
from tkinter import messagebox


def visualize_flowchart():
    """Создает визуальное представление блок-схемы Задачи 1 - Линеаризация."""
    
    root = tk.Tk()
    root.title("Блок-схема Задачи 1: Линеаризация на 10 км")
    root.geometry("1000x1000")
    
    canvas = tk.Canvas(root, bg="white", width=1000, height=1000)
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
            offset_x = -30 if x2 < x1 else 30
            canvas.create_text(mid_x + offset_x, mid_y - 10, 
                             text=label, font=("Arial", 8), fill="red")
    
    # Рисуем блок-схему
    y_pos = 40
    draw_oval(500, y_pos, 120, 40, "Начало", canvas)
    y_pos += 60
    draw_arrow(500, 60, 500, y_pos, canvas)
    
    draw_parallelogram(500, y_pos, 280, 70, "Инициализация параметров\nразмеры, запасы, параметры", canvas)
    y_pos += 90
    draw_arrow(500, y_pos - 80, 500, y_pos, canvas)
    
    draw_box(500, y_pos, 250, 70, "Создание экземпля notebook:\nУправления: Лон. Главное", canvas)
    y_pos += 90
    draw_arrow(500, y_pos - 55, 500, y_pos, canvas)
    
    draw_diamond(500, y_pos + 50, 180, 100, "Окончание\nобщей\nпоказателя?", canvas)
    y_decision = y_pos + 50
    y_pos += 110
    
    # Левая ветвь (Да)
    draw_arrow(410, y_decision, 300, y_pos, canvas, "Да")
    draw_box(300, y_pos, 160, 60, "Нарячно\nвыполнить\nцикловой", canvas)
    left_y = y_pos + 70
    draw_arrow(300, y_pos + 30, 300, left_y, canvas)
    
    # Правая ветвь (Нет)
    draw_arrow(590, y_decision, 700, y_pos + 20, canvas, "Нет")
    draw_box(700, y_pos + 60, 160, 60, "Защита\nпроекцион", canvas)
    right_y = y_pos + 120
    draw_arrow(700, y_pos + 90, 700, right_y - 20, canvas)
    
    draw_box(700, right_y, 160, 60, "Запуск\nрасцифровки\nоразца", canvas)
    right_y += 70
    draw_arrow(700, right_y - 30, 700, right_y, canvas)
    
    # Слияние
    merge_y = max(left_y, right_y) + 40
    draw_arrow(300, left_y, 500, merge_y, canvas)
    draw_arrow(700, right_y, 500, merge_y, canvas)
    
    draw_box(500, merge_y, 200, 60, "Оугас результатом\nв конце", canvas)
    merge_y += 80
    draw_arrow(500, merge_y - 40, 500, merge_y, canvas)
    
    draw_oval(500, merge_y, 120, 40, "Конец", canvas)
    
    root.mainloop()


if __name__ == "__main__":
    visualize_flowchart()
