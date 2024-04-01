import sys
import contextlib
f=open("output_file.txt","w")
with contextlib.redirect_stdout(f):
    command_dictionary= {
        "00000":["A","add"], 
        "00001":["A","sub"],
        "00010":["B","mov_immediate"],
        "00011":["C","mov_register"],
        "00100":["D","load"],
        "00101":["D", "store"],
        "00110":["A","multiply"],
        "00111":["C","divide"],
        "01000":["B","right_shift"],
        "01001":["B","left_shift"],
        "01010":["A","xor"],
        "01011":["A","or"],
        "01100":["A","and"],
        "01101":["C","inverse"],
        "01110":["C","cmp"],
        "01111":["E","unconditional_jump"],
        "11100":["E","jump_if_less_than"],
        "11101":["E","jump_if_greater_than"],
        "11111":["E","jump_if_equal"],
        "11010":["F","halt"],

        "10000":["A","addf"],#
        "10001":["A","subf"],#
        "10010":["B","movf"],#

        "10011":["A","expo"],#
        "10100":["B","addi"],#
        "10101":["B","subi"],#
        "10110":["B","muli"],#
        "10111":["B","divi"],#
        
    }


    register_dictionary={"000":0,"001":1,"010":2,"011":3,
    "100":4,"101":5, "110":6,"111":7}




    def int_to_binary_reg(num):
        binary_string = bin(num)[2:]  # Convert num to binary and remove the '0b' prefix
        binary_string = binary_string.zfill(3)  # Pad the string with leading zeros if necessary
        return binary_string

    def int_to_binary(num):
        binary_string = bin(num)[2:]  # Convert num to binary and remove the '0b' prefix
        binary_string = binary_string.zfill(16)  # Pad the string with leading zeros if necessary
        return binary_string


    def binary_to_int(binary_str):
        return int(binary_str, 2)

    def int_to_binary_pc(num):

        binary_string = bin(num)[2:]  # Convert num to binary and remove the '0b' prefix
        binary_string = binary_string.zfill(7)  # Pad the string with leading zeros if necessary
        return binary_string


    def right_shift_integer(num, shift):#num is int 
        
        shifted_num=num>>shift
        
        return shifted_num


    def left_shift_integer(num, shift):
        shifted_num=num<<shift
        
        return shifted_num
    
    def binary_to_float(binary):
        expo=binary[0:3]
        mantissa=binary[3:]
        significand=1+float(mantissa[0])*0.5+float(mantissa[1])*0.25+float(mantissa[2])*0.125+float(mantissa[3])*0.0625+float(mantissa[4])*0.03125
        exponent=binary_to_int(expo)
        result=float(significand*(2**exponent))
        return result
    
    def float_to_binary(value):
    

        # Check if the value is zero
        if value == 0.0:
            return '0' * 8

        # Calculate the exponent and adjust the value accordingly
        exponent = 0
        while value < 1.0:
            value *= 2
            exponent -= 1
        while value >= 2.0:
            value /= 2
            exponent += 1

        # Convert the fraction part to binary
        fraction = ""
        for _ in range(5):
            value *= 2
            if value >= 1.0:
                fraction += '1'
                value -= 1
            else:
                fraction += '0'

        # Convert the exponent to binary
        exponent_bits = bin(exponent & 0x07)[2:].zfill(3)

        # Combine the sign, exponent, and mantissa bits
        binary_representation =  exponent_bits + fraction

        # Pad with zeros to make it 8 bits
        binary_representation = binary_representation.ljust(8, '0')

        return binary_representation



    class Memory:
        def __init__(self):
            self.memory = ["0000000000000000"]*128

        def read(self, address): # we will use it to read th memory with address and address will be a integer 
            #we will convert address into binary at time of printing
            
            return self.memory[(address)]

        def write(self, address, data):# we will use it to first initialize the memory
            
            self.memory[int(address)] = data





    class RegisterFile:
        def __init__(self):
            self.registers = [0] * 7  # R0, R1, ..., R6
            self.flags = [0,0,0,0]# in order V(overflow)  Less Great Equal

        def read(self, register):# register is code of register so it goes to that index and reads the values out
            if register == "111":
                return str(self.flags[0])+str(self.flags[1])+str(self.flags[2])+str(self.flags[3])

            else:
                register_num = self.registers[register_dictionary[register]]  # Extract the register number from the register name
                return register_num

        def write(self, register, data):# register is code of register
            if register == "111":
                self.flags = data
            else:
                self.registers[register_dictionary[register]] = data





    class ExecutionEngine:
        def __init__(self, memory, register_file): #takes input as memory and register file
            self.memory = memory
            self.register_file = register_file

            


        #pc will start from 0000000

        def execute(self, instruction, PC):# instruction is 16 length string  
            instruction=instruction.strip()
            opcode = instruction[0:5]  # Extract the opcode from the instruction
            #operand1 = (instruction >> 10) & 0b111  # Extract the first operand from the instruction
            #operand2 = (instruction >> 7) & 0b111  # Extract the second operand from the instruction
            #imm_value = instruction & 0b1111111  # Extract the immediate value from the instruction
            sys.stdout.write(int_to_binary_pc(PC))
            #print(int_to_binary_pc(PC))
            

            new_PC = None
            halted = False
            
            output_reg0=""
        
            output_reg1=""
        
            output_reg2=""
        
            output_reg3=""
            output_reg4=""
        
            output_reg5=""
        
            output_reg6=""

            if command_dictionary[str(opcode)][0]=="A":
                
                reg1=instruction[7:10]
                reg2=instruction[10:13]
                reg3=instruction[13:]
                
                if command_dictionary[str(opcode)][1]=="add":
                    sum=self.register_file.read(reg2)+self.register_file.read(reg3)
                    if 0<=sum and sum<128:


                        self.register_file.write((reg1),self.register_file.read(reg2)+self.register_file.read(reg3))
                    else:
                        self.register_file.write(reg1,0)
                        self.register_file.flags[0]=1#overflow activated

                elif command_dictionary[str(opcode)][1]=="sub":
                    result=self.register_file.read(reg2)-self.register_file.read(reg3)
                    if result<0 :
                        self.register_file.flags[0]=1#overflow activated
                        self.register_file.write(reg1,0)
                    else:

                        self.register_file.write((reg1),result)

                elif command_dictionary[str(opcode)][1]=="multiply":
                    result=self.register_file.read(reg2)*self.register_file.read(reg3)
                    if result<0 or result>=128:
                        self.register_file.flags[0]=1#overflow activated
                        self.register_file.write(reg1,0)

                    else:
                        self.register_file.write(reg1,result)
                
                elif command_dictionary[str(opcode)][1]=="xor":

                    self.register_file.write((reg1),self.register_file.read(reg2 ) ^ self.register_file.read(reg3))
                elif command_dictionary[str(opcode)][1]=="or":
                    self.register_file.write((reg1),self.register_file.read(reg2) |self.register_file.read(reg3))
                elif command_dictionary[str(opcode)][1]=="and":
                    self.register_file.write((reg1),self.register_file.read(reg2) & self.register_file.read(reg3))
                
                
                
                #new_opcode_________________________________________________________________________
                elif command_dictionary[str(opcode)][1]=="expo":
                    result=self.register_file.read(reg2)**self.register_file.read(reg3)
                    if result>128:
                        self.register_file.flags[0]=1
                        self.register_file.write(reg1,0)
                    else:
                    
                        self.register_file.write((reg1),self.register_file.read(reg2)**self.register_file.read(reg3))
                
                
                
                elif command_dictionary[str(opcode)][1]=="addf":
                    sum=(self.register_file.read(reg2))+(self.register_file.read(reg3))
                    if 0<=sum and sum<128:


                        self.register_file.write((reg1),self.register_file.read(reg2)+self.register_file.read(reg3))
                    else:
                        self.register_file.write(reg1,0)
                        self.register_file.flags[0]=1#overflow activated


                elif command_dictionary[str(opcode)][1]=="subf":
                    result=float(self.register_file.read(reg2))-float(self.register_file.read(reg3))
                    if result<0 :
                        self.register_file.flags[0]=1#overflow activated
                        self.register_file.write(reg1,0)
                    else:

                        self.register_file.write((reg1),result)

                
                new_PC=PC+1
            elif command_dictionary[str(opcode)][0]=="B":

                
                reg1=instruction[6:9]
                immediate=instruction[9:]
                if command_dictionary[str(opcode)][1]=="mov_immediate":
                    self.register_file.write(reg1,binary_to_int(immediate))
                elif command_dictionary[str(opcode)][1]=="right_shift":
                    self.register_file.write(reg1,(right_shift_integer(self.register_file.read(reg1),binary_to_int(immediate))))
                elif command_dictionary[str(opcode)][1]=="left_shift":
                    self.register_file.write(reg1,(left_shift_integer(self.register_file.read(reg1),binary_to_int(immediate))))
                
                
                
                #new opcodes_________________________________________________________
                elif command_dictionary[str(opcode)][1]=="addi":

                    sum=self.register_file.read(reg1)+binary_to_int(immediate)
                    if sum>=128:
                        self.register_file.write(reg1,0)
                        self.register_file.flags[0]=1
                    else:
                        self.register_file.write(reg1,sum)
                elif  command_dictionary[str(opcode)][1]=="subi":
                    sum=self.register_file.read(reg1)-binary_to_int(immediate)
                    if sum<0:
                        self.register_file.write(reg1,0)
                        self.register_file.flags[0]=1
                    else:
                        self.register_file.write(reg1,sum)
                elif  command_dictionary[str(opcode)][1]=="muli":
                    sum=self.register_file.read(reg1)*binary_to_int(immediate)
                    if sum>=128:
                        self.register_file.write(reg1,0)
                        self.register_file.flags[0]=1
                    else:
                        self.register_file.write(reg1,sum)
                elif  command_dictionary[str(opcode)][1]=="divi":
                    quotient=self.register_file.read(reg1)/binary_to_int(immediate)
                    remainder=self.register_file.read(reg1)%binary_to_int(immediate)
                    if binary_to_int(immediate)== 0:
                        self.register_file.write("000",0)
                        self.register_file.write("001",0)
                        self.register_file.flags[0]=1

                    else:
                        self.register_file.write("000",quotient)
                        self.register_file.write("001",remainder)
                elif command_dictionary[str(opcode)][1]=="movf":
                    reg1=instruction[5:8]
                    immediate=instruction[8:]
                    float_value=binary_to_float(immediate)
                    self.register_file.write(reg1,float_value)





                new_PC=PC+1

            
            
            
            
            
            
            
            
            
            elif command_dictionary[str(opcode)][0]=="C":


                reg1=instruction[10:13]
                reg2= instruction[13:]

                if command_dictionary[str(opcode)][1]=="mov_register":
                    if reg2=="111":#_________________________
                        #text=self.register_file.read(reg2)
                        #binary = format(int(text, 2), '016b')
                        #self.register_file.write(reg1,)
                        self.register_file.write(reg1,binary_to_int( self.register_file.read(reg2)))
                
                elif command_dictionary[str(opcode)][1]=="divide":
                    if self.register_file.read(reg2)==0:
                        self.register_file.flags[0]=1#overflow activated
                        self.register_file.write("000",0)#R0 and R1 set to 0
                        self.register_file.write("001",0)
                    else:
                        
                        quotient= (self.register_file.read(reg1))/self.register_file.read(reg2)
                        remainder=(self.register_file.read(reg1))%self.register_file.read(reg2)
                        self.register_file.write("000",quotient)
                        self.register_file.write("001",remainder)
                
                elif command_dictionary[str(opcode)][1]=="inverse":
                    self.register_file.write(reg1,~(self.register_file.read(reg2)))#not -> ~
                
                elif command_dictionary[str(opcode)][1]=="cmp":
                    r1=self.register_file.read(reg1)
                    r2=self.register_file.read(reg2)
                    if r1>r2:
                        self.register_file.flags[2]=1#VLGE flag
                    elif r1<r2:
                        self.register_file.flags[1]=1
                    else:
                        self.register_file.flags[3]=1
                new_PC=PC+1
                

            elif command_dictionary[str(opcode)][0]=="D":#________________
                reg1= instruction[6:9]
                address= instruction[9:]
                if command_dictionary[(opcode)][1]=="load":
                    self.register_file.write(reg1,binary_to_int( self.memory.read(binary_to_int( address))))
                elif command_dictionary[(opcode)][1]=="store":
                    self.memory.write(binary_to_int(address),int_to_binary( self.register_file.read(reg1)))
                new_PC=PC+1




            elif command_dictionary[str(opcode)][0]=="E":

                address=instruction[9:]

                if command_dictionary[str(opcode)][1]=="unconditional_jump":
                    new_PC=binary_to_int(address)
                


                elif command_dictionary[str(opcode)][1]=="jump_if_less_than":
                    if self.register_file.flags[1]==1:
                        new_PC=binary_to_int(address)
                        #sys.stdout.write(str(new_PC))
                        self.register_file.flags=[0,0,0,0]
                
                elif command_dictionary[str(opcode)][1]=="jump_if_greater_than":
                    if self.register_file.flags[2]==1:
                        new_PC=binary_to_int(address)
                        self.register_file.flags=[0,0,0,0]
                        #sys.stdout.write(str(new_PC))


                elif command_dictionary[str(opcode)][1]=="jump_if_equal":
                    if self.register_file.flags[3]==1:
                        new_PC=binary_to_int(address)
                        self.register_file.flags=[0,0,0,0]
                       #sys.stdout.write(str(new_PC))

                else:
                    new_PC=PC+1



            elif command_dictionary[str(opcode)][0]=="F":
                halted=True
                

            float_list=[]
            for i in range(7):
                if type(self.register_file.read(int_to_binary_reg(int((f"00{i}")))))==float:
                    file=int_to_binary_reg(int((f"00{i}")))
                    if i==0:
                        output_reg0=float_to_binary(self.register_file.read(file))
                    if i==1:
                        output_reg0=float_to_binary(self.register_file.read(file))
                    if i==2:
                        output_reg0=float_to_binary(self.register_file.read(file))
                    if i==3:
                        output_reg0=float_to_binary(self.register_file.read(file))
                    if i==4:
                        output_reg0=float_to_binary(self.register_file.read(file))
                    if i==5:
                        output_reg0=float_to_binary(self.register_file.read(file))
                    if i==6:
                        output_reg0=float_to_binary(self.register_file.read(file))
                else:
                    if i==0:
                        output_reg0=bin(self.register_file.read("000"))[2:].zfill(16)
                    if i==1:
                        output_reg1=bin(self.register_file.read("001"))[2:].zfill(16)
                    if i==2:
                        output_reg2=bin(self.register_file.read("010"))[2:].zfill(16)
                    if i==3:
                        output_reg3=bin(self.register_file.read("011"))[2:].zfill(16)
                    if i==4:
                        output_reg4=bin(self.register_file.read("100"))[2:].zfill(16)
                    if i==5:
                        output_reg5=bin(self.register_file.read("101"))[2:].zfill(16)
                    if i==6:
                        output_reg6=bin(self.register_file.read("110"))[2:].zfill(16)

            

                    
                


                #dump memory
            #sys.stdout.write("        "+str(int_to_binary(self.register_file.read("000")))+" "+str(int_to_binary(self.register_file.read("001")))+" "+str(int_to_binary(self.register_file.read("010")))+" "+str(int_to_binary(self.register_file.read("011")))+" "+str(int_to_binary(self.register_file.read("100")))+" "+str(int_to_binary(self.register_file.read("101")))+" "+str(int_to_binary(self.register_file.read("110")))+" "+"0"*12+str(self.register_file.read("111")[1])+str(self.register_file.read("111")[1])+str(self.register_file.read("111")[2])+str(self.register_file.read("111")[3])+"\n")
            sys.stdout.write("        " + output_reg0
                    + " " + output_reg1
                    + " " + output_reg2
                    + " " + output_reg3
                    + " " + output_reg4
                    + " " + output_reg5
                    + " " + output_reg6
                    +" "  +"0"*12+(self.register_file.read("111"))+"\n")
                    #+ " " + "0" * 12 + str(self.register_file.flags[0])+str(self.register_file.flags[1])+
                    #str(self.register_file.flags[2])+str(self.register_file.flags[3]) + "\n")

            #print("        "+str(int_to_binary(self.register_file.read("000")))+" "+str(int_to_binary(self.register_file.read("001")))+" "+str(int_to_binary(self.register_file.read("010")))+" "+str(int_to_binary(self.register_file.read("011")))+" "+str(int_to_binary(self.register_file.read("100")))+" "+str(int_to_binary(self.register_file.read("101")))+" "+str(int_to_binary(self.register_file.read("110")))+" "+"0"*12+str(self.register_file.read("111")[1])+str(self.register_file.read("111")[1])+str(self.register_file.read("111")[2])+str(self.register_file.read("111")[3])+"\n")
            #sys.stdout.write(register_file.read())

            
            return halted,new_PC




    codelist=sys.stdin.readlines()


    memory = Memory()#128 elements of storage
    pc=0
    for line in codelist:
        line=line.strip()
        memory.write(pc,line)
        #sys.stdout.write(memory.read(pc)+"\n")
        pc+=1
    pc=0
    """
    while pc<128:

        instruction=input()#sys.stdin.readlines()
        
        if not instruction:
            break
        memory.write(pc,instruction) #instruction is string
        pc+=1
    """
    
    """
    while 128-pc:
        print(memory.read(pc))
        print("\n")
        pc+=1
    """
    register_file = RegisterFile()

    engine = ExecutionEngine(memory, register_file)
    pc=0
    new_pc=0
    halted=False
    while not halted:
        
        halted,new_pc=engine.execute(memory.read(pc),pc)
        pc=new_pc
        
        if pc==None:
            break

    
    
    pc=0
    while 128-pc:
        if 128-pc!=1:
            sys.stdout.write(str(memory.read((pc)))+"\n")
            
        elif 128-pc==1:
            sys.stdout.write(str(memory.read((pc))))
        #print(memory.read(pc))
        pc+=1

