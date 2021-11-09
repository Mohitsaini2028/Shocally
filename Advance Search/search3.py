#with open("cities.txt", "r") as f:
#    cities = f.read().split("\n")

with open("data.csv", "r") as f:
    cities = f.read().split(",")


#from fuzzywuzzy import process
from fuzzywuzzy import fuzz, process

'''
soundex = fuzz.Soundex(10)
# Text to process
word = 'phone'
soundex(word)
'''




def get_matches(query, choices, limit=3):
        results = process.extract(query, choices, limit=limit)
        return results

'''
try to apply sorting features for on higher to lower order aur on the basic of date

agar data extract karne par 0 ya 5 s kam matching nikle toh fir word ko match karna fir wapis s fetch karna database s  

'''


match=get_matches("compyter", cities)

for i in match:
        print(i[0])
print(type(match))
