# Following the steps of: 
# PBFVMC: A New Pseudo-Boolean Formulation to Virtual-Machine Consolidation
# https://www.brunoribas.com.br/publicacoes/files/bracis-2013-pbfvmc.pdf

from sys import stdin
import os
import numpy as np
import pathlib


pathlib.Path('./outputs').mkdir(parents=True, exist_ok=True) 
f = open("./outputs/out.desc", "w+")

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

    def claspHandler(self):
        linearArray = []

        with open('./outputs/outClasp.txt') as f:
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
        matrix = linearArray[self.n :].reshape(self.n,self.m)
        
        
        print("VM" , end="    ")
        for i in range(0, (self.m)):
            print(f"{i+1}", end=" ")
        print()
        
        for i in range(0, (self.n)):
            print(f"HW({i+1})", end = " ")
            for j in range(0, self.m):
                if("-" in matrix[i, j]):
                    print(0, end=" ")
                else:
                    print(1, end = " ")
                # print(f"HW {i+1} {matrix[i, j]}")
            print()


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
    
    
    
    
    def minimizes_rule(self):
        variable = 1
        f.write("min:")
        for key, item in self.dictHW.items():
            f.write(f" +1 x{str(variable)}")
            variable += 1
        f.write(";")

    def summation_of_hardware_cpu_ram_ammount(self):
        '''
            This fuction runs steps 8 and 9 of thesis and generate rule to check if\
                ammount of ram and cpu in virtual machines are lower than hardware max availale.  
        '''
        
        #loop to ammount of RAM
        #Step 8
        variable = 1
        for key, item in self.dictHW.items():
            f.write(f"+{item[0]} x{str(variable)} ")
            variable += 1
        f.write(f">= {str(self.totalRamVM)};")
        
        #loop to ammount of CPU
        #Step 9
        variable = 1
        for key, item in self.dictHW.items():
            f.write(f"+{item[1]} x{str(variable)} ")
            variable += 1
        f.write(f">= {str(self.totalCpuVM)};")


    def limit_hardware_provided_to_virtualmachines(self):
        #The following line is a 'gabiarra'
        #this is my try to create new variable to each VM in each Hw
        Ki = int(len(self.dictHW))+1
        
        Ni = 1
        for keyh, itemh in self.dictHW.items():
            for key, item in self.dictVM.items():
                f.write(f"+{item[0]} ~x{str(Ki)} ")
                Ki+=1
                # item[0]
            f.write(f"+{itemh[0]} x{Ni}")
            Ni+=1
            f.write(f" >= {self.totalRamVM};")
        
        Ni = 1
        Ki = int(len(self.dictHW))+1

        for keyh, itemh in self.dictHW.items():
            for key, item in self.dictVM.items():
                f.write(f"+{item[1]} ~x{str(Ki)} ")
                Ki+=1
                # item[0]
            f.write(f"+{itemh[1]} x{Ni}")
            Ni+=1
            f.write(f" >= {self.totalCpuVM};")
    
    def virtual_machines_in_hardwares(self):
        totalHardwares = int(len(self.dictHW))
        totalVms = int(len(self.dictVM))
        kj = 0
        steps = 0
        
        j=1
        for keyVM, itemVM in self.dictVM.items():
            kj=0
            for keyHW, itemHW in self.dictHW.items():
                f.write(f"+{1} x{str(kj+j+totalHardwares)} ")
                kj+=totalVms            
            f.write(r">= 1;")

            kj=0
            for keyHW, itemHW in self.dictHW.items():
                f.write(f"+{1} ~x{str(kj+j+totalHardwares)} ")
                kj+=totalVms         
            j+=1

            f.write(f">= { totalHardwares-1 };")



sat = Sat()
dictHW, dictVM = sat.input()
#Total number of Hardwares * Virtual Machines + Number of hardwares
# In another word is the number of variables used in Virtual machines +\
# The possibility that each virtual machine cold be allocated in each hardware
totalHW = int(len(dictHW))
totalVM = int(len(dictVM))

variables = (totalHW * totalVM) + totalHW

#one constrain generated in step 7 
#2 constrain generated in step 8 and 9 
#2*(number of hardware) constrain generated in step 10 and 11 
#2*(number of VM's) constrains generated in step 12 and 13 
constraint= (2 + 2*totalHW + 2*totalVM)

f.write(f"* #variable= {variables} #constraint= {constraint}")

sat.minimizes_rule()
sat.summation_of_hardware_cpu_ram_ammount()
sat.limit_hardware_provided_to_virtualmachines()
sat.virtual_machines_in_hardwares()

f.write(f"* #variable= {variables} #constraint= {constraint}")


f.close()
os.system('clasp ./outputs/out.desc > ./outputs/outClasp.txt')

sat.claspHandler()


if os.path.exists("./outputs/out.desc"):
  os.remove("./outputs/out.desc")
else:
  print("The file does not exist")
  
if os.path.exists("./outputs/outClasp.txt"):
  os.remove("./outputs/outClasp.txt")
else:
  print("The file does not exist")
