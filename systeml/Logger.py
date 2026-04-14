"""
Централизованный логгер для BFR.
Все логи пишутся в один файл, указанный в settings.LOG_FILE.
Файл пересоздаётся при каждой новой инициализации BFR.
"""

from datetime import datetime
import os

class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        # Создаём папку если её нет
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        # Пересоздаём файл при инициализации
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"NEW SESSION STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*60}\n\n")
    
    def log(self, message):
        """Записывает сообщение в лог-файл и выводит в stdout."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        formatted_message = f"[{timestamp}] {message}"
        
        # Запись в файл
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(formatted_message + "\n")
            f.flush()
    
    def error(self, message):
        """Записывает ошибку в лог-файл и выводит в stderr."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        formatted_message = f"[{timestamp}] ERROR: {message}"
        
        # Запись в файл
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(formatted_message + "\n")
            f.flush()