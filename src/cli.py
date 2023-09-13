import os
import sys
from app_context import AppContext
from models import Category, Config, Schedule
from app_context import AppContext
from utils import clear_console, Table, get_template_config

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
    
    def restart(self, data: dict[str, any] = {}):
        self.current_menu._exit(data)
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

    def _enter(self, data: dict[str, any] = {}):
        headers = ["Directory", "Categories", "Schedule", "Active"]
        table_data = [
            (config.directory, str(len(config.categories)), str(config.schedule.active), str(config.active)) 
            for config 
            in self.ctx.service.get_configs()
        ]

        self.config_table = Table(headers=headers, data=table_data)
    
    def _display(self):
        print("Configuration list")
        if self.config_table.empty():
            print("No configs found...")
        else:
            self.config_table.draw_table()
        
        print()

        print("Choose action:")
        print("   --show      <directory>")
        print("   --create")
        print("   --delete    <directory>")
        print("   --search    <directory>/<empty>")
        print("   --organize  <directory>/<empty>")
        print("   --reset")
        print("   --help")
        print("   --exit")
        
    
    
    def _update(self):
        action = input("Action: ")
        if "--show" in action:
            try:
                dir = action.split()[1]
                config = self.ctx.service.get_config(directory=dir)
                if config:
                    self.menu_manager.change_menu(ConfigShowMenu(self.menu_manager, self.ctx), {'config': config})
                else:
                    input(f"config in directory path `{dir}` not found...")
            except IndexError as e:
                input("You dind't specify a directory...")
        elif "--create" in action:
            self.menu_manager.change_menu(ConfigCreateMenu(self.menu_manager, self.ctx))
        elif "--delete" in action:
            try:
                dir = action.split()[1]
                config = self.ctx.service.get_config(directory=dir)
                if config:
                    self.ctx.service.delete_config(directory=config.directory)
                    self.menu_manager.restart()
                    input(f"Deleted config for {dir}")
                else:
                    input(f"config in directory path `{dir}` not found...")
            except IndexError as e:
                input("You dind't specify a directory...")
            except Exception as e:
                input(f"Something went wrong deleting config of directory: {dir}")
        elif "--search" in action:
            try:
                searched = action.split()[1]
                # Filtering the configs based on the search term
                matched_configs = [config for config in self.ctx.service.get_configs() if searched.lower() in config.directory.lower()]
            
                # Display the matched configurations in a table format
                data = [
                    (config.directory, str(len(config.categories)), str(config.schedule.active), str(config.active)) 
                    for config in matched_configs
                ]
            
                self.config_table.set_data(data)
            except IndexError as e:
                data = [
                    (config.directory, str(len(config.categories)), str(config.schedule.active), str(config.active)) 
                    for config 
                    in self.ctx.service.get_configs()
                ]
                self.config_table.set_data(data)
        elif "--organize" in action:
            try:
                dir = action.split()[1]
                config = self.ctx.service.get_config(directory=dir)
                if config:
                    self.ctx.organizer.process_config(config)
            except IndexError as e:
                configs = self.ctx.service.get_configs()
                self.ctx.organizer.process_configs(configs)
            finally:
                input("Finished organizing")
        elif "--reset" in action:
            try:
                dir = action.split()[1]
                config = self.ctx.service.get_config(directory=dir)
                if config:
                    self.ctx.organizer.reset_directory(directory=config.directory, categories=config.categories)
                    self.ctx.organizer.cleanup_directory(directory=config.directory, categories=config.categories)
                
                input(f"Finished reseting {dir}")
            except IndexError as e:
                input("You didn't specifiy a directory")
        elif "--help" in action:
            self.menu_manager.change_menu(HelpMenu(self.menu_manager, self.ctx))
        elif "--exit" in action:
            sys.exit(0)
        else:
            input(f"This action don't exists: {action}")


