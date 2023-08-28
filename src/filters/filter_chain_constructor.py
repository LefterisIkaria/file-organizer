from filters.directory_filters import (
    DirectoryExistenceFilter, DirectoryCriticalFilter, DirectoryPermissionsFilter)
from filters.category_filters import (
    CategoryExistenceFilter, CategoryExtensionSubdirsValidationFilter)
from filters.file_filters import (
    FileHiddenFilter, FileValidationFilter, FileExtensionFilter)
from filters.organize_filters import (
    MoveFilesToCategoriesFilter, CategorizeByExtensionFilter, CleanupFilter)
from filter_chain import FilterChain


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
