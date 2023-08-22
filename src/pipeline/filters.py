import os
import shutil
import logging

from typing import Dict, Any
from pathlib import Path
from pipeline.base import Filter


class ScanDirectoryFilter(Filter[Dict[str, Any], Dict[str, Any]]):
    def process(self, data: Dict[str, Any]) -> Dict[str, any]:
        # todo: path is relative to home
        directory = os.path.join(Path.home(), data['dir'])

        files = files = [f for f in os.listdir(
            directory) if os.path.isfile(os.path.join(directory, f))]

        logging.info(
            f"Scanning directory: {directory}, found {len(files)} files.")

        data['files'] = files
        return data


class MoveFilesFilter(Filter[Dict[str, Any], Dict[str, any]]):
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        directory = os.path.join(Path.home(), data['dir'])
        for file, category in data['file_categories'].items():
            src = os.path.join(directory, file)
            dest_dir = os.path.join(directory, category)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
                logging.info(f"Created new directory: {dest_dir}")
            shutil.move(src, os.path.join(dest_dir, file))
            logging.info(f"Moved file: {file} to category: {category}")
        return data


class FileClassificationFilter(Filter[Dict[str, Any], Dict[str, Any]]):
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        file_categories = {}
        misc_category = data.get('misc_category', None)

        for file in data['files']:
            ext = os.path.splitext(file)[1]
            categorized = False
            for category, extensions in data['categories'].items():
                if ext in extensions:
                    file_categories[file] = category
                    logging.info(f"Categorized file: {file} as {category}")
                    categorized = True
                    break

            if not categorized and misc_category:
                file_categories[file] = misc_category
                logging.warning(
                    f"File: {file} not categorized. Moved to: {misc_category}")

        data['file_categories'] = file_categories
        return data
