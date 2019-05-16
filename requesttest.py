import matplotlib.pyplot as plt
import csv

CAPITA_FILE = 'csvfolder/vakiluvut/vakiluku_tiedosto.csv'

""" x = [2, 4, 6]
y = [1, 3, 5]
plt.plot(x,y)
plt.show() """

selected_country = "Finland"

xlist = []
ylist = []

index = 1960
while index <= 2019:
    xlist.append(index)
    index = index + 1

with open(CAPITA_FILE) as f:
        csv_reader = csv.reader(f, delimiter=',')
        for line in csv_reader:
            if type(line) is list:
                if len(line) is not 0:
                    if line[0] == selected_country:
                        del line[0:4]
                        for x in line:
                            if x is '':
                                x = 0
                                ylist.append(x)
                            else:
                                ylist.append(x)
plt.plot(xlist,ylist)
plt.show()