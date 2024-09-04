import random

def display(memory):
    '''displaying memory card'''

    print("\nEXTERNAL MAIN MEMORY: ")
    for i in range(len(memory)):
        print(i,end='\t')
        for j in range(4):
            print(memory[i][j],end='')
        print()
    print()


def load():
    '''loading the instructions in memory'''

    def allocate():
            '''allocating memory for program'''

            global check,PTR
            while(1):
                temp=random.randint(0,29)
                if check[temp]==0:
                    check[temp]=1
                    break
            return temp

    def mos():
            '''machine operation system'''

            def terminate(e):
                '''terminating the program'''

                global ic,ir,ttc,llc,jobid,flag
                flag =0

                em={0:"NO ERROR",1:"OUT OF DATA",2:"LINE LIMIT EXCEEDED",3:"TIME LIMIT EXCEEDED",4:"OPERATION CODE ERROR",5:"OPERAND ERROR",6:"INVALID PAGE FAULT"}
                file = open('OS\Phase1\output.txt','a')
                file.write('JOB ID: '+str(int(jobid))+'\n')

                if len(e)==1:
                    file.write(' '+em[e[0]]+'\n')
                elif len(e)==2:
                    file.write(' '+em[e[0]]+' and '+em[e[1]]+'\n')
                else:
                    file.write(' '+em[e[0]]+' and '+em[e[1]]+' and '+em[e[2]]+'\n')

                file.write('IC\t\t:\t'+str(ic)+'\n')
                file.write('IR\t\t:\t'+str(ir)+'\n')
                file.write('TTC\t\t:\t'+str(ttc)+'\n')
                file.write('LLC\t\t:\t'+str(llc)+'\n')
                file.write('\n\n')
                file.close()
                load()
            
            def gd(loc):
                '''get data function and reading data from input file'''

                data=f.readline().rstrip('\n')
                if data[0:4]=='$END':
                    terminate((1,))
                n=len(data)
                ptr=n
                i=loc
                j=0
                while (ptr):
                    rmemory[i][j]=data[n-ptr]
                    ptr-=1
                    j+=1
                    if j==4:
                        j=0
                        i+=1
                execute()

            def pd(loc):
                '''put data function and writing data in output file'''

                global tll,llc,ti
                llc+=1
                if llc>tll:
                    terminate((2,))
                data=''
                temp=((loc//10)+1)*10
                i=loc
                j=0
                while i!=temp-1 and i<300:
                    data+=rmemory[i][j]
                    j+=1
                    if j==4:
                        j=0
                        i+=1
                file = open('OS\Phase1\output.txt','a')
                file.write(data)
                file.write('\n')
                file.close()
                if ti==2:
                    return
                execute()



            global si,pi,ti,ra,ttc,ir,ic,ttl
            if ti==0:
                if si==1:
                    si=0
                    gd(ra)
                elif si==2:
                    si=0
                    pd(ra)
                elif si==3:
                    si=0
                    terminate((0,))
                    return
                elif pi==1:
                    terminate((4,))
                elif pi==2:
                    terminate((5,))
                elif pi==3:
                    pi=0
                    if ir[0:2]=='GD' or ir[0:2]=='SR':
                        temp=allocate()
                        loc=int(ir[2:4])
                        rmemory[PTR+loc//10][2]=str(temp).zfill(2)[0]
                        rmemory[PTR+loc//10][3]=str(temp).zfill(2)[1]
                        ic-=1
                        execute()
                    else:
                        terminate((6,))
            elif ti==2:
                if si==1:
                    si=0
                    ti=0
                    gd(ra)
                    terminate((3,))
                elif si==2:
                    si=0
                    pd(ra)
                    ti=0
                    terminate((3,))
                elif si==3:
                    si=0
                    terminate((0,))
                elif pi==1:
                    pi=0
                    ti=0
                    terminate((3,4))
                elif pi==2:
                    pi=0
                    ti=0
                    terminate((3,5))
                elif pi==3:
                    pi=0
                    ti=0
                    terminate((3,))

            

    def execute():
        '''executing all the instructions'''

        def address_map(va):
            '''address mapping function and mapping virtual address to real address'''

            global PTR,pte,pi,rmemory,ir
            
            if ir[0:2]=='H':
                return va
            elif va.isnumeric()==0:
                pi=2
                return -1
            else:
                va=int(va)
                if ir[0:2]=='BT':
                    return va
                elif va>=0 and va<=99:
                    pte=PTR + va//10
                    if rmemory[pte][3]=='':
                        pi=3
                        return -1
                    temp=("".join(rmemory[pte][2:4]))
                    ra=int(temp)*10 + va%10
                    return ra
                else:
                    pi=2
                    return -1
        
        def lr(loc):
            '''load register function and storing data in register'''
            global register
            register=''
            temp=((loc//10)+1)*10
            i=loc
            j=0

            while i!=temp-1 and i<300  and len(register)<4:
                register+=rmemory[i][j]
                j+=1
                if j==4:
                    j=0
                    i+=1
            
        def sr(loc):
            '''store register function and storing register data in rmemory'''
            global register
            n=len(register)
            ptr=n

            i=loc
            j=0
            while (ptr):
                rmemory[i][j]=register[n-ptr]
                ptr-=1
                j+=1
                if j==4:
                    j=0
                    i+=1

        def cr(loc):
            '''compare register function and comparing register data with memory data'''
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

            while i!=temp and loc+i<300 and temp<300 and ptr<n:
                #print(register[ptr],memory[i][j])
                if register[ptr]!=rmemory[i][j]:
                    c=0
                    return
                
                ptr+=1
                j+=1
                if j==4:
                    j=0
                    i+=1
            c=1
            return
        
        def add(loc):
            '''add function and adding memory data to register data'''

            global register
            data=''
            temp=((loc//10)+1)*10
            i=loc
            j=0

            while i!=temp-1 and i<300:
                data+=rmemory[i][j]
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
                rmemory[i][j]=temp1[n-ptr]
                ptr-=1
                j+=1
                if j==4:
                    j=0
                    i+=1
            return



        while(1):
            global ic,c,si,pi,ti,ir,ttl,tll,ttc,llc,ra
            
            
            ir=''
            ra=address_map(str(ic))
            if pi!=0:
                break
            for j in range(4):
                ir+=rmemory[ra][j]
            ic+=1
            ra=address_map(ir[2:4])
            if pi!=0:
                break

            if ir[0:2]=='LR':
                ttc+=1
                lr(ra)
            elif ir[0:2]=='SR':
                ttc+=1
                sr(ra)
            elif ir[0:2]=='CR':
                ttc+=1
                cr(ra)
            elif ir[0:2]=='BT':
                ttc+=1
                if c==1:
                    ic=ra
                    c=0
                    continue
                else:
                    pass
            elif ir[0:2]=='GD':
                si=1
                break
            elif ir[0:2]=='PD':
                si=2
                break
            elif ir[0:1]=='H':
                si=3
                break
            elif ir[0:2]=='AD':
                add(ra)
                ir=''
            else:
                pi=1
                break
        ttc+=1
        
        if ic>ttl:
            ti=2
        mos() 
  




    m=0
    global flag,ic
    while True:
        data=f.readline().rstrip('\n')
        
        if data[0:4]=='$AMJ':
            global jobid,ttl,tll,llc,ttc,pcb,check,rmemory,vmemory
            flag=1
            jobid,ttl,tll,llc,ttc='','','',0,0
            pcb={"jobid":jobid,"ttl":ttl, "tll":tll, "llc":llc, "ttc":ttc}

            rmemory=[]
            vmemory=[]
            check=[]
            for i in range(300):
                rmemory.append(['']*4)
            for i in range(100):
                vmemory.append(['']*4)
            for i in range(30):
                check.append(0)
            
            global ir,register,c,si,pi,ti,PTR
            ir=''
            ic=0
            register=''
            c=0
            si,pi,ti=0,0,0
            PTR=allocate()*10
            print("PTR:",PTR)

            jobid=data[4:8]
            ttl=int(data[8:12])
            tll=int(data[12:16])
            print()
            print(jobid,ttl,tll)
        
        elif data[0:4]=='$END':
            print("JOB DONE")
            display(rmemory)
            load()

        elif data=='':
            exit(1)

        elif flag==0:
            continue
        elif data[0:4]=='$DTA':
            ic=0
            execute()
        
        elif data!='':
            loc=0
            temp=allocate()
            print("Instruction block:",temp)
            rmemory[PTR+m//10][2]=str(temp).zfill(2)[0]
            rmemory[PTR+m//10][3]=str(temp).zfill(2)[1]
            temp*=10
            for i in range(temp,temp+(len(data)+3)//4):
                for j in range(4):
                    if data[loc]=="H":
                        rmemory[i][j]=data[loc]
                        break
                    else:
                        rmemory[i][j]=data[loc]
                    loc+=1
            m+=10
        
        


global flag
flag=0
f= open('OS\Phase1\input.txt','r')
file=open('OS\Phase1\output.txt','w')
file.close()
load()


""" 

LR 25

pte=30+2=32

pte=PTR+VM//10
RM=M[pte]*10 + VM%10 = M[32]+25%10=

 """

""" 

EXTERNAL MAIN MEMORY:
0       GD20
1       PD20
2       H
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20      Hell
21      o
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99

 """
""" 

load:
    allocate:

    execute:
        address map:

        instructions functions: except gd, pd, h

        main:
            calls instruction function
            calls mos()

        
    mos:
        h=terminate:
        gd:
        pd:
        main:
            interrupts handle

            
    main:
        data card, program card, control card
        $amj
        instruction store
        $dta: 
            calls execute
        $end
        if nothing
 """