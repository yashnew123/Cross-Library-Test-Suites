import pandas as pd
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 
from nltk.stem import PorterStemmer
from stemming.porter2 import stem
import numpy as np
import math as mt
import re
import urllib
import operator
from requests import get
import sys

ps=PorterStemmer()
stop_words=set(stopwords.words('english'))
sss_url = "http://swoogle.umbc.edu/SimService/GetSimilarity?"
symbols=['.',',',';',':','<','>','{','}','[',']','|','\\','+','-','*','/','=','_','!','@','#','$','%','^','&','(',')','~','`','``','?',"'","..","''",",,",". '"]


def sss(s1, s2, type='relation', corpus='webbase'):
    #print s2
    try:
        response = get(sss_url, params={'operation':'api','phrase1':s1,'phrase2':s2,'type':type,'corpus':corpus})
        return float(response.text.strip())
    except:
        print 'Error in getting similarity for %s: %s' % ((s1,s2), response)
        return 0.0

def camel_case_split(identifier):
    x=identifier.split("-")
    #print x
    y=[]
    for j in x:
     z=j.split("/")
     y+=z
    #print y
    x=[]
    for j in y:
     y1=j.split(".")
     x+=y1
    z=[]
    for j in x:
     y2=j.split('_')
     z+=y2
    x=z[:]
    #print x
    matches=[]
    for i in x:
     matches +=(re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', i))
    #print matches
    matches1=[]
    for i in matches:
     #print i.group(0)
     matches1.append(i.group(0).lower())
    #print matches1
    return matches1
#print 'date/time'.split('/')
#print camel_case_split('date/time')
def Find(string):
    # findall() has been used 
    # with valid conditions for urls in string
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return url
 
def jaccard(v1,v2):
 intsec=[]
 #print v1
 #print v2
 for w in v1:
  if w in v2 :
   intsec.append(w)
 #print intsec
 sim=float(len(intsec))/(10.0)
 return sim,intsec


def tf_idf(q,doc,freq,N):
  q_tf={}
  doc_tf={}
  for i in q:
   if i not in q_tf:
    q_tf[i]=1
   else:
    q_tf[i]+=1
  for i in doc:
   if i not in doc_tf:
     doc_tf[i]=1
   else:
     doc_tf[i]+=1
  idf={}
  q_tfidf={}
  doc_tfidf={}
  for i in q_tf:
   if i in freq and freq[i]!=0:
     val=float(freq[i])
     idf[i]=mt.log((N/val),2)
   else:
     idf[i]=0.0
  for i in doc_tf:
   if i in freq:
    val=float(freq[i])
    idf[i]=mt.log((N/val),2)
   else:
    idf[i]=0.0
  for i in q_tf:
   q_tfidf[i]=q_tf[i]*idf[i]
  for i in doc_tf:
   doc_tfidf[i]=doc_tf[i]*idf[i]
  
  q_keys=[]
  doc_keys=[]
  x1=sorted(q_tfidf.items(),key=operator.itemgetter(1))
  x2=sorted(doc_tfidf.items(),key=operator.itemgetter(1))
  ctr=0
  idx=len(x1)-1
  while idx>=0:
   x=x1[idx][0]
   idx-=1
   q_keys.append(x)
   ctr+=1
   if ctr==10:
    break
  ctr=0
  idx=len(x2)-1
  while idx>=0:
   x=x2[idx][0]
   idx-=1
   doc_keys.append(x)
   ctr+=1
   if ctr==10:
    break
  #print q_keys
  #print doc_keys
  sim,intsec=jaccard(q_keys,doc_keys)
  #print doc_keys
  return sim,intsec
  
w1=[]
w1.append(0.6)
w1.append(0.4)

w2=[]
w2.append(1.0)
w2.append(0.0)

w3=[]
w3.append(0.0)
w3.append(1.0) 
 
file='/home/yashbnit/Downloads/Similar Methods (by documentation).xlsx'
xl=pd.ExcelFile(file)
df=xl.parse('TestData')
m_sig=(df['M1 signature'])
#print idx1
#ip_name=str(raw_input("Enter method name: "))
#fo=open("documentation.txt","r")
doc_set1=df["Documentation/desc 1"]
for i in np.arange(len(doc_set1)):
 l=str(unicode(doc_set1[i]).encode('utf8')).split(" ")
 lt=""
 for j in l:
  if str(j)==">>>":
   doc_set1[i]=lt
   break
  if lt=="":
   lt+=str(j)
  else:
   lt+=" "+str(j)
 doc_set1[i]=lt
doc_set2=df["Documentation/desc 2"]
dset1=[]


words=[]
ctr=-1
ids=df.index.values
#print ids
for i in doc_set1:
  #print "Hello"+str(ctr)
  #print i
  #print i
  ctr+=1
  #print str(i)
  #i=unicode(i).encode('utf8')
  urls=Find(str(i))
  if len(urls)!=0 or str(i)=='nan':
   #idv=ids[ctr]
   try:
    df.drop(ids[ctr],inplace=True)
   except:
    continue
   continue
  
  dw1=word_tokenize(str(i))
  dw=[]
  
  for ws in dw1:
   #print "Hello1"
   #print ws
   x=camel_case_split(ws)
   #print "Hello"
   #print x
   dw+=x
  vec=[]
  for j in dw:
   if j==">>>":
    break
   j=j.lower()
   if j not in stop_words and j not in symbols:
    try:
     x1=pos_tag([str(j)])
     if x1[0][1][0]!='N':
      continue
     #print x1
     w=str(ps.stem(j))
    except:
     continue
    vec.append(str(w))
    if w not in words:
     words.append(str(w))
  dset1.append(vec)
for ip_name in df.index.values:
        flag=0
        d1=[]
        print "Method: "+str(ip_name)
	try:
	 doc_i=str(df.loc[ip_name]["Documentation/desc 2"])
	except:
	 continue
	if doc_i=='nan' or doc_i==" ":
	  flag=1
	i_row=df.loc[ip_name]
	sig=str(i_row['M2 signature'])
	i_name=""
	s1=""
	s2=""
	if sig=='nan':
	 sig=""
	for l in np.arange(len(sig)):
	 if sig[l]==' ':
	  s2=s1[:]
	  continue
	 elif sig[l]=='(':
	  i_name=s2[:]
	  s2=s1[:]
	 else:
	  s2+=sig[l]
	#print "Method Name: "+str(i_name) 
	#print doc_i
	l1=camel_case_split(i_name)
	i_name=""
	for j2 in l1:
	  i_name+=str(ps.stem(j2))
	  i_name+=' '
	if i_name=="" and flag==1:
	 continue

	dw1=word_tokenize(str(doc_i))
	dw=[]
	for ws in dw1:
	  x=camel_case_split(ws)
	  for z in x:
	    dw.append(z)
	#print dw
	for j in dw:
	  if j==">>>":
	   break
	  j=j.lower()
	  if j not in stop_words and j not in symbols:
	   try:
	     x1=pos_tag([str(j)])
	     if x1[0][1][0]!='N' and x1[0][1][0]!='J':
	      continue
	     #print x1
	     w=str(stem(j))
	   except:
	     continue
	   d1.append(str(w)) 
	   if w not in words:
	     words.append(w)

	freq={}
	for w in words:
	 freq[w]=0.0
	 for i in np.arange(len(dset1)):
	  d=dset1[i]
	  if w in d:
	   freq[w]+=1


	print "\n\nTF-IDF Similarity: "
	N=len(dset1)
	ids=df.index.values
	ctr=-1
	sim_scores1={}

	sim_methods1=[]
	keywords={}
	scores={}
	for d in dset1:
	 ctr+=1
	 s1=""
	 s2=""
	 m_name=""
	 sig1=str(df.loc[ids[ctr]]['M1 signature'])
	 for l in np.arange(len(sig1)):
	  if sig1[l]==' ':
	   s2=s1[:]
	  elif sig1[l]=='(':
	   m_name=s2[:]
	   s2=s1[:]
	  else:
	   s2+=sig1[l]
	 if i_name=="" or m_name=="":
	  w=w2[:]
	 elif i_name!="" and len(d1)!=0:
	  w=w1[:]
	 else:
	  w=w3[:]
	 sim,intsec=tf_idf(d1,d,freq,N)
	 try:
	  keywords[ids[ctr]]=intsec
	 except:
	  ctr=-1
	  break
	 l2=camel_case_split(m_name)
	 m_name=""
	 for j2 in l2:
	  m_name+=str(stem(j2))
	  m_name+=' '
	 try:
	  name_sim=sss(i_name.upper(),m_name.upper())
	 except:
	  continue
	 if name_sim==-float('inf'):
	  name_sim=0
	 #print sim
	 sim=(w[0]*sim+w[1]*name_sim)
	 scores[ids[ctr]]=sim
	 #print sim
	 print (i_name,m_name,w)
	 print str(ids[ctr])+" : "+str(sim)
	 sim_scores1[str(ids[ctr])]=sim

	sort_methods1=sorted(sim_scores1.items(),key=operator.itemgetter(1))

	ctr=0
	idx=len(sort_methods1)-1
	while ctr<3:
	 sim_methods1.append(sort_methods1[idx][0])
	 ctr+=1
	 idx-=1

	print "\n\nTop three libraries: "
	print sim_methods1
	
