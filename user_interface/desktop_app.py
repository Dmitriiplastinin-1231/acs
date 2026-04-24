"""desktop_app.py

Графический интерфейс проекта.

Интерфейс позволяет:
- запускать расчёты;
- строить графики;
- смотреть текстовый вывод;
- автоматически открывать соответствующий график после запуска.
"""

from __future__ import annotations

import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk

from PIL import Image, ImageTk


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class GraphTab(ttk.Frame):
    """Одна вкладка с одним графиком."""

    def __init__(self, master: ttk.Notebook, title: str, graph_path: Path) -> None:
        super().__init__(master)

        self.graph_path = graph_path
        self.original_image: Image.Image | None = None
        self.tk_image: ImageTk.PhotoImage | None = None

        self.canvas = tk.Canvas(self, background="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.info_label = ttk.Label(self, anchor="center")
        self.info_label.pack(fill="x", pady=(4, 4))

        if not graph_path.exists():
            self.canvas.create_text(
                20,
                20,
                anchor="nw",
                text="Файл графика не найден:\n" + str(graph_path),
                font=("Arial", 14),
            )
            self.info_label.configure(text="График не найден")
            return

        self.original_image = Image.open(graph_path)

        # График пересчитывается каждый раз, когда меняется размер области показа.
        self.canvas.bind("<Configure>", self.redraw_image)

        # Первый пересчёт делаем с задержкой, чтобы окно успело получить размер.
        self.after(300, self.redraw_image)

    def redraw_image(self, event: tk.Event | None = None) -> None:
        """Масштабирует изображение под текущий размер вкладки."""
        if self.original_image is None:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width < 200 or canvas_height < 200:
            self.after(200, self.redraw_image)
            return

        available_width = canvas_width - 30
        available_height = canvas_height - 30

        image_width, image_height = self.original_image.size

        scale = min(
            available_width / image_width,
            available_height / image_height,
        )

        # Не увеличиваем выше 100%, чтобы изображение не становилось размытым.
        scale = min(scale, 1.0)

        new_width = max(1, int(image_width * scale))
        new_height = max(1, int(image_height * scale))

        resized = self.original_image.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS,
        )

        self.tk_image = ImageTk.PhotoImage(resized)

        self.canvas.delete("all")

        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2

        self.canvas.create_image(x, y, anchor="nw", image=self.tk_image)

        self.info_label.configure(
            text=(
                f"Файл: {self.graph_path.name}    "
                f"Масштаб отображения: {scale * 100:.0f}%"
            )
        )


class GraphWindow(tk.Toplevel):
    """Отдельное окно для просмотра одного или нескольких графиков."""

    def __init__(self, master: tk.Tk, graph_files: list[tuple[str, Path]]) -> None:
        super().__init__(master)

        self.title("Графики результатов")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = int(screen_width * 0.96)
        window_height = int(screen_height * 0.92)

        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        try:
            self.attributes("-zoomed", True)
        except tk.TclError:
            pass

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        for title, graph_path in graph_files:
            tab = GraphTab(notebook, title, graph_path)
            notebook.add(tab, text=title)


class OffshoreLaunchApp(tk.Tk):
    """Основное окно запуска расчётов."""

    def __init__(self) -> None:
        super().__init__()

        self.title("Запуск алгоритмов")
        self.geometry("1050x720")

        self.parameters: dict[str, tk.StringVar] = {}

        self._build_interface()

    def _build_interface(self) -> None:
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill="both", expand=True)

        params_frame = ttk.LabelFrame(main_frame, text="Параметры модели", padding=10)
        params_frame.pack(fill="x")

        default_values = {
            "A": "0.03490658503988659",
            "T": "8.0",
            "tau": "0.3",
            "a": "0.05",
            "dt": "0.01",
            "az": "10.0",
            "phi0": "0.0",
            "theta0_deg": "2.0",
            "n_small": "8",
            "n_large": "72",
        }

        labels = {
            "A": "A — амплитуда качки, рад",
            "T": "T — период качки, с",
            "tau": "tau — задержка управления, с",
            "a": "a — коэффициент управления",
            "dt": "dt — шаг интегрирования, с",
            "az": "az — вертикальное ускорение, м/с²",
            "phi0": "phi0 — фаза старта, рад",
            "theta0_deg": "theta0_deg — начальный наклон для задачи 1, град",
            "n_small": "n_small — основная сетка",
            "n_large": "n_large — контрольная сетка",
        }

        for index, key in enumerate(default_values):
            row = index // 3
            col = (index % 3) * 2

            ttk.Label(params_frame, text=labels[key]).grid(
                row=row,
                column=col,
                sticky="w",
                padx=5,
                pady=5,
            )

            variable = tk.StringVar(value=default_values[key])
            self.parameters[key] = variable

            ttk.Entry(params_frame, textvariable=variable, width=18).grid(
                row=row,
                column=col + 1,
                sticky="w",
                padx=5,
                pady=5,
            )

        buttons_frame = ttk.LabelFrame(main_frame, text="Запуск", padding=10)
        buttons_frame.pack(fill="x", pady=10)

        ttk.Button(
            buttons_frame,
            text="Задача 1: линеаризация",
            command=self.run_task1_linearization,
        ).grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        ttk.Button(
            buttons_frame,
            text="Задача 1: RK2",
            command=self.run_task1_rk2,
        ).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(
            buttons_frame,
            text="Задача 2: sweep",
            command=self.run_task2_sweep,
        ).grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        ttk.Button(
            buttons_frame,
            text="График задачи 1",
            command=self.plot_task1_comparison,
        ).grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        ttk.Button(
            buttons_frame,
            text="График sweep",
            command=self.plot_task2_phase_sweep,
        ).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(
            buttons_frame,
            text="Сравнение N=8 и N=72",
            command=self.plot_task2_grid_comparison,
        ).grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        ttk.Button(
            buttons_frame,
            text="Запустить всё",
            command=self.run_all,
        ).grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        ttk.Button(
            buttons_frame,
            text="Открыть все графики",
            command=self.open_all_graphs,
        ).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(
            buttons_frame,
            text="Очистить логи",
            command=self.clear_logs,
        ).grid(row=2, column=2, padx=5, pady=5, sticky="ew")

        for i in range(3):
            buttons_frame.columnconfigure(i, weight=1)

        logs_frame = ttk.LabelFrame(main_frame, text="Логи выполнения", padding=10)
        logs_frame.pack(fill="both", expand=True)

        self.log_text = tk.Text(logs_frame, height=18, wrap="word")
        self.log_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(logs_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=scrollbar.set)

    def common_args(self) -> list[str]:
        return [
            "--A", self.parameters["A"].get(),
            "--T", self.parameters["T"].get(),
            "--tau", self.parameters["tau"].get(),
            "--a", self.parameters["a"].get(),
            "--dt", self.parameters["dt"].get(),
            "--az", self.parameters["az"].get(),
        ]

    def log(self, text: str) -> None:
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")
        self.update_idletasks()

    def clear_logs(self) -> None:
        self.log_text.delete("1.0", "end")

    def run_command(self, command: list[str]) -> bool:
        self.log(f"\n$ {' '.join(command)}")

        try:
            result = subprocess.run(
                command,
                cwd=PROJECT_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
        except Exception as exc:
            self.log(f"Ошибка запуска: {exc}")
            return False

        if result.stdout:
            self.log(result.stdout.rstrip())

        if result.stderr:
            self.log("Ошибки / предупреждения:")
            self.log(result.stderr.rstrip())

        if result.returncode != 0:
            self.log(f"Команда завершилась с ошибкой: код {result.returncode}")
            return False

        self.log("Готово.")
        return True

    def run_task1_linearization(self, show_graph: bool = True) -> None:
        ok = self.run_command([
            sys.executable,
            "-m",
            "calculation_scenarios.calculate_task1_linearization",
            *self.common_args(),
            "--phi0",
            self.parameters["phi0"].get(),
            "--theta0-deg",
            self.parameters["theta0_deg"].get(),
        ])

        if ok and show_graph:
            if self.build_task1_graph():
                self.open_task1_graph()

    def run_task1_rk2(self, show_graph: bool = True) -> None:
        ok = self.run_command([
            sys.executable,
            "-m",
            "calculation_scenarios.calculate_task1_rk2",
            *self.common_args(),
            "--phi0",
            self.parameters["phi0"].get(),
            "--theta0-deg",
            self.parameters["theta0_deg"].get(),
        ])

        if ok and show_graph:
            if self.build_task1_graph():
                self.open_task1_graph()

    def run_task2_sweep(self, show_graph: bool = True) -> None:
        ok = self.run_command([
            sys.executable,
            "-m",
            "calculation_scenarios.calculate_task2_phase_sweep",
            *self.common_args(),
            "--n-small",
            self.parameters["n_small"].get(),
            "--n-large",
            self.parameters["n_large"].get(),
        ])

        if ok and show_graph:
            phase_ok = self.build_task2_phase_sweep_graph()
            grid_ok = self.build_task2_grid_comparison_graph()

            if phase_ok or grid_ok:
                self.open_task2_graphs()

    def build_task1_graph(self) -> bool:
        return self.run_command([
            sys.executable,
            "graph_scripts/plot_task1_comparison.py",
            "--theta0-deg",
            self.parameters["theta0_deg"].get(),
        ])

    def build_task2_phase_sweep_graph(self) -> bool:
        return self.run_command([
            sys.executable,
            "graph_scripts/plot_task2_phase_sweep.py",
        ])

    def build_task2_grid_comparison_graph(self) -> bool:
        return self.run_command([
            sys.executable,
            "graph_scripts/plot_task2_grid_comparison.py",
        ])

    def plot_task1_comparison(self) -> None:
        if self.build_task1_graph():
            self.open_task1_graph()

    def plot_task2_phase_sweep(self) -> None:
        if self.build_task2_phase_sweep_graph():
            self.open_phase_sweep_graph()

    def plot_task2_grid_comparison(self) -> None:
        if self.build_task2_grid_comparison_graph():
            self.open_grid_comparison_graph()

    def run_all(self) -> None:
        self.run_task1_linearization(show_graph=False)
        self.run_task1_rk2(show_graph=False)
        self.run_task2_sweep(show_graph=False)

        self.build_task1_graph()
        self.build_task2_phase_sweep_graph()
        self.build_task2_grid_comparison_graph()

        self.open_all_graphs()

    def open_graphs(self, graph_files: list[tuple[str, Path]]) -> None:
        GraphWindow(self, graph_files)

    def open_task1_graph(self) -> None:
        self.open_graphs([
            (
                "Задача 1",
                PROJECT_ROOT / "calculation_results/figures/task1_linearization_vs_rk2.png",
            )
        ])

    def open_phase_sweep_graph(self) -> None:
        self.open_graphs([
            (
                "Задача 2: sweep",
                PROJECT_ROOT / "calculation_results/figures/task2_phase_sweep.png",
            )
        ])

    def open_grid_comparison_graph(self) -> None:
        self.open_graphs([
            (
                "Сравнение N=8 и N=72",
                PROJECT_ROOT / "calculation_results/figures/task2_grid_comparison.png",
            )
        ])

    def open_task2_graphs(self) -> None:
        self.open_graphs([
            (
                "Задача 2: sweep",
                PROJECT_ROOT / "calculation_results/figures/task2_phase_sweep.png",
            ),
            (
                "Сравнение N=8 и N=72",
                PROJECT_ROOT / "calculation_results/figures/task2_grid_comparison.png",
            ),
        ])

    def open_all_graphs(self) -> None:
        self.open_graphs([
            (
                "Задача 1",
                PROJECT_ROOT / "calculation_results/figures/task1_linearization_vs_rk2.png",
            ),
            (
                "Задача 2: sweep",
                PROJECT_ROOT / "calculation_results/figures/task2_phase_sweep.png",
            ),
            (
                "Сравнение N=8 и N=72",
                PROJECT_ROOT / "calculation_results/figures/task2_grid_comparison.png",
            ),
        ])


def main() -> None:
    app = OffshoreLaunchApp()
    app.mainloop()


if __name__ == "__main__":
    main()
