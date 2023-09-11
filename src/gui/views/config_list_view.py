import ttkbootstrap as tb
from ttkbootstrap.tableview import Tableview

from src.models.config import Config
from src.models.config_manager import ConfigManager


class ConfigListView(tb.Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)


        # add button
        self.add_btn = tb.Button(self, text="Add Config", command=lambda: print("Add config..."))
        self.add_btn.pack(fill=tb.X)


        # config table
        self.config_table = self.ConfigTable(self, bootstyle="primary")
        self.config_table.pack(fill=tb.Y, expand=True)



    class ConfigTable(Tableview):

        def __init__(self, master, *args, **kwargs):
            super().__init__(master, *args, **kwargs)

            # data
            self.config_manager: ConfigManager = self._root().config_manager
            self.selected_dir = ""

            # initialize
            self._searchable=True
            self.insert_column(index=0, text="Directory Path", stretch=True)
            self.load_data()

            self.view.bind("<<TreeviewSelect>>", self.handle_item_select)
        

        def load_data(self):

            configs = self.config_manager.get_configs()
            for config in configs:
                self.insert_row("end", values=(
                    config.dir,
                ))

            self.load_table_data()
        

        def handle_item_select(self, event):
            # Get the selected items
            selected_items = event.widget.selection()
            # If no items stop
            if not selected_items:
                return
            
            # Get the selected table row
            selected_iid = selected_items[0]
            selected_row = self.get_row(iid=selected_iid)
            
            # Extract the directory path
            dir = selected_row.values[0]

            # If already selected stop
            if dir == self.selected_dir:
                return

            # Set selected dir
            self.selected_dir = dir 

            # Generate event
            self.event_generate("<<OnConfigSelect>>")
