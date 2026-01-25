import pandas as pd
import re
import ast
from io import StringIO

class Parsing():
    def is_csv(self, text, min_rows = 3):
        possible_delimiters = [',', ';', '\t', '|']
        
        for delim in possible_delimiters:
            try:
                df = pd.read_csv(StringIO(text), sep=delim, engine='python', nrows=min_rows)
                if len(df) >= min_rows:
                    return True
            except Exception:
                continue
        return False

    def is_markdown(self, text):
        if not text or len(text.strip()) < 10:
            # TEXT IS TOO SHORT
            return False
        
        text = text.strip()
        indicators_count = 0
        
        # 1. HEADERS - CHECK THAT # IS AT THE BEGINNING OF LINE FOLLOWED BY SPACE
        if re.search(r'^#{1,6}\s+\S+', text, re.M):
            indicators_count += 1
        
        # 2. BOLD TEXT - MINIMUM 2 CHARACTERS BETWEEN **
        bold_matches = re.findall(r'\*\*(.+?)\*\*', text)
        if bold_matches and any(len(match.strip()) >= 2 for match in bold_matches):
            indicators_count += 1
        
        # 3. ITALIC TEXT - MINIMUM 2 CHARACTERS BETWEEN *
        italic_matches = re.findall(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', text)
        if italic_matches and any(len(match.strip()) >= 2 for match in italic_matches):
            indicators_count += 1
        
        # 4. CODE BLOCKS - CHECK COMPLETE BLOCKS WITH OR WITHOUT LANGUAGE SPECIFICATION
        if re.search(r'^```[\w]*\n.*?\n```', text, re.S | re.M):
            indicators_count += 1
        
        # 5. INLINE CODE - MINIMUM 1 CHARACTER BETWEEN `
        if re.search(r'`[^`\n]+`', text):
            indicators_count += 1
        
        # 6. BULLET LISTS - * OR - AT THE BEGINNING OF LINE WITH SPACE AND TEXT
        if re.search(r'^[\*\-]\s+\S+', text, re.M):
            # CHECK THAT THERE ARE AT LEAST 2 LIST ITEMS
            list_items = re.findall(r'^[\*\-]\s+.+', text, re.M)
            if len(list_items) >= 2:
                indicators_count += 1
        
        # 7. NUMBERED LISTS - DIGIT, DOT, SPACE, TEXT
        if re.search(r'^\d+\.\s+\S+', text, re.M):
            # CHECK THAT THERE ARE AT LEAST 2 LIST ITEMS
            numbered_items = re.findall(r'^\d+\.\s+.+', text, re.M)
            if len(numbered_items) >= 2:
                indicators_count += 1
        
        # 8. LINKS - CHECK CORRECT FORMAT [TEXT](URL)
        link_pattern = r'\[([^\[\]]+)\]\(([^\s\(\)]+)\)'
        if re.search(link_pattern, text):
            indicators_count += 1
        
        # 9. QUOTES - > AT THE BEGINNING OF LINE WITH SPACE AND TEXT
        if re.search(r'^>\s+\S+', text, re.M):
            indicators_count += 1
        
        # 10. TABLES - MINIMUM 2 ROWS WITH | SEPARATORS
        table_rows = re.findall(r'^.*\|.*\|.*$', text, re.M)
        if len(table_rows) >= 2:
            # CHECK FOR TABLE SEPARATOR ROW
            if any(re.match(r'^[\|\s\-:]+$', row.strip()) for row in table_rows):
                indicators_count += 1
        
        # 11. HORIZONTAL LINES
        if re.search(r'^(---+|\*\*\*+|___+)\s*$', text, re.M):
            indicators_count += 1
        
        # 12. STRIKETHROUGH TEXT
        if re.search(r'~~.+?~~', text):
            indicators_count += 1
        
        # ADDITIONAL CHECKS TO EXCLUDE FALSE POSITIVES
        # EXCLUDE REGULAR SENTENCES WITH RANDOM CHARACTERS
        sentences = text.split('.')
        if len(sentences) > 3:
            # MANY SENTENCES
            # IF TEXT LOOKS MORE LIKE REGULAR PROSE
            words_count = len(text.split())
            special_chars_count = len(re.findall(r'[#*`\[\]()>|~-]', text))
            
            # IF TOO FEW SPECIAL CHARACTERS RELATIVE TO WORD COUNT
            if words_count > 20 and special_chars_count / words_count < 0.05:
                return False
        
        # REQUIRE MINIMUM 2 INDICATORS TO CLASSIFY AS MARKDOWN
        # FOR SHORT TEXTS (< 100 CHARACTERS) REQUIRE MORE INDICATORS
        min_indicators = 3 if len(text) < 100 else 2
        return indicators_count >= min_indicators

    def is_python(self, text):
        if not text or not isinstance(text, str):
            return False
        
        text = text.strip()
        if not text:
            return False
        
        # CHECK FOR OBVIOUS NON-CODE PATTERNS
        if re.search(r'<[^>]+>', text):  # HTML TAGS
            return False
        if re.search(r'https?://', text):  # URLS
            return False
        
        try:
            tree = ast.parse(text)
            # CHECK IF CONTAINS ACTUAL CODE STRUCTURES
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Import, 
                                ast.ImportFrom, ast.If, ast.For, ast.While, ast.Assign)):
                    return True
            return False
        except:
            return False