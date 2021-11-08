from datetime import date
todaydate = date.today()
todate = str(todaydate)
filetype = ".txt"
filename = todate + filetype
ip='127.0.0.1'
with open(filename, "a+") as f:
    

    f.seek(0)
    #read content of file to string
    data = f.readlines()
    print(data)
    #get number of occurrences of the substring in the string
    occurrences = data.count(f"{ip}\n")

    if occurrences<5:
        
        f.writelines(f"{ip}\n")
        print("Inserted in Database")
    print('Number of occurrences of the word :', occurrences)
