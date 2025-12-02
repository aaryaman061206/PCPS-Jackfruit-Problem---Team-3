#Importing the pandas module and matplot library
import pandas as pd
import matplotlib.pyplot as plt

#Assigning the file name and important column titles to variables for ease
file="delhi_air_quality_feature_store_processed.csv"
datec="event_timestamp"
AQI="aqi"

#Function to read the data from the selected columns in the csv file
def readdata():
    df = pd.read_csv(file)
    #Assigning all of the columns to the framework
    df.columns=[c.strip().lower() for c in df.columns]

    #Converting the values in the datec column to the datetime format
    df[datec] = pd.to_datetime(df[datec], errors="coerce")
    #Removing any NaN or NaT times
    df = df.dropna(subset=[datec, AQI])

    #Creating a new series with only the year values from the datec column
    df["year"]=df[datec].dt.year
    return df

#Function to calculate the descriptive statistics based on the daily AQI
def descriptivestatistics(df):
    #Using built-in functions to calculate mean, max, min and standard deviation of the data
    avgaqi=df[AQI].mean()
    maxaqi=df[AQI].max()
    minaqi=df[AQI].min()
    stdev=df[AQI].std()

    #Printing the statistics
    print("\n-----Delhi AQI Descriptive Statistics (2000–2024)-----")
    print(f"Mean AQI: {avgaqi:.2f}")
    print(f"Maximum AQI: {maxaqi:.2f}")
    print(f"Minimum AQI: {minaqi:.2f}")
    print(f"Standard Deviation of AQI: {stdev:.2f}")

#This function is used to sort the average AQI on a daily basis, removing time 
def fdaily(df):
    daily=df.copy()
    #Extracting the date and creating a new series to store the same
    daily["date"]=daily[datec].dt.normalize()
    #Grouping the rows based on date and calculating the mean AQI
    #Reset index is done to counteract the leftward shift of the columns
    daily=daily.groupby("date")[AQI].mean().reset_index()
    return daily.sort_values("date")

#Function to split the daily AQI mean based on the AQI categories
def categorysplit(df):
    #Calling the fdaily function to create a copy of the dataframe
    daily = fdaily(df)
    tot=len(daily)
    catcount={}
    computed=[]
    
    #Using elif to split days based on their AQI categories and appending the category to a list
    for i in daily[AQI]:
        if i <= 50:
            computed.append("Good")
        elif i <= 100:
            computed.append("Satisfactory")
        elif i <= 200:
            computed.append("Moderate")
        elif i <= 300:
            computed.append("Poor")
        elif i <= 400:
            computed.append("Very Poor")
        else:
            computed.append("Severe")  
    daily["computed"]=computed

    #FOR loop that iterates through the category column and counts the instances of each
    for i in daily["computed"]:
        if i in catcount:
            catcount[i]+=1
        else:
            catcount[i]=1

    print("\n-----Days in each AQI category (2000–2024)-----")
    for cat,c in catcount.items():
        per=c*100/tot
        print(f"{cat}: {c} days ({per:.1f}%)")

    #Calculating the number of unsafe days in the dataset (>200)
    ud=0
    for i in daily[AQI]:
        if i>200:
            ud+=1
        else:
            continue
    udper=ud*100/tot
    print("Over the last 24 years, ", ud, "out of", tot, "days have had an AQI dangerous to everyone.")
    print(f"Percentage of days with a dangerous AQI (>200): {udper:.2f}%")

#Function to plot the variation of daily mean AQI in the form of a line
def dailyline(df):
    #Calling the fdaily function to create a copy of the dataframe
    daily=fdaily(df)
    plt.figure(figsize=(12,6))
    #Inputting specifications about the  trendline
    plt.plot(daily["date"], daily[AQI], marker="*", linestyle="-", label="Daily AQI")
    #Inputting specifications about the reference lines
    for val,col,des in [
        (50, "green", "Good"),
        (100, "yellow", "Satisfactory"),
        (200, "orange", "Moderate"),
        (300, "red", "Poor"),
    ]:
        #Plotting straight lines at these reference points
        plt.axhline(val, color=col, linestyle="-", label=des)
    plt.xlabel("Date")
    plt.ylabel("AQI")
    plt.title("Daily AQI in Delhi (2000–2024)")
    plt.legend()
    plt.show()

#Function to plot the yearly mean AQI in the form of a bar chart
def yearlybar(df):
    #Calling the fdaily function to create a copy of the dataframe
    daily=fdaily(df)

    #Extracting the year and creating a new series to store the same
    daily["year"]=daily["date"].dt.year
    #Grouping the rows based on year and calculating the mean AQI
    #Reset index is done to counteract the leftward shift of the columns
    yearly=daily.groupby("year")[AQI].mean().reset_index()
    
    plt.figure(figsize=(12, 6))
    plt.bar(yearly["year"],yearly[AQI])
    plt.xlabel("Year")
    plt.ylabel("Average AQI")
    plt.title("Average Yearly AQI in Delhi (2000–2024)")
    plt.show()

#Intialising start as True to maintain an infinte loop
start=True
#Function for displaying the welcome screen
def welcomescreen():
    #All the data is stored in the dataframe 'df'
    df = readdata()
    #Since the value of start is never altered, an infinite while loop is generated for user convenience
    while start==True:
        print("\n-----Delhi Air Quality Analyzer-----")
        print("1) Descriptive Statistics")
        print("2) AQI Category Based Daily Split")
        print("3) Average Daily AQI Line Graph")
        print("4) Average Yearly AQI Bar Graph")
        print("5) Exit")

        #The user's choice of option is taken
        num=int(input("Enter choice (1-5): "))

        #The corresponding function is called
        if num==1:
            descriptivestatistics(df)
        elif num==2:
            categorysplit(df)
        elif num==3:
            dailyline(df)
        elif num==4:
            yearlybar(df)
        #If '5' is chosen, the program breaks the loop
        elif num==5:
            print("Program has been terminated.")
            break
        #An error message is displayed if a number outside the range is entered
        else:
            print("Invalid. Enter a number from 1 to 5.")

#When the program is run, the 'welcomescreen' function is called, starting the infinte loop
welcomescreen()
