#!/usr/bin/env python
import csv, json, sys

def convert(csvname):
    with open(csvname, 'r') as csvfile:
        fieldnames = ["starttime","recordpath","frequency","length","startearly",
                "logfilepath","gain"]
        recordings = []
        reader = csv.reader(csvfile, fieldnames)
        vals = next(reader)
        for row in reader:
            if not row[0].startswith('#'): # Assumes startime is 1st
                recordings.append(row)

        master_dict = { 'recordings' : recordings,
                'name'      : vals[0],
                'startingpath'  : vals[1],
                'logpath'       : vals[2],
                'rfsnids'       : [int(x) for x in vals[3:]] }
    return json.dumps(master_dict)

if __name__ ==  "__main__":
    if len(sys.argv) > 1:
        print(convert(sys.argv[1]))
    else:
        print("Give csv name of schedule as parameter.")
