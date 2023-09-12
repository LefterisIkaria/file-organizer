import os
from random import choice
import shutil
import unittest
import tempfile
import src.setup as setup
from unittest.mock import patch, mock_open
from src.file_organizer import FileOrganizer


FILE_EXTENSIONS = [
    # Text and Documents
    ".txt", ".doc", ".docx", ".pdf", ".odt", ".rtf", ".tex", ".wpd",

    # Images
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", ".svg", ".psd", ".ai", ".indd", ".raw",

    # Audio
    ".mp3", ".wav", ".ogg", ".flac", ".aac", ".wma", ".m4a",

    # Video
    ".mp4", ".mkv", ".flv", ".mov", ".avi", ".wmv", ".m4v",

    # Archives
    ".zip", ".rar", ".tar", ".gz", ".7z", ".bz2",

    # Programming and Code
    ".py", ".js", ".html", ".css", ".c", ".cpp", ".java", ".cs", ".php", ".go", ".rb", ".pl", ".swift",

    # Databases
    ".sql", ".db", ".mdb", ".accdb", ".sqlite",

    # Spreadsheet and Presentations
    ".xls", ".xlsx", ".ods", ".ppt", ".pptx", ".odp",

    # System and Miscellaneous
    ".exe", ".dll", ".bat", ".sh", ".apk", ".iso", ".bin"
]



class TestFileOrganizer(unittest.TestCase):


    @classmethod
    def setUpClass(cls) -> None:
        setup.setup_logging("config/logging.json")

    def setUp(self) -> None:

        
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()
        print(f"Temp directory created at {self.temp_dir}")

        for i in range(100):
            filename = f"file{i}{choice(FILE_EXTENSIONS)}"
            filepath = os.path.join(self.temp_dir, filename)
            with open(filepath, 'w') as f:
                f.write("some content")

        self.organizer = FileOrganizer()
    

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    

    def test_validate_directory_existance(self):

        try:
            self.organizer.validate_directory(self.temp_dir)
        except Exception as e:
            self.fail(f"'validate_directory' method raised {type(e)} unexpectedly!")

        with self.assertRaises(ValueError):
            self.organizer.validate_directory("/path/not/exists")
    



if __name__ == "__main__":
    unittest.main()
