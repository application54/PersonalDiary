# Модуль графического интерфейса личного дневника

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.database import DatabaseManager
from src.config import APP_NAME

class DiaryGUI:
    """Класс графического интерфейса личного дневника."""

    def __init__(self, root, master_password):
        self.root = root
        self.master_password = master_password
        self.db = DatabaseManager()
        self.root.title(APP_NAME)
        self.root.geometry("900x650")
        self.create_widgets()
        self.refresh_entries()

    def create_widgets(self):
        """Создание всех виджетов интерфейса."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Вкладка "Все записи"
        self.tab_all = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_all, text='Все записи')
        self.create_all_tab()

        # Вкладка "Добавить запись"
        self.tab_add = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_add, text='Добавить запись')
        self.create_add_tab()

        # Вкладка "Поиск"
        self.tab_search = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_search, text='Поиск')
        self.create_search_tab()

    def create_all_tab(self):
        """Вкладка отображения всех записей."""
        # Панель управления
        control_frame = ttk.Frame(self.tab_all)
        control_frame.pack(fill='x', padx=5, pady=5)

        ttk.Button(control_frame, text='Обновить',
                   command=self.refresh_entries).pack(side='left', padx=5)

        ttk.Label(control_frame, text='Поиск:').pack(side='left', padx=(10, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', lambda *args: self.filter_entries())
        ttk.Entry(control_frame, textvariable=self.search_var, width=30).pack(side='left', padx=5)

        # Таблица записей
        columns = ('ID', 'Дата', 'Заголовок')
        tree_frame = ttk.Frame(self.tab_all)
        tree_frame.pack(fill='both', expand=True, padx=5, pady=5)

        v_scroll = ttk.Scrollbar(tree_frame)
        v_scroll.pack(side='right', fill='y')

        h_scroll = ttk.Scrollbar(tree_frame, orient='horizontal')
        h_scroll.pack(side='bottom', fill='x')

        self.tree = ttk.Treeview(tree_frame, columns=columns,
                                 show='headings', height=20,
                                 yscrollcommand=v_scroll.set,
                                 xscrollcommand=h_scroll.set)
        self.tree.pack(side='left', fill='both', expand=True)

        v_scroll.config(command=self.tree.yview)
        h_scroll.config(command=self.tree.xview)

        # Настройка колонок
        self.tree.heading('ID', text='ID')
        self.tree.heading('Дата', text='Дата')
        self.tree.heading('Заголовок', text='Заголовок')
        self.tree.column('ID', width=50, minwidth=30)
        self.tree.column('Дата', width=100, minwidth=80)
        self.tree.column('Заголовок', width=200, minwidth=150)

        # Двойной клик - открыть запись
        self.tree.bind('<Double-1>', lambda e: self.open_entry())

        # Панель действий
        action_frame = ttk.Frame(self.tab_all)
        action_frame.pack(fill='x', padx=5, pady=5)

        ttk.Button(action_frame, text='Открыть',
                   command=self.open_entry).pack(side='left', padx=5)
        ttk.Button(action_frame, text='Редактировать',
                   command=self.edit_entry).pack(side='left', padx=5)
        ttk.Button(action_frame, text='Удалить',
                   command=self.delete_entry).pack(side='left', padx=5)

    def create_add_tab(self):
        """Вкладка добавления новой записи."""
        form_frame = ttk.Frame(self.tab_add)
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Дата
        ttk.Label(form_frame, text='Дата:*').grid(row=0, column=0, sticky='w', pady=10)
        self.entry_date = ttk.Entry(form_frame, width=20)
        self.entry_date.grid(row=0, column=1, pady=10, padx=10, sticky='w')
        self.entry_date.insert(0, datetime.now().strftime('%Y-%m-%d'))

        # Заголовок
        ttk.Label(form_frame, text='Заголовок:*').grid(row=1, column=0, sticky='w', pady=10)
        self.entry_title = ttk.Entry(form_frame, width=50)
        self.entry_title.grid(row=1, column=1, pady=10, padx=10, sticky='w')

        # Содержимое
        ttk.Label(form_frame, text='Содержимое:*').grid(row=2, column=0, sticky='nw', pady=10)
        self.text_content = tk.Text(form_frame, width=60, height=15)
        self.text_content.grid(row=2, column=1, pady=10, padx=10, sticky='w')

        # Кнопки
        button_frame = ttk.Frame(self.tab_add)
        button_frame.pack(fill='x', padx=20, pady=10)

        ttk.Button(button_frame, text='Сохранить',
                   command=self.save_entry).pack(side='left', padx=5)
        ttk.Button(button_frame, text='Очистить',
                   command=self.clear_form).pack(side='left', padx=5)

    def create_search_tab(self):
        """Вкладка расширенного поиска."""
        # Панель параметров поиска
        search_frame = ttk.LabelFrame(self.tab_search, text='Параметры поиска', padding=10)
        search_frame.pack(fill='x', padx=10, pady=10)

        ttk.Label(search_frame, text='Ключевое слово:').grid(row=0, column=0, sticky='w', pady=5)
        self.search_keyword = ttk.Entry(search_frame, width=40)
        self.search_keyword.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        ttk.Label(search_frame, text='Дата с:').grid(row=1, column=0, sticky='w', pady=5)
        self.search_date_from = ttk.Entry(search_frame, width=15)
        self.search_date_from.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        self.search_date_from.insert(0, 'ГГГГ-ММ-ДД')

        ttk.Label(search_frame, text='Дата по:').grid(row=2, column=0, sticky='w', pady=5)
        self.search_date_to = ttk.Entry(search_frame, width=15)
        self.search_date_to.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        self.search_date_to.insert(0, 'ГГГГ-ММ-ДД')

        ttk.Button(search_frame, text='Найти',
                   command=self.perform_search).grid(row=3, column=1, pady=10, sticky='w')

        # Результаты поиска
        result_frame = ttk.LabelFrame(self.tab_search, text='Результаты', padding=10)
        result_frame.pack(fill='both', expand=True, padx=10, pady=10)

        columns = ('ID', 'Дата', 'Заголовок')
        self.search_tree = ttk.Treeview(result_frame, columns=columns,
                                        show='headings', height=15)
        self.search_tree.pack(fill='both', expand=True)

        self.search_tree.heading('ID', text='ID')
        self.search_tree.heading('Дата', text='Дата')
        self.search_tree.heading('Заголовок', text='Заголовок')
        self.search_tree.column('ID', width=50)
        self.search_tree.column('Дата', width=100)
        self.search_tree.column('Заголовок', width=200)

        self.search_tree.bind('<Double-1>', lambda e: self.open_entry_from_search())

    def refresh_entries(self):
        """Обновление списка записей на вкладке 'Все записи'."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.entries = self.db.get_all_entries(self.master_password)
        for entry in self.entries:
            self.tree.insert('', 'end', values=(
                entry['id'],
                entry['date'],
                entry['title']
            ))

    def filter_entries(self):
        """Фильтрация записей по ключевому слову (по заголовку и дате)."""
        keyword = self.search_var.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)

        for entry in self.entries:
            if keyword in entry['title'].lower() or keyword in entry['date']:
                self.tree.insert('', 'end', values=(
                    entry['id'],
                    entry['date'],
                    entry['title']
                ))

    def open_entry(self):
        """Открыть выбранную запись для просмотра."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Ошибка', 'Выберите запись для просмотра')
            return

        item = self.tree.item(selected[0])
        entry_id = item['values'][0]

        # Найти запись в полном списке
        entry = next((e for e in self.entries if e['id'] == entry_id), None)
        if not entry:
            messagebox.showerror('Ошибка', 'Запись не найдена')
            return

        self.show_entry_window(entry)

    def open_entry_from_search(self):
        """Открыть запись из результатов поиска."""
        selected = self.search_tree.selection()
        if not selected:
            return
        item = self.search_tree.item(selected[0])
        entry_id = item['values'][0]
        entry = next((e for e in self.entries if e['id'] == entry_id), None)
        if entry:
            self.show_entry_window(entry)

    def show_entry_window(self, entry):
        """Отображение окна с полным содержимым записи и возможностью редактирования."""
        win = tk.Toplevel(self.root)
        win.title(f"Запись от {entry['date']}")
        win.geometry("600x500")
        win.resizable(True, True)

        main_frame = ttk.Frame(win, padding=10)
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text=f"Дата: {entry['date']}",
                  font=('Arial', 10, 'bold')).pack(anchor='w', pady=5)
        ttk.Label(main_frame, text=f"Заголовок: {entry['title']}",
                  font=('Arial', 10, 'bold')).pack(anchor='w', pady=5)

        ttk.Label(main_frame, text="Содержимое:").pack(anchor='w', pady=(10, 5))

        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill='both', expand=True)

        v_scroll = ttk.Scrollbar(text_frame)
        v_scroll.pack(side='right', fill='y')

        text = tk.Text(text_frame, wrap='word', yscrollcommand=v_scroll.set)
        text.pack(side='left', fill='both', expand=True)
        v_scroll.config(command=text.yview)

        text.insert('1.0', entry['content'])
        text.config(state='disabled')

        # Кнопки
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=10)

        ttk.Button(btn_frame, text='Редактировать',
                   command=lambda: self.edit_entry_window(entry, win)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Закрыть',
                   command=win.destroy).pack(side='right', padx=5)

    def edit_entry_window(self, entry, parent_win=None):
        """Окно редактирования записи."""
        if parent_win:
            parent_win.destroy()

        win = tk.Toplevel(self.root)
        win.title("Редактирование записи")
        win.geometry("600x500")
        win.resizable(True, True)

        main_frame = ttk.Frame(win, padding=10)
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text='Дата:').grid(row=0, column=0, sticky='w', pady=5)
        date_var = tk.StringVar(value=entry['date'])
        ttk.Entry(main_frame, textvariable=date_var, width=15).grid(row=0, column=1, sticky='w', padx=10)

        ttk.Label(main_frame, text='Заголовок:').grid(row=1, column=0, sticky='w', pady=5)
        title_var = tk.StringVar(value=entry['title'])
        ttk.Entry(main_frame, textvariable=title_var, width=50).grid(row=1, column=1, sticky='w', padx=10)

        ttk.Label(main_frame, text='Содержимое:').grid(row=2, column=0, sticky='nw', pady=5)
        text_content = tk.Text(main_frame, width=60, height=20)
        text_content.grid(row=2, column=1, pady=5, padx=10, sticky='w')
        text_content.insert('1.0', entry['content'])

        def save_changes():
            new_date = date_var.get().strip()
            new_title = title_var.get().strip()
            new_content = text_content.get('1.0', 'end-1c').strip()
            if not new_date or not new_title or not new_content:
                messagebox.showwarning('Ошибка', 'Все поля обязательны для заполнения')
                return
            if self.db.update_entry(entry['id'], new_date, new_title,
                                    new_content, self.master_password):
                messagebox.showinfo('Успех', 'Запись обновлена')
                win.destroy()
                self.refresh_entries()
            else:
                messagebox.showerror('Ошибка', 'Не удалось обновить запись')

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=1, pady=10, sticky='w')

        ttk.Button(btn_frame, text='Сохранить',
                   command=save_changes).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Отмена',
                   command=win.destroy).pack(side='left', padx=5)

    def edit_entry(self):
        """Редактирование выбранной записи (через кнопку на вкладке)."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Ошибка', 'Выберите запись для редактирования')
            return

        item = self.tree.item(selected[0])
        entry_id = item['values'][0]
        entry = next((e for e in self.entries if e['id'] == entry_id), None)
        if entry:
            self.edit_entry_window(entry)

    def delete_entry(self):
        """Удаление выбранной записи."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Ошибка', 'Выберите запись для удаления')
            return

        item = self.tree.item(selected[0])
        entry_id = item['values'][0]

        if messagebox.askyesno('Подтверждение', 'Удалить выбранную запись?'):
            if self.db.delete_entry(entry_id):
                messagebox.showinfo('Успех', 'Запись удалена')
                self.refresh_entries()
            else:
                messagebox.showerror('Ошибка', 'Не удалось удалить запись')

    def save_entry(self):
        """Сохранение новой записи."""
        date = self.entry_date.get().strip()
        title = self.entry_title.get().strip()
        content = self.text_content.get('1.0', 'end-1c').strip()

        if not date:
            messagebox.showwarning('Ошибка', 'Введите дату!')
            self.entry_date.focus()
            return
        if not title:
            messagebox.showwarning('Ошибка', 'Введите заголовок!')
            self.entry_title.focus()
            return
        if not content:
            messagebox.showwarning('Ошибка', 'Введите содержимое записи!')
            self.text_content.focus()
            return

        if self.db.add_entry(date, title, content, self.master_password):
            messagebox.showinfo('Успех', 'Запись сохранена')
            self.clear_form()
            self.refresh_entries()
            self.notebook.select(0)  # Переключиться на вкладку "Все записи"
        else:
            messagebox.showerror('Ошибка', 'Не удалось сохранить запись')

    def clear_form(self):
        """Очистка формы добавления."""
        self.entry_date.delete(0, 'end')
        self.entry_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.entry_title.delete(0, 'end')
        self.text_content.delete('1.0', 'end')
        self.entry_title.focus()

    def perform_search(self):
        """Выполнение расширенного поиска."""
        keyword = self.search_keyword.get().strip().lower()
        date_from = self.search_date_from.get().strip()
        date_to = self.search_date_to.get().strip()

        # Очистка предыдущих результатов
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)

        # Фильтрация записей
        for entry in self.entries:
            # Проверка по ключевому слову (в заголовке или содержимом)
            match_keyword = True
            if keyword:
                match_keyword = (keyword in entry['title'].lower() or
                                 keyword in entry['content'].lower())

            # Проверка по дате
            match_date = True
            if date_from and date_from != 'ГГГГ-ММ-ДД':
                match_date = entry['date'] >= date_from
            if date_to and date_to != 'ГГГГ-ММ-ДД':
                match_date = match_date and entry['date'] <= date_to

            if match_keyword and match_date:
                self.search_tree.insert('', 'end', values=(
                    entry['id'],
                    entry['date'],
                    entry['title']
                ))