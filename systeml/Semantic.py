# STRING COMPARISON
from difflib import SequenceMatcher
from Levenshtein import distance as levenshtein_distance

class Semantic():
    def extract_code_block_from_text(self, text):
        if not isinstance(text, str):
            return text
        
        # REMOVE SPACES ONLY AT EDGES, PRESERVING INTERNAL STRUCTURE
        original_text = text
        text = text.strip()
        
        if not text:
            return original_text
        
        lines = text.split('\n')
        
        # MINIMUM 3 LINES: OPENING, CONTENT (CAN BE EMPTY), CLOSING
        if len(lines) < 3:
            return original_text
        
        first_line = lines[0]
        last_line = lines[-1]
        
        # CHECK OPENING LINE: ``` + OPTIONAL LANGUAGE
        if not first_line.startswith('```'):
            return original_text
        
        # AFTER ``` CAN ONLY BE LANGUAGE NAME (LETTERS, DIGITS, HYPHENS, UNDERSCORES)
        language_part = first_line[3:]  # EVERYTHING AFTER ```
        if language_part and not language_part.replace('-', '').replace('_', '').isalnum():
            return original_text
        
        # CHECK CLOSING LINE: EXACTLY ```
        if last_line != '```':
            return original_text
        
        # CHECK THAT CONTENT HAS NO OTHER WRAPPERS
        content_lines = lines[1:-1]
        for line in content_lines:
            if line.startswith('```'):
                return original_text  # FOUND NESTED OR ADDITIONAL WRAPPER
        
        # ADDITIONAL CHECK: COUNT ALL LINES STARTING WITH ```
        wrapper_count = sum(1 for line in lines if line.startswith('```'))
        if wrapper_count != 2:  # SHOULD BE EXACTLY 2: OPENING AND CLOSING
            return original_text
        
        # CHECK THAT CLOSING WRAPPER IS NOT IN THE MIDDLE
        for i, line in enumerate(lines):
            if line == '```' and i != len(lines) - 1:
                return original_text  # CLOSING WRAPPER NOT AT THE END
        
        # ALL CHECKS PASSED, EXTRACT CONTENT
        return '\n'.join(content_lines)
    
    def _compare_cached(self, s1_norm, s2_norm):
        if not s1_norm or not s2_norm:
            return 0.0
            
        # Точное совпадение после нормализации
        if s1_norm == s2_norm:
            return 1.0

        # Проверка на большую разницу в длине (ранний выход)
        len1, len2 = len(s1_norm), len(s2_norm)
        max_len = max(len1, len2)
        min_len = min(len1, len2)
        
        if max_len == 0:
            return 1.0

        if min_len / max_len < 0.5:
            return 0.0

        # 1. SequenceMatcher - учитывает порядок и непрерывные последовательности
        seq_ratio = SequenceMatcher(None, s1_norm, s2_norm).ratio()
        
        # РАННИЙ ВЫХОД: если seq_ratio очень высокий - это точно совпадение
        if seq_ratio >= 0.95:
            return seq_ratio  # Не тратим время на Levenshtein!
        
        # РАННИЙ ВЫХОД: если seq_ratio очень низкий - это точно НЕ совпадение  
        if seq_ratio < 0.7:  # меньше 70% сходства
            return seq_ratio  # Levenshtein не улучшит результат значительно
        
        # 2. Только для пограничных случаев (70-95%) считаем Levenshtein
        lev_distance = levenshtein_distance(s1_norm, s2_norm)
        lev_ratio = 1.0 - (lev_distance / max_len)
        
        combined_ratio = (seq_ratio * 0.6) + (lev_ratio * 0.4)
        
        return combined_ratio

    def compare_strings(self, s1, s2):
        """
        Комбинированный метод для сравнения строк с учётом различных аспектов сходства.
        Возвращает значение от 0.0 до 1.0
        """
        if not s1 or not s2:
            return 0.0
        
        # Нормализация: lower case, убираем пробелы и подчёркивания
        s1_norm = s1.lower().replace(" ", "").replace("_", "").replace("-", "")
        s2_norm = s2.lower().replace(" ", "").replace("_", "").replace("-", "")
        
        return self._compare_cached(s1_norm, s2_norm)