class ConfigCreateMenu(Menu):
 

    def _display(self):
        print("Create new Config")
        print("Options:")
        print("1. From template")
        print("2. New config")
        print("3. Back")
    
    def _update(self):
        option = input("Option: ")
        if option == "1":
            dir = input("Directory path: ")
            found = self.ctx.service.get_config(dir)
            if found:
                input(f"Config already exists for {found} directory")
                return
            
            if not os.path.exists(dir):
                input(f"path: {dir} don't exists")
            
            config = get_template_config()
            if config:
                config.directory = dir
                self.ctx.service.create_config(config)
                input(f"Config for {dir} created succesfully")
            else:
                input("Something went wrong, couldn't create config from template")
        elif option == "2":
            dir = input("Directory path: ")
            found = self.ctx.service.get_config(dir)
            if found:
                input(f"Config already exists for {found} directory")
                return

            config = Config(directory=dir)

            categories_input = input("Add Categories: ")
            for category_name in set(categories_input.strip().split(",")):
                category = Category(name=category_name)
                config.categories.add(category)

            input(f"Added {len(config.categories)} categories")
            confirm = input("Save config? (yes/no)")
            if confirm == "yes":
                self.ctx.service.create_config(config)
                input(f"Created new config for directory: {dir}")
        elif option == "3":
            self.menu_manager.back()


class HelpMenu(Menu):

    def _enter(self, data: dict[str, any] = {}):
        headers = ["Action", "Params", "Description"]
        data = [
            ("--show", "<directory>", "Show details for the config in the specified directory."),
            ("--create", "", "Open menu to create a new configuration file."),
            ("--delete", "<directory>", "Deletes a configuration of the specified directory"),
            ("--search", "<directory>/<empty>", "Search for a configuration by the directory, reset table if no params"),
            ("--organize", "<directory>/<empty>", "Run the organizer for all configs if no params else for a specific config."),
            ("--reset", "<directory>", "Reset the directory for a specific config."),
            ("--exit", "", "Close the programm"),
        ]
        self.help_table = Table(headers=headers, data=data)

    def _display(self):
        print("Help")
        self.help_table.draw_table()
        print("Options: ")
        print("1. Back")

    def _update(self):
        option = input("Options")
        if option == "1":
            self.menu_manager.back()
        else:
            input(f"Invalid option: {option}")
        
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
            self.menu_manager.change_menu(ConfigEditDirectoryMenu(self.menu_manager, self.ctx), {'config': self.config}) 
        elif option == "2":
            self.menu_manager.change_menu(ConfigEditCategoriesMenu(self.menu_manager, self.ctx), {'config': self.config})
        elif option == "3":
            self.menu_manager.change_menu(ConfigEditScheduleMenu(self.menu_manager, self.ctx), {'config': self.config})
        elif option == "4":
            self.menu_manager.back()


class ConfigEditDirectoryMenu(Menu):

    def _enter(self, data: dict[str, any] = {}):
        self.config: Config = data.get('config', None)

        if not self.config:
            input("Config was not provided..")
            self.menu_manager.back()
            return


    def _display(self):
        print(f"Directory: {self.config.directory}")

        print("Options:")
        print("1. Change path")
        print("2. Back")
    

    def _update(self):
        option = input("Option: ")

        if option == "1":
            new_dir = input("Change path to: ")

            try:
                existing_config = self.ctx.service.get_config(new_dir)
                if existing_config:
                    raise ValueError("Another config already exists for this directory path.")
                if not os.path.exists(new_dir):
                    raise ValueError(f"The path `{new_dir}` don't exists")
                
                print(f"Do you confirm the new path? (yes/no): {new_dir}")
                confirm = input()

                if confirm == "yes":
                    old_dir = self.config.directory
                    self.config.directory = new_dir
                    self.ctx.service.update_config(directory=old_dir, config=self.config)
                    self.menu_manager.back({'config': self.config})

            except Exception as e:
                input(f"Error: {e}")
        elif option == "2":
            self.menu_manager.back({'config': self.config})


class ConfigEditCategoriesMenu(Menu):

    def _enter(self, data: dict[str, any] = {}):
        self.config: Config = data.get('config', None)

        if not self.config:
            input("Config was not provided..")
            self.menu_manager.back()
            return
    

        headers = ["Name", "Extensions", "Categorize Ext."]
        
        data = []
        for category in self.config.categories:
            data.append((
                category.name,
                str(category.extensions),
                str(category.categorize_extensions)
            ))

        self.categories_table = Table(headers=headers, data=data)

    
    def _display(self):
        print(f"Directory: {self.config.directory}")
        print("Categories")
        self.categories_table.draw_table()
        print("Options:")
        print("1. Add Category")
        print("2. Rename Category")
        print("3. Remove Category")
        print("4. Add Extension(s)")
        print("5. Remove Extension(s)")
        print("6. Toggle Categorize Ext.")
        print("7. Back")

    def _update(self):
        option = input("Option: ")

        if option == "1":
            self.add_category()
        elif option == "2":
            self.rename_category()
        elif option =="3":
            self.remove_category()
        elif option == "4":
            self.add_extensions()
        elif option == "5":
            self.remove_extensions()
        elif option == "6":
            self.toggle_categorize_extensions()
        elif option == "7":
            self.menu_manager.back({'config': self.config})
        
    
    def add_category(self):
        try:            
            # Handle name
            category_name = input("Category name: ")
            if category_name in [category.name for category in self.config.categories]:
                input(f"Category {category_name} already exists.")
                return
            new_category = Category(name=category_name)

            # Handle extensions
            extensions_input = input("Add extensions: ")
            self.add_extensions_to_category(new_category, extensions_input)

            # Handle Categorize extensions
            categorize = input("Categorize Extensions? (yes/no)")
            new_category.categorize_extensions = categorize.lower() == "yes"

            # Save category
            self.config.categories.append(new_category)
            self.ctx.service.update_config(self.config.directory, self.config)

            # restart manu
            self.menu_manager.restart({'config': self.config})
        except Exception as e:
            if new_category in self.config.categories:
                self.config.categories.remove(new_category)
            
            input(f"Error {e}")

    def add_extensions_to_category(self, new_category, extensions_input):
        extensions_added = 0
        if extensions_input:
            all_extensions = {ext for category in self.config.categories for ext in category.extensions}
            extensions = extensions_input.strip().split(",")
            for ext in extensions:
                extension = ext
                if not ext.startswith("."):
                    extension = "." + ext
                    
                if extension not in all_extensions:
                    new_category.extensions.append(extension)
                    extensions_added += 1
                else:
                    print(f"{extension} already exists in another category")
        
        return extensions_added


    def remove_extensions_from_category(self, category, extensions_input):
        extensions_removed = 0
        if extensions_input:
            # all_extensions = {ext for category in self.config.categories for ext in category.extensions}
            extensions = extensions_input.strip().split(",")
            for ext in extensions:
                extension = ext
                if not ext.startswith("."):
                    extension = "." + ext
                    
                if extension not in category.extensions:
                    print(f"{extension} don't exists in {category.name}")
                else:
                    category.extensions.remove(extension)
                    extensions_removed += 1
        
        return extensions_removed        
    

    def rename_category(self):
        category_name = input("Name of category: ")
        for category in self.config.categories:
            if category_name == category.name:
                new_category_name = input(f"Rename {category_name} to: ")
                if new_category_name not in [category.name for category in self.config.categories]:
                    category.name = new_category_name
                else:
                    input(f"The name {new_category_name} already exists.")
                    return
        try:
            self.ctx.service.update_config(self.config.directory, self.config)
            self.menu_manager.restart({'config': self.config})
        except Exception as e:
            input(f"{e}")
    

    def remove_category(self):
        category_name = input("Category name: ")
        if not category_name:
            return
        if category_name not in [category.name for category in self.config.categories]:
            input(f"{category_name} don't exists in this config")
            return
        
        for category in self.config.categories:
            if category.name == category_name:
                self.config.categories.remove(category)
                self.ctx.service.update_config(self.config.directory, self.config)
                input(f"Removed {category_name}")
                self.menu_manager.restart({'config': self.config})
                return
    
    def add_extensions(self):
        category_name = input("Category name: ")
        if not category_name or category_name not in [category.name for category in self.config.categories]:
            input(f"{category_name} don't exists")
            return

        for category in self.config.categories:
            if category.name == category_name:

                extensions_input = input("Add extensions: ")
                added_extensions = self.add_extensions_to_category(category, extensions_input)

                self.ctx.service.update_config(self.config.directory, self.config)
                input(f"Added {added_extensions} extensions to {category_name}")
                self.menu_manager.restart({'config': self.config})
                return
    

    def remove_extensions(self):
        category_name = input("Category name: ")
        if not category_name or category_name not in [category.name for category in self.config.categories]:
            input(f"{category_name} don't exists")
            return

        for category in self.config.categories:
            if category.name == category_name:

                extensions_input = input("Remove extensions: ")
                removed_extensions = self.remove_extensions_from_category(category, extensions_input)

                self.ctx.service.update_config(self.config.directory, self.config)
                self.menu_manager.restart({'config': self.config})
                input(f"Removed {removed_extensions} from {category_name}")
                return


    def toggle_categorize_extensions(self):
        category_name = input("Category name: ")
        if not category_name:
            return
        if category_name not in [category.name for category in self.config.categories]:
            input(f"{category_name} don't exists in this config")
            return

        for category in self.config.categories:
            if category.name == category_name:
                category.categorize_extensions = not category.categorize_extensions

                self.ctx.service.update_config(self.config.directory, self.config)
                self.menu_manager.restart({'config': self.config})
                input(f"{category_name} categorize ext. now is {category.categorize_extensions}")
                return


