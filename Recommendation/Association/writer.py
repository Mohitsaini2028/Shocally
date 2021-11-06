import csv,json


obj = json.loads('{"pr12":[1,"shoes",499],"pr5":[1,"shocs",50000]}')

category = ["car","tv"]

descList = []
prodList = []
setForCat = set()

for key in obj:
        prodId = int(key[2:])
        #id = user.id
        print("product id - ",prodId)             #product id
        #prod=Product.objects.get(id=prodId)
        cat = "car"                             #prod.category

        setForCat.add(cat)  # contain all unique category 
         
        lis = obj[key]
        name = lis[1]
        price = lis[2]
        #prodList.append(prod)
        
        descList.append([prodId, cat, name, price ])
                                     #user id
        print("user id - ",lis[0])


def updateList(lis,fileName):
    with open(fileName,'a',newline='') as f_object:
        writer_object = csv.writer(f_object)
        writer_object.writerow(lis)


        
print(descList)

print(len(setForCat))


for item in setForCat:
     rowUpdate =[]
     for i in descList:
            if i[1]==item:
                rowUpdate.append(i[2]) #list for row update
     print(rowUpdate)
     updateList(rowUpdate,'store_data0 - Copy.csv')
     rowUpdate.insert(0,1)
     updateList(rowUpdate,'OrderDetail.csv')

     

        
#updateList(['Monitor','mouses'])
        


