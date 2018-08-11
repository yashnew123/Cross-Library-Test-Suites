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
import numpy as np
print "Hello1"
file='/home/yashbnit/Final_Data_Python.xlsx'
xl=pd.ExcelFile(file)
df=xl.parse('Sheet1')
#print df
nlp=English()
tokenizer = English().Defaults.create_tokenizer(nlp)

def mytest():
    file_contents = repo.get_file_contents(path)
    return file_contents


def tokenize_docstring(text):
    """Apply tokenization using spacy to docstrings."""
    tokens = tokenizer(text)
    return [token.text.lower() for token in tokens if not token.is_space]


def tokenize_code(text):
    """A very basic procedure for tokenizing code strings."""
    return RegexpTokenizer(r'\w+').tokenize(text)


def get_function_docstring_pairs(blob,r,p):
    """Extract (function/method, docstring) pairs from a given code blob."""
    pairs = []
    try:
        module = ast.parse(blob)
        classes = [node for node in module.body if isinstance(node, ast.ClassDef)]
        functions = [node for node in module.body if isinstance(node, ast.FunctionDef)]
        for _class in classes:
            functions.extend([node for node in _class.body if isinstance(node, ast.FunctionDef)])

        for f in functions:
            ids=df1.index.values
            source = astor.to_source(f)
            docstring = ast.get_docstring(f) if ast.get_docstring(f) else ''
            function = source.replace(ast.get_docstring(f, clean=False), '') if docstring else source
            if p in pt:
              return
            if len(ids)==0:
             max_id=0
            else:
             max_id=ids[len(ids)-1]+1
            print docstring
            results=[]
            results.append(r)
            results.append(p)
            results.append(function)
            results.append(docstring)
            df1.loc[max_id]=results
            writer=pd.ExcelWriter('Final_Data.xlsx')
	    df1.to_excel(writer,'Sheet1')
	    writer.save()
	    
    except (AssertionError, MemoryError, SyntaxError, UnicodeEncodeError):
        pass

g=Github(username,password)
user=g.get_user()
for i in np.arange(len(df)):
 tp=df.loc[i]
 rep_name=tp['repo_name']
 path=tp['repo_path']
 repo=g.get_repo(rep_name)
 print (rep_name,path)
 f2='/home/yashbnit/Final_Data.xlsx'
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
 get_function_docstring_pairs(x,rep_name,path)
