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
print "Hello12"
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
     z=j.split('_')
     y+=z
    x=y[:]
    y=[]
    for j in x:
     z=j.split("/")
     y+=z
    #print y
    x=[]
    for j in y:
     y1=j.split(".")
     x+=y1
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
 print v1
 print v2
 for w in v1:
  if w in v2 :
   intsec.append(w)
 #print intsec
 sim=float(len(intsec))/(10.0)
 return sim,intsec


def tf_idf(doc,freq,N):
  #q_tf={}
  doc_tf={}
  for i in doc:
   if i not in doc_tf:
     doc_tf[i]=1
   else:
     doc_tf[i]+=1
  idf={}
  #q_tfidf={}
  doc_tfidf={}
  for i in doc_tf:
   if i in freq:
    val=float(freq[i])
    idf[i]=mt.log((N/val),2)
   else:
    idf[i]=0.0
  for i in doc_tf:
   doc_tfidf[i]=doc_tf[i]*idf[i]
  
  #q_keys=[]
  doc_keys=[]
  #x1=sorted(q_tfidf.items(),key=operator.itemgetter(1))
  x2=sorted(doc_tfidf.items(),key=operator.itemgetter(1))
  ctr=0
  idx=len(x2)-1
  while idx>=0:
   x=x2[idx][0]
   idx-=1
   doc_keys.append(x)
   ctr+=1
   if ctr==10:
    break
  size=len(doc_keys)
  while size<10:
   doc_keys.append("")
   size+=1
  print doc_keys
  return doc_keys
  
 
 
file='/home/yashbnit/Downloads/Java_Data_1.xlsx'
xl=pd.ExcelFile(file)
df=xl.parse('Sheet1')
f1='/home/yashbnit/Downloads/Java_Keys_1.xlsx'
xl1=pd.ExcelFile(f1)
df1=xl1.parse('Sheet1')
#print df
#print idx1
#ip_name=str(raw_input("Enter method name: "))
#fo=open("documentation.txt","r")
doc_set1=list(df["docstring"])
for i in np.arange(len(doc_set1)):
 print i
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
#doc_set2=df["Documentation/desc 2"]
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
  #print ctr
  #print str(i)
  #i=unicode(i).encode('utf8')
  
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
     w=str(stem(j))
    except:
     continue
    vec.append(str(w))
    if w not in words:
     words.append(str(w))
  dset1.append(vec)
freq={}
for w in words:
 freq[w]=0.0
 for i in np.arange(len(dset1)):
  d=dset1[i]
  if w in d:
   freq[w]+=1
N=len(df)
visited=list(df1['repo_path'])
for i in np.arange(len(df)):
        print i
        if df.loc[i]['repo_path'] in visited:
         continue
        keys=tf_idf(dset1[i],freq,N)
        results=[]
        results.append(df.loc[i]['repo_name'])
        results.append(df.loc[i]['repo_path'])
        results.append(df.loc[i]['method'])
        results.append(df.loc[i]['docstring'])
        f1='/home/yashbnit/Downloads/Java_Keys_1.xlsx'
        xl1=pd.ExcelFile(f1)
        df1=xl1.parse('Sheet1')
        ids=df1.index.values
        if len(ids)==0:
         maxid=0
        else:
         maxid=ids[len(ids)-1]+1
        for j in np.arange(len(keys)):
         results.append(keys[j])
	df1.loc[maxid]=results
	writer=pd.ExcelWriter(f1)
	df1.to_excel(writer,'Sheet1')
	writer.save()
	ctr=-1
