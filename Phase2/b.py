import random

#displaying memory card
def display(memory):
    print("\nEXTERNAL MAIN MEMORY: ")
    for i in range(100):
        print(i,end='\t')
        for j in range(4):
            print(memory[i][j],end='')
        print()
    print()

def address_map(va):
    global PTR,pte,pi
    if va>=0 and va<=99:
        pte=PTR + va//10
        temp=("".join(memory[pte][0:2]))
        if temp=="":
            pi=3
            return
        ra=int(temp)*10 + va%10
        return ra
    else:
        pi=2

def allocate():
    global check,PTR
    
    while(1):
        temp=random.randint(0,29)
        if check[temp]==0:
            check[temp]=1
            break


    return temp*10

#storing instructions
def load(data):
    """ for i in range(instno-1):
        for j in range(4):
            temp=f.read(1)
            if temp=='\n':
                temp=f.read(1)
            memory[i][j]=temp
    
    memory[i+1][0]=f.read(1)
    f.read(1) """

    loc=allocate()



#get data function and storing data in memory
def gd(loc):
    data=f.readline().rstrip('\n')
    n=len(data)
    ptr=n

    i=loc
    j=0
    while (ptr):
        memory[i][j]=data[n-ptr]
        ptr-=1
        j+=1
        if j==4:
            j=0
            i+=1

#put data function and writing data in output file      
def pd(loc):

    data=''
    temp=((loc//10)+1)*10
    i=loc
    j=0

    while i!=temp-1 and i<100:
        data+=memory[i][j]
        j+=1
        if j==4:
            j=0
            i+=1
    file = open('OS\Phase1\output.txt','a')
    file.write(data)
    file.write('\n')
    file.close()

def terminate():
    file = open('OS\Phase1\output.txt','a')
    file.write('\n\n')
    file.close()
    print("JOB DONE")
    return

#load register function and storing data in register
def lr(loc):
    global register
    register=''
    temp=((loc//10)+1)*10
    i=loc
    j=0

    while i!=temp-1 and i<100  and len(register)<4:
        register+=memory[i][j]
        j+=1
        if j==4:
            j=0
            i+=1
    

#load register function and storing register data in memory
def sr(loc):
    global register
    n=len(register)
    ptr=n

    i=loc
    j=0
    while (ptr):
        memory[i][j]=register[n-ptr]
        ptr-=1
        j+=1
        if j==4:
            j=0
            i+=1

#compare register function and comparing register data with memory data
def cr(loc):
    global c
    global register
    n=len(register)
    ptr=0
    temp=((loc//10)+1)*10
    i=loc
    j=0

    if n==0:
        c=0
        return

    while i!=temp and loc+i<100 and temp<100 and ptr<n:
        print(register[ptr],memory[i][j])
        if register[ptr]!=memory[i][j]:
            c=0
            return
        
        ptr+=1
        j+=1
        if j==4:
            j=0
            i+=1
    c=1
    return

""" def add(loc):
    global register
    

    data=''
    temp=((loc//10)+1)*10
    i=loc
    j=0

    while i!=temp-1 and i<100:
        data+=memory[i][j]
        j+=1
        if j==4:
            j=0
            i+=1

    temp1=str(int(register)+int(data))

    n=len(str(temp1))
    ptr=n
    i=loc
    j=0
    while (ptr):
        memory[i][j]=temp1[n-ptr]
        ptr-=1
        j+=1
        if j==4:
            j=0
            i+=1
    return """

#executing all the instructions
def execute():
    global c, mode, ic, inst, si
    inst=''
    ic=0
    while(1):
        for j in range(4):
            inst+=memory[ic][j]
        
        if inst[0:2]=='GD':
            mode=1
            si=1
            gd(int(inst[2:4]))
            inst=''
        elif inst[0:2]=='PD':
            mode=1
            si=2
            pd(int(inst[2:4]))
            inst=''
        elif inst[0:1]=='H':
            mode=1
            si=3
            terminate()
            return
        elif inst[0:2]=='LR':
            lr(int(inst[2:4]))
            inst=''
        elif inst[0:2]=='SR':
            sr(int(inst[2:4]))
            inst=''
        elif inst[0:2]=='CR':
            cr(int(inst[2:4]))
            inst=''
        elif inst[0:2]=='BT':
            if c==1:
                i=int(inst[2:4])
                c=0
                inst=''
                continue
            else:
                inst=''
        """ elif inst[0:2]=='AD':
            add(int(inst[2:4]))
            inst='' """
        mode=0
        i+=1

        



f=open(r"OS\Phase1\input7.txt","r")

file=open('OS\Phase1\output.txt','w')
file.close()

while(1):
    if f.read(4)!='$AMJ':
        break


    PTR=-1
    si,pi,ti=3,0,0
    jobid,ttl,tll,tlc,ttc='','','','',''
    pcb={"jobid":jobid,"ttl":ttl, "tll":tll, "tlc":tlc, "ttc":ttc}
    em={0:"No error",1:"Out of Data",2:"Line Limit Exceeded",3:"Time Limit Exceeded",4:"Operation Code Error",5:"Operand Error",6:"Invalid Page Fault"}

    register=''
    c=0
    mode=0
    ic=0
    inst=''
    
    memory=[]
    check=[]
    for i in range(300):
        memory.append(['']*4)
    for i in range(30):
        check.append(0)
    PTR=allocate()
    
    


    jobid=f.read(4)
    ttl=int(f.read(4))
    tll=int(f.read(4))
    f.read(1)

    print()
    print(jobid,ttl,ttl)

    while(1):
        data=f.readline().rstrip('\n')
        if data=='$DTA':
            execute()
            break
        else:
            load(data)
    

    if f.read(8)=='$END'+jobid:
        f.read(1)
        display(memory)

f.close()