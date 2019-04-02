def minFunc(numVar, stringIn):
	#parses the input to get the lists in the desired manner
	def parseInput(x):
		g = x.split('d')
		f=[]
		d=[]
		if '(' in g[0]:
			f=g[0].split('(')[1].replace(')','').replace(' ','').split(',')
		if '(' in g[1]:
			d=g[1].split('(')[1].replace(')','').replace(' ','').split(',')
		return f,d

	#converts list with decimals to a list with their corresponding binary equivalent
	def dectobin(n,f):
		b =[]
		for i in f:
			b.append(bin(int(i)).split('b')[1].rjust(n).replace(' ','0'))
		return b
	#converts the list into a dictionary
	def dicify(b):
		a={}
		for i in b:
			a[i] = [int(i,2)]
		return a
	#creates the groups according to the number of 1's
	def grouping(n,b):
		p=[]
		for i in range(n+1):
			q=[]
			for j in b.keys():
				tmp={}
				if j.count("1")==i:
					tmp[j] = b[j]
					q.append(tmp)
			p.append(q)
		return p

	#creates all the prime implicants
	def pairing(n,b):
		p = grouping(n,b)
		qq = []
		pis = {}
		for x in b.keys():
			z={}
			z[x]=b[x]
			qq.extend([z,0])
		for i in range(len(p)-1):
			for k in p[i]:
				for d in p[i+1]:
					s=''
					counter = 0
					for x in range(n):
						if list(k.keys())[0][x]==list(d.keys())[0][x]:
							s+=str(list(k.keys())[0][x])
						else:
							s+='-'
							counter += 1
							h1=qq.index(k)
							qq[h1+1] += 1
							h2=qq.index(d)
							qq[h2+1] += 1
						if counter >1:
							h1=qq.index(k)
							qq[h1+1] -= 2
							h2=qq.index(d)
							qq[h2+1] -= 2
							s=''
							break
					if s!='':			
						pis[s] = list(k.values())[0]+list(d.values())[0]
		for g in range(0,len(qq),2):
			if qq[g+1] < 1:
				pis[list(qq[g].keys())[0]]=list(qq[g].values())[0]
		return pis		
	#to select the essential prime implicants		
	def makepichart(pis,f):
		epi={}
		fqc = {}
		for i in f:
			fqc[i] = 0
		for i in fqc:
			for j in pis.keys():
				if int(i) in pis[j]:
					fqc[i] += 1
		for i in fqc:
			if fqc[i]==1:
				for j in pis:
					if int(i) in pis[j]:
						epi[j]=pis[j]
						break		
		return epi,fqc
	#a function to multiply 2 lists
	def multiplylists(a,b):
		x=[]
		for i in a:
			for j in b:
				x.append(list(set(i+j)))
		if len(a)==0 and len(b) != 0:
			return reduced([b])[0]
		if len(a) != 0 and len(b) == 0:
			return reduced([a])[0]
		return reduced([x])[0]
	#chooses the expressions with minimium no of literals amongst all the possiblities
	def selectminliteral(a):
		nol_list=[]
		for i in a:
			c=0
			for j in i:
				if j in chars:
					c+=1
			nol_list.append(c)
		x = min(nol_list)
		min_nol_list=[]
		for i in range(len(a)):
			if nol_list[i]==x:
				min_nol_list.append(a[i])
		return min_nol_list
	#to select the remaining prime implicants if any
	def selectpi(pis,fqc):
		mul = []
		for i in fqc:
			if fqc[i] > 1:
				a=[]
				t=0
				for h in pis.keys():
					t+=1
					if int(i) in pis[h]:
						a.append([h])
				mul.append(a)
				if len(mul) > 1:
					mul = [multiplylists(mul[0],mul[1])]
		len_list=[]
		if len(mul)==0:
			return []
		return mul[0]
	#to reduce the expressions using boolean algebra
	def reduced(a):
		delem=[]
		ha=[]
		for i in range(1,n+1):
			for j in a[0]:
				if len(j) == i:
					for k in a[0]:
						if len(k) > i:
							c=1
							for l in j:
								if l not in k:
									c=0
									break
							if c==1:
								delem.append(k)	
								
		for b in a[0]:
			if b not in delem and b not in ha:
				ha.append(b)
		return [ha]
	#a function to simply convert the binary representation to a beautiful expression
	def beautify(a):
		s=''	
		for i in sorted(a[0]):
			for k in i:
				s+= k
			s+='+'
		k = ''
		c=0
		for i in s:
			if i=='0':
				k += chars[c] + "'"
				c+=1
			if i=='1':
				k += chars[c]
				c+=1
			if i=='+':
				k+= '+'
				c=0
			if i=='-':
				c+=1
		return ''.join(i + '+' for i in sorted(k[:len(k)-1].split('+')))[:-1]
	#main stuff
	chars = 'wxyzabcdef'
	n = numVar		
	f,d = parseInput(stringIn)
	#handling a corner case
	if n==1:
		if len(f)==0:
			return ('Simplified Expression: 0')
			#exit()
		if len(f)==1:
			return ('Simplified Exression: 1')
			#exit()
	if len(f)==0:
		return ('Simplified Expression: 0')
	v=[]
	for i in f+d:
		if i!='':
			v.append(i)
	t = dectobin(n,v)
	t=dicify(t)
	for i in range(1,n+1):
		t = pairing(n,t)
	pis = t
	epi,fqc = makepichart(t,f)
	minimizers = selectpi(pis,fqc)
	g=''
	big_x=[]
	x = list(epi.keys())
	x=multiplylists([x],minimizers)
	mi=[]
	for i in x:
		mi.append(beautify([i]))
	mi = selectminliteral(mi)
	for i in mi:
		g += i + ' OR '
	#taking care for corner cases
	if g=='' or g[:4] == ' OR ':
		if len(pis) > 0:
			g = '1    '
		else:
			g = '0    '
	g = 'Simplified Expression: ' + g
	return (g[:len(g)-4])
'''
Sample Input/Output method -
numVar = int(input("No. of variables: "))
StringIn = input("Function: ")
print (minFunc(numVar,StringIn))
'''	

	
