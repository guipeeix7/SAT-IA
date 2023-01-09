# Following the steps of: 
# PBFVMC: A New Pseudo-Boolean Formulation to Virtual-Machine Consolidation
# https://www.brunoribas.com.br/publicacoes/files/bracis-2013-pbfvmc.pdf

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

    def __construct():
        return

    def input(self):
        '''
            Receives user or txt input and set:
            dictHW, dictVM, totalRamVM, totalCpuVM variables values
        '''
        n = int(input())
        for i in range(n):
            nomeH, ramH, cpuH = input().split()
            self.dictHW[nomeH] = [ramH, cpuH]

            self.totalRamHW += int(ramH)
            self.totalCpuHW += int(cpuH)

        m = int(input())
        for j in range(m):
            nomeV, ramV, cpuV = input().split()
            self.dictVM[nomeV] = [ramV, cpuV]

            #Pre calculate the total ammount of ram and Cpu used by VMs    
            self.totalRamVM += int(ramV)
            self.totalCpuVM += int(cpuV)


        return self.dictHW, self.dictVM

    def minimizes_rule(self):
        variable = 1
        print("min:",end="")
        for key, item in self.dictHW.items():
            print(f" +1 x{str(variable)}", end = "")
            variable += 1
        print(";", end="")

    def summation_of_hardware_cpu_ram_ammount(self):
        '''
            This fuction runs steps 8 and 9 of thesis and generate rule to check if\
                ammount of ram and cpu in virtual machines are lower than hardware max availale.  
        '''
        
        #loop to ammount of RAM
        #Step 8
        variable = 1
        for key, item in self.dictHW.items():
            print(f"+{item[0]} x{str(variable)}", end = " ")
            variable += 1
        print(f">= {str(self.totalRamVM)};")
        
        #loop to ammount of CPU
        #Step 9
        variable = 1
        for key, item in self.dictHW.items():
            print(f"+{item[1]} x{str(variable)}", end = " ")
            variable += 1
        print(f">= {str(self.totalCpuVM)};")


    def limit_hardware_provided_to_virtualmachines(self):
        #The following line is a 'gabiarra'
        #this is my try to create new variable to each VM in each Hw
        Ki = int(len(self.dictHW))+1
        
        Ni = 1
        for keyh, itemh in self.dictHW.items():
            for key, item in self.dictVM.items():
                print(f"+{item[0]} ~x{str(Ki)}", end = " ")
                Ki+=1
                # item[0]
            print(f"+{itemh[0]} x{Ni}", end ="")
            Ni+=1
            print(f" >= {self.totalRamVM};")
        
        Ni = 1
        Ki = int(len(self.dictHW))+1

        for keyh, itemh in self.dictHW.items():
            for key, item in self.dictVM.items():
                print(f"+{item[1]} ~x{str(Ki)}", end = " ")
                Ki+=1
                # item[0]
            print(f"+{itemh[1]} x{Ni}", end ="")
            Ni+=1
            print(f" >= {self.totalCpuVM};")
    
    def virtual_machines_in_hardwares(self):
        totalHardwares = int(len(self.dictHW))
        totalVms = int(len(self.dictVM))
        kj = 0
        steps = 0
        
        j=1
        for keyVM, itemVM in self.dictVM.items():
            kj=0
            for keyHW, itemHW in self.dictHW.items():
                print(f"+{1} x{str(kj+j+totalHardwares)}", end = " ")
                kj+=totalVms            
            print(r">= 1;")

            kj=0
            for keyHW, itemHW in self.dictHW.items():
                print(f"+{1} ~x{str(kj+j+totalHardwares)}", end = " ")
                kj+=totalVms         
            j+=1

            print(f">= { totalHardwares-1 };")


sat = Sat()
dictHW, dictVM = sat.input()
# print(dictHW, dictVM)
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

print(f"* #variable= {variables} #constraint= {constraint}")
# print()
sat.minimizes_rule()
# print()
sat.summation_of_hardware_cpu_ram_ammount()
# print()
sat.limit_hardware_provided_to_virtualmachines()
# print()
sat.virtual_machines_in_hardwares()
# print()
#print(dictHW, dictVM)
print(f"* #variable= {variables} #constraint= {constraint}")
