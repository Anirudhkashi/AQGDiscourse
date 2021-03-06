import re
import enchant
class Features():
	def __init__(self):
			self.prevInChain=0
			self.braceCount=0
			self.commentBlock=""
			self.encModel=enchant.Dict("en_US")
			self.keywords=["public","static","void","main","if","else","for","while","class","import","int","float","String","private","return","this","new","char","double","short","bool","byte","extends","implements"]	#Set

	def ratioK(self, s):
		sW=[ele for ele in re.split("[^A-Za-z0-9_$]",s) if ele!=""]	
		l=len(sW)
		c=0.0
		for ele in sW:
			if ele in self.keywords:
				c+=1
		if float(l)!=0.0:
			return c/l
		return 0.0

	def operators(self, s):
		operatorList=["+","-","*","/","^","%",">","<","="]	#set
		for ele in operatorList:
			if ele in s:
				return 1.0
		return 0.0

	def comments(self, s):
		commentSingle=["//"]	#set
		commentMultiple=[["/*","*/"],["/**","*/"]]	#set
		commentDict={"//":0,"/*":1,"/**":1}
		if self.commentBlock!="":
			for ele in commentMultiple:
				if ele[0]==self.commentBlock:
					if ele[1] in s:
						self.commentBlock=""
			return 1.0
		else:
			cIndex=9999
			cValue=-1
			for k,v in commentDict.items():
				if k in s and cIndex>s.index(k):
					cIndex=s.index(k)
					cValue=v
			if cValue==0:
				return 1.0
			elif cValue==1:
				for ele in commentMultiple:
					if ele[0] in s:
						if ele[1] not in s:
							self.commentBlock=ele[0]
				return 1.0
			else:
				return 0.0
		return 0.0

	def braces(self, s):
		tmp=0
		if "{" in s:
			self.braceCount+=1
		if self.braceCount>0:
			tmp=1
		if "}" in s:
			self.braceCount-=1
		return float(tmp)

	def indent(self, s):
		if s[0]==" " or s[0]=="\t":
			return 1.0
		return 0.0

	def semicolon(self, s):
		if s[:-1]==";":
			return 1.0
		return 0.0

	def programChain(self):
		if self.prevInChain==1:
			self.prevInChain=0
			return 1.0
		return 0.0

	def capital(self, s):
		for i in s:
			if i==" " or i=="\t":
				continue
			else:
				if i>="a" and i<="z":
					return 1.0
				return 0.0

	def ratioC(self, s):
		sW=[ele for ele in re.split("[^A-Za-z0-9_$]",s) if ele!="" and ele not in self.keywords]	
		l=len(sW)
		c=0.0
		for ele in sW:
			if self.encModel.check(ele):
				c+=1
		if float(l)!=0.0:
			return 1.0-c/l
		return 1.0