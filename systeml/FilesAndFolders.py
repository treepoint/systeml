import os
from pathlib import Path
import shutil
import re
import uuid
from unidecode import unidecode
import json

class FilesAndFolders():
    def clear_folder(self, folder):
        if not os.path.exists(folder):
            return

        if not os.path.isdir(folder):
            return
        
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path) 
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error while delete {file_path}. Reason: {e}")

    def create_folder(self, folder):
        path = Path(folder)
        path.mkdir(parents = True, exist_ok = True)

    def is_folder_exists(self, folder):
        return os.path.isdir(folder)
    
    def make_filename_from_text(self, text, max_words = 10, max_length = 100):
        # TRANSLITERATE TO ASCII (E.G., РУССКИЙ -> RUSSKII)
        text = unidecode(text)

        # GET FIRST WORDS FROM TEXT
        words = re.findall(r'\w+', text.lower())
        short_text = '_'.join(words[:max_words])

        # GENERATE SHORT UNIQUE ID (FIRST 8 CHARS OF UUID)
        unique_id = str(uuid.uuid4()).replace("-", "")[:8]

        # COMBINE TEXT AND ID
        base_name = f"{short_text}_{unique_id}"

        # REMOVE INVALID CHARACTERS FOR FILENAMES
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '', base_name)

        # TRIM TO MAXIMUM LENGTH
        safe_name = safe_name[:max_length]

        return safe_name
    
    def dump_object_to_file(self, obj, path):
        json_str = json.dumps(obj, ensure_ascii=False, indent=4)

        with open(path, "w", encoding="utf-8") as f:
            f.write(json_str)


    def load_object_from_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: File not found - {path}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Error: Failed to decode JSON - {e}")
            return False