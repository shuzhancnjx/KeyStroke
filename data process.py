# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 15:21:59 2017

@author: ZSHU
"""
from xml.dom.minidom import parse
import os
import csv
import re
import sys 
import zipfile 
import json 
import time 
from datetime import datetime, timedelta, date


reload(sys)
sys.setdefaultencoding('utf8')

working_path= 'C:/Users/ZSHU/Desktop/writing'
os.chdir(working_path)
from_path= r'I:\2017\Pearson\DBA XML Data\Observable Data'

## extact files from I drive 
for path, dirs, names in os.walk(from_path):
    if names: 
        subdir=re.split(r'\\', path)[-1]
        try:
            os.makedirs(working_path+'/'+subdir)
        except WindowsError:
            pass 
        for name in names:
            with zipfile.ZipFile(path+'\\'+name) as zip_ref:
                zip_ref.extractall(working_path+'/'+subdir)
            
            temp_path=working_path+'/'+subdir
            for f in os.listdir(temp_path):
                source=parse(temp_path+'/'+f).getElementsByTagName('testResult')[0]
                if source.getAttribute('subjectName')!='writing':
                    os.remove(temp_path+'/'+f)


###############random codes####################

names=os.listdir(working_path+'/extracted')

source_object=parse(names[0])

ele=source_object.getElementsByTagName('testResult')

ele[0].getAttribute('subjectName')

a=ele[0].attributes.values()

check=[]
for att in ele[0].attributes.values():
    check+= att.value,

ele[0].tagName

temp=[]
with open('sample.csv', 'r') as csvfile:
    samples= csv.reader(csvfile)
    for row in samples:
        temp.append( (row[-5], row[-1])) 


################parsing a sample xml file########################
ob=parse('3590004291_ObservableData.xml').getElementsByTagName('itemResult')

parsed=[]
#saved=sys.stderr
#log= open('log.txt', 'w')
#sys.stdout= log
for element in ob:
    for value in element.getElementsByTagName('outcomeVariable'):
        tmp, time=[], None
        for val in value.getElementsByTagName('value'):
            if val.getAttribute('baseType')=='dateTime':
               time = datetime.strptime(val.firstChild.nodeValue, '%Y-%m-%dT%H:%M:%S.%fZ')  
            if val.getAttribute('baseType')=='string':
                try:
                    mediate=json.loads(val.firstChild.nodeValue)
                    if mediate['name']=='text.change':
                        
                        tmp.extend( [[ time, (mediate['selection']['endPos'], mediate['selection']['startPos']), 
                                      (x['edit'],x['pos'],x['text']), 
                                      mediate['textDiff']['textContext'], 
                                      mediate['textDiff']['textLength']] 
                                      for x in mediate['textDiff']['diffs'] ])

                        parsed.extend(tmp)
                        
                    elif mediate['name']=='UPDATESELECTION':
                        tmp.extend( [time, 'cursor move to %d' % (mediate['selection']['endPos']) ] )
                        parsed.append(tmp)
                except Exception, err:
                    print err
                    pass 
        
############Interval Search############

def IntervalSearch(word_intervals, loc):
    word_intervals.sort()
    l, r= 0, len(word_intervals)-1
    while l<=r:
        m= l+(r-l)/2
        m1, m2= word_intervals[m][0], word_intervals[m][-1]
        if m1<=loc<=m2:
            return word_intervals[m]
        elif loc<m1:
            r=m-1
        else:
            l=m+1
    return None 

def wordSearch(loc):
    l, r=loc-1, loc+1
    while l>=0 and l<len(text) and text[l] not in '.;:, ' :
        l-=1
    while r>=0 and r<len(text) and text[r] not in '.;:, ' :
        r+=1    
    return text[l:r]

def handleNonBreaking(record, preIns):
    new=set(record)
    for edit, loc, letter in record:
        
        if letter.startswith(' '):
            if edit=='INS':
                new.remove(('DEL', preIns+2, u'\xa0'))
            else:
                new.remove(('INS', preIns, u'\xa0' ))
    return sorted(list(new), key=lambda x: x[1])
                
######text construction#############
text=''
texts=[]
for i, records in enumerate(parsed):
    if len(records)<=2:
        continue 
    
    edit, loc, letter = records[2]
    if edit =='INS':
        text= text[:loc-1]+ (str(letter) if letter!=u'\xa0' else ' ') + text[loc-1:]
    elif edit=='DEL':
        text= text[:loc-1]+text[loc-1+len(letter):]
text
########catching valid wrods#####################

words=[]
curword=[]
L_parsed=len(parsed)
for i, records in enumerate(parsed):
    if len(records)==2: # handle cursor move
        if curword!=[]:
            words.append(curword)
            words.append( records[1] )
            curword=[]
        else:
            words.append( records[1] )
    
    else:
        edit, loc, letter=records[2]
        if edit=='INS':
            if letter==u'\xa0':
                if i+1<L_parsed and len(parsed[i+1])>2 and parsed[i+1][2][0]=='INS':
                    words.append(curword)
                    curword=[]
            elif len(letter)==2 and (letter[0]==' ' or letter[1]==' '):
                curword.append( (loc+1,letter[1]) if letter[1]!=' ' else (loc,letter[0]))
            elif letter in '.,:?! ':
                words.append(curword)
                if letter!=' ':
                    words.append([(loc, letter)])
                curword=[]
            else:
                curword+= (loc, letter), 
        else:
            if letter!=u'\xa0':
                if len(letter)==2:
                    curword.append( [loc, letter[1]] if letter[1]!=' ' else [loc-1, letter[0]]  ) 
                    words.append(curword)
                    curword=[]
                elif letter in '.,:?! ':
                    if curword!=[]:
                        words.append(curword)
                    curword=[[loc, letter]]
                else:
                    curword.append( [loc, letter])

words= filter(lambda x: not isinstance(x, str), words)
with open('words.txt', 'w') as f:
    for x in words:
        f.write(str(x)+'\n')
######## processing words#####



            

       
    
    
        
########parsing datetime###############
datetime.strptime(parsed[0][0], '%Y-%m-%dT%H:%M:%S.%fZ')  

