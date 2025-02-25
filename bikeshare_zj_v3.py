import os
import sys
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# dict to store the City/datafile combinations.
# CSV files assumed in same directory as script file!!
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Month list used, when processing user input for date filtering.
MONTH = {0 : 'all',
         1 : 'January',
         2 : 'February',
         3 : 'March',
         4 : 'April',
         5 : 'May',
         6 : 'June',
         7 : 'July',
         8 : 'August',
         9 : 'September',
         10 : 'October',
         11 : 'November',
         12 : 'December'}

# weekdey list used, when processing user input for date filtering.
WEEKDAYS = {0 : 'Monday', 
            1 : 'Tuesday', 
            2 : 'Wednesday', 
            3 : 'Thursday',
            4 : 'Friday',
            5 : 'Saturday',
            6 : 'Sunday',
            9 : 'all'}

# number of records displayed in one batch, when browsing raw data.
BATCH_SIZE = 3

def clear_screen():
    """
        Execute "clear screen" command suitable for OS the script is running in.
        
        Args: NONE
        Returns: NONE
    """
    # Check if the OS is Windows
    if os.name == 'nt':
        os.system('cls')
    # Otherwise, assume it's a Unix-based system (macOS, Linux)
    else:
        os.system('clear')


def print_line():
    """
        Little function to print horizontal dashed line on terminal,
        with proper length (terminal columns).
        Requires import of module os.
        
        Args: NONE
        
        Returns: NONE
    """
    terminal_cols , terminal_lines = os.get_terminal_size()
    #print(terminal_cols , terminal_lines)
    print()
    print("-" * terminal_cols)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    print("You will be asked for some filters, to be used while analysing data.")
    print("Please read the hints carefully, as the input loops are operated in \'until you get it right\' mode!!")
    print_line()
    
    # get user input for city (chicago, new york city, washington). 
    # HINT: Use a while loop to handle invalid inputs
    print("City selection first. Your choices are: ")
    for key , value in CITY_DATA.items():
        print("  {}".format(key))
    print()
    
    city = ""
    city_list = list(CITY_DATA.keys())
    while city not in city_list:
        city = input("For which City do you want to analyse data? Please choose from the above set. ")
        city = city.lower()
        print("You entered: {}".format(city))
        if city not in city_list:
            print("Your choice \'{}\' is not part of available list of cities: {}.".format(city, city_list))
            print("Try again...")
    
    # Ask for date filter option to be applied.
    print()
    print("Would you like to filter the data by month (m), day (d), both (b) or not at all (n)?")
    
    date_filter_list = ['m', 'd', 'b', 'n']
    date_filter_option = ''
    while date_filter_option not in date_filter_list:
        date_filter_option = input("Enter your date filter option (m, d, b, n): ")
        date_filter_option = date_filter_option.lower()
        print("You entered: {}".format(date_filter_option))
        if date_filter_option not in date_filter_list:
            print("Your choice \'{}\' is not part of the available options {}.".format(date_filter_option, date_filter_list))
            print("Try again...")

    if date_filter_option == 'm':
        month = get_month()
        day = "all"
    elif date_filter_option == 'd':
        month = "all"
        day = get_day()
    elif date_filter_option == 'b':
        month = get_month()
        day = get_day()
    else:
        month = "all"
        day = "all"

    print_line()
    return city, month, day


def get_month():
    """
        get user input for month (all, january, february, ... , june)
        
        Args: NONE
        
        Returns: Name of month as specified in MONTH dictionnary.
    """
    
    month = 9999
    month_list = list(MONTH.keys())
    while int(month) not in month_list:
        try:
            month = int(input("Select month (0 - all, 1 - january, 2 - february, ..., 12 - december). "))
            print("You entered: {}".format(month))
            if int(month) not in month_list:
                print("Your choice {} is not available.".format(int(month)))
                print("Please try again. Your choices are: {}.".format(month_list))
        except ValueError:
            print("You entered a non-integer value.")
            print("Please try again. Your choices are: {}.".format(month_list))
    
    return MONTH[int(month)]


