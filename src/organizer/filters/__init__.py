from .directory_filters import DirectoryPermissionsFilter, DirectoryExistenceFilter, DirectoryCriticalFilter
from .category_filters import CategoryExistenceFilter, CategoryExtensionSubdirsValidationFilter
from .file_filters import FileExtensionFilter, FileHiddenFilter, FileValidationFilter
from .organize_filters import CategorizeByExtensionFilter, MoveFilesToCategoriesFilter, CleanupFilter


ORGANIZER_FILTERS = [
    DirectoryPermissionsFilter,
    DirectoryCriticalFilter,
    DirectoryExistenceFilter,
    CategoryExistenceFilter,
    CategoryExtensionSubdirsValidationFilter,
    FileExtensionFilter,
    FileHiddenFilter,
    FileValidationFilter,
    MoveFilesToCategoriesFilter,
    CategorizeByExtensionFilter,
    CleanupFilter
]