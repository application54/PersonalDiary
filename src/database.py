# Модуль работы с базой данных

import sqlite3
from src.security import SecurityManager
from src.config import DB_NAME

class DatabaseManager:
    """Класс управления базой данных дневника."""

    def __init__(self, db_path: str = DB_NAME):
        self.db_path = db_path
        self.security = SecurityManager()
        self._init_database()

    def _init_database(self):
        """Создание таблицы entries, если она не существует."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                title TEXT NOT NULL,
                encrypted_content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def add_entry(self, date: str, title: str, content: str, master_password: str) -> bool:
        """Добавление новой записи в дневник."""
        try:
            encrypted_content = self.security.encrypt(content, master_password)
            if not encrypted_content:
                return False
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO entries (date, title, encrypted_content)
                VALUES (?, ?, ?)
            ''', (date, title, encrypted_content))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления записи: {e}")
            return False

    def get_all_entries(self, master_password: str):
        """Получение всех записей дневника с расшифрованным содержимым."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM entries ORDER BY date DESC, created_at DESC')
            rows = cursor.fetchall()
            entries = []
            for row in rows:
                try:
                    decrypted_content = self.security.decrypt(row[3], master_password)
                    if decrypted_content is not None:
                        entries.append({
                            'id': row[0],
                            'date': row[1],
                            'title': row[2],
                            'content': decrypted_content,
                            'created_at': row[4]
                        })
                except Exception as e:
                    print(f"Ошибка расшифровки записи ID {row[0]}: {e}")
                    continue
            conn.close()
            return entries
        except Exception as e:
            print(f"Ошибка получения записей: {e}")
            return []

    def update_entry(self, entry_id: int, date: str, title: str, content: str, master_password: str) -> bool:
        """Обновление существующей записи."""
        try:
            encrypted_content = self.security.encrypt(content, master_password)
            if not encrypted_content:
                return False
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE entries
                SET date = ?, title = ?, encrypted_content = ?
                WHERE id = ?
            ''', (date, title, encrypted_content, entry_id))
            conn.commit()
            conn.close()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Ошибка обновления записи: {e}")
            return False

    def delete_entry(self, entry_id: int) -> bool:
        """Удаление записи по ID."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
            conn.commit()
            conn.close()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Ошибка удаления записи: {e}")
            return False