import subprocess
import numpy as np
from github import Github
from github import ContentFile
from github.ContentFile import *
from spacy import *
import ast
from ast import *
import astor
from spacy.lang.en import English
from regex import *
from nltk import *
import pandas as pd

print "Hello1"
file='/home/yashbnit/Downloads/Final_Data_Java.xlsx'
xl=pd.ExcelFile(file)
df=xl.parse('Sheet1')
#print df
def get_function_docstring_pairs(repo_name,path):
        print "Hello3"
	command = ['./gradlew','run']
	p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None)
	text = p.stdout.read()
	retcode = p.wait()
	string= text.decode("utf-8")
        print "Hello2"
	name=""
	code=""
	javadoc=""
	temp=""
	extra=""
	flag=-1
	i=0
	while i<len(string):
	 if string[i]=='#' and flag==-1:
	  i=i+20
	  flag=0
	  #print 'Hello1'
	 elif string[i]=='$' and flag==0:
	  i=i+20
	  name=temp[:]
	  
	  temp=""
	  flag=1
	  #print 'Hello2'
	 elif string[i]=='~' and flag==1:
	  i=i+20
	  code=temp[:]
	  
	  temp=""
	  flag=2
	  #print 'Hello3'
	 elif string[i]=='`' and flag!=3:
	  i=i+20
	  flag=3
	  #print 'Hello4'
	 elif string[i]=='`' and flag==3:
	  i=i+20
	  extra+=temp
	  temp=""
	  flag=-1
	  #print 'Hello4'
	 elif string[i]=='^' and (flag==2 or flag==1):
	  i=i+20
	  if flag==2:
	   javadoc=temp[:]
	   
	   temp=""
	  elif flag==1:
	   code=temp[:]
	   temp=""
	  #print 'Hello5 '+str(flag)
	  flag=-1
	  temp1=""
	  j=0
	  if len(javadoc)>0:
	   while j<len(javadoc):
	    if code[j]==javadoc[j]:
	     j+=1
	    else:
	     break
	   temp1=code[j:]
	   code=temp1[:]
	  f1='/home/yashbnit/Final_Data_1.xlsx'
          xl1=pd.ExcelFile(f1)
          df1=xl1.parse('Sheet1')
          f2='/home/yashbnit/Extra_Data_Java.xlsx'
          xl2=pd.ExcelFile(f2)
          df2=xl2.parse('Sheet1')
          try:
		  print "Name: "+str(name)
		  print "Code: "+str(code)
		  print "Javadoc: "+str(javadoc)
		  ids=df1.index.values
		  if len(ids)==0:
		     max_id=0
		  else:
		     max_id=ids[len(ids)-1]+1
		    
		  results=[]
		  results.append(repo_name)
		  results.append(path)
		  results.append(code)
		  results.append(javadoc)
		  df1.loc[max_id]=results
		  writer=pd.ExcelWriter('/home/yashbnit/Final_Data_1.xlsx')
		  df1.to_excel(writer,'Sheet1')
		  writer.save()
	  except:
	   print "Encoding Error"
	  name=""
	  code=""
	  javadoc=""
	 else:
	  if string[i]!='/' and string[i]!='*' :
	   #if flag==1:
	    #if string[i]!=' ' and string[i]!='\n':
	     temp=temp+string[i]
	  i+=1
        try:
		print "Extra: "+str(extra)
		if len(extra)>0:
		    results1=[]
		    results1.append(repo_name)
		    results1.append(path)
		    results1.append(extra)
		    ids=df2.index.values
		    if len(ids)==0:
		     max_id=0
		    else:
		     max_id=ids[len(ids)-1]+1
		    df2.loc[max_id]=results1
		    writer=pd.ExcelWriter('/home/yashbnit/Extra_Data_Java.xlsx')
		    df2.to_excel(writer,'Sheet1')
		    writer.save()
        except:
          print "Encoding Error1" 

g=Github(username,password)
user=g.get_user()
for i in np.arange(len(df)):
 tp=df.loc[i]
 rep_name=tp['repo_name']
 path=tp['repo_path']
 repo=g.get_repo(rep_name)
 print (rep_name,path)
 f2='/home/yashbnit/Final_Data_1.xlsx'
 xl2=pd.ExcelFile(f2)
 df1=xl2.parse('Sheet1')
 pt=list(df1['repo_path'])
 #print pt
 if (path) in pt:
  print "Yes"
  continue
 #sys.exit(0)
 
 #print repo.get_readme().decoded_content
 try:
  print "Hello"
  file_contents = repo.get_file_contents(path)
 except:
  print "Error"
  continue
 x=file_contents.decoded_content
 #print x
 fp=open('source_to_parse/temp.java','w')
 fp.write(x)
 fp.close()
 get_function_docstring_pairs(rep_name,path)
