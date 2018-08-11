import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 
from nltk.stem import PorterStemmer
import numpy as np
import math as mt
import re
import urllib

ps=PorterStemmer()
stop_words=set(stopwords.words('english'))

symbols=['.',',',';',':','<','>','{','}','[',']','|','\\','+','-','*','/','=','_','!','@','#','$','%','^','&','(',')','~','`','``','?',"'","..","''",",,",". '"]

 
def Find(string):
    # findall() has been used 
    # with valid conditions for urls in string
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return url

def make_vectors(doc,dset1,dset2,df,words,f1,f2):
 vec1=[]
 vec2=[]
 fmap={}
 #print doc
 #print f1
 #print f2
 m=-1
 N=len(dset1)
 for i in words:
  fmap[i]=0
 for j in np.arange(len(doc)):
   w=doc[j]
   fmap[w]+=1
   if fmap[w]>m:
    m=fmap[w]
 for i in words:
   tf=(fmap[i])
   try:
    idf1=mt.log(N/(f1[i]+1),10)
   except:
    idf1=0
   tf_idf1=tf*idf1
   vec1.append(tf_idf1)
   try:
    idf2=mt.log(N/(f2[i]+1),10)
   except:
    idf2=0
   tf_idf2=tf*idf2
   vec2.append(tf_idf2)
 vec_set1=[]
 vec_set2=[]
 for v in dset1:
  fmap1={}
  m1=-1
  v1=[]
  for i in words:
   
   fmap1[i]=0
  for j in np.arange(len(v)):
     w=v[j]
     #print w
     fmap1[w]+=1
     if fmap1[w]>m1:
      m=fmap1[w]
  for i in words:
   try:
    tf=(fmap1[i])
   except:
    tf=0.0
   try:
    idf=mt.log((float)(N)/(f1[i]+1.0),10)
   except:
    idf=0.0
   tf_idf=tf*idf
   #print (i,tf_idf)
   v1.append(tf_idf) 
  vec_set1.append(v1)
 for v in dset2:
  if len(v)==0:
   v_new=[]
   for k in np.arange(len(words)):
    v_new.append(0.0)
   vec_set.append(v_new)
   continue
  fmap1={}
  m1=-1
  v1=[]
  for i in words:
   fmap1[i]=0
  for j in np.arange(len(v)):
     w=v[j]
     fmap1[w]+=1
     if fmap1[w]>m1:
      m=fmap1[w]
  for i in words:
   tf=(fmap1[i])
   try:
    idf=mt.log((float)(N)/(f2[i]+1.0),10)
   except:
    idf=0.0
   tf_idf=tf*idf
   v1.append(tf_idf) 
  vec_set2.append(v1) 
 return vec1,vec2,vec_set1,vec_set2  

def cosine(v1,v2):
 s=0
 #print (v1,v2)
 for i in np.arange(len(v1)):
  s+=v1[i]*v2[i]
 m1=0
 m2=0
 for i in v1:
  m1+=i*i
 for i in v2:
  m2+=i*i
 m1=mt.sqrt(m1)
 m2=mt.sqrt(m2)
 return (float)(s)/(m1*m2)

def find_similarity(dvec1,dvec2,vset1,vset2,df):
  sim_data=[]
  sim_methods=[]
  ids=df.index.values
  #print ids
  #print len(df)
  #print ids
  for i in np.arange(len(df)):
   sim1=cosine(dvec1,vset1[i])
   
   if sim1>=0.95:
    sim_data.append(df.loc[ids[i]])
    sim_methods.append(ids[i])
    continue
   sim2=cosine(dvec2,vset2[i])
   print (sim1,sim2)
   ##if sim2>=0.95:
    #sim_data.append(df.loc[ids[i]])
    #sim_methods.append(ids[i])
  return sim_data,sim_methods  

file='/home/yashbnit/Downloads/Similar Methods (by documentation).xlsx'

xl=pd.ExcelFile(file)

df=xl.parse('TestData')

fo=open("documentation.txt","r")

doc_i=str(fo.read())

doc_set1=df["Documentation/desc 1"]
doc_set2=df["Documentation/desc 2"]

dset1=[]
dset2=[]
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
  
  dw=word_tokenize(str(i))
  vec=[]
  for j in dw:
   if j not in stop_words and j not in symbols and j!='NaN':
    #w=ps.stem(j)
    w=j
    vec.append(str(w))
    if w not in words:
     words.append(str(w))
  #print vec
  dset1.append(vec)
#print ctr
#print df
ctr=-1
for i in doc_set2:
  ctr+=1
  urls=Find(str(i))
  if len(urls)!=0 or i=='nan':
   idv=ids[ctr]
   df.drop(ids[ctr],inplace=True)
   continue
  
  dw=word_tokenize(str(i))
  vec=[]
  for j in dw:
   if j not in stop_words and j not in symbols:
    #w=ps.stem(j)
    w=j
    vec.append(str(w))
    if w not in words:
     words.append(str(w))
  dset2.append(vec)


dw=word_tokenize(str(doc_i))
for j in dw:
  if j not in stop_words and j not in symbols:
   #w=ps.stem(j)
   w=j
   d1.append(str(w)) 

freq_map1={}
freq_map2={}
for i in words:
 freq_map1[i]=0.0
 freq_map2[i]=0.0
 for j in dset1:
  if i in j:
   if i not in freq_map1:
    freq_map1[i]=1
   else:
    freq_map1[i]+=1
 for j in dset2:
  if i in j:
   if i not in freq_map2:
    freq_map2[i]=1
   else:
    freq_map2[i]+=1

#print df

dvec1,dvec2,vec_set1,vec_set2=make_vectors(d1,dset1,dset2,df,words,freq_map1,freq_map2)
#print dvec1
#print dvec2
sim_data,sim_methods=find_similarity(dvec1,dvec2,vec_set1,vec_set2,df)
for i in sim_methods:
 print str(i)
