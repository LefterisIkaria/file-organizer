import logging
from app_context import AppContext
from src.setup import setup_environment
from src.file_organizer import FileOrganizer
from src.cli import MainMenu, MenuManager

# Configure logging
LOG = logging.getLogger(__name__)


def main():

    # Set up the application folders and logging
    setup_environment()
    
    app_context = AppContext()

    menu_manager = MenuManager(RootMenu=MainMenu, ctx=app_context)
    menu_manager.run()


if __name__ == "__main__":
    main()
