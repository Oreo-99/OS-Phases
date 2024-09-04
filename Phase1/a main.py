def display(memory):
    '''displaying memory card'''

    print("\nEXTERNAL MAIN MEMORY: ")
    for i in range(100):
        print(i,end='\t')
        for j in range(4):
            print(memory[i][j],end='')
        print()
    print()




def load():
    '''loading the instructions in memory'''

    def mos():
            '''machine operation system'''

            def gd(loc):
                '''get data function and reading data from input file'''
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
                execute()

            def pd(loc):
                '''put data function and writing data in output file'''
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
                execute()

            def terminate():
                '''terminating the program'''
                file = open('OS\Phase1\output.txt','a')
                file.write('\n\n')
                file.close()
                load()
            

    
            global si,inst
            if si==1:
                gd(int(inst[2:4]))
                si=0
            elif si==2:
                pd(int(inst[2:4]))
                si=0
            elif si==3:
                terminate()
                si=0
                return
            
    def execute():
        '''executing all the instructions'''

        def lr(loc):
            '''load register function and storing data in register'''
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
            
        def sr(loc):
            '''store register function and storing register data in memory'''
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

            while i!=temp and loc+i<100 and temp<100 and ptr<n:
                #print(register[ptr],memory[i][j])
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
        
        def add(loc):
            '''add function and adding memory data to register data'''

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
            return



        while(1):
            global ic,c,si,inst
            inst=''
            for j in range(4):
                inst+=memory[ic][j]
            ic+=1

            if inst[0:2]=='LR':
                lr(int(inst[2:4]))
            elif inst[0:2]=='SR':
                sr(int(inst[2:4]))
            elif inst[0:2]=='CR':
                cr(int(inst[2:4]))
            elif inst[0:2]=='BT':
                if c==1:
                    ic=int(inst[2:4])
                    c=0
                    continue
                else:
                    pass
            elif inst[0:2]=='GD':
                si=1
                mos()
            elif inst[0:2]=='PD':
                si=2
                mos()
            elif inst[0:1]=='H':
                si=3
                mos()
            elif inst[0:2]=='AD':
                add(int(inst[2:4]))
                inst='' 
  




    m=0

    while True:
        data=f.readline().rstrip('\n')
        
        if data[0:4]=='$AMJ':
            global memory
            memory=[]
            for i in range(100):
                memory.append(['']*4)
            
            global inst,ic,register,c,si
            inst=''
            ic=0
            register=''
            c=0
            si=0

            jobno=data[4:8]
            instno=data[8:12]
            linelim=data[12:16]
            print()
            print(jobno,instno,linelim)
        
        elif data[0:4]=='$DTA':
            ic=0
            execute()
        
        elif data[0:4]=='$END':
            print("JOB DONE")
            display(memory)
            load()
        
        elif data!='':
            loc=0
            for i in range(m,m+(len(data)+3)//4):
                for j in range(4):
                    if data[loc]=="H":
                        memory[i][j]=data[loc]
                        break
                    else:
                        memory[i][j]=data[loc]
                    loc+=1
                    
            m+=10
        else:
            exit(1)


f= open(r'OS\Phase1\input1.txt','r')
file=open('OS\Phase1\output.txt','w')
file.close()
load()

