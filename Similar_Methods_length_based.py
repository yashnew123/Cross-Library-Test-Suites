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
ADL=0.0

sss_url = "http://swoogle.umbc.edu/SimService/GetSimilarity?"

def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]

def sss(s1, s2, type='relation', corpus='webbase'):
    #print s2
    try:
        response = get(sss_url, params={'operation':'api','phrase1':s1,'phrase2':s2,'type':type,'corpus':corpus})
        return float(response.text.strip())
    except:
        print 'Error in getting similarity for %s: %s' % ((s1,s2), response)
        return 0.0



def Find(string):
    # findall() has been used 
    # with valid conditions for urls in string
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return url

def tf_idf(q,doc,freq,N,qlf):
 #print doc
 tf_id={}
 ritf={}
 lrtf={}
 britf={}
 blrtf={}
 tff={}
 #print "Query: "+str(q)
 #print "Doc: "+str(doc)
 for w in q:
  if w not in tf_id:
   tf_id[w]=0.0
 for w in doc:
  if w in q:
   tf_id[w]+=1
 #mx=-100
 #print tf_id
 avg_tf=0.0
 tf={}
 for i in doc:
  if i not in tf:
   tf[i]=1.0
  else:
   tf[i]+=1
 for i in tf:
  val=tf[i]
  avg_tf+=val
 avg_tf=avg_tf/len(tf)
 #print "Avg_TF: "+str(avg_tf)
 for i in tf_id:
  val=tf_id[i]
 # try:
  ritf[i]=(float)(mt.log((1+val),2))/mt.log((1+avg_tf),2)
  #except:
   #ritf[i]=(float)(mt.log((1+val),2))/(1+mt.log((1+avg_tf),2))
  lrtf[i]=tf_id[i]*mt.log((1+(ADL/len(doc))),2)
  #print "lrtf: "+str(i)+" "+str(lrtf[i])
 for i in ritf:
  val=ritf[i]
  britf[i]=(float)(val)/(1+val)
 for i in lrtf:
  val=lrtf[i]
  blrtf[i]=(float)(val)/(1+val)
 for i in ritf:
   tff[i]=qlf*britf[i]+(1.0-qlf)*blrtf[i]
 sim_score=0.0
 idf_sum=0.0
 for w in tff:
  idf=mt.log((float(N)/(1.0+freq[w])),10)
  #print "idf: "+str(idf)
  sim_score+=tff[w]*idf
  #print tff[w]
  idf_sum+=idf
 sim_score=(float)(sim_score)/(idf_sum)
 #sim_score=sim_score*0.8+0.2
 return sim_score
 
 
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
  ctr+=1
  #print str(i)
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
    w=str(ps.stem(j))
    vec.append(str(w))
    if w not in words:
     words.append(str(w))
  dset1.append(vec)

for i in dset1:
 l=len(i)
 ADL+=l

ADL=(float)(ADL)/len(dset1)
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

qlf=2.0/(1+mt.log((1+len(d1)),2))
print "\n\nTF-IDF Similarity: "
N=len(dset1)
ids=df.index.values
ctr=-1
sim_scores1={}

sim_methods1=[]
for d in dset1:
 ctr+=1
 sim=tf_idf(d1,d,freq,N,qlf)
 name_sim=sss(ip_name.upper(),str(ids[ctr]).upper())
 if name_sim==-float('inf'):
  name_sim=0
 #print sim
 sim=((sim+name_sim)/2.0)*0.8+0.2
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

sim_scores2={}
doc_set3=df['Documentation/desc 1']
dset3=[]
for i in doc_set3:
  ctr+=1
  #print str(i)
  urls=Find(str(i))
  if len(urls)!=0 or str(i)=='nan':
   continue
  
  dw1=word_tokenize(str(i))
  dw=[]
  #for ws in dw1:
   #x=camel_case_split(ws)
  # for z in x:
    #dw.append(z.upper())
  #print dw
  dw=dw1
  text=""
  for j in dw:
   if j==">>>":
    break
   if j!='nan':
    w=str(j)
    text=text+" "+str(w)
  dset3.append(text)
  #print "Doc: "
  #print text

d3=""
dw1=word_tokenize(str(doc_i))
dw=[]
#for ws in dw1:
 #x=camel_case_split(ws)
 #for z in x:
  #dw.append(z)
dw=dw1
for j in dw:
  #print j
  if j==">>>":
   break
  w=str(j)
  d3=d3+" "+str(w) 

print "\n\nSemantic Similarity: "

#print d3

ctr=-1
for i in dset3:
 
 ctr+=1
 sim=(sss(d3,i)+sss(ip_name.upper(),str(ids[ctr]).upper()))/2.0
 sim_scores2[ids[ctr]]=sim
 print ids[ctr]+" : "+str(sim)
 
sort_methods2=sorted(sim_scores2.items(),key=operator.itemgetter(1))

idx=len(sort_methods2)-1
ctr=0
sim_methods2=[]
while ctr<3:
 sim_methods2.append(str(sort_methods2[idx][0]))
 idx-=1
 ctr+=1

print "\n\nTop three libraries: "
print sim_methods2
 
