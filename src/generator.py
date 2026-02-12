# Модуль генерации паролей

import random
import string

# Класс генератора паролей
class PasswordGenerator:

    # Генерация случайного пароля
    @staticmethod
    def generate(length: int = 16,
                 use_lowercase: bool = True,
                 use_uppercase: bool = True,
                 use_digits: bool = True,
                 use_special: bool = True) -> str:
        char_pool = ''
        if use_lowercase:
            char_pool += string.ascii_lowercase
        if use_uppercase:
            char_pool += string.ascii_uppercase
        if use_digits:
            char_pool += string.digits
        if use_special:
            char_pool += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        password = []
        if use_lowercase:
            password.append(random.choice(string.ascii_lowercase))
        if use_uppercase:
            password.append(random.choice(string.ascii_uppercase))
        if use_digits:
            password.append(random.choice(string.digits))
        if use_special:
            password.append(random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
        remaining_length = length - len(password)
        password.extend(random.choice(char_pool) for _ in range(remaining_length))
        random.shuffle(password)
        return ''.join(password)

    # Проверка надежности пароля
    @staticmethod
    def check_strength(password: str) -> str:
        if len(password) < 8:
            return "Слабый"
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        score = sum([has_upper, has_lower, has_digit, has_special])
        if score == 4 and len(password) >= 12:
            return "Отличный"
        elif score >= 3:
            return "Хороший"
        elif score >= 2:
            return "Средний"
        else:
            return "Слабый"