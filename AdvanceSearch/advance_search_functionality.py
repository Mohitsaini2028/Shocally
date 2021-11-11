

term = []
l=[]
oper=[]

def extract_numbers_from_text(text):
    del l[:]
    for t in text.split(' '):
        try:
            l.append(float(t))
        except ValueError:
            if t.upper() not in operations.keys():
               term.append(t)

    return(l)

def above(number):
    return number

def below(number):
    return number


def aboveResult(term,number):
        allProductName= Product.objects.filter(product_name__icontains=term,seller__pincode=pincode)

        allProductCategory= Product.objects.filter(category__icontains=term,seller__pincode=pincode)
        allProductSubCategory =Product.objects.filter(subCategory__icontains=term,seller__pincode=pincode)
        allProduct =  allProductName.union(allProductCategory, allProductSubCategory)
    return allProduct




operations={"ABOVE":above, "MINIMUM":above, "BELOW":below, "UNDER":below, "MAXIMUM":below}
termFilter={"ABOVE":aboveResult, "MINIMUM":aboveResult , "BELOW":below , "UNDER":below, "MAXIMUM":below}



def main(string):
        del term[:]

        print()
        text=string
        for word in text.split(' '):
            if word.upper() in operations.keys():
                try:
                    l=extract_numbers_from_text(text)
                    r=operations[word.upper()](l[0])
                    oper.append(word.upper()) #taking first number
                    print(r)
                    print(term)
                except:
                    print("Something is wrong please retry")
                finally:
                    break

        else:
            return False
        return [oper,l,term]


if __name__=="__main__":
    main("laptop and mobile below 2")