class ConfigEditScheduleMenu(Menu):

    SCHEDULE_TYPES = {
        1: "MINUTE",
        2: "HOUR",
        3: "WEEK",
        4: "MONTH",
        5: "YEAR"
    }


    def _enter(self, data: dict[str, any] = {}):
        self.config: Config = data.get('config', None)

        if not self.config:
            input("Config was not provided..")
            self.menu_manager.back()
            return
    

    def _display(self):
        print(f"Directory: {self.config.directory}")
        print()
        print("Schedule:")
        print(f"Type: {self.config.schedule.type}")
        print(f"Interval: {self.config.schedule.interval}")
        print(f"Active: {self.config.schedule.active}")
        print("Options:")
        print("1. Select type")
        print("2. Change Interval")
        print("3. Toggle Active")
        print("4. Back")
    

    def _update(self):
        option = input("Option: ")

        if option == "1":
            print("types")
            for num, type in self.SCHEDULE_TYPES.items():
                print(f"{num}. {type}")
            
            num = input("Select type: ")
            if not str.isdigit(num):
                input(f"Option {num} not a number")
                return
            
            num = int(num)
            
            if not num in self.SCHEDULE_TYPES.keys():
                input(f"Option {num} don't exists")
                return
            
            type = self.SCHEDULE_TYPES[num]
            self.config.schedule.type = type
            self.ctx.service.update_config(self.config.directory, self.config)
            self.menu_manager.restart({'config': self.config})
            input(f"Setted type to {type}")
        elif option == "2":
            interval = input("Select interval: ")
            if not str.isdigit(interval):
                input(f"{interval} is not a digit")
                return
            
            self.config.schedule.interval = interval
            self.ctx.service.update_config(self.config.directory, self.config)
            self.menu_manager.restart({'config': self.config})
            input(f"Setted interval to {interval}")
        elif option == "3":
            is_active = self.config.schedule.active
            self.config.schedule.active = not is_active
            self.ctx.service.update_config(self.config.directory, self.config)
            self.menu_manager.restart({'config': self.config})
            input(f"Toggled schedule from {is_active} to {self.config.schedule.active}")
        elif option == "4":
            self.menu_manager.back({'config': self.config})
        else:
            input(f"Invalid option: {option}")

