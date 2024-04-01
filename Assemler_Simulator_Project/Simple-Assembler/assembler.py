
command_dictionary= {
    "add":{"opcode":"00000","type":"A"}, 
    "sub": {"opcode":"00001","type":"A"},
    "mov":{"opcode":["00010","00011"],"type":["B","C"]},
    "ld":{ "opcode":"00100","type":"D"},
    "st":{"opcode": "00101","type":"D"},
    "mul": {"opcode":"00110","type":"A"},
    "div":{"opcode":"00111","type":"C"},
    "rs": {"opcode":"01000","type":"B"},
    "ls":{"opcode":"01001","type":"B"},
    "xor":{"opcode":"01010","type":"A"},
    "or":{"opcode":"01011","type":"A"},
    "and":{"opcode":"01100","type":"A"},
    "not":{"opcode":"01101","type":"C"},
    "cmp":{"opcode":"01110","type":"C"},
    "jmp":{"opcode":"01111","type":"E"},
    "jlt":{"opcode":"11100","type":"E"},
    "jgt":{"opcode":"11101","type":"E"},
    "je":{"opcode":"11111","type":"E"},
    "hlt":{"opcode":"11010","type":"F"}
}


register_dictionary={"R0":"000","R1":"001","R2":"010","R3":"011",
"R4":"100","R5":"101","R6": "110","FLAGS":"111"}


program_counter=-1 # will act as program counter
var_counter=0
labels={}
variables={}
Imm_max=127
Imm_min=0
halt_counter=0
halt_occurences=[]

import sys
code_list=sys.stdin.readlines()


for line in code_list:
        instruction=line.split()

        if not line:
            continue

        program_counter+=1
        if ":" in line:
            if ":" in instruction[0]:
                label=instruction[0].rstrip(":")
                

                if label in labels:
                    
                    raise Exception(f"ERROR : line {program_counter} CONTAINS LABEL WHICH HAS ALREADY BEEN DECLARED")
                labels[label]=format(program_counter,'07b')
                
                if instruction[1]=="hlt":
                    halt_counter+=1
                    halt_occurences.append(program_counter)
            elif ":" not in instruction[0]:
                raise Exception(f"ERROR: line {program_counter} contains ILLEGAL synatx of label declaration")

        if instruction[0]=="var":
            if instruction[1] in variables:
                raise Exception(f"ERROR: line {program_counter} contains var that has already been declared")
            
            else:
                program_counter-=1
                var_counter+=1
                variables[instruction[1]]=var_counter

        if instruction[0]=="hlt":
            halt_counter+=1
            halt_occurences.append(program_counter)
        
        if program_counter>128:
            raise Exception("ERROR: maximum lines exceeded")
        



if halt_counter==0:
    
    raise Exception("ERROR: HALT NOT IN PROGRAM")
if halt_occurences[-1]!=program_counter:
    
    raise Exception("ERROR: HAlT not at end of program")
for i in variables:
    variables[i]=format(program_counter+variables[i],'07b')#as they are given address at last

binary_code=""

program_counter=-1



