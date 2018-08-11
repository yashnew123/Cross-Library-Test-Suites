import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 
from nltk.stem import PorterStemmer
import numpy as np
import math as mt
import re
import urllib
import operator
from requests import get
import sys

ps=PorterStemmer()
stop_words=set(stopwords.words('english'))

symbols=['.',',',';',':','<','>','{','}','[',']','|','\\','+','-','*','/','=','_','!','@','#','$','%','^','&','(',')','~','`','``','?',"'","..","''",",,",". '"]

def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]

def Find(string):
    # findall() has been used 
    # with valid conditions for urls in string
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return url
 
def jaccard(v1,v2):
 intsec=[]
 for w in v1:
  if w in v2 :
   intsec.append(w)
 #print intsec
 sim=float(len(intsec))/(len(v1)+len(v2)-len(intsec))
 return sim


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
   if ctr==20:
    break
  ctr=0
  idx=len(x2)-1
  while idx>=0:
   x=x2[idx][0]
   idx-=1
   doc_keys.append(x)
   ctr+=1
   if ctr==20:
    break
  #print q_keys
  #print doc_keys
  sim=jaccard(q_keys,doc_keys)
  #print doc_keys
  return sim
  
 
 
file='/home/yashbnit/Downloads/Similar Methods (by documentation).xlsx'

xl=pd.ExcelFile(file)

df=xl.parse('TestData')
ip_name=str(raw_input("Enter method name: "))
#fo=open("documentation.txt","r")

doc_i=str(df.loc[ip_name]["Documentation/desc 2"])
col_alternate="Documentation/desc 1"
if doc_i=='nan':
  print "No Data"
  sys.exit()
doc_set1=df["Documentation/desc 1"]
#print doc_i
dset1=[]

d1=[]
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
  i=unicode(i).encode('utf8')
  urls=Find(str(i))
  if len(urls)!=0 or str(i)=='nan':
   idv=ids[ctr]
   df.drop(ids[ctr],inplace=True)
   continue
  
  dw1=word_tokenize(str(i))
  dw=[]
  for ws in dw1:
   x=camel_case_split(ws)
   if len(x)==0:
    dw=dw1[:]
   for z in x:
    dw.append(z)
  #print dw
  vec=[]
  for j in dw:
   if j==">>>":
    break
   j=j.lower()
   if j not in stop_words and j not in symbols:
    try:
     w=(ps.stem(j))
    except:
     continue
    vec.append(str(w))
    if w not in words:
     words.append(str(w))
  dset1.append(vec)

dw1=word_tokenize(str(doc_i))
dw=[]
for ws in dw1:
  x=camel_case_split(ws)
  for z in x:
    dw.append(z)
for j in dw:
  if j==">>>":
   break
  j=j.lower()
  if j not in stop_words and j not in symbols:
   w=str(ps.stem(j))
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
for d in dset1:
 ctr+=1
 sim=tf_idf(d1,d,freq,N)
 #print sim
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

