import json
import os
import tkinter as tk

from tkinter import ttk, StringVar

from src.organizer.file_organizer import FileOrganizer
from src.models.config import Config

class App(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        super(App, self).__init__(*args, **kwargs)

        self.file_organizer = FileOrganizer()

        # initialize root   
        self.title("File Organizer")
        self.geometry("900x400")

        # Create root frame
        self.root_frame = ttk.Frame(self)
        self.root_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        self.root_frame.grid_rowconfigure(1, weight=1)
        self.root_frame.grid_columnconfigure(0, weight=1)

        # Create top frame for search bar and button
        self.top_frame = ttk.Frame(self.root_frame)
        self.top_frame.grid(row=0, column=0, sticky="ew")
        self.top_frame.rowconfigure(0, weight=1)
        self.top_frame.columnconfigure((0, 1), weight=1)

        # Create search bar
        self.search_var = StringVar()
        self.search_bar = ttk.Entry(self.top_frame, textvariable=self.search_var)
        self.search_bar.bind("<KeyRelease>", self.on_search)
        self.search_bar.grid(row=0, column=0, sticky="w")

        # Create 'New Configuration' button
        self.new_button = ttk.Button(self.top_frame, text="New Configuration", command= lambda: print("new config"))
        self.new_button.grid(row=0, column=1, sticky="e")

        # Create main frame for TreeView
        self.main_frame = ttk.Frame(self.root_frame)
        self.main_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        # Create ConfigTreeView
        self.tree = ConfigTreeView(self.main_frame)
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.load_data(App.load_config())

        # Create bottom frame for 'Run Configurations' Button
        self.bottom_frame = ttk.Frame(self.root_frame)
        self.bottom_frame.grid(row=2, column=0, sticky="ew")
        self.bottom_frame.rowconfigure(0, weight=1)
        self.bottom_frame.columnconfigure(0, weight=1)

        # Create 'Run All Configurations' Button
        self.run_button = ttk.Button(self.bottom_frame, text="Run All Configurations", command=self.on_run_configs)
        self.run_button.grid(row=0, column=0, sticky="e")


    @staticmethod
    def get_config_path() -> str:
        home_path = os.path.expanduser("~")
        return os.path.join(home_path, ".file-organizer", "app.json")

    @staticmethod
    def load_config() -> list[Config]:
        app_config_path = App.get_config_path()
        with open(app_config_path, 'r') as f:
            configurations = json.load(f)
            return [Config(config) for config in configurations]
    

    def on_search(self, event):
        searched_configs = [config for config in App.load_config() if self.search_var.get() in config.dir]
        self.tree.clear_data()
        self.tree.load_data(searched_configs)
    
    def on_run_configs(self):
        app_config_path = App.get_config_path()
        self.file_organizer.run(app_config_path)


class ConfigTreeView(ttk.Treeview):
    def __init__(self, parent, *args, **kwargs):
        super(ConfigTreeView, self).__init__(parent, *args, **kwargs)
        self.build_tree()

    def build_tree(self):
        self["columns"] = ("Directory", "Categories", "Schedule", "Active")
        self["show"] = "headings"
        self.heading("Directory", text="Directory Path")
        self.heading("Categories", text="Number of Categories")
        self.heading("Schedule", text="Schedule")
        self.heading("Active", text="Active")


    def clear_data(self):
        for row in self.get_children():
            self.delete(row)

    def load_data(self, data: list[Config]):
        for i, config in enumerate(data):
            self.insert("", i, values=(
                config.dir,
                len(config.categories),
                "daily at 02:00 pm", # replace it with actual schedule logic
                config.active
            ))
    