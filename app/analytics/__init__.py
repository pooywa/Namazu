from app.analytics.handel_null_invalid import main as validate_main
from app.analytics.convert_column_type import main as conv_main
from app.analytics.remove_dublication import main as rem_main
from app.analytics.clean_region import clean_regions
from app.analytics.analytics import main as analy_main
from app.analytics.combine_region_and_category import main as comb_main
from app.analytics.filter_and_sort import main as filter_main
from app.analytics.add_index import main as indexing_main
from app.analytics.fill_data_to_earthquakes import main as fill_main

def main():
    validate_main()
    conv_main()
    rem_main()
    fill_main()
    analy_main()
    comb_main()
    filter_main()
    indexing_main()