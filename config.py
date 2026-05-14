"""
File for path to different directories of project
"""

from pathlib import Path

# Path to project directory
PATH = Path(__file__).parent
PATH_TO_PRICE = PATH / "data" / "price.json"
PATH_TO_DATA = PATH / "data"


if __name__ == "__main__":
    print(type(PATH_TO_PRICE))