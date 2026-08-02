from app.database.preview_data import main as preview_main
from app.database.importer import main as importer_main


def main():
    importer_main()
    preview_main()