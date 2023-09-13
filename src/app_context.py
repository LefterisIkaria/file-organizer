from config_service import IConfigService
from file_organizer import FileOrganizer


class AppContext:
    def __init__(self, service: IConfigService, organizer: FileOrganizer) -> None:
        self.service = service
        self.organizer = organizer