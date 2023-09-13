import time
from app_context import AppContext
from src.models import Category, Config, Schedule
from src.app_context import AppContext
from src.utils import clear_console, Table

class MenuManager:
    def __init__(self, RootMenu: type['Menu'], ctx: AppContext, initial_data: dict[str, any] = {}):
        
        self.root_menu = RootMenu(self, ctx)
        self.root_menu._enter(data=initial_data)
        
        self.menus_stack = [self.root_menu]

    @property
    def current_menu(self) -> 'Menu':
        return self.menus_stack[-1]

    def change_menu(self, new_menu: 'Menu', data: dict[str, any] = {}):
        self.current_menu._exit(data)
        self.menus_stack.append(new_menu)
        self.current_menu._enter(data)

    def back(self, data: dict[str, any] = {}):
        if len(self.menus_stack) > 1:
            self.menus_stack.pop()._exit(data)
            self.current_menu._enter(data)
    
    def back_to_root(self, data: dict[str, any] = {}):
        while self.current_menu != self.root_menu:
            self.back(data)

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
    
    def _enter(self, data: dict[str, any] = {}):
        """Initialize method when entering a menu"""
        pass

    def _display(self):
        """Display the menu options for this state."""
        pass

    def _update(self):
        """Return the next state based on user input."""
        pass

    def _exit(self, data: dict[str, any] = {}):
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
        ...        
        

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

    def _enter(self, data: dict[str, any] = {}):
        headers = ["Directory", "Categories", "Schedule", "Active"]
        table_data = [
            (config.directory, str(len(config.categories)), str(config.schedule.active), str(config.active)) 
            for config 
            in self.ctx.service.get_configs()
        ]

        self.config_table = Table(headers=headers, data=table_data)
        

    def _display(self):
        print("Configuration List")
        self.display_config_config_table()
        print("Options: ")
        print("1. Actions")
        print("     --show <directory>")
        print("     --search <directory>")
        print("     --reset")
        print("2. Back")
        
    

    def display_config_config_table(self):
       
       if self.config_table.empty():
           print("No configs found")
           return
       
       self.config_table.draw_table()
    

    def _update(self):
        option = input("Option: ")
        if option == "1":
            print("Write an action instead..")
        elif any(opt in option for opt in ["--show", "--search", "--reset"]):
            self.process_action(option)
        

        elif option == "2":
            self.menu_manager.back()
        

    def process_action(self, action: str):
        
        if "--show" in action:
            dir = action.split()[1]
            config = self.ctx.service.get_config(directory=dir)
            if config:
                self.menu_manager.change_menu(ConfigShowMenu(self.menu_manager, self.ctx), {'config': config})
            else:
                input(f"config if path `{dir}` not found...")
        elif "--search" in action:
            searched = action.split()[1]
            self.search_action(searched)
        elif "--reset" in action:
            self.reset_action()
        else:
            print(f"No such action exists: {action}") 
    

    def search_action(self, searched):
        print(f"searched for: {searched}")
    
        # Filtering the DUMMY_CONFIGS based on the search term
        matched_configs = [config for config in self.ctx.service.get_configs() if searched.lower() in config.directory.lower()]
        
        # Display the matched configurations in a table format
        data = [
            (config.directory, str(len(config.categories)), str(config.schedule.active), str(config.active)) 
            for config in matched_configs
        ]
        
        self.config_table.set_data(data)
    
    
    def reset_action(self):
        data = [
            (config.directory, str(len(config.categories)), str(config.schedule.active), str(config.active)) 
            for config 
            in self.ctx.service.get_configs()
        ]

        self.config_table.set_data(data)
        


class ConfigShowMenu(Menu):

    def _enter(self, data: dict[str, any] = {}):
        self.config: Config = data.get('config', None)
        
        if not self.config:
            input("Config was not provided..")
            self.menu_manager.back()
            return
        
    
    def _display(self):
        
        print("=" * 25 + " CONFIG DETAILS " + "=" * 25)
        print("\nDIRECTORY:", self.config.directory)
        
        print("\n----- CATEGORIES -----")
        for idx, category in enumerate(self.config.categories, 1):
            print(f"{idx}. {category.name}")
            print("   Extensions:", ', '.join(category.extensions))
            print(f"   Categorize Extensions: {'Yes' if category.categorize_extensions else 'No'}")
        
        print("\n----- SCHEDULE -----")
        print("Type:", self.config.schedule.type)
        print("Interval:", self.config.schedule.interval)
        print(f"Active: {'Yes' if self.config.schedule.active else 'No'}")
        
        print("=" * 28 + " END OF DETAILS " + "=" * 28)

        print()    
        print("Options: ")
        print("1. Edit Directory")
        print("2. Edit Categories")
        print("3. Edit Schedule")
        print("4. Back")
        

    def _update(self):
        option = input("Option: ")
        if option == "1":
            self.menu_manager.change_menu() 
        elif option == "2":
            ...
        elif option == "3":
            ...
        elif option == "4":
            ...