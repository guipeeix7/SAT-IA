# Following the steps of: 
# PBFVMC: A New Pseudo-Boolean Formulation to Virtual-Machine Consolidation
# https://www.brunoribas.com.br/publicacoes/files/bracis-2013-pbfvmc.pdf

from sys import stdin
from sys import argv
import os
import numpy as np
import pathlib
import signal
from time import sleep

# exit()
# os.path.basename('/root/file.ext')
filePath = os.path.basename(argv[1])

pathlib.Path('./outputs').mkdir(parents=True, exist_ok=True) 
f = open("./outputs/"+str(filePath), "w+")

class Sat:
    '''  
        dictHW {} : Dictionary containing hardware cpu and ram  
        dictVM {} : Dictionary containing virtual Machines cpu and ram 
        totalRamVM int : Totaa ram used by Virtual Machines 
        totalCpuVM int : Total Cpu used by Virtual Machines
    '''
    dictHW = {}
    dictVM = {}
    totalRamVM = 0
    totalCpuVM = 0

    totalRamHW = 0
    totalCpuHW = 0
    variables = 0
    n = 0 
    m = 0

    def __construct():
        return

    def input(self):
        '''
            Receives user or txt input and set:
            dictHW, dictVM, totalRamVM, totalCpuVM variables values
        '''
        n = int(input())
        self.n = n
        for i in range(n):
            nomeH, ramH, cpuH = input().split()
            self.dictHW[nomeH] = [ramH, cpuH]

            self.totalRamHW += int(ramH)
            self.totalCpuHW += int(cpuH)

        m = int(input())
        self.m = m
        for j in range(m):
            nomeV, ramV, cpuV = input().split()
            self.dictVM[nomeV] = [ramV, cpuV]

            #Pre calculate the total ammount of ram and Cpu used by VMs    
            self.totalRamVM += int(ramV)
            self.totalCpuVM += int(cpuV)

        return self.dictHW, self.dictVM  
    def inputFromParameter(self):
        '''
            Receives user or txt input and set:
            dictHW, dictVM, totalRamVM, totalCpuVM variables values
        '''
        f = open(str(argv[1]), "r")

        lines = f.readlines()
        # for line in lines:
        #     print(line)
        
        self.n = int(lines[0])
        i = 1 
        for i in range(1, self.n+1):
            nomeH, ramH, cpuH = lines[i].split()
            self.dictHW[nomeH] = [ramH, cpuH]

            self.totalRamHW += int(ramH)
            self.totalCpuHW += int(cpuH)
        
        
        self.m = int(lines[i+1])
        
        for j in range(i+2, self.m+self.n+2):
            nomeV, ramV, cpuV = lines[j].split()
            self.dictVM[nomeV] = [ramV, cpuV]

            #Pre calculate the total ammount of ram and Cpu used by VMs    
            self.totalRamVM += int(ramV)
            self.totalCpuVM += int(cpuV)
        return self.dictHW, self.dictVM  
        # print(i+2)
        # exit()

    def minimizes_rule(self):
        '''
            Minimize the ammount of hardware according to formula 7
        '''
        variable = 1
        f.write("min:")
        for key, item in self.dictHW.items():
            f.write(f" +{str(1)} x{str(variable)}")
            variable += 1
        f.write(" ;\n")

    def minimize_ram(self):
        '''
            Minimize the ammount of RAM based on formula 7
        '''
        variable = 1
        f.write("min:")
        for key, item in self.dictHW.items():
            f.write(f" +{str(item[0])} x{str(variable)}")
            variable += 1
        f.write(";\n")

    def minimize_cpu(self):
        '''
            Minimize the ammount of CPU based on formula 7
        '''
        variable = 1
        f.write("min:")
        for key, item in self.dictHW.items():
            f.write(f" +{str(item[1])} x{str(variable)}")
            variable += 1
        f.write(";\n")


    def summation_of_hardware_cpu_ram_ammount(self):
        '''
            This fuction runs steps 8 and 9 of scientific
            article and generate rule to check if
            ammount of ram and cpu in virtual machines 
            are lower than hardware max availale.  
        '''
        #loop to ammount of RAM
        #Step 8
        variable = 1
        for key, item in self.dictHW.items():
            f.write(f"+{item[0]} x{str(variable)} ")
            variable += 1
        f.write(f">= {str(self.totalRamVM)};\n")
        
        #loop to ammount of CPU
        #Step 9
        variable = 1
        for key, item in self.dictHW.items():
            f.write(f"+{item[1]} x{str(variable)} ")
            variable += 1
        f.write(f">= {str(self.totalCpuVM)};\n")


    def limit_hardware_provided_to_virtualmachines(self):
        '''
            Creating the variable that represents each VM running into HW
        '''
        #step 10
        Ki = int(len(self.dictHW))+1
        Ni = 1
        for keyh, itemh in self.dictHW.items():
            for key, item in self.dictVM.items():
                f.write(f"+{item[0]} ~x{str(Ki)} ")
                Ki+=1
            f.write(f"+{itemh[0]} x{Ni}")
            Ni+=1
            f.write(f" >= {self.totalRamVM};\n")
        
        #Step 11
        Ni = 1
        Ki = int(len(self.dictHW))+1
        for keyh, itemh in self.dictHW.items():
            for key, item in self.dictVM.items():
                f.write(f"+{item[1]} ~x{str(Ki)} ")
                Ki+=1
            f.write(f"+{itemh[1]} x{Ni}")
            Ni+=1
            f.write(f" >= {self.totalCpuVM};\n")
    
    def virtual_machines_in_hardwares(self):
        #Represent Steps 12 and 13
        totalHardwares = int(len(self.dictHW))
        totalVms = int(len(self.dictVM))
        kj = 0
        steps = 0
        
        j=1
        for keyVM, itemVM in self.dictVM.items():
            #Step 12
            kj=0
            for keyHW, itemHW in self.dictHW.items():
                f.write(f"+{1} x{str(kj+j+totalHardwares)} ")
                kj+=totalVms            
            f.write(f">= 1;\n")

            #Step 13 
            kj=0
            for keyHW, itemHW in self.dictHW.items():
                f.write(f"+{1} ~x{str(kj+j+totalHardwares)} ")
                kj+=totalVms         
            j+=1

            f.write(f">= { totalHardwares-1 };\n")

    def claspHandler(self):
        linearArray = []

        with open('./outputs/'+os.path.splitext(str(filePath))[0]+'.clasp') as f:
            lines = f.readlines()
            for line in lines:
                if(line[0] == 'v'):
                    tempLine = line[1:]
                    tempLineArr = tempLine.split()
                    linearArray = np.concatenate((linearArray, tempLineArr), axis=None)
        
        self.getMachines(linearArray)
        self.getVirtuals(linearArray)

        return linearArray     
                    
    def getVirtuals(self, linearArray):
        f = open('./outputs/'+os.path.splitext(str(filePath))[0]+'.readable', "w+")


        matrix = linearArray[self.n :].reshape(self.n,self.m)
        
        f.write(f"VM    ")

        for i in range(0, (self.m)):
            f.write(f"{i+1} ")
        f.write('\n')
        
        for i in range(0, (self.n)):
            f.write(f"HW({i+1}) ")
            for j in range(0, self.m):
                if("-" in matrix[i, j]):
                    f.write(str(0)+' ')
                else:
                    f.write(str(1)+' ')
                # print(f"HW {i+1} {matrix[i, j]}")
            f.write("\n")


    def getMachines(self, tempLineArr):
        HwMachines = []
        i = 0 

        for i in range(1, self.n):
            if('-' not in tempLineArr[i]):
                HwMachines.append(1)
            else:
                HwMachines.append(0)
        # print(HwMachines)
        return (i)

    def writeResults(self):

        os.system('clasp ./outputs/'+str(filePath)+' > ./outputs/'+os.path.splitext(str(filePath))[0]+'.clasp') 

sat = Sat()
dictHW, dictVM = sat.inputFromParameter()

# print(sat.inputFromParameter())
# exit()
#Total number of Hardwares * Virtual Machines + Number of hardwares
# In another word is the number of variables used in Virtual machines +\
# The possibility that each virtual machine cold be allocated in each hardware
totalHW = int(len(dictHW))
totalVM = int(len(dictVM))
print(totalHW, totalVM)
variables = (totalHW * totalVM) + totalHW
#one constrain generated in step 7 
#2 constrain generated in step 8 and 9 
#2*(number of hardware) constrain generated in step 10 and 11 
#2*(number of VM's) constrains generated in step 12 and 13 
constraint= (2 + 2*totalHW + 2*totalVM)

f.write(f"* #variable= {variables} #constraint= {constraint}\n")
# minimize_ram
# minimize_cpu

sat.minimizes_rule()
sat.summation_of_hardware_cpu_ram_ammount()
sat.limit_hardware_provided_to_virtualmachines()
sat.virtual_machines_in_hardwares()

f.write(f"* #variable= {variables} #constraint= {constraint}\n")

# exit()
f.close()
# sleep(2)
sat.writeResults()
# exit()
# exit()
# signal.signal(signal.SIGALRM, sat.writeResults()) 
# signal.alarm(10) 

sat.claspHandler()
#Ele deve abrir um arquivo por parametro e gerar um output no nome do arquivo de entrada
# (: 
# Coisa boa



# if os.path.exists("./outputs/out.desc"):
#   os.remove("./outputs/out.desc")
# else:
#   print("The file does not exist")
  
# if os.path.exists("./outputs/outClasp.txt"):
#   os.remove("./outputs/outClasp.txt")
# else:
#   print("The file does not exist")
