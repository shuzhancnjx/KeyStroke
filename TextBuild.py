# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 10:09:22 2017

@author: ZSHU
"""
class Node(object):
    def __init__(self, position, letter):
        self.position= position 
        self.curLetter=letter
        self.history=''
        self.pre=None
        self.next=None

class LinkedList(object):
    def __init__(self):
        self.head=Node(0, '')
        self.tail=Node('End', '')
        self.head.next=self.tail
        self.tail.pre=self.head
        self.pos={0: self.head, -1:self.tail}
    
    def AddBeforeTail(self, letter, loc):
        node=Node(loc, letter)
        node.next=self.tail
        node.pre=self.tail.pre
        self.tail.pre.next=node
        self.tail.pre=node
        self.pos[loc]=node 
        
    def DelBeforeTail(self):
        if self.head.next!=self.tail:
            
            node=self.tail.pre.pre
            node_to_del= self.tail.pre
            
            self.tail.pre=node
            node.next=self.tail 
            
            del node_to_del
        
            
    def UpDate(self, loc, letter, edit):
        node=self.pos[loc]
        if edit=='INS':
            while letter!='' and node!=self.tail:
                preLetter=node.curLetter
                node.curLetter=letter
                self.pos[loc]=node 
                letter=preLetter
                node=node.next 
                loc+=1
                
            if node==self.tail:
                assert(loc!='')    
                self.AddBeforeTail(letter,self.tail.pre.position+1 )
        else:
            assert(node.curLetter==letter)
            while node.curLetter!='' and node.next:
                pre=node.curLetter
                node.curLetter= node.next.curLetter
                node.history+= (str(pre)+str([str(pre)]) if pre.isalpha() else '')
                self.pos[loc]=node
                
                node=node.next
                loc+=1
                

            
############Testing Case ###########################################
parsed= filter(lambda x: len(x)==5, parsed)
with open('w.txt','w') as f:
    for i, w in enumerate(parsed):
        f.write(str(i)+' '+str(w[2])+'\n')



text= LinkedList()
for i, records in enumerate(parsed[:2563]):
    

    
    edit, loc, letter = records[2]

    if loc not in text.pos:
        for j, l in enumerate(letter):
            text.AddBeforeTail(l, loc+j)
    else:
        if edit=='INS':
            for j, l in enumerate(letter):
                text.UpDate(loc+j, l, edit)
        else:
            for j, l in enumerate(letter[::-1]):
                
                text.UpDate(len(letter)+loc-j-1, l, edit)



t=''
m=text.head.next
while m!=text.tail:
   t+= ('('+m.history+')' if m.history!='' else '') +m.curLetter
   m=m.next
t


    
        
    