

# Run instruction

The solution was programmed with Python 3.6.2

The running of the solution requires no additional library, environment, or dependency. Only the Python Standard Library is used.

The code was tested on a computer with Windows Subsystem for Linux (Ubuntu 16.04.2 LTS). The original bash files 'run.sh' in the main folder and 'run_tests.sh' in insight testsuite folder were not working with the bash command due to the '/r/n' found in the bash files. So I used the linux command 'dos2unix' and transformed the 'run.sh' and 'run tests.sh' into the unix/linux format. After transformation, the two bash files worked well on the test1 coming with the challenge and also my own test as shown in the temp folder. 




# Approach

For this challenge, I employed a 'donors' dictionary to record the valid donors' information and identify the repeated donors, and another 'output' dictionary to record the repeated donations. The dict key for the 'donors' dictionary would be 'donor name + 5 digit zip code', and for the 'output' dictionary would be 'recipient ID + zip code + transaction year'. The steps of the solution are as below:

1. Streaming each line from input file.
2.  Identify and name all the useful fields from each line, and validate those input items in the right format, for example, the OTHER_ID should always be empty.
3.  Use the donors' name and zip code as their special ID. 
If a repeated donor is identified, then record the repeated donation in the output dict, and calculate the total number of transactions from the repeated donors, the percentile as well as the total amount of the repeated donations.
4. Write the identified repeated donation to the output file in every cycle of streaming.
5. The function used to calculate the percentile is based on the description by Wikipedia.