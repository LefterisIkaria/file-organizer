import ttkbootstrap as tb
from gui.views.config_list import ConfigList


class App(tb.Window):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("File Organizer")
        self.configure(padx=10, pady=10)

        # Left Frame Config List
        # Display all configs in a tableview
        self.config_list = ConfigList(self)
        self.config_list.pack(side=tb.LEFT, fill=tb.Y)

        # Content Frame Display Config details
        self.content_frame = tb.Frame(self, style="warning")
        self.content_frame.pack(side=tb.RIGHT, fill=tb.BOTH, expand=True)
