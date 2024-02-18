# %%

import os
import sys
from typing import List
from natsort import natsorted


class FileProcessor:
    """
    FileProcessor class is responsible for handling file operations such as building lists of file paths.

    To run this class use the following code snippet:

    processor: FileProcessor = FileProcessor()

    DIRECTORY: str = "path/to/directory"
    FILE_EXTENSION: str = "igc"

    file_paths: List[str] = processor.get_file_paths(DIRECTORY, FILE_EXTENSION)

    for path in file_paths:
        print(f"File path: {path}")
    """

    def __init__(self) -> None:
        pass

    def get_file_paths(self, path: str, file_extension: str) -> List[str]:
        """
        Returns a list of file paths in the given directory and sort by filename.

        Args:
        - path (str): Directory path.
        - file_extension (str): File extension.
        """

        if not os.path.isdir(path):
            raise ValueError(f"{path} is not a directory.")

        if not path.endswith("/"):
            path += "/"

        file_paths: List[str] = [
            os.path.join(path, file)
            for file in os.listdir(path)
            if file.endswith(file_extension)
        ]

        return natsorted(file_paths)


# %%
