import csv, sys, getopt
from datetime import datetime

inputfile = ''

#Add microseconds to date/time
def updateDateTime(x):
    x = x + ".000"
    return x

#Move PRI decimal 3 places
def updatePRI(x):
    x = float(x) * 0.001
    return x


#Load the input file and set global variables
def loadCSV(inputfile):
    #print("Ready to load the file!")
    f = open(inputfile)
    csv_f = csv.reader(f)
    next(csv_f)
    for row in csv_f:
        row[1] = updateDateTime(row[1])
        #print(row[1])
        row[2] = updatePRI(row[2])
        #print(row[2])

    print("File processed and converted successfully!")

def main(argv):
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile="])
   except getopt.GetoptError:
      print('test.py -i <inputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
          print('test.py -i <inputfile>')
          sys.exit()
      elif opt in ("-i", "--ifile"):
         global inputfile
         inputfile = arg

   #Ready to open the csv and begin processing it
   loadCSV(inputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
