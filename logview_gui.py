from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from logview_core import existing_logs, export_text, file_info, filter_lines, tail_lines


class LogViewApp:
    BG = "#0C1222"
    PANEL = "#151E33"
    PANEL_LIGHT = "#23304C"
    OUTPUT_BG = "#080D18"
    TEXT = "#F4F7FF"
    MUTED = "#B7C2D9"
    BORDER = "#344464"
    PURPLE = "#8B5CF6"
    PURPLE_HOVER = "#A78BFA"
    CYAN = "#22D3EE"
    CYAN_HOVER = "#67E8F9"
    PINK = "#F472B6"
    PINK_HOVER = "#F9A8D4"
    RED = "#FB7185"
    RED_HOVER = "#FDA4AF"

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("LogView — Linux Log Explorer")
        self.root.geometry("1080x700")
        self.root.minsize(900, 600)
        self.root.configure(bg=self.BG)
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        self.available_logs = existing_logs()
        self.selected_path = tk.StringVar()
        self.search_var = tk.StringVar()
        self.limit_var = tk.StringVar(value="200")
        self.status_var = tk.StringVar(value="Готово к работе")
        self.file_info_var = tk.StringVar(value="Выберите лог-файл")

        self._build_header()
        self._build_body()
        self._build_statusbar()
        self._populate_logs()

    def _build_header(self) -> None:
        header = tk.Frame(self.root, bg=self.PANEL, height=76)
        header.pack(fill="x")
        header.pack_propagate(False)

        title_box = tk.Frame(header, bg=self.PANEL)
        title_box.pack(side="left", padx=24, pady=14)

        tk.Label(
            title_box,
            text="LOGVIEW",
            bg=self.PANEL,
            fg=self.CYAN,
            font=("DejaVu Sans", 20, "bold"),
        ).pack(anchor="w")

        tk.Label(
            title_box,
            text="Linux Log Explorer",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("DejaVu Sans", 10),
        ).pack(anchor="w")

        self._button(
            header,
            text="✕",
            command=self.root.destroy,
            bg=self.RED,
            hover=self.RED_HOVER,
            fg="#3A0B15",
            width=3,
            font=("DejaVu Sans", 14, "bold"),
        ).pack(side="right", padx=20, pady=16)

    def _build_body(self) -> None:
        body = tk.Frame(self.root, bg=self.BG)
        body.pack(fill="both", expand=True, padx=18, pady=18)

        sidebar = tk.Frame(
            body,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
            width=300,
        )
        sidebar.pack(side="left", fill="y", padx=(0, 14))
        sidebar.pack_propagate(False)

        content = tk.Frame(
            body,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        content.pack(side="left", fill="both", expand=True)

        self._build_sidebar(sidebar)
        self._build_content(content)

    def _build_sidebar(self, parent: tk.Frame) -> None:
        tk.Label(
            parent,
            text="УПРАВЛЕНИЕ",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("DejaVu Sans", 13, "bold"),
        ).pack(anchor="w", padx=18, pady=(18, 12))

        self._small_label(parent, "Стандартный лог").pack(anchor="w", padx=18)
        self.log_combo = ttk.Combobox(
            parent,
            state="readonly",
            textvariable=self.selected_path,
            font=("DejaVu Sans", 10),
        )
        self.log_combo.pack(fill="x", padx=18, pady=(6, 13))
        self.log_combo.bind("<<ComboboxSelected>>", lambda _event: self.load_log())

        self._button(
            parent,
            "Открыть свой файл",
            self.choose_file,
            self.PURPLE,
            self.PURPLE_HOVER,
        ).pack(fill="x", padx=18, pady=(0, 16))

        self._small_label(parent, "Количество последних строк").pack(anchor="w", padx=18)
        tk.Entry(
            parent,
            textvariable=self.limit_var,
            bg=self.PANEL_LIGHT,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat",
            font=("DejaVu Sans", 11),
        ).pack(fill="x", padx=18, pady=(6, 13), ipady=7)

        self._small_label(parent, "Фильтр по тексту").pack(anchor="w", padx=18)
        search = tk.Entry(
            parent,
            textvariable=self.search_var,
            bg=self.PANEL_LIGHT,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat",
            font=("DejaVu Sans", 11),
        )
        search.pack(fill="x", padx=18, pady=(6, 13), ipady=7)
        search.bind("<Return>", lambda _event: self.load_log())

        self._button(
            parent,
            "Обновить",
            self.load_log,
            self.CYAN,
            self.CYAN_HOVER,
            fg="#07363D",
        ).pack(fill="x", padx=18, pady=6)

        self._button(
            parent,
            "Очистить поле",
            self.clear_output,
            self.PINK,
            self.PINK_HOVER,
            fg="#45142E",
        ).pack(fill="x", padx=18, pady=6)

        self._button(
            parent,
            "Сохранить результат",
            self.save_output,
            self.PURPLE,
            self.PURPLE_HOVER,
        ).pack(fill="x", padx=18, pady=6)

        self._button(
            parent,
            "Выход",
            self.root.destroy,
            self.RED,
            self.RED_HOVER,
            fg="#3A0B15",
        ).pack(fill="x", padx=18, pady=(6, 18))

    def _build_content(self, parent: tk.Frame) -> None:
        tk.Label(
            parent,
            text="Просмотр логов",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("DejaVu Sans", 16, "bold"),
        ).pack(anchor="w", padx=18, pady=(16, 2))

        tk.Label(
            parent,
            textvariable=self.file_info_var,
            bg=self.PANEL,
            fg=self.MUTED,
            font=("DejaVu Sans", 10),
        ).pack(anchor="w", padx=18, pady=(0, 12))

        output_wrap = tk.Frame(parent, bg=self.PANEL)
        output_wrap.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        scrollbar = tk.Scrollbar(output_wrap)
        scrollbar.pack(side="right", fill="y")

        self.output = tk.Text(
            output_wrap,
            bg=self.OUTPUT_BG,
            fg="#E3ECFF",
            insertbackground=self.TEXT,
            selectbackground=self.PURPLE,
            relief="flat",
            wrap="none",
            font=("DejaVu Sans Mono", 10),
            padx=12,
            pady=12,
            yscrollcommand=scrollbar.set,
        )
        self.output.pack(fill="both", expand=True)
        scrollbar.config(command=self.output.yview)

        self._set_output(
            "LogView готов к работе.\n\n"
            "Выберите стандартный лог слева или откройте собственный текстовый файл.\n"
            "После этого нажмите «Обновить».\n"
        )

    def _build_statusbar(self) -> None:
        tk.Label(
            self.root,
            textvariable=self.status_var,
            bg=self.PANEL_LIGHT,
            fg=self.MUTED,
            anchor="w",
            padx=14,
            pady=6,
            font=("DejaVu Sans", 9),
        ).pack(fill="x", side="bottom")

    def _populate_logs(self) -> None:
        values = [f"{title} — {path}" for path, title in self.available_logs]
        self.log_combo["values"] = values
        if values:
            self.log_combo.current(0)
            self.selected_path.set(values[0])
        else:
            self.selected_path.set("Стандартные логи не найдены")

    def _resolve_selected_path(self) -> Path | None:
        value = self.selected_path.get().strip()
        if " — " in value:
            return Path(value.rsplit(" — ", 1)[1])
        if value and value != "Стандартные логи не найдены":
            return Path(value)
        return None

    def choose_file(self) -> None:
        selected = filedialog.askopenfilename(
            title="Выберите лог-файл",
            initialdir="/var/log",
            filetypes=(("Текстовые файлы", "*.log *.txt"), ("Все файлы", "*.*")),
        )
        if selected:
            self.selected_path.set(selected)
            self.load_log()

    def load_log(self) -> None:
        path = self._resolve_selected_path()
        if path is None:
            messagebox.showinfo("LogView", "Выберите лог-файл.")
            return

        try:
            limit = int(self.limit_var.get().strip())
            lines = tail_lines(path, limit)
            visible_lines = filter_lines(lines, self.search_var.get())
            info = file_info(path)
        except ValueError as error:
            messagebox.showerror("Ошибка", str(error))
            return
        except PermissionError:
            messagebox.showerror(
                "Нет доступа",
                "Нет прав на чтение этого файла. Выберите другой файл.",
            )
            return
        except OSError as error:
            messagebox.showerror("Ошибка", str(error))
            return

        text = "".join(visible_lines) or "Подходящие строки не найдены.\n"
        self._set_output(text)
        self.file_info_var.set(
            f"{info['path']}  •  Размер: {info['size']}  •  Изменен: {info['modified']}"
        )
        self.status_var.set(f"Показано строк: {len(visible_lines)} из {len(lines)}")

    def clear_output(self) -> None:
        self._set_output("")
        self.status_var.set("Поле очищено")

    def save_output(self) -> None:
        current_text = self.output.get("1.0", "end-1c")
        if not current_text.strip():
            messagebox.showinfo("LogView", "Сначала выведите данные.")
            return

        selected = filedialog.asksaveasfilename(
            title="Сохранить результат",
            defaultextension=".txt",
            filetypes=(("Текстовый файл", "*.txt"),),
        )
        if selected:
            export_text(selected, current_text)
            self.status_var.set(f"Результат сохранен: {selected}")

    def _set_output(self, value: str) -> None:
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", value)
        self.output.config(state="disabled")

    def _small_label(self, parent: tk.Widget, text: str) -> tk.Label:
        return tk.Label(
            parent,
            text=text,
            bg=self.PANEL,
            fg=self.MUTED,
            font=("DejaVu Sans", 10),
        )

    def _button(
        self,
        parent: tk.Widget,
        text: str,
        command,
        bg: str,
        hover: str,
        fg: str = "#FFFFFF",
        width: int | None = None,
        font=("DejaVu Sans", 10, "bold"),
    ) -> tk.Button:
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=hover,
            activeforeground=fg,
            relief="flat",
            bd=0,
            padx=12,
            pady=9,
            cursor="hand2",
            font=font,
            width=width,
        )
        button.bind("<Enter>", lambda _event: button.config(bg=hover))
        button.bind("<Leave>", lambda _event: button.config(bg=bg))
        return button


def main() -> None:
    root = tk.Tk()
    LogViewApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
