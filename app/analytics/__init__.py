from app.analytics.handel_null_invalid import main as validate_main
from app.analytics.convert_column_type import main as conv_main
from app.analytics.remove_dublication import main as rem_main

def main():
    validate_main()
    conv_main()
    rem_main()