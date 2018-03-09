import re
import fileinput
import random
from flask import Flask,request,make_response
import json
app = Flask(__name__)

@app.route('/',methods=['POST'])
def webhook():
	file = open('data_txt', 'r')
	text = file.read()
	data_file = open('data_txt', 'r')
	yourResult = [line.split(',') for line in data_file.readlines()]
	gx=[]
	for i in range(len(yourResult)):
		try:
			gx.append([yourResult[i][0],yourResult[i][1]])
		except Exception as e:
			pass	
	req=request.json
	val=req.get('queryResult').get('parameters').get('text')
	str="शब्द"
	if str in val:
		res=wordOfTheDay(gx)
	else:
		res=getSentence(val,gx)
	res=json.dumps(res,indent=4)
	r=make_response(res)
	r.headers['Content-Type']='application/json'
	return r

def wordOfTheDay(gx):
	k=random.choice(gx)
	try:
		a=k[0].split(':')
		b=k[1].split(':')
		#print(a)
		#print("word of day is:")
		str1=a[0]
		str1=str1.replace("[","")
		str1=str1.replace("\'","")
		str1=str1.replace("  ","")
		#print(str1)
		fstr=''
		#print("synonyms are:")
		for i in range(1,len(a)):
			str2=a[i]
			str2=str2.replace("\'","")
			str2=str2.replace("  ","")
			#print(str2)
			fstr+=str2
		#print("meaning is:")
		str3=b[0]
		str3=str3.replace("\' ","")
		#print(str3)	
		#print("sentence is:")
		str4=b[1]
		str4=str4.replace("\\n']","")
		str4=str4.replace("\"","")
		#print(str4)
		speech="शब्द :\n"+str1+"\n समानार्थक शब्द :\n"+fstr+"\n अर्थ :\n"+str3+"\n वाक्य :\n"+str4
		#print(finalstr)
		return {
		"fulfillmentText": speech,        
        # "data": data,
        # "contextOut": [],
        "source": "127.0.0.1:5000"
    	}
	except Exception as e:
		wordOfTheDay()

def getSentence(str,gx):
	gx1=[]
	gx3=[]
	for i in range(len(gx)):
		gx1.append(gx[i][0])
	#print(gx1[0])
	for i in range(len(gx1)):
		gx2 = ''.join(gx1[i])
		gx2=gx2.split(':')
		gx2[0]=gx2[0].replace("[","")
		gx2[0]=gx2[0].replace("\'","")
		gx2[0]=gx2[0].replace("  ","")
		gx2[0]=gx2[0].replace(" ","")
		gx3.append(gx2[0])
	#print(gx3)
	a=str.split(" ")
	#print(a)
	fstr=''
	for i in range(0,len(a)):
		if a[i] in gx3:
			k=gx3.index(a[i])
			#print(k)
			gx2=gx1[k].split(':')
			k=len(gx2)-1
			#print(k)
			if k!=0:
				str1=gx2[1]
				str1=str1.replace("\'","")
				str1=str1.replace(" ","")
			#print(str1)
			elif k==0:
				str1=a[i]
			fstr+=str1+" "
		else:
			fstr+=a[i]+" "
	return {
		"fulfillmentText": fstr,        
        # "data": data,
        # "contextOut": [],
        "source": "127.0.0.1:5000"
    	}

if __name__=='__main__':
	app.run(debug=True)







