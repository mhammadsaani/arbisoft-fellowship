import argparse
import csv 
from constants import RECOVERED_RATIO, SAFETY_MEASURE_ARG, MOST_EFFICIENT_SAFETY_MEASURES, GRAPHICAL_DISPLAY, COVID_FILES_PATH, CASES_STATS, SAFETY_MEASURES, TASK_FLAGS


def parse_arguments() -> object:
    """Parse the command line arguments into object

    Returns:
        object with report and weatehrman_data_path as attributes
    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        COVID_FILES_PATH, help="data_dir"
    )
    parser.add_argument(
        TASK_FLAGS[RECOVERED_RATIO], '--recovered_ratio', help="To find the recovered ratio of country"
    )
    parser.add_argument(
        TASK_FLAGS[SAFETY_MEASURE_ARG], '--safety_measure', help="To find average death rate"
    )
    parser.add_argument(
        TASK_FLAGS[MOST_EFFICIENT_SAFETY_MEASURES], '--most_efficient_safetey_measures',
        action="store_true", help="To find top 5 efficient safety measures"
    )
    parser.add_argument(
        TASK_FLAGS[GRAPHICAL_DISPLAY], '--graphical_display_of_efficient_safety_measures'
        ,action="store_true", help="See a bar plot of most efficient safety measures"
        )
    args = parser.parse_args()    
    return args


def read_files(covid_analyzer_file_path: str) -> dict:
    """read the files in the given path to covid dictionary

    Args:
        covid_data (dict): a dictionay where data needs to be stroed
        covid_analyzer_file_path (str): path wehre files exist
    """
    
    covid_data = {
        CASES_STATS: [],
        SAFETY_MEASURES: []
    }
    
    with open(f'{covid_analyzer_file_path}/covid_cases_stats.csv') as csv_file:
        covid_cases_stats = csv.reader(csv_file, delimiter=',')
        covid_data[CASES_STATS] = [
            covid_data_per_country for covid_data_per_country in covid_cases_stats
            ]
        covid_data[CASES_STATS] = covid_data[CASES_STATS][1:-8]
        
    with open(f'{covid_analyzer_file_path}/covid_safety_measures.csv') as csv_file:
        covid_safety_measures = csv.reader(csv_file, delimiter=',')
        covid_data[SAFETY_MEASURES] = [
            covid_data_per_country for covid_data_per_country in covid_safety_measures
            ]
        covid_data[SAFETY_MEASURES] = covid_data[SAFETY_MEASURES][1:]
    return covid_data
