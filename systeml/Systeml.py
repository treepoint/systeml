from .LLM import LLM
from .Mime import Mime
from .Parsing import Parsing
from .Semantic import Semantic
from .FilesAndFolders import FilesAndFolders
from .Logger import Logger

from types import SimpleNamespace

class Systeml(Parsing, FilesAndFolders, Mime, Semantic, LLM):
    def __init__(self):
        super().__init__()

        self.settings = SimpleNamespace(LOG_FILE="./temp/log_file.txt")
        self.chunk_size = 4096

        self.logger = Logger(self.settings.LOG_FILE)