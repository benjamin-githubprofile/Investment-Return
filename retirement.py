import csv
import sys
from datetime import datetime


# ok heres my logics #
# 1. open all the csvs, likes the ones inside the elva files, so that it can read and calculate #
# 2. write out formula for Strategy One, Two and Three (remember to use Float) #
# 3. Under each Strategy functions, make sure they print under column 2,3,4 and date for 1#
# 4. Use write file function from notebook and export to CSV #
# 5. write process() funciton and run with the python3 command on Sakai #

 
balance = 0

# read file first #
# keep [] form and use csv.read #


def read_file(stock_data_file):
    # data will be imported as CSV file #
    data = []

    try:
        with open(stock_data_file, 'r') as file:

            # CSV reader function for the file #
            reader = csv.reader(file)

            # read each row #
            for row in reader:
                data.append(row)

    # add testing function #
    except Exception as e:
        if "bond" in stock_data_file:
            error_code = 30  # Error code for "unable to read bond info"
        else:
            error_code = 20  # Default error code for other cases

        print(f"Error: unable to read file {stock_data_file}: {e}")
        sys.exit(error_code)

    return data

# use the read_file function that I created above to read input CSV file with data #


# Function to implement Strategy 1 without date conversion # 
def strategy_1_ror_and_balance(stock_data_file, start_date, end_date):
    newest_balance_1 = []

    # balance starts at 0 # 
    starting_balance = 0.00

    # monthly contribution is 100 as instructed # 
    monthly_contribution = 100.00

    # starting index is None , absence value #
    start_index_for_stock = None
    end_index_for_stock = None
    current_year = None

    # start the loop with skiping header #
    for i, row in enumerate(stock_data_file[1:], start=1):  

        # first element from row , convert to float #
        date = float(row[0])

        # store the date when it == start date #
        if date == start_date:
            start_index_for_stock = i

            # Initial year , conver to integer #
            current_year = int(start_date)  
        if date == end_date:
            end_index_for_stock = i

    # for loop, use end index for stock + 1 to make sure it include everything #
    for month_date_index in range(start_index_for_stock, end_index_for_stock + 1):
        current_month_value = stock_data_file[month_date_index]
        previous_month_value = stock_data_file[month_date_index - 1]

        # instruction to formuala then vover to float for calculaiton #
        S_and_P_t = float(current_month_value[1])
        S_and_P_t_minus_1 = float(previous_month_value[1])
        Dividend_t_minues_1 = float(current_month_value[2])

        # same here as above #
        S_and_P_ROR_t = (S_and_P_t / S_and_P_t_minus_1) - 1
        Dividend_ROR_t = (Dividend_t_minues_1 / 12) / S_and_P_t
        portfolio_ROR_r = S_and_P_ROR_t + Dividend_ROR_t
        
        # Updating the monthly contribution in Jan of each year #
        if int(float(current_month_value[0])) > current_year:
            monthly_contribution *= 1.025
            current_year = int(float(current_month_value[0]))
            
        # round the answer to two decimals compare to the example.csv #
        starting_balance = starting_balance * (1 + portfolio_ROR_r) + monthly_contribution

        # add new value to each row #
        newest_balance_1.append([float(current_month_value[0]), starting_balance])

    return newest_balance_1

# read second file #
# keep [] form and use csv.read #
# stratety 2 #


def strategy_2_ror_and_balance(bond_data_file, start_date, end_date):
    newest_balance_2 = []

    # balance starts at 0 # 
    starting_balance = 0.00
    monthly_contribution = 100.00
    start_index_for_bond = None
    end_index_for_bond = None
    current_year = None

    # skip the header to prevent errors # 
    for i, row in enumerate(bond_data_file[1:], start=1):  
        date = float(row[0])
        if date == start_date:
            start_index_for_bond = i

            # first year #
            current_year = int(start_date)  

            # last year #
        if date == end_date:
            end_index_for_bond = i

    for month_date_index in range(start_index_for_bond, end_index_for_bond + 1):
        current_month_value = bond_data_file[month_date_index]

        # updating the monthly contribution in January of each year #
        if int(float(current_month_value[0])) > current_year:

            # monthly contribution increase by 2.5% on each Jan on every year # 
            monthly_contribution *= 1.025
            current_year = int(float(current_month_value[0]))

        # Keeping Bond ROR in percentage form as Sakai instructed #   
        Bond_ROR_t_percentage = float(current_month_value[1]) / 12 

        # Convert to 4 decimal for the formula # 
        Bond_ROR_t_decimal = Bond_ROR_t_percentage / 100

        # recursion function #  
        starting_balance = starting_balance * (1 + Bond_ROR_t_decimal) + monthly_contribution

        # round the output to 2 decimals like the example.csv #
        newest_balance_2.append([float(current_month_value[0]), starting_balance])  

    return newest_balance_2


# Function to implement Strategy 3
def strategy_3_balance(stock_data_file, bond_data_file, start_date, end_date):
    newest_balance_3 = []
    cumulative_invest = 0.00
    monthly_contribution = 100.00

    # contribution increase in 2.5% per year on Jan #
    increase_for_contribution = 0.025

    # lifecycle allocation is 100%, decease 2% per year #
    lifecycle_allocation = 1.00  # Starting with 100% allocation to equities

    # retrive next item from the function #
    start_index = next((i for i, row in enumerate(stock_data_file[1:], 1) if float(row[0]) == start_date), None)
    end_index = next((i for i, row in enumerate(stock_data_file[1:], 1) if float(row[0]) == end_date), None)

    # extracts data from row at 'start index' and convert to float #
    previous_month_value = stock_data_file[start_index]

    # I cant find a proper way to extract data from date , so I use str[star:end] #
    previous_year = stock_data_file[start_index][0][:4]
        
    for month_date_index in range(start_index, end_index + 1):
        # get the date and data for the current month #
        current_date = stock_data_file[month_date_index][0]

        # extracting the year from the date string #
        current_year = current_date[:4]  
        current_month_value = stock_data_file[month_date_index]
        bond_rate = float(bond_data_file[month_date_index][1])

        # refer back to the formula above #
        S_and_P_t = float(current_month_value[1])
        S_and_P_t_minus_1 = float(previous_month_value[1])
        Dividend_t_minues_1 = float(current_month_value[2])

        # refer to the instruction in Sakai #
        S_and_P_ROR_t = (S_and_P_t / S_and_P_t_minus_1) - 1
        Dividend_ROR_t = (Dividend_t_minues_1 / 12) / S_and_P_t
        portfolio_ror = S_and_P_ROR_t + Dividend_ROR_t 

        # update previous month value and make sure #
        # it equals the current month value #
        previous_month_value = current_month_value

        bond_ror = bond_rate / 12 / 100

        # check if current date ends with substring '.01' to makre sure #
        # is the first month of a year #
        if current_date.endswith('.01') and current_year != previous_year:
            lifecycle_allocation -= 0.02  # Decrease lifecycle allocation by 2%
            monthly_contribution *= (1 + increase_for_contribution)  # Increase monthly contribution by 2.5%
            previous_year = current_year

        # stratety three formula instrcuted by Sakai # 
        cumulative_invest = (
            (cumulative_invest * (1 + portfolio_ror) * lifecycle_allocation) +
            (cumulative_invest * (1 + bond_ror) * (1 - lifecycle_allocation)) +
            monthly_contribution
        )
    
        newest_balance_3.append([current_date, cumulative_invest])

    return newest_balance_3


# start export CSV function #


def output_to_CSV(newest_balance_strategyOne, newest_balance_strategyTwo, newest_balance_strategyThree, start_date):
    # Find the minimum length among the three lists #
    min_length = min(len(newest_balance_strategyOne), len(newest_balance_strategyTwo), len(newest_balance_strategyThree))

    # this make sure when I put the date in command #
    # it will detect and split the date into year and month with dot #
    start_year, start_month = map(int, start_date.split('.'))

    # Write the results to a new CSV file
    with open("portfolio.csv", mode='w', newline='') as file:
        writer = csv.writer(file)

        # Header row 1. Date, 2. StrategyOne, 3.StrategyTwo, 4.StrategyThree #
        writer.writerow(['Date', 'StrategyOne', 'StrategyTwo', 'StrategyThree'])

        # Write data up to the minimum length #
        for row in range(min_length):
            date_float = newest_balance_strategyOne[row][0]

            # I cant figure this out it keep showing the weird dates #
            # and I convert to string with two decimal places #
            date_str = f'{date_float:.2f}'  

            # split the year and month with dot #
            year_str, month_str = date_str.split('.')

            # reformatted the date with zfill where it will make zero into '01' #
            formatted_date = f'{year_str}.{month_str.zfill(2)}'

            start_date_obj = datetime.strptime(start_date, '%Y.%m')

            # reformatted the date in YYYY.MM #
            formatted_date_obj = datetime.strptime(formatted_date, '%Y.%m')
            
            if formatted_date_obj >= start_date_obj:
                writer.writerow([
                    # date in index 0, followed by strategy two and three
                    formatted_date,
                    f'{newest_balance_strategyOne[row][1]:.2f}',
                    f'{newest_balance_strategyTwo[row][1]:.2f}',
                    f'{newest_balance_strategyThree[row][1]:.2f}',
                ])


def process(stock_data_file, bond_data_file, start_date, end_date):
    # Read financial data from CSV files
    stock_data = read_file(stock_data_file)
    bond_data = read_file(bond_data_file)

    # Calculate strategies
    newest_balance_strategyOne = strategy_1_ror_and_balance(stock_data, start_date, end_date)
    newest_balance_strategyTwo = strategy_2_ror_and_balance(bond_data, start_date, end_date)
    newest_balance_strategyThree = strategy_3_balance(stock_data, bond_data, start_date, end_date)

    # Export results to CSV
    output_to_CSV(newest_balance_strategyOne, newest_balance_strategyTwo, newest_balance_strategyThree, "1971.12")

# run directly #


if __name__ == "__main__":
    # make sure 4 command line argument to make total of 5 #
    if len(sys.argv) != 5:
        print("Usage: python script.py stock_data_file bond_data_file start_date end_date")
        sys.exit(10)

    # all the command line 1,2,3,4 #
    stock_data_file = sys.argv[1]
    bond_data_file = sys.argv[2]
    start_date = float(sys.argv[3])
    end_date = float(sys.argv[4])

    if end_date < start_date:
        error_code = 10  # Set error code to 10 for "end date before start date"
        print("Error: End date cannot be before start date")
        sys.exit(error_code)

    process(stock_data_file, bond_data_file, start_date, end_date)