for line in code_list:


        if not line:# remove empty lines

            continue
        instruction=line.split()
        program_counter+=1
        if program_counter in range(var_counter):

            if instruction[0]!="var":
                raise Exception(f"ERROR: line {program_counter}VARIABLES HAVE NOT BEEN DECLARED AT START OF CODE")
            # as they are not to be counted 
            
            continue
        
        if ":" in line:
            instruction.remove(instruction[0])
        
        if instruction[0] not in command_dictionary:
            raise Exception("INVALID COMMAND")
        
        




        if instruction[0]=="mov":

            if instruction[1] in register_dictionary:
                if instruction[2]  in register_dictionary:# that is not c type
                    if (instruction[1]=="FLAGS") :
                        
                        raise Exception(f"ERROR:{program_counter} INVALID USAGE OF FLAGS REGISTERS")

                    
                    binary_code=command_dictionary[instruction[0]]["opcode"][1]+"00000"+register_dictionary[instruction[1]]+register_dictionary[instruction[2]]+"\n"
                    sys.stdout.write(binary_code)
                    
                    continue
                
                


                if instruction[2].startswith("$"):
                    instruction[2]=instruction[2].replace("$","",1)
                    try:
                        int(instruction[2])
                    except ValueError:
                        raise Exception(f"ERROR: {program_counter} immediate is not a integer")
                    if int(instruction[2])<0:
                        
                        raise Exception(f"ERROR: {program_counter} immediate is negative ")
                    if Imm_min>int(instruction[2]) or int(instruction[2])>Imm_max:
                        
                        raise Exception(f"ERROR: {program_counter} immediate not in supported range ")
                    binary_code=command_dictionary[instruction[0]]["opcode"][0]+"0"+register_dictionary[instruction[1]]+str(format(int(instruction[2]),'07b'))+"\n"
                    sys.stdout.write(binary_code)
                    
                    continue


                
                else:
                    
                    raise Exception(f"ERROR: {program_counter} 2nd argument is not a correct immediate nor a register ")

            else:
                
                raise Exception(f"ERROR: {program_counter} 1st argument is not  defined as register")

            #_______type C__________
        else:
            type=command_dictionary[instruction[0]]["type"]

            if type=="A":######_________type A__________
                
                
                if (instruction[1]=="FLAGS") or (instruction[2]=="FLAGS") or (instruction[3]=="FLAGS"):
                    
                    raise Exception(f"ERROR:{program_counter} INVALID USAGE OF FLAGS REGISTERS")
                
                if (instruction[1]in register_dictionary and instruction[2] in register_dictionary and instruction[3] in register_dictionary):
                    binary_code=command_dictionary[instruction[0]]["opcode"]+"00"+register_dictionary[instruction[1]]+register_dictionary[instruction[2]]+register_dictionary[instruction[3]]+"\n"
                    sys.stdout.write(binary_code)
                    
                    continue

                else:
                    
                    raise Exception(f"ERROR:{program_counter}INVALID REGISTER NAME")
            
            
            
            
            
            
            
            if type=="B":#___________whatif mov is encountered go up_________
                if instruction[1]=="FLAGS":
                    
                    raise Exception(f"ERROR:{program_counter} INVALID USAGE OF FLAGS REGISTERS")
                if instruction[2].startswith("$"):
                    instruction[2]=instruction[2].replace("$","",1)
                    try:
                        int(instruction[2])
                    except ValueError:
                        
                        raise Exception(f"ERROR: {program_counter} immediate is not a integer")
                    if int(instruction[2])<0:
                        
                        raise Exception(f"ERROR: {program_counter} immediate is negative ")
                    if Imm_min>int(instruction[2]) or int(instruction[2])>Imm_max:
                        
                        raise Exception(f"ERROR: {program_counter} immediate not in supported range ")
                    
                    if( (instruction[1] in register_dictionary) and (Imm_min<=int(instruction[2])<=Imm_max )):
                        binary_code=command_dictionary[instruction[0]]["opcode"]+"0"+register_dictionary[instruction[1]]+format(int(instruction[2]),'07b')+"\n"
                        sys.stdout.write(binary_code)
                        
                        continue


                    elif instruction[1] not in register_dictionary:
                        
                        raise Exception(f"ERROR: {program_counter}REGISTER INVALID")
                
                
                else:
                    raise Exception(f"ERROR: {program_counter} SYNTAX ERROR IN IMMEDIATE")
            




            #_________type C_____________
            
            
            
            
            
            
            if type=="C":
                if (instruction[1]=="FLAGS") or (instruction[2]=="FlAGS"):
                    
                    raise Exception(f"ERROR:{program_counter} INVALID USAGE OF FLAGS REGISTERS")

                if (instruction[1]in register_dictionary) and (instruction[2] in register_dictionary):
                    binary_code=command_dictionary[instruction[0]]["opcode"]+"00000"+register_dictionary[instruction[1]]+register_dictionary[instruction[2]]+"\n"
                    sys.stdout.write(binary_code)
                    
                    continue
                
                else:
                    
                    raise Exception(f"ERROR:{program_counter}  Invalid register names")
            #_______typeD_________
            if type=="D":
                
                
                if instruction[1] not in register_dictionary:
                    
                    raise Exception(f"ERROR: {program_counter} REGISTER CODE INVALID ")
                
                
                if (instruction[2] in variables) and (instruction[1]!="FLAGS") :
                    binary_code=command_dictionary[instruction[0]]["opcode"]+"0"+register_dictionary[instruction[1]]+variables[instruction[2]]+"\n"#memory address in variables corresp var 
                    sys.stdout.write(binary_code)
                    
                    continue

                elif instruction[2] in labels :
                    
                    raise Exception(f"ERROR: line {program_counter}INVALID USAGE OF LABELS instead of variables")
                
                    
                elif instruction[2]  not in variables: 
                    
                    raise Exception(f"ERROR: line {program_counter}: MEMORY NOT ACCESSIBLE as variable {instruction[2]} not defined")
        
                elif instruction[1]=="FLAGS":# if reg 1 is flag
                    
                    raise Exception(f"invalid usage of flags in line {program_counter}")
                
                #general syntax error
                else:
                    
                    raise Exception(f"ERROR: line  {program_counter}GENERAL SYNTAX ERROR")
        #else cond and reg and memory check

            if type=="E":
                #if command[1] in variables:
                 #   binary_code=command_dictionary[command[0]]["opcode"]+"0000"+variables[command[1]]#+mem address
                  #  sys.stdout.write(binary_code)
                   # output_file.write("\n")

                if instruction[1] in labels:# checks if memory is stored as memory address as labels
                    binary_code=command_dictionary[instruction[0]]["opcode"]+"0000"+labels[instruction[1]]+"\n"
                    sys.stdout.write(binary_code)
                    
                    continue
                
                
                elif instruction[1] in variables:# prevents from jumping to variables
                    
                    raise Exception(f"{program_counter} invalid use of variables")

                
                else:
                    
                    raise Exception(f"ERROR: {program_counter} MEMORY NOT ACCESSIBLE LABEL NOT DECLARED")
                
            if type=="F":
                binary_code=command_dictionary[instruction[0]]["opcode"]+"0"*11+"\n"
                sys.stdout.write(binary_code)
                break 
        




