import datetime
import math
import sys
import os
import io
global str

# Build the donors dict to record the donor id and identify the repeated donors
# The dict key would be 'donor name + 5 digit zip code'
donors = {}

# Build the output dict to record the repeated donations
# The dict key would be 'recipient ID + zip code + transaction year'
# The dict value is a list of the donations recieved by the recipient from a specific zip code in a specific year
output = {}

# Validate the input items are in the right format, for example, the _OTHER_ID should always be empty
# Will return True if all the items are in correct format, otherwise False
def validate_arg(_CMTE_ID, _NAME, _ZIP_CODE, _TRANS_DT, _TRANS_AMT, _OTHER_ID):
    if _OTHER_ID:
        return False
    if not validate_date(_TRANS_DT):
        return False
    if _TRANS_AMT == '' or int(_TRANS_AMT) <= 0:
        return False
    if not _NAME.replace(',', '').replace('.', '').replace(' ', '').isalpha():
        return False
    if not _CMTE_ID.isalnum() or len(_CMTE_ID) != 9:
        return False
    if not _ZIP_CODE.isdigit() or len(_ZIP_CODE) != 5:
        return False
    
    return True

# The function used to validate the transaction date is in the right format 'mmddyyyy'
def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%m%d%Y')
    except ValueError :
        return False
    return True

# The function used to calculate the percentile based on the description by Wikipedia
def get_percentile(nums, _percentile_value):

    length = float(len(nums))
    val = float(_percentile_value*length/100)
    if (float(val) % 1) >= 0.5:
        x = math.ceil(val)
    else:
        x = math.floor(val)
    return nums[int(x - 1)]

# The function used to generate the repeated donations
def generate_repeat_donors(_input_file, _percentile_file, _output_file):
    # Open all the required files
    f_percentile = open(_percentile_file, 'r')
    percentile_value = int(f_percentile.read())
    f_input = open(_input_file, 'r')
    f_output = open(_output_file, 'w+')

    # Streaming each line from input file
    for line in f_input.readlines():

        # Identify and name all the required info 
        fields = line.split('|')
        CMTE_ID = fields[0]
        NAME = fields[7]
        ZIP_CODE = fields[10][:5]
        TRANS_DT = fields[13]
        TRANS_AMT = fields[14]
        OTHER_ID = fields[15]

        # Validate all the items are in the right format
        if validate_arg(CMTE_ID, NAME, ZIP_CODE, TRANS_DT, TRANS_AMT, OTHER_ID):
            YEAR = int(TRANS_DT[-4:])
            AMT = int(TRANS_AMT)
            # Use the donors' name and zip code as their special ID
            donor_ID = '|'.join([NAME, ZIP_CODE])
            # If a repeated donor is identified, then record the repeated donation in the output dict
            if donor_ID in donors:
                if donors[donor_ID] < YEAR:
                    r = '|'.join([CMTE_ID, ZIP_CODE, str(YEAR)])
                    if r in output:
                        output[r].append(AMT)
                    else:
                        output[r] = [AMT]
                    
                    # Calculate the total number of transactions from the repeated donors
                    l = str(len(output[r]))
                    # Calculate the percentile
                    percentile = get_percentile(sorted(output[r]), percentile_value)
                    # Calculate the total amount of the repeated donations
                    total = sum(output[r])
                    # Write all the information to the output file
                    f_output.write('|'.join([r, str(percentile), str(total), str(l)]) + os.linesep)

                # In case the data is listed out of order, record the earliest year for the specific donor ID for future use.
                donors[donor_ID] = min(YEAR, donors[donor_ID])
            else:
                # Record the donor if their info were not found before
                donors[donor_ID] = YEAR

        else:
            continue
    
    f_percentile.close()
    f_input.close()
    f_output.close()
        
        

def main():
    # Read in all the argv for the .py file
    input_file = sys.argv[1:][0]
    percentile_file = sys.argv[1:][1]
    output_file = sys.argv[1:][2]
    generate_repeat_donors(input_file, percentile_file, output_file)

if __name__ == "__main__":
    main()
