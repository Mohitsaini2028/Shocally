from datetime import date
todaydate = date.today()
todate = str(todaydate)
filetype = ".txt"
filename = todate + filetype
f = open(filename, "w")
