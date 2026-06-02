"""flowchart_task2_sweep.py

Визуализация блок-схемы Задачи 2 с фазовой разверткой.
Соответствует логике в calculate_task2_phase_sweep.py

Блок-схема:
┌──────────────────────────┐
│       Начало             │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────────────────┐
│ Ввод параметров                      │
│ н±10м, углы и интеграция             │
└────────────┬─────────────────────────┘
             │
             ▼
         ◇────────◇
        ╱          ╲
       ╱  Задача по ╲
      │  углу найти?  │
       ╲             ╱
        ╲           ╱
         ◇────────◇
        ╱ Да │ Нет ╲
       │     │       │
       ▼     ▼       ▼
     [Да] [Нет]   [Ошибка]
       │     │       │
       └─────┴───────┘
             │
             ▼
     ◇─────────────◇
    ╱               ╲
   ╱ Вышина РукОВ   ╲
  │  с.кг эв 10 км?  │
   ╲                 ╱
    ╲               ╱
     ◇─────────────◇
    ╱ Да    │    Нет ╲
   │        │         │
   ▼        ▼         ▼
 
 [Расчет Рунга-Кутты 2]  [Сохранение в CSV]
        │                        │
        │                        ▼
        │          ┌──────────────────────┐
        │          │ Расчет администрации │
        │          │ для кривой           │
        │          └──────────┬───────────┘
        │                     │
        └─────────────────────┘
                    │
                    ▼
        ┌────────────────────────┐
        │ Вывод итогового        │
        │ отчета обновления      │
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
    """Создает визуальное представление блок-схемы Задачи 2."""
    
    root = tk.Tk()
    root.title("Блок-схема Задачи 2: Фазовая развертка + RK2")
    root.geometry("1000x1200")
    
    # Создаем холст для рисования
    canvas = tk.Canvas(root, bg="white", width=1000, height=1200)
    canvas.pack(fill="both", expand=True)
    
    # Функции для рисования элементов блок-схемы
    def draw_box(x, y, width, height, text, canvas):
        """Рисует прямоугольник (процесс)."""
        canvas.create_rectangle(
            x - width/2, y - height/2,
            x + width/2, y + height/2,
            outline="black", width=2
        )
        canvas.create_text(x, y, text=text, font=("Arial", 9), justify="center")
    
    def draw_diamond(x, y, width, height, text, canvas):
        """Рисует ромб (решение)."""
        points = [
            x, y - height/2,  # вершина
            x + width/2, y,   # правая точка
            x, y + height/2,  # нижняя точка
            x - width/2, y    # левая точка
        ]
        canvas.create_polygon(points, outline="black", width=2, fill="lightblue")
        canvas.create_text(x, y, text=text, font=("Arial", 9), justify="center")
    
    def draw_oval(x, y, width, height, text, canvas):
        """Рисует овал (начало/конец)."""
        canvas.create_oval(
            x - width/2, y - height/2,
            x + width/2, y + height/2,
            outline="black", width=2
        )
        canvas.create_text(x, y, text=text, font=("Arial", 9), justify="center")
    
    def draw_parallelogram(x, y, width, height, text, canvas):
        """Рисует параллелограмм (ввод/вывод)."""
        offset = 20
        points = [
            x - width/2 + offset, y - height/2,
            x + width/2 + offset, y - height/2,
            x + width/2 - offset, y + height/2,
            x - width/2 - offset, y + height/2
        ]
        canvas.create_polygon(points, outline="black", width=2, fill="lightyellow")
        canvas.create_text(x, y, text=text, font=("Arial", 9), justify="center")
    
    def draw_arrow(x1, y1, x2, y2, canvas, label=""):
        """Рисует стрелку."""
        canvas.create_line(x1, y1, x2, y2, arrow="last", width=2)
        if label:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            canvas.create_text(mid_x + 20, mid_y, text=label, font=("Arial", 8), fill="red")
    
    # Рисуем блок-схему
    y_pos = 50
    draw_oval(500, y_pos, 120, 40, "Начало", canvas)
    y_pos += 60
    draw_arrow(500, 50 + 20, 500, y_pos - 20, canvas)
    
    draw_parallelogram(500, y_pos, 280, 60, "Ввод параметров\nн±10м, углы и интеграция", canvas)
    y_pos += 80
    draw_arrow(500, y_pos - 60, 500, y_pos - 20, canvas)
    
    draw_diamond(500, y_pos, 180, 100, "Задача по\nуглу найти?", canvas)
    y_pos_decision = y_pos
    y_pos += 110
    
    # Да - влево
    draw_arrow(410, y_pos_decision, 300, y_pos, canvas, "Да")
    # Нет - вправо
    draw_arrow(590, y_pos_decision, 700, y_pos, canvas, "Нет")
    
    # Левая ветвь (Да)
    draw_box(300, y_pos, 140, 50, "Использовано\nзаданное\nугдов", canvas)
    left_y = y_pos + 70
    draw_arrow(300, y_pos + 25, 300, left_y, canvas)
    
    draw_diamond(300, left_y + 60, 160, 100, "Вышина\nс.кг эв\n10 км?", canvas)
    left_y_decision = left_y + 60
    left_y += 130
    
    # Да - вверх (слияние)
    draw_arrow(240, left_y_decision, 200, left_y, canvas, "Да")
    draw_box(200, left_y, 140, 50, "Шаг Рунга-Кутты 2\nне перено", canvas)
    
    # Нет - вниз
    draw_arrow(300, left_y_decision + 50, 300, left_y + 50, canvas, "Нет")
    left_y = left_y + 100
    draw_box(300, left_y, 160, 50, "Сохранение истории\nполугемы", canvas)
    
    # Правая ветвь (Нет)
    right_y = y_pos
    draw_box(700, right_y, 140, 50, "Получение\nпараграф\nи теория", canvas)
    right_y += 70
    draw_arrow(700, y_pos + 25, 700, right_y - 20, canvas)
    
    draw_diamond(700, right_y + 50, 160, 100, "Вышина\nс.кг эв\n10 км?", canvas)
    right_y_decision = right_y + 50
    right_y += 120
    
    # Да
    draw_arrow(760, right_y_decision, 800, right_y, canvas, "Да")
    draw_box(800, right_y, 140, 50, "Шаг Рунга-Кутты 2\nперено Фаза", canvas)
    
    # Нет
    draw_arrow(700, right_y_decision + 50, 700, right_y + 50, canvas, "Нет")
    right_y = right_y + 100
    draw_parallelogram(700, right_y, 180, 50, "Сохранение\nвыходных", canvas)
    
    # Слияние потоков
    merge_y = max(left_y, right_y) + 70
    draw_arrow(200, left_y + 25, 500, merge_y - 40, canvas)
    draw_arrow(300, left_y + 25, 500, merge_y - 40, canvas)
    draw_arrow(800, right_y, 500, merge_y - 40, canvas)
    draw_arrow(700, right_y + 25, 500, merge_y - 40, canvas)
    
    draw_box(500, merge_y, 200, 60, "Расчет администрации\nдля кривой", canvas)
    merge_y += 80
    draw_arrow(500, merge_y - 40, 500, merge_y, canvas)
    
    draw_parallelogram(500, merge_y, 220, 60, "Вывод итогового\nотчета обновления", canvas)
    merge_y += 90
    draw_arrow(500, merge_y - 30, 500, merge_y, canvas)
    
    draw_oval(500, merge_y, 120, 40, "Конец", canvas)
    
    root.mainloop()


if __name__ == "__main__":
    visualize_flowchart()
