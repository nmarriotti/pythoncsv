import csv, time, sys, getopt
from datetime import datetime

################################################################################
# Need to first convert Excel date/times to show sec and milliseconds
# This will add three decimal places to some numbers.
# Calculate difference in seconds for multiple report numbers
# Need to add all the column names that are in the inputfile
################################################################################

inputfile = ''
outfile = ''

# Add microseconds to date/time
def updateDateTime(x):
    x = x + ":00.000"
    return x

# Move PRI decimal 3 places
def updatePRI(x):
    x = float(x) * 0.001
    return x

def open_csv(filename):
    with open(filename, "rU") as csvfile:
        csv_data = csv.DictReader(csvfile)
        count = 0
        for row in csv_data:
            yield row

# Load the input file and set global variables
def processCSV():
    count = 0
    before = time.time()
    report_numbers = {}
    with open(outfile, 'w') as csvfile:
        fields = ['report_number','date_time','difference','numbers']
        writer = csv.DictWriter(csvfile, fieldnames=fields, delimiter=',', lineterminator='\n')
        writer.writeheader()

        for row in open_csv(inputfile):
            #row['date_time'] = updateDateTime(row['date_time'])
            row['numbers'] = updatePRI(row['numbers'])

            # Count the rows
            count+=1

            # Check if the report number is in the array, None if it's not
            first_time = report_numbers.get(row['report_number'], None)
            second_time = datetime.strptime(row['date_time'], '%m/%d/%Y %H:%M:%S.%f')

            if first_time is None:
                row['difference'] = '0'
            else:
                row['difference'] = (second_time - first_time).total_seconds()

            # Add the current rows report number to an array
            report_numbers[row['report_number']] = second_time

            # Write the current row to the output file
            writer.writerow(row)

    after = time.time()
    print("{rows} rows processed in {time} seconds".format(rows=count, time=after-before))

def main(argv):
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["infile=","outfile="])
   except getopt.GetoptError:
      print('python convert.py -i <infile> -o <outfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
          print('python convert.py -i <infile> -o <outfile>')
          sys.exit()
      elif opt in ("-i", "--infile"):
         global inputfile
         inputfile = arg
      elif opt in ("-o", "--outfile"):
         global outfile
         outfile = arg

   #Ready to open the csv and begin processing it
   processCSV()

if __name__ == "__main__":
   main(sys.argv[1:])
