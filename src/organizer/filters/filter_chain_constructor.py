from src.organizer.filters.directory_filters import (
    DirectoryExistenceFilter, DirectoryCriticalFilter, DirectoryPermissionsFilter)
from src.organizer.filters.category_filters import (
    CategoryExistenceFilter, CategoryExtensionSubdirsValidationFilter)
from src.organizer.filters.file_filters import (
    FileHiddenFilter, FileValidationFilter, FileExtensionFilter)
from src.organizer.filters.organize_filters import (
    MoveFilesToCategoriesFilter, CategorizeByExtensionFilter, CleanupFilter)
from src.organizer.filter_chain import FilterChain


def build_filter_chain() -> FilterChain:
    # Instantiate filters
    filters = [
        DirectoryExistenceFilter(),
        DirectoryCriticalFilter(),
        DirectoryPermissionsFilter(),
        CategoryExistenceFilter(),
        CategoryExtensionSubdirsValidationFilter(),
        FileHiddenFilter(),
        FileValidationFilter(),
        FileExtensionFilter(),
        MoveFilesToCategoriesFilter(),
        CategorizeByExtensionFilter(),
        CleanupFilter()
    ]

    # Construct the filter chain
    return FilterChain(filters)
