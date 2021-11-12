from datetime import date
todaydate = date.today()
todate = str(todaydate)

def get_filename(word):
    filetype = ".txt"
    filename = word+'_'+todate + filetype
    return filename

def update_ip(word,ID,ip):    
    filename = get_filename(word) 
    with open(filename, "a+") as f:   
        f.seek(0)
        #read content of file to string
        data = f.readlines()
        #print(data)
        #get number of occurrences of the substring in the string
        occurrences = data.count(f"{ID},{ip}\n")

        if occurrences<5:
            
            f.writelines(f"{ID},{ip}\n")
            print("Inserted in Database")
        print('Number of occurrences of the word :', occurrences)
        

#                 filename, id, ip  
def check_occurrences(word,ID): 
    filename = get_filename(word)
    with open(filename, "r") as f:
        f.seek(0)
        #read content of file to string
        data = f.readlines()

        ids = []
        for i in data:
            i = i.split(',')
            i = i[0]
            ids.append(i)
              
        #get number of occurrences of the substring in the string
        occurrences = ids.count(f"{ID}")
        print(f"OCCURRENCES of {ID} is :",occurrences)
    return occurrences

def main():
    word = 'shop' 
    ip='445456.565.456456.455,127.0.0.1'
    ID = 4 #shopid #newsid
    #update_ip(word,ID,ip)
    print(check_occurrences(word,ID))
