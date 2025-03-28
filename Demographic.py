import pandas as pd

def calculate_demographic_data(print_data=True):
    # Read data from file
    # Adjust the file path as needed (this assumes the CSV file is in your working directory)
    df = pd.read_csv("adult.data.csv")
    
    # 1. How many people of each race are represented in this dataset?
    race_count = df['race'].value_counts()

    # 2. What is the average age of men?
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # 3. What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round((df['education'] == 'Bachelors').mean() * 100, 1)

    # 4. What percentage of people with advanced education 
    # (Bachelors, Masters, or Doctorate) make more than 50K?
    higher_education = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    higher_education_rich = round((df[higher_education]['salary'] == '>50K').mean() * 100, 1)

    # 5. What percentage of people without advanced education make more than 50K?
    lower_education = ~higher_education
    lower_education_rich = round((df[lower_education]['salary'] == '>50K').mean() * 100, 1)

    # 6. What is the minimum number of hours a person works per week?
    min_work_hours = int(df['hours-per-week'].min())

    # 7. What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df[df['hours-per-week'] == min_work_hours]
    if len(num_min_workers) > 0:
        rich_percentage = round((num_min_workers['salary'] == '>50K').mean() * 100, 1)
    else:
        rich_percentage = 0.0

    # 8. What country has the highest percentage of people that earn >50K?
    country_group = df.groupby('native-country')
    # Compute percentage of >50K earners in each country
    country_rich_percentage = (country_group.apply(lambda x: (x['salary'] == '>50K').mean()) * 100)
    highest_earning_country_percentage = round(country_rich_percentage.max(), 1)
    highest_earning_country = country_rich_percentage.idxmax()

    # 9. Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]['occupation'].value_counts().idxmax()

    # Create the dictionary to return results
    if print_data:
        print("Number of each race:\n", race_count)
        print("\nAverage age of men:", average_age_men)
        print(f"\nPercentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"\nPercentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"\nPercentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"\nMin work time: {min_work_hours} hours/week")
        print(f"\nPercentage of rich among those who work fewest hours: {rich_percentage}%")
        print(f"\nCountry with highest percentage of rich: {highest_earning_country}")
        print(f"\nHighest percentage of rich people in country: {highest_earning_country_percentage}%")
        print(f"\nTop occupations in India: {top_IN_occupation}")
    
    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

if __name__ == '__main__':
    calculate_demographic_data()
