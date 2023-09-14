from utils import clear_console
from app_context import AppContext



class MenuManager:
    """
    Manages the navigation and state of menus in the application.
    
    Attributes:
        root_menu (Menu): The starting menu of the application.
        menus_stack (list[Menu]): A stack representing the navigation history of menus.
        ctx (AppContext): The application context that is provided to all menus
    """
    def __init__(self, RootMenu: type['Menu'], ctx: AppContext, initial_data: dict[str, any] = {}):
        
        self.root_menu = RootMenu(self, ctx)
        self.root_menu._enter(data=initial_data)
        
        self.menus_stack = [self.root_menu]

    @property
    def current_menu(self) -> 'Menu':
        """Returns the current active menu."""
        return self.menus_stack[-1]

    def change_menu(self, new_menu: 'Menu', data: dict[str, any] = {}):
        """Changes to a new menu."""
        self.current_menu._exit(data)
        self.menus_stack.append(new_menu)
        self.current_menu._enter(data)

    def back(self, data: dict[str, any] = {}):
        """Navigates back to the previous menu."""
        if len(self.menus_stack) > 1:
            self.menus_stack.pop()._exit(data)
            self.current_menu._enter(data)
    
    def restart(self, data: dict[str, any] = {}):
        """Restarts the current menu."""
        self.current_menu._exit(data)
        self.current_menu._enter(data)
    
    def back_to_root(self, data: dict[str, any] = {}):
        """Navigates back to the root menu."""
        while self.current_menu != self.root_menu:
            self.back(data)

    def exit(self):
        """Exits the application."""
        self.back_to_root()
        self.root_menu._exit()
        exit(0)

    def run(self):
        """Main loop to run the menu system."""
        while True:
            clear_console()
            self.current_menu._display()
            self.current_menu._update()


class Menu:
    """
    Base class for all menus in the application.
    
    Attributes:
        menu_manager (MenuManager): The manager handling this menu.
        ctx (AppContext): The application context.
    """
   
    def __init__(self, menu_manager: MenuManager, ctx: AppContext):
        self.menu_manager = menu_manager
        self.ctx = ctx
    
    def _enter(self, data: dict[str, any] = {}):
        """
        Initialize method that called when entering a menu.
        
        Args:
            data (dict[str, any], optional): Additional data for menu initialization. Defaults to an empty dictionary.
        """
        pass

    def _display(self):
        """Displays the content and options of this menu."""
        pass

    def _update(self):
        """Updates the state and handles user input for this menu."""
        pass

    def _exit(self, data: dict[str, any] = {}):
        """
        Finalize method called when exiting a menu.
        
        Args:
            data (dict[str, any], optional): Additional data for menu cleanup. Defaults to an empty dictionary.
        """
        pass