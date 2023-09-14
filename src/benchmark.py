from datetime import datetime
import json
import os
from random import choice
import time
import shutil
from file_organizer import FileOrganizer 
import matplotlib.pyplot as plt

from models import Config

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

def create_files_in_directory(directory, num_files):
    os.makedirs(directory, exist_ok=True)
    for i in range(num_files):
        with open(os.path.join(directory, f"file_{i}{choice(FILE_EXTENSIONS)}"), 'w') as f:
            f.write("Test file content")

def load_template_config(template_path="config/template.json"):
    with open(template_path, 'r') as file:
        data = json.load(file)
    return Config.from_dict(data)

def benchmark_organizer_single_dir(num_files_list):
    times = []
    template_config = load_template_config()
    
    for num_files in num_files_list:
        temp_dir = f"temp_{num_files}_files"
        create_files_in_directory(temp_dir, num_files)
        template_config.directory = temp_dir
        organizer = FileOrganizer()
        
        start_time = time.time()
        organizer.process_config(template_config)
        end_time = time.time()

        times.append(end_time - start_time)
        shutil.rmtree(temp_dir)

    return times

def benchmark_organizer_multiple_dir(num_dir_list, num_files):
    times_matrix = []

    template_config = load_template_config()
    for num_dirs in num_dir_list:
        total_time = 0
        for _ in range(num_dirs):
            temp_dir = f"temp_{num_files}_files_dir_{_}"
            create_files_in_directory(temp_dir, num_files)
            template_config.directory = temp_dir
            organizer = FileOrganizer()

            start_time = time.time()
            organizer.process_config(template_config)
            end_time = time.time()

            total_time += (end_time - start_time)
            shutil.rmtree(temp_dir)

        times_matrix.append(total_time / num_dirs)
    
    return times_matrix

def plot_single_dir_results(num_files_list, times):
    plt.plot(num_files_list, times, marker='o')
    plt.xlabel("Number of Files")
    plt.ylabel("Time (seconds)")
    plt.title("Single Directory Benchmark")
    plt.grid(True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plt.savefig(f"benchmark/results_single_dir_{timestamp}.png")
    plt.show()

def plot_multi_dir_results(num_files_list, num_dir_list, times_matrix):
    for idx, num_dirs in enumerate(num_dir_list):
        plt.plot(num_files_list, times_matrix[idx], marker='o', label=f'{num_dirs} directories')
    
    plt.xlabel("Number of Files per Directory")
    plt.ylabel("Average Time (seconds)")
    plt.title("Multiple Directories Benchmark")
    plt.legend()
    plt.grid(True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plt.savefig(f"benchmark/results_multi_dir_{timestamp}.png")
    plt.show()
