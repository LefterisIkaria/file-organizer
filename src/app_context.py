from config_service import IConfigService
from file_organizer import FileOrganizer


class AppContext:
    """
    The AppContext class represents the application's context, providing 
    centralized access to services and utilities used throughout the application.
    
    Attributes:
        service (IConfigService): An instance of a configuration service.
        organizer (FileOrganizer): An instance of the file organizer utility.
    """
    def __init__(self, service: IConfigService, organizer: FileOrganizer) -> None:
        self.service = service
        self.organizer = organizer