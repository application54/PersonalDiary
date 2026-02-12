# Главный модуль приложения

import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk
from src.gui import DiaryGUI
from src.config import APP_NAME, DB_NAME

def create_password_window(title=APP_NAME, is_first_run=False):
    """Создание окна ввода/создания мастер-пароля."""
    window = tk.Tk()
    window.title(title)
    window.geometry("400x250")
    window.resizable(False, False)

    # Центрирование окна
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'400x250+{x}+{y}')

    result = {"password": None}
    main_frame = ttk.Frame(window, padding="20")
    main_frame.pack(fill='both', expand=True)

    if is_first_run:
        ttk.Label(main_frame, text="Создание мастер-пароля:",
                  font=('Arial', 12, 'bold')).pack(pady=(0, 15))
    else:
        ttk.Label(main_frame, text="Введите мастер-пароль:",
                  font=('Arial', 12, 'bold')).pack(pady=(0, 15))

    ttk.Label(main_frame, text="Пароль:").pack(anchor='w')
    password_var = tk.StringVar()
    password_entry = ttk.Entry(main_frame, textvariable=password_var,
                               show='*', width=30)
    password_entry.pack(fill='x', pady=5)
    password_entry.focus()

    if is_first_run:
        ttk.Label(main_frame, text="Подтверждение пароля:").pack(anchor='w', pady=(10, 0))
        confirm_var = tk.StringVar()
        confirm_entry = ttk.Entry(main_frame, textvariable=confirm_var,
                                  show='*', width=30)
        confirm_entry.pack(fill='x', pady=5)

    def on_ok():
        password = password_var.get().strip()
        if not password:
            messagebox.showwarning("Ошибка", "Пароль не может быть пустым!")
            return
        if is_first_run:
            confirm = confirm_var.get().strip()
            if password != confirm:
                messagebox.showerror("Ошибка", "Пароли не совпадают!")
                return
        result["password"] = password
        window.destroy()

    def on_cancel():
        window.destroy()

    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=20)
    ttk.Button(button_frame, text="OK", width=10, command=on_ok).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Отмена", width=10, command=on_cancel).pack(side='left', padx=5)

    window.bind('<Return>', lambda e: on_ok())
    window.bind('<Escape>', lambda e: on_cancel())
    window.mainloop()

    return result["password"]

def main():
    """Главная функция приложения."""
    db_exists = os.path.exists(DB_NAME)

    if not db_exists:
        master_password = create_password_window(
            f"{APP_NAME} - Первый запуск",
            is_first_run=True
        )
        if not master_password:
            sys.exit(0)
        messagebox.showinfo(
            "Добро пожаловать",
            f"{APP_NAME} готов к использованию!\n\n"
            "Мастер-пароль установлен.\n"
            "Запомните его! Без него вы не сможете восстановить данные."
        )
    else:
        master_password = create_password_window(
            f"{APP_NAME} - Вход",
            is_first_run=False
        )
        if not master_password:
            sys.exit(0)

    root = tk.Tk()
    root.title(APP_NAME)
    root.geometry("900x650")

    try:
        app = DiaryGUI(root, master_password)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить приложение:\n{str(e)}")
        sys.exit(1)

    root.mainloop()

if __name__ == "__main__":
    main()