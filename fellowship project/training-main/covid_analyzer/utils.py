import matplotlib.pyplot as plt
from constants import (
    COUNTRY_NAME_IDX_IN_COVID_STATS, TOTAL_PATIENTS, TOTAL_RECOVERED_PATIENTS, COUNTRY_NAME_IDX_IN_COVID_SAFETY_MEASURES,
    SAFETY_MEASURES, IMPLEMENTED_SAFETY_MEASURES, TOTAL_DEATHS, EMPTY_STRING, TOTAL_CASES, ZERO, EFFICIENCY, SAFETY_MEASURE,
    CASES_STATS
    )


def get_ratio_of_recovered_patients(covid_data, country: str) -> None: 
    """Return the ratio of recovered patients of a country

    Args:
        country (str): country name (case sensitive)
 
    Returns:
        : prints Country data not available if the country's name or data do not exist,
           otherwise returns the ratio
    """
    
    for covid_cases_details_per_country in covid_data[CASES_STATS]:
        if covid_cases_details_per_country[COUNTRY_NAME_IDX_IN_COVID_STATS] == country:
            try:
                recovered_ratio = round(
                    int(covid_cases_details_per_country[TOTAL_RECOVERED_PATIENTS])
                    / int(covid_cases_details_per_country[TOTAL_PATIENTS]), 2
                )
                print(f'Recovered/total ratio: {recovered_ratio}')
                return
            except ValueError:
                 print("Country data not available")
    else:
        print("Country data not available")

    
def get_countries_following_the_safety_measure(covid_data, safety_measure: str) -> list:
    """Returns the list of countries that follows given safety measure

    Args:
        safety_measure (str): a measure country has implemented

    Returns:
        list: countries list 
    """
    
    country_following_the_safety_measures = [
        covid_safety_measures_details_per_country[COUNTRY_NAME_IDX_IN_COVID_SAFETY_MEASURES]
        for covid_safety_measures_details_per_country in covid_data[SAFETY_MEASURES]
        if covid_safety_measures_details_per_country[IMPLEMENTED_SAFETY_MEASURES] == safety_measure
    ]
    return set(country_following_the_safety_measures)


def get_average_death_rate(covid_data, safety_measure: str) -> tuple:
    """Returns the average death ratio against a safety measure
    calculated as total deaths that occurs in the specific countries which have taken economic measures) 
    divided by overall  deaths in the globe. The result is multiplied by 100.

    Args:
        safety_measure (str): the safety measure against which 
        the average death rate needs to be calculated

    Returns:
        tuple: containing the total number of countries that has implemented the safety measure and 
               average death rate
    """
    
    countries_following_the_safety_measure =  get_countries_following_the_safety_measure(covid_data, safety_measure)
    total_deaths_in_country_following_the_measures = 0
    total_deaths_around_the_globe = 0
    for covid_cases_details_per_country in covid_data[CASES_STATS]:
        if all([covid_cases_details_per_country[COUNTRY_NAME_IDX_IN_COVID_STATS] in countries_following_the_safety_measure,
                (deaths:=covid_cases_details_per_country[TOTAL_DEATHS]) != EMPTY_STRING]
            ):
                total_deaths_in_country_following_the_measures += int(deaths)
                
        if (deaths:=covid_cases_details_per_country[TOTAL_DEATHS]) != EMPTY_STRING:
            total_deaths_around_the_globe += int(deaths)

    countries, death_percentage = (len(countries_following_the_safety_measure),
           round((total_deaths_in_country_following_the_measures / total_deaths_around_the_globe) * 100, 2))
    print(f'{death_percentage}% death average found in {countries} countries. ')
    return countries, death_percentage
           
           
def get_efficiency(covid_data, countries_follwoing_the_safety_measures: list) -> int:
    """Returns the efficiency against safety measure calculated as 
        total recovered cases of all countries taken the measure 
        divided by total cases of all countries taken the measure

    Args:
        countries_follwoing_the_safety_measures (list): list of countries that follow safety measure

    Returns:
        int: efficiency value
    """

    total_recovered_cases_of_all_countries = 0
    total_cases_of_all_countries = 0
    for covid_stats_detail_per_country in covid_data[CASES_STATS]:
        country_name = covid_stats_detail_per_country[COUNTRY_NAME_IDX_IN_COVID_STATS]
        if all([
            (country_name != EMPTY_STRING),
            (country_name in countries_follwoing_the_safety_measures),
            covid_stats_detail_per_country[TOTAL_CASES] != EMPTY_STRING,
            covid_stats_detail_per_country[TOTAL_RECOVERED_PATIENTS] != EMPTY_STRING,
            covid_stats_detail_per_country[TOTAL_RECOVERED_PATIENTS] != ZERO
        ]):
            total_cases_of_all_countries += int(covid_stats_detail_per_country[TOTAL_CASES])
            total_recovered_cases_of_all_countries += int(covid_stats_detail_per_country[TOTAL_RECOVERED_PATIENTS])
                         
    if total_cases_of_all_countries == ZERO:
        return ZERO
    
    return round(total_recovered_cases_of_all_countries/total_cases_of_all_countries, 2)


def get_most_efficient_safety_measures(covid_data) -> list:
    """find most efficient safey measures with efficiency value

    Returns:
        list: top 5 most efficient measures with efficiency value
    """
    efficiencies_against_safety_measure = []
    unique_safety_measures = list(
            set([
            safety_measure_details[IMPLEMENTED_SAFETY_MEASURES] for safety_measure_details in covid_data[SAFETY_MEASURES]
            ])
    )
    for safety_measure in unique_safety_measures:
        countries_following_the_safety_measure = get_countries_following_the_safety_measure(covid_data, safety_measure)
        efficiency_for_specific_measure = get_efficiency(covid_data, countries_following_the_safety_measure)
        efficiencies_against_safety_measure.append((safety_measure, efficiency_for_specific_measure))
    return sorted(efficiencies_against_safety_measure, key=lambda x: x[EFFICIENCY], reverse=True)[:5]


def graphical_display_of_efficient_safety_measures(covid_data) -> None:
    """plot a bar graph for top 5 most efficient safety measures with efficieny value"""
    
    most_efficient_safety_measures = get_most_efficient_safety_measures(covid_data)
    safety_measures = [
        efficient_safety_measure[SAFETY_MEASURE] for efficient_safety_measure in most_efficient_safety_measures
    ]
    efficiencies = [
        efficient_safety_measure[EFFICIENCY] for efficient_safety_measure in most_efficient_safety_measures
    ]
    plt.figure('Top 5 Safety measures with Efficiencies', figsize=(10, 6))
    plt.xlabel("Efficiency Vaue")
    plt.ylabel('Safety Measure')
    plt.barh(safety_measures, efficiencies)
    plt.tight_layout() 
    plt.show()
