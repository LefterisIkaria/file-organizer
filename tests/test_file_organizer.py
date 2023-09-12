import os
from random import choice
import shutil
import unittest
import tempfile
import logging
from src.models import Category
import src.setup as setup
from src.file_organizer import FileOrganizer


LOG = logging.getLogger(__name__)


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


NUM_OF_FILES = 100


class TestFileOrganizer(unittest.TestCase):


    @classmethod
    def setUpClass(cls) -> None:
        
        # setup logging
        setup.setup_logging("config/logging.json")


    def setUp(self) -> None:
        
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()
        LOG.debug(f"Temp directory created at {self.temp_dir}")

        # generate some files with random extensions
        for i in range(NUM_OF_FILES):
            filename = f"file{i}{choice(FILE_EXTENSIONS)}"
            filepath = os.path.join(self.temp_dir, filename)
            with open(filepath, 'w') as f:
                f.write("some content")

        # initialize FileOrganizer object
        self.organizer = FileOrganizer()
    

    def tearDown(self) -> None:
        # remove the temp_dir
        shutil.rmtree(self.temp_dir)

    

    def test_validate_directory_existance(self):

        try:
            self.organizer.validate_directory(self.temp_dir)
        except Exception as e:
            self.fail(f"'validate_directory' method raised {type(e)} unexpectedly!")

        with self.assertRaises(ValueError):
            self.organizer.validate_directory("/path/not/exists")
    

    def test_validate_critical_directory(self):
        # choose a critical directory to test
        critical_dir = choice(FileOrganizer.CRITICAL_DIRECTORIES['Linux'])
        with self.assertRaises(ValueError):
            self.organizer.validate_directory(critical_dir)
    

    def test_validate_directory_permissions(self):
        try:
            # Remove all permissions for the user
            os.chmod(self.temp_dir, 0o000)

            with self.assertRaises(PermissionError):
                # Try to list the directory (or any other operation that requires permissions)
                os.listdir(self.temp_dir)
        finally:
            # Restore permissions to the directory to allow cleanup
            os.chmod(self.temp_dir, 0o700)
    

    def test_create_categories(self):
        categories = [
            Category(name="Test1", extensions=[".one", ".two"], categorize_extensions=True),
            Category(name="Test2", extensions=[".test"], categorize_extensions=False)
        ]

        # Invoke the method you want to test
        self.organizer.create_categories(self.temp_dir, categories)

        # Check that each category directory exists
        for category in categories:
            category_path = os.path.join(self.temp_dir, category.name)
            self.assertTrue(os.path.exists(category_path), f"Category {category.name} was not created")

            # If categorize_extensions is True, check for subdirectories
            if category.categorize_extensions:
                for ext in category.extensions:
                    ext_dir = os.path.join(category_path, ext.lstrip('.'))
                    self.assertTrue(os.path.exists(ext_dir), f"Extension directory {ext_dir} was not created")
        

    def test_categorize_files(self):

        # Create some test files in the temporary directory
        test_files = ['test1.one', 'test2.two', 'test3.test', 'test4.other', '.hiddenfile.txt']
        for filename in test_files:
            filepath = os.path.join(self.temp_dir, filename)
            with open(filepath, 'w') as f:
                f.write("some content")
        
        # Define some sample categories that match the extensions of the test files
        categories = [
            Category(name="Category1", extensions=[".one", ".two"], categorize_extensions=True),
            Category(name="Category2", extensions=[".test"], categorize_extensions=False),
        ]

        # First create the categories
        self.organizer.create_categories(self.temp_dir, categories)

        # Run the method you want to test
        self.organizer.categorize_files(self.temp_dir, categories)

        # Check if the files have been moved to the correct category directories
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "Category1", "one", "test1.one")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "Category1", "two", "test2.two")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "Category2", "test3.test")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "Uncategorized", "test4.other")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, ".hidden", ".hiddenfile.txt")))

    

    def test_cleanup_directory(self):
         # Create some test category directories in the temporary directory
        categories = [
            Category(name="EmptyCategory", extensions=[], categorize_extensions=False),
            Category(name="NonEmptyCategory", extensions=[], categorize_extensions=False),
            Category(name="MixedCategory", extensions=[".one", ".two"], categorize_extensions=True)
        ]

        os.makedirs(os.path.join(self.temp_dir, "EmptyCategory"))
        os.makedirs(os.path.join(self.temp_dir, "NonEmptyCategory"))
        os.makedirs(os.path.join(self.temp_dir, "MixedCategory", "one"))
        os.makedirs(os.path.join(self.temp_dir, "MixedCategory", "two"))

        # Add a file to NonEmptyCategory
        with open(os.path.join(self.temp_dir, "NonEmptyCategory", "test.txt"), 'w') as f:
            f.write("some content")

        # Add a file to a subdirectory of MixedCategory
        with open(os.path.join(self.temp_dir, "MixedCategory", "one", "test1.one"), 'w') as f:
            f.write("some content")

        # Run the method you want to test
        self.organizer.cleanup_directory(self.temp_dir, categories)

        # Check the results
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, "EmptyCategory")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "NonEmptyCategory")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "MixedCategory", "one")))
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, "MixedCategory", "two")))
    

    def test_reset_directory(self):
        # Create some test category directories in the temporary directory
        categories = [
            Category(name="CategoryA", extensions=[".one", ".two"], categorize_extensions=True),
            Category(name="CategoryB", extensions=[".test"], categorize_extensions=False)
        ]

        # Creating directories and adding files
        os.makedirs(os.path.join(self.temp_dir, "CategoryA", "one"))
        os.makedirs(os.path.join(self.temp_dir, "CategoryA", "two"))
        os.makedirs(os.path.join(self.temp_dir, "CategoryB"))

        # Write 3 files
        with open(os.path.join(self.temp_dir, "CategoryA", "one", "test1.one"), 'w') as f:
            f.write("some content")
        with open(os.path.join(self.temp_dir, "CategoryA", "two", "test2.two"), 'w') as f:
            f.write("some content")
        with open(os.path.join(self.temp_dir, "CategoryB", "test3.test"), 'w') as f:
            f.write("some content")

        # Run the method you want to test
        self.organizer.reset_directory(self.temp_dir, categories)

        # Check the results
        # Count the number of files in the main directory
        tmpdir_files_count = [f for f in os.listdir(self.temp_dir) if os.path.isfile(os.path.join(self.temp_dir, f))]
        self.assertEqual(len(tmpdir_files_count), NUM_OF_FILES + 3) # plus the 3 created

        # Check if files are moved to main directory
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "test1.one")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "test2.two")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "test3.test")))

        # Check if subdirectories are removed
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, "CategoryA", "one")))
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, "CategoryA", "two")))
        
        # Check if main category directories remain intact
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "CategoryA")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "CategoryB")))

    



if __name__ == "__main__":
    unittest.main()
