from .Parsing import Parsing
from .FilesAndFolders import FilesAndFolders
from .Mime import Mime
from .Semantic import Semantic
from .LLM import LLM

class Systeml(Parsing, FilesAndFolders, Mime, Semantic, LLM):
    def __init__(self):
        super().__init__()

        self.chunk_size = 4096