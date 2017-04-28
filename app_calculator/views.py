from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect

# Create your views here.
def isnumber(id):
    flag=True
    chars=id.split()
    for c in chars:
        if c<'0' or c>'9':
            flag=False
            return flag
    return flag


def isoperator(c):
    if c=='+' or c=='-' or c=='*' or c=='/':
        return True
    else:
        return False

def check_nondigit(st):
    flag=False
    for c in st:
        if isoperator(c) or (c>='0' and c<='9') or c=='(' or c==')':
            continue
        else:
            flag=True
    return flag

def tokenizer(st):
    li=[]
    l=len(st)
    i=0
    while i<l:
        if st[i]==' ':
            i=i+1
            continue
        elif st[i]>='0' and st[i]<='9':
            w=""
            while i<l and st[i]>='0' and st[i]<='9':
                w=w+st[i]
                i=i+1
            li.append(w)
        else:
            li.append(st[i])
            i=i+1
    return li


def convert(e):
    post_exp=[]
    op_stack=[]
    prec={}
    prec['+']=1
    prec['-']=1
    prec['*']=2
    prec['/']=2
    i=0
    l=len(e)
    while i < l:
        token=e[i]
        if isnumber(token):
            post_exp.append(int(token))
        elif token=='(':
            op_stack.append(token)
        elif token==')':
            while True:
                length = len(op_stack)
                if(op_stack[length-1]=='('):
                    op_stack.pop()
                    break
                else:
                    post_exp.append(op_stack.pop())
        else:
            if op_stack:
                while not op_stack and prec[op_stack[-1]]<= prec[token]:
                    post_exp.append(op_stack.pop())
            op_stack.append(token)
        i=i+1
    while op_stack:
        post_exp.append(op_stack.pop())
    return  post_exp

def evaluate(exp):
    result=0
    st=[]
    for c in exp:
        if isoperator(c):
            r=0
            if c=='+':
                id1=st.pop()
                id2=st.pop()
                r=id2+id1
            elif c=='-':
                id1=st.pop()
                id2=st.pop()
                r=id2-id1
            elif c=='*':
                id1=st.pop()
                id2=st.pop()
                r=id2*id1
            elif c=='/':
                id1=st.pop()
                id2=st.pop()
                r=id2/id1
            st.append(r)
        else:
            st.append(c)
    return st[0]

def remove_space(str):
    s=""
    for ch in str:
        if ch!=' ':
            s=s+ch
    return s;

def calculator_page(request):
    success=False
    if request.method=='POST':
        success=True
        error=""
        result=0
        exp=request.POST.get('expression')
        exp=remove_space(exp)
        if(exp==""):
            error="You entered a empty expression."
        elif check_nondigit(exp):
            error="You have entered some non-digit character."
        else:
            tokens=tokenizer(exp)
            post_fix=convert(tokens)
            result=evaluate(post_fix)
        return render(request,'calculator.html',{'success':success,'expression':exp,'result':result,'error':error})
    else:
        return render(request,'calculator.html')
