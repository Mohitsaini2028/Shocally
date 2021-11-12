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
        

#                  filename, id, ip  
def check_occurrences(word,ID,ip): 
    filename = get_filename(word)
    with open(filename, "r") as f:
        f.seek(0)
        #read content of file to string
        data = f.readlines()
        #print(data)
        #get number of occurrences of the substring in the string
        occurrences = data.count(f"{ID},{ip}\n")
    return occurrences

def main():
    word = 'shop' 
    ip='127.0.0.1'
    ID = 4 #shopid #newsid
    update_ip(word,ID,ip)
    print(check_occurrences(word,ID,ip))


