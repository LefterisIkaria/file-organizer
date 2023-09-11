import ttkbootstrap as tb
from gui.views.config_list_view import ConfigListView


class App(tb.Window):
    
    def __init__(self, config_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # The config manager to make CRUD operations on the config file
        self.config_manager = config_manager

        # Configure window
        self.title("File Organizer")
        self.minsize(width=800, height=500)
        
        self.configure(padx=10, pady=10)

        # ConfigList on the left side
        # Display all configs in a tableview
        self.config_list_view = ConfigListView(self)
        self.config_list_view.pack(side=tb.LEFT, fill=tb.Y)
        self.config_list_view.config_table.bind("<<OnConfigSelect>>", self.handle_config_select)

        # Content Frame
        # Display different views like ConfigDetails, ConfigEdit, etc.
        self.content_frame = tb.Frame(self, style="warning")
        self.content_frame.pack(side=tb.RIGHT, fill=tb.BOTH, expand=True)


    def handle_config_select(self, event):
        selected_dir = event.widget.selected_dir
        print(selected_dir)