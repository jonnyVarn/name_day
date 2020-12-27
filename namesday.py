import requests
RQ=requests
import json



my_url = "https://sholiday.faboul.se/dagar/v2.1/"

fabol_answer=RQ.api.get(my_url)
#print(type(fabol_answer))
my_dict=fabol_answer.json()
#print(my_dict)
#print(type(my_dict))
days=my_dict['dagar']
#print(days)
#print(type(days))
#print(days[0])
days_dict=days[0]
#print(type (days_dict))
names=days_dict.get('namnsdag')
date=days_dict.get('datum')
print(type(names))
file=open('names.txt', 'a+')
file.write(date +" Dagens namn: ")
for i in range(len(names)):
    if i!=len(names)-1:
        file.write(names[i] + ", ")
    else:
        file.write(names[i] +" .")
    #print(names[i])
file.write("\n")

        
#namesday=my_dict["uri"]
#print(namesday)

#print(Content['namnsdag'])
#days=json_data["namnsdag"]


#if fabol_answer.content.find(200):
    #date_str=fabol_answer.text
    #print(date_str)
    #print(type(date_str))
    #nameday=date_str.find("namnsdag")
    #nameday=int(nameday) 
    #stop=nameday+100
    #print(date_str[nameday])
    #print(date_str.format({"cachetid":"2020-12-26 22:56:01", "namnsdag":}))

#print(dayname.text)
#print(answer.text)

#namnsdag":["Stefan","Staffan"]

"""logg

https://github.com/jonnyVarn/name_day/
2020-12-27 created repo from github webpage
2020-12-27 created and added  __init__.py git add __init__.py git commit -m "added __init__.py" git push
2020-12-27 added file namesday.py 



"""