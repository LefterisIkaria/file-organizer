import ttkbootstrap as tb
from ttkbootstrap.tableview import Tableview

from models.config import Config


class ConfigList(tb.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(master=parent, *args, **kwargs)

        self.configure(borderwidth=2, relief="groove")

        # add button
        self.add_btn = tb.Button(self, text="Add Config", command=lambda: print("Add config..."))
        self.add_btn.pack(fill=tb.X)


        # config table
        self.config_table = Tableview(self, searchable=True, bootstyle="primary")
        self.config_table.pack(fill=tb.Y, expand=True)
        self.config_table.insert_column(index=0, text="Directory Path", stretch=True)
    


    def load_data(self):

        dummy = {
            {
                "dir": "/path/to/dir1",
                "categories": {
                    "TestDir1": {
                        "extensions": [".a1", ".a2", ".a3"],
                        "categorize_extensions": True
                    },
                    "TestDir2": {
                        "extensions": [".b1", ".b2"],
                        "categorize_extensions": False
                    },
                    "TestDir3": {
                        "extensions": [".c1", ".c2"],
                        "categorize_extensions": True
                    },
                    "TestDir4": {
                        "extensions": [".d1", ".d2"],
                        "categorize_extensions": False
                    },
                },
                "schedule": {
                    "type": "SECOND",
                    "interval": 1,
                    "month": None,
                    "day": None,
                    "weekday": None,
                    "time": None
                },
                "active": True
            },
            {
                "dir": "/path/to/dir2",
                "categories": {
                    "TestDir1": {
                        "extensions": [".some", ".test"],
                        "categorize_extensions": True
                    },
                    "TestDir2": {
                        "extensions": [],
                        "categorize_extensions": True
                    },
                    "TestDir3": {
                        "extensions": [],
                        "categorize_extensions": True
                    },
                    "TestDir4": {
                        "extensions": [],
                        "categorize_extensions": True
                    },
                },
                "schedule": {
                    "type": "WEEK",
                    "interval": 3,
                    "month": None,
                    "day": None,
                    "weekday": "MONDAY",
                    "time": "00:00"
                },
                "active": False
            }
        }
        

        for cfg in dummy:
            config = Config(cfg)
            