def get_day():
    """
        get user input for day of week (all, monday, tuesday, ... sunday)
        get user input as day-of-week-index and map to WEEKDAYS dictionnary.
        
        Args: NONE
        
        Returns: name of weekday as speicified in WEEKDAYS dictionnary.
    """
    
    day = 9999
    day_list = list(WEEKDAYS.keys())
    while int(day) not in WEEKDAYS.keys():
        try:
            day = int(input("Select weekday (9 - all,  0 - monday, 1 - Tuesday, ..., 5 - Saturday, 6 - sunday)."))
            print("You entered: {}".format(day))
            if int(day) not in day_list:
                print("Your choice {} is not available.".format(int(day)))
                print("Please try again and select from the list presented below.")
        except ValueError:
            print("You entered a non-integer value.")
            print("Please try again and select from the list presented below.")
        
    return WEEKDAYS[int(day)]


def print_filter_settings(city, month, day):
    """
        print filter settings in statistcs function: 
        
        Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        
        Returns: NONE
    """
    print("... with the following filter settings applied: city: {}, month: {}, day: {}.\n".format(city, month, day))


def dataframe_overview(df):
    """ Display basic properties of the loaded dataframe.
    
        Args:
            (df) df - dataframe holding data loaded.
            
        Returns: NONE
    
    """
    print("Dataframe basic infos:")
    print(df.info())
    print()
    
    print("Dataframe first 5 rows:")
    print(df.head())
    print()
    
    # List of columns with NULL or NaN values
    columns_with_nan = [col for col in df.columns if df[col].isnull().any()]

    print("Columns with NULL or NaN values:", columns_with_nan)
    
    print_line()


