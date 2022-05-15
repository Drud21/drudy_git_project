#-----Bike Share Project Completed by Mike Drudy on May 1, 2022-----
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

city_lst = ['Chicago', 'New York', 'Washington'] #List of cities to compare to.
month_lst = ['January', 'February', 'March', 'April', 'May', 'June', 'All'] #List of months to compare to.
day_lst = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All'] # List of days to compare to.

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    global city
    global month
    global day
    while True:
        try:
            #Ask what city and capitalize the first letter in each word
            city = input('Which city would you like to analyze? Chicago, New York, or Washington? ').title()
            if city in city_lst:
                print('You selected: {}'.format(city))
                break
            else:
                print('Error: Enter either Chicago, New York, or Washington. You entered: {}'.format(city))
        except ValueError:
            print('Sorry I didn\'t understand that.  Please try entering in a city again.')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            #Ask what month and capitalize the first letter in each word
            month = input('Which month would you like to analyze? Enter January through June or "all" for no filter. ').title()
            if month in month_lst:
                print('You selected: {}'.format(month))
                break
            else:
                print('Error: Enter "all" or the correct month. You entered: {}'.format(month))
        except ValueError:
            print('Sorry I didn\'t understand that.  Please try entering in a month again.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            #Ask what day of the week and capitalize the first letter in each word
            day = input('Which day of the week would you like to analyze? Enter Sunday through Saturday or "all" for no filter. ').title()
            if day in day_lst:
                print('You selected: {}'.format(day))
                break
            else:
                print('Error: Enter "all" or the correct day of the week. You entered: {}'.format(day))
        except ValueError:
            print('Sorry I didn\'t understand that.  Please try entering in a day again.')

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    if city == 'Chicago':
        df = pd.read_csv('./chicago.csv')
    elif city == 'New York':
        df = pd.read_csv('./new_york_city.csv')
    elif city == 'Washington':
        df = pd.read_csv('./washington.csv')
    else:
        print('Oh no, the person programing this doesn\'t know what they\'re doing!')
    #-----Create two new columns.  1 for month and 1 for day of the week-----
    #First, convert Start Time and End time from string to datetime data type
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')
    df['End Time'] = pd.to_datetime(df['End Time'], format='%Y-%m-%d %H:%M:%S')
    #Then, create the two new columns to help with filtering
    df['Start Month'] = df['Start Time'].dt.month_name()
    df['Start Day of Week'] = df['Start Time'].dt.day_name()
    #Selecting rows that are for the specified month
    if month == 'All':
        pass
    else:
        df = df[df['Start Month'] == month]
    #Selecting rows that are for the specified day of the week
    if day == 'All':
        pass
    else:
        df = df[df['Start Day of Week'] == day]
    
    print('Here are the first 5 rows of data you slected for city: {}, month: {}, day of the week: {}\n'\
        .format(city, month, day))
    print(df.head())

    print('Here are the last 5 rows of data you slected for city: {}, month: {}, day of the week: {}\n'\
        .format(city, month, day))
    print(df.tail())
    print('-'*40)

    i = 0
    j = 5
    while True:
        try:
            cont = input('\nDo you want to see more data?  Enter yes or no. ').title()
            if cont == 'Yes':
                print(df.iloc[i:j])
                i += 5
                j += 5
            elif cont == 'No':
                break
            else:
                print('\nTry again typing in either yes or no.')
        except ValueError:
            print('\nSorry I didn\'t understand that.  Please try entering in a day again.')

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'All':
        month_max = df['Start Month'].value_counts().idxmax()
        month_max_count = df['Start Month'].value_counts().max()
        print('The most common month in your selection is {} with {} occurances.\n'.format(month_max, month_max_count))
    else:
        print('Since you filtered the data by {}, the most comman month in your dataset is {}.\n'.format(month, month))

    # display the most common day of week
    if day == 'All':
        day_max = df['Start Day of Week'].value_counts().idxmax()
        day_max_count = df['Start Day of Week'].value_counts().max()
        print('The most common day of the week in your selection is {} with {} occurances.\n'.format(day_max, day_max_count))
    else:
        print('Since you filtered the data by {}, the most comman day in your dataset is {}.\n'.format(day, day))

    # display the most common start hour
    start_hour = pd.Series(df['Start Time'].dt.hour)
    hour_max = start_hour.value_counts().idxmax()
    hour_max_count = start_hour.value_counts().max()
    print('The most common hour to start renting a bike for your selection is {} with {} occurances.'.format(hour_max, hour_max_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_loc = df['Start Station'].value_counts().idxmax()
    start_loc_count = df['Start Station'].value_counts().max()
    print('The most common start station is {} with {} occurances.\n'.format(start_loc, start_loc_count))

    # display most commonly used end station
    end_loc = df['End Station'].value_counts().idxmax()
    end_loc_count = df['End Station'].value_counts().max()
    print('The most common end station is {} with {} occurances.\n'.format(end_loc, end_loc_count))

    # display most frequent combination of start station and end station trip
    trip = pd.Series(df['Start Station'] + ' to ' + df['End Station'])
    trip_max = trip.value_counts().idxmax()
    trip_max_count = trip.value_counts().max()
    print('The most common trip is {} with {} occurances.'.format(trip_max, trip_max_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = pd.Series(df['End Time'] - df['Start Time'])
    print('The total travel time for your selection is {}\n'.format(travel_time.sum()))

    # display mean travel time
    print('The average travel time for your selection is {}'.format(travel_time.mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    df2 = df.groupby('User Type')['Unnamed: 0'].nunique()
    print('The following shows the number of user types for your selection.', df2, '\n')

    # Display counts of gender
    if city == 'Washington':
        print('This city does not have any gender data to report on.\n')
    else:
        df3 = df.groupby('Gender')['Unnamed: 0'].nunique()
        print('The following shows the number of males and females for your selection.', df3, '\n')

    # Display earliest, most recent, and most common year of birth
    if city == 'Washington':
        print('This city does not have any birth year data to report on.')
    else:
        print('The earliest year of birth for your selection is {}\n'.format(df['Birth Year'].min()))
        print('The most recent year of birth for your selection is {}\n'.format(df['Birth Year'].max()))
        print('The most common year of birth for your selection is {}.'.format(df['Birth Year'].value_counts().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
