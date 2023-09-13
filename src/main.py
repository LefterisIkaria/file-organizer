import logging
from src.app_context import AppContext
from src.config_service import ConfigFileService
from src.setup import configs_path, setup_environment
from src.file_organizer import FileOrganizer
from src.cli import MainMenu, MenuManager

# Configure logging
LOG = logging.getLogger(__name__)


def main():

    # Set up the application folders and logging
    setup_environment()
    
    # Setup application ctx dependencies
    service = ConfigFileService(configs_directory=configs_path())
    organizer = FileOrganizer()
    
    # Initialize application context
    app_context = AppContext(service=service, organizer=organizer)
    
    menu_manager = MenuManager(RootMenu=MainMenu, ctx=app_context)
    menu_manager.run()


if __name__ == "__main__":
    main()