def load_data(city, month, day, script_name):
    """
        Loads data for the specified city and filters by month and day if applicable.
        The function also adds 4 columns required in the stats functions later on.
        * month
        * day
        * hour
        * StationsCombined
    

        Args:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
        
        Returns:
            df - Pandas DataFrame containing city data filtered by month and day
    """
    #city = 'test'
    # load data based in city and CITY_DATA.
    # if somehow an invalid city is encountered, terminate script.
    pathname = os.path.dirname(script_name)
    full_path = os.path.abspath(pathname)
    
    if city in CITY_DATA.keys():
        try:
            df = pd.read_csv(CITY_DATA[city])
        except FileNotFoundError as e:
            print("Error while laoding data: {}.".format(e))
            print("Check location of script and data files.")
            print("They should all be located in the same directory!!")
            print("Current working directory is: {}.".format(full_path))
            print("Terminating script...")
            exit()
            
        #print(df.head())
    else:
        print("City \'{}\' not found.".format(city))
        print("Please check against config in CITY_DATA:")
        print(CITY_DATA)
        print("Script terminated...")
        exit()
    
    # convert Start Time and End Time columns to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # For later usage in the stats functions:
    # - extract month, day of week and hour from the Start Time column and make them
    #   columns on their own.
    # - add column 'StationsCombined', by concatenating 'Start Station' and 'End Station' 
    #   agg() function used to create new column 'StationsCombined'
    df['month'] = df['Start Time'].dt.month_name()
    df['day'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    
    df['StationsCombined'] = df[['Start Station', 'End Station']].agg('/'.join, axis=1)
    #print(df.head())
    
    # apply the date filters.
    #print("Filter the dataframe with day = {} and month = {}.".format(day, month))
    if day != 'all':
        df = df[df['day'] == day]
    
    if month != 'all':
        df = df[df['month'] == month]

    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel.
       This function calculates the most frequent travel times based on the filters chosen and 
       offers a plot of the most popular starting hours.
       
        Args:
        (dataframe) df - dataframe holding the bike trip data based on the below filters.
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        
        Returns: NONE
    """

    print('\nCalculating The Most Frequent Times of Travel...')
    print_filter_settings(city, month, day)
    start_time = time.time()
    
    # display the most common month
    popular_month = df['month'].mode()[0]
    popular_month_count = df['month'].value_counts()
    #print(popular_month_count.iloc[0])
    
    print("Most popular month: {}, with a count of {}.".format(popular_month, popular_month_count.iloc[0]))
    
    # display the most common day of week
    popular_day = df['day'].mode()[0]
    popular_day_count = df['day'].value_counts()
    #print(popular_day)
    
    print("Most popular day: {}, with a count of {}.".format(popular_day, popular_day_count.iloc[0]))
    
    # display the most common start hour
    popular_start_hour = df['hour'].mode()[0]
    popular_start_hour_count = df['hour'].value_counts(sort = False)
    #print(popular_start_hour_count)
    
    print("Most popular start hour: {}, with a count of {}.".format(popular_start_hour, popular_start_hour_count.iloc[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    
    # Plot value counts, if desired.
    print("Would you like to see a plot showing the trip start hour counts?")
    show_plot = input("Type \'yes\' to get it or anything else to continue with next stats function.")
    
    if show_plot.lower() == 'yes':
        popular_start_hour_count.sort_index().plot(kind='bar', color='skyblue')
        plt.xlabel('Start Hour')
        plt.ylabel('Count')
        plt.title('Value Counts of bike trip start hours \nwith filter: city: {}, month: {}, day: {}.'.format(city, month, day))
        plt.show()
    
    print_line()


def station_stats(df, city, month, day):
    """Displays statistics on the most popular stations and trip.
        This function calculates the most frequently occuring start end end stations, as well as the most
        popular start/end station combination based on the filters chosen and 
        offers a plot of the most popular start/end station combination.
        
        Args:
        (dataframe) df - dataframe holding the bike trip data based on the below filters.
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        
    Returns:
        NONE
    """

    print('\nCalculating The Most Popular Stations and Trip...')
    print_filter_settings(city, month, day)
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_count = df['Start Station'].value_counts()
    #print(popular_start_station_count)
    
    print("Most popular start station: {}, with a count of {}.".format(popular_start_station, popular_start_station_count.iloc[0]))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_station_count = df['End Station'].value_counts()
    #print(popular_start_station_count)
    
    print("Most popular end station: {}, with a count of {}.".format(popular_end_station, popular_end_station_count.iloc[0]))

    # display most frequent combination of start station and end station trip
    popular_start_end_combi = df['StationsCombined'].mode()[0]
    popular_start_end_combi_count = df['StationsCombined'].value_counts()
    #print(popular_start_station_count)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    
    # Plot value counts, if desired.
    print("Would you like to see a plot showing the top 10 start/end station combination counts?")
    show_plot = input("Type \'yes\' to get it or anything else to continue with next stats function.")
    
    if show_plot.lower() == 'yes':
        no_of_bars = 10
        # since the start/end station combinations are loo long for display as x tics, customize the x-tick labels with abbreviations
        #labels = [f'Start/End {i}' for i in range(no_of_bars)]
        
        popular_start_end_combi_count.head(no_of_bars).sort_index().plot(kind='bar', color='skyblue')
        plt.xlabel('Start/End Station')
        plt.ylabel('Count')
        plt.xticks(fontsize=8, rotation=45)
        #plt.xticks(ticks=np.arange(no_of_bars, 1), labels=labels)
        plt.title('Value Counts of start/end station combinations \nwith filter: city: {}, month: {}, day: {}.'.format(city, month, day))
        plt.show()

    print_line()


def trip_duration_stats(df, city, month, day):
    """Displays statistics on the total and average trip duration.
    
    Args:
        (dataframe) df - dataframe holding the bike trip data based on the below filters.
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        
        This function calculates the overall duration of all trips as well as the average
        trip duration.
        
    Returns:
        NONE
    """

    print('\nCalculating Trip Duration...')
    print_filter_settings(city, month, day)
    start_time = time.time()

    # display total travel time
    print("Total travel time: {}.".format(df['Trip Duration'].sum()))
    
    # display mean travel time
    print("Average travel time: {}.".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_line()


def user_stats(df, city, month, day):
    """Displays statistics on bikeshare users.
        This function displays user types and some birth year statistics.
        A plot with the most frequently occuring birth years can be generated, if required.
    
     Args:
        (dataframe) df - dataframe holding the bike trip data based on the below filters.
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        
    Returns:
        NONE
    """

    print('\nCalculating User Stats...')
    print_filter_settings(city, month, day)
    start_time = time.time()

    # Display counts of user types and the corresponding percentages
    user_types = df['User Type'].value_counts(dropna=False)
    user_types_percentage = df['User Type'].value_counts(normalize=True, dropna=False) * 100
    combined_uytpe = pd.concat([user_types, user_types_percentage], axis=1)

    # Iterate through the dataframe and print all items.
    print("User type statistics:")
    for index, row in combined_uytpe.iterrows():
        print("User type: {}, Count: {}, Percentage: {}%".format(index, row['count'], round(row['proportion'], 2)))

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts(dropna=False)
        gender_percentage = df['Gender'].value_counts(normalize=True, dropna=False) * 100
        combined_gender = pd.concat([gender_counts, gender_percentage], axis=1)
        
        # iterate through series and print all items.
        print("\nGender statistics:")
        for index, row in combined_gender.iterrows():
            print("Gender: {}, Count: {}, Percentage: {}%".format(index, row['count'], round(row['proportion'], 2)))
    else:
        print("No gender info in dataset for {}.".format(city))

    
    # Display earliest, most recent, and most common year of birth.
    print("\nBirth year statatistics:")
    if 'Birth Year' in df.columns:
        min_birth_year = int(df['Birth Year'].min())
        max_birth_year = int(df['Birth Year'].max())
        
        print("Min birth year is: {}".format(min_birth_year))
        print("Max birth year is: {}".format(max_birth_year))
        
        popular_birth_year = df['Birth Year'].mode()[0]
        popular_birth_year_count = df['Birth Year'].value_counts()
        #print(popular_start_station_count)
    
        print("Most popular birth year: {}, with a count of {}.".format(int(popular_birth_year), popular_birth_year_count.iloc[0]))
        
        # Plot value counts, if required.
        print("Would you like to see a plot showing the top 10 birth year counts?")
        show_plot = input("Type \'yes\' to get it or anything else to get back to main menue.")
        
        if show_plot.lower() == 'yes':
            no_of_bars = 10
            # since the start/end station combinations are loo long for display as x tics, customize the x-tick labels with abbreviations
            #labels = [f'Start/End {i}' for i in range(no_of_bars)]
            
            popular_birth_year_count.head(no_of_bars).sort_index().plot(kind='bar', color='skyblue')
            plt.xlabel('Brih Year')
            plt.ylabel('Count')
            plt.xticks(fontsize=8, rotation=45)
            #plt.xticks(ticks=np.arange(no_of_bars, 1), labels=labels)
            plt.title('Value Counts of birth years \nwith filter: city: {}, month: {}, day: {}.'.format(city, month, day))
            plt.show()
            
        else:
            print("Birth year info not available in dataset for {}.".format(city))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print_line()


def browse_data(df):
    """
        Browse the dataset records in batches of BATCH_SIZE.
        
        Args:
            (df) df - dataframe loaded.
            
        Returns: NONE
    """
    rows, columns = df.shape
    print("Rows: {}, columns: {}.".format(rows, columns))
    
    loop_control = 'm'
    i = 0
    row_index = 0
    
    # Display the dataset BATCH_SIZE rows at a time, as a dictionnary for better readability of raw data (hopefully).
    # iterate over all rows, but maintain a counter, that stops after BATCH_SIZE rows, 
    # if more is required, reset counter.
    i = 0
    for index, row in df.iterrows():
        print("Row {}: {}".format(index, row.to_dict()))
        i +=1
        if i == BATCH_SIZE:
            loop_control = input("Press \'m\' for more, anything else to quit browsing mode: ")
            if loop_control != 'm': 
                break
            i = 0
    
    print_line()


def main(argv):
    
    clear_screen()
    
    while True:
        city, month, day = get_filters()
        
        print("Your filter choices:")
        print("City: {}.".format(city))
        print("Month(s): {}.".format(month))
        print("Day(s): {}".format(day))
        
        print("Loading data...")
        start_time = time.time()
        
        # pass the script name to load function, 
        # so that it can be used in case of error encountered while loading data.
        df = load_data(city, month, day, sys.argv[0])
        
        print("... data loaded. This took %s seconds." % (time.time() - start_time))
        print_line()
        
        decision = 'i'
        #while decision in ('b', 'i', 'x'):
        while True:
            try: 
                print("Your options are:")
                decision = input("\'b\' to browse raw data,\
                                \n\'i\' for dataset basic info and summary,\
                                \n\'x\' to execute the stats functions and \
                                \nany other key to go back to main menue. ")
                print("your decison is: ",  decision)
        
                if decision == 'b':
                    browse_data(df)
                elif decision == 'i':
                    dataframe_overview(df)
                elif decision == 'x':
                    time_stats(df , city, month, day)
                    station_stats(df , city, month, day)
                    trip_duration_stats(df , city, month, day)
                    user_stats(df , city, month, day)
                else:
                    print("Back to main menue...")
                    break
            except ValueError:
                print("Invalid input.")

        restart = input('\nWould you like to restart? Enter yes to restart and anything else to quit: ')
        if restart.lower() != 'yes':
            print("Terminating script. Good bye...")
            break


if __name__ == "__main__":
    main(sys.argv)
