statev=-1
def generateState():
    global statev
    statev+=1
    return statev

def isOperator(ch):
    if ch=='+' or ch=='*' or ch=='|' or ch=='@' or ch=='?' or ch=='^':
        return True
    else:
        return False
    
def isBinOperator(op):
    if op=='|' or op=='@':
        return True
    else:
        return False


class State:
    def __init__(self):
        self.atrans=list()
        self.btrans=list()
        self.etrans=list()
        self.initial=None
        self.final=None

class Stack:
    def __init__(self):
        self.stls=list()
    
    def push(self,node):
        self.stls.append(node)
        return None
    
    def pop(self):
        if len(self.stls)>=1:
            return self.stls.pop()
        else:
            print 'Stack empty'
            return None

    def top(self):
        if len(self.stls)>=1:
            leng=len(self.stls)
            leng-=1
            return self.stls[leng]
        else:        
            return None
    def stackEmpty(self):
        if len(self.stls)==0:
            return True
        else:
            return False

    def disp(self):
        print 'Stack',self.stls    
        return None

def alternation(op1,op2):
    fin=State()
    x=generateState()
    y=generateState()
    fin.initial=x
    fin.final=y
    tmp=list()
    for item in op1.atrans:
        tmp+=item
    fin.atrans.append(tmp)
    tmp=list()
    for item in op2.atrans:
        tmp+=item
    fin.atrans.append(tmp)
    tmp=list()
    for item in op1.btrans:
        tmp+=item
    fin.btrans.append(tmp)
    tmp=list()
    for item in op2.btrans:
        tmp+=item
    fin.btrans.append(tmp)
    tmp=list()
	
    fin.etrans.append(op1.etrans)
    fin.etrans.append(op2.etrans)
    
    fin.etrans.append([x,op1.initial])
    fin.etrans.append([x,op2.initial])
    fin.etrans.append([op1.final,y])
    fin.etrans.append([op2.final,y])
    
    return fin        
		
def concat(op1,op2):
    fin=State()
    tmp=list()
    for item in op1.atrans:
        tmp+=item
    fin.atrans.append(tmp)
    tmp=list()
    for item in op2.atrans:
        tmp+=item
    fin.atrans.append(tmp)
    tmp=list()
    for item in op1.btrans:
        tmp+=item
    fin.btrans.append(tmp)
    tmp=list()
    for item in op2.btrans:
        tmp+=item
    fin.btrans.append(tmp)
    tmp=list()
	
    fin.etrans+=op1.etrans
    fin.etrans+=op2.etrans
        
    fin.etrans.append([op1.final,op2.initial])
    fin.initial=op1.initial
    fin.final=op2.final
    return fin

def kclosure(op1):	
    fin=State()
    x=generateState()
    y=generateState()
    tmp=list()
    for item in op1.atrans:
        tmp+=item
    fin.atrans.append(tmp)
    tmp=list()
    for item in op1.btrans:
        tmp+=item
    fin.btrans.append(tmp)
    tmp=list()
    
    fin.etrans.append([op1.final,op1.initial])
    fin.etrans.append([x,op1.initial])
    fin.etrans.append([op1.final,y])
    fin.etrans.append([x,y])
    fin.initial=x
    fin.final=y
    return fin
		
def operate(o1,o2,op):
    if op=='|':
        return alternation(o1,o2)
    elif op=='@':
        return concat(o1,o2)
			
def coper(o1,op):
	if op=='*':
		return kclosure(o1)

def priority(c):
	if c=='|':
		return 1
	elif c=='@':
		return  2
	elif c=='+' or c=='*' or c=='?':
		return 3
	elif c=='^':
		return 4
		
def beg():
	firch=None
	secch=None
	op=''
	ip=raw_input('Enter a regular expression(only a and b are allowed):')
	f_ind=0
	s_ind=1
	op+=ip[0]
	while f_ind<len(ip) and s_ind<len(ip):
		firch=ip[f_ind]
		f_ind+=1
		secch=ip[s_ind]
		s_ind+=1
		if firch=='(' or (secch=='|' or secch=='*' or secch=='+' or secch=='?') or (secch==')') or(firch=='|'):
			op+=secch
		else:
			op+='@'+secch
	return op


def main():
    sta=Stack()
    inp=beg()	
    ind=0
    char=None
    tmp=None
    op=''
    toptoken=None
    while ind<len(inp):
        char=inp[ind]
        if char=='(':
            sta.push(char)
        elif char==')':
            tmp=sta.pop()
            while tmp!='(':
                op+=tmp
                tmp=sta.pop()
        elif isOperator(char):
            toptoken=sta.top()			
            while not sta.stackEmpty() and priority(char)<=priority(toptoken): 
                op+=sta.pop()
                toptoken=sta.top()
            sta.push(char)		
        else:
            op+=str(inp[ind])
        ind+=1
    while not sta.stackEmpty():
        tmp=sta.pop()
        op+=tmp
    print 'post fix',op		
	
    ip=op
    ind=0
    ch=None
    op1=None
    op2=None
    res=None
    st=Stack()
    while ind<len(ip):
        ch=ip[ind]
        if not isOperator(ch):
            sta=State()
            one=generateState()
            two=generateState()
            tran=list()
            tran.append(one)
            tran.append(two)

            sta.initial=one
            sta.final=two
            
            if ch=='a':
                sta.atrans.append(tran)
            elif ch=='b':
                sta.btrans.append(tran)
                
            st.push(sta)
        elif isOperator(ch):
            if isBinOperator(ch) and not st.stackEmpty(): 
                op2=st.pop()
                op1=st.pop()
                res=operate(op1,op2,ch)
                st.push(res)
                
            elif not isBinOperator(ch) and not st.stackEmpty():
                op1=st.pop()
                res=coper(op1,ch)
                st.push(res)
		
            else:
                pass
        ind+=1
        
    tmp=State()
    if not st.stackEmpty():
        tmp=st.pop()
        print 'a trans list',tmp.atrans
        print 'b trans list',tmp.btrans
        print 'epsilon transition',tmp.etrans
        print 'initial',tmp.initial
        print 'final',tmp.final

if __name__=='__main__':
    main()



