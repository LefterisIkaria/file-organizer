import time
from src.models import Category, Config, Schedule
from src.app_context import AppContext
from src.utils import clear_console, draw_table

class MenuManager:
    def __init__(self, RootMenu: type['Menu'], ctx: AppContext):
        
        self.root_menu = RootMenu(self, ctx)
        self.root_menu._enter()
        
        self.menus_stack = [self.root_menu]

    @property
    def current_menu(self) -> 'Menu':
        return self.menus_stack[-1]

    def change_menu(self, new_menu: 'Menu'):
        self.current_menu._exit()
        self.menus_stack.append(new_menu)
        self.current_menu._enter()

    def back(self):
        if len(self.menus_stack) > 1:
            self.menus_stack.pop()._exit()
            self.current_menu._enter()
    
    def back_to_root(self):
        while self.current_menu != self.root_menu:
            self.back()

    def exit(self):
        self.back_to_root()
        self.root_menu._exit()
        exit(0)

    def run(self):
        while True:
            clear_console()
            self.current_menu._display()
            self.current_menu._update()


class Menu:
    """Base class for all states."""
    def __init__(self, menu_manager: MenuManager, ctx: AppContext):
        self.menu_manager = menu_manager
        self.ctx = ctx
    
    def _enter(self):
        """Initialize method when entering a menu"""
        pass

    def _display(self):
        """Display the menu options for this state."""
        pass

    def _update(self):
        """Return the next state based on user input."""
        pass

    def _exit(self):
        """Clean up method called when exiting e menu"""
        pass



class MainMenu(Menu):
    
    def _display(self):
        print("Choose a menu:")
        print("1. Config Management")
        print("2. Actions")
        print("3. Exit")
    
    
    def _update(self):
        option = input("Option: ")
        if option == "1":
             self.menu_manager.change_menu(ConfigMenu(self.menu_manager, self.ctx))
        elif option == "2":
            self.menu_manager.change_menu(ActionsMenu(self.menu_manager, self.ctx))
        elif option == "3":
            self.menu_manager.exit()
        else:
            print(f"The {option} option doesn't exist.")


class ConfigMenu(Menu):

   

    def _display(self):
        print("Config Management:")
        print("1. List configurations")
        print("2. View configuration details")
        print("3. Return to main menu")

    def _update(self):
        option = input("Option: ")
        if option == "1":
            self.menu_manager.change_menu(ConfigurationListMenu(self.menu_manager, self.ctx))
        elif option == "2":
            directory_path = input("Enter the directory path: ")
            input("Press enter...")
        elif option == "3":
            self.menu_manager.back()
        else:
            print(f"The {option} option doesn't exist.")
    

   
    

    def display_configuration_details(self, config: Config):
        print(f"Directory: {config.directory} - {'Active' if config.active else 'Inactive'}")
        print(f"Schedule: Every {config.schedule.interval} {config.schedule.type}(s)")
        
        headers = ["#", "Name", "Extensions", "Categorize"]
        data = []
        for idx, category in enumerate(config.categories, 1):
            data.append([str(idx), category.name, str(len(category.extensions)), str(category.categorize_extensions)])
        
        draw_table(headers=headers, data=data)


class ActionsMenu(Menu):
    def _display(self):
        print("Actions:")
        print("1. Run all configurations")
        print("2. Clean directory")
        print("3. Return to main menu")

    def _update(self):
        option = input("Option: ")
        if option == "1":
            print("Running configurations...")
        elif option == "2":
            print("Cleaning directory...")
        elif option == "3":
            self.menu_manager.back()
        else:
            print(f"The {option} option doesn't exist.")


class ConfigurationListMenu(Menu):

    DUMMY_CONFIGS = [
        Config(
            active=True,
            directory="/path/to/dir1",
            categories=[
                Category(name="Category1", extensions=[".txt", ".pdf"], categorize_extensions=False),
                Category(name="Category2", extensions=[".notok", ".ok"], categorize_extensions=False)
            ],
            schedule=Schedule(type="MINUTE", interval=1, active=True)
        ),
        Config(
            active=False,
            directory="/path/to/dir2",
            categories=[
                Category(name="Dummy1", extensions=[".dm", ".md"], categorize_extensions=True),
            ],
            schedule=Schedule(type="HOUR", interval=3, active=True)
        )
    ]

    def _display(self):
        print("Configuration List")
        self.display_config_list()
        print("Options: ")
        print("1. Back")
        print("--details (index/directory)")
        print("--edit (index/directory)")
        print("--filter (directory/categories/schedule/active)")

    

    def _update(self):
        input("Option: ")
    

    def display_config_list(self):
       
        if not self.DUMMY_CONFIGS:
            print("No configurations found.")
            return
    
        headers = ["#", "Directory", "Categories", "Schedule", "Active"]
        # Here, I'm assuming each config file is a text file with a single line description.
        # The date created is the file's creation date.
        data = []
        for idx, config in enumerate(self.DUMMY_CONFIGS, 1):
            data.append([str(idx), config.directory, str(len(config.categories)), str(config.schedule.active), str(config.active)])
        
        draw_table(headers=headers, data=data)