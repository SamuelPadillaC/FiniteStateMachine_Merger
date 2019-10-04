########################################
# Created by Samuelito Perro #
########################################
# This is a Finite State Mahcine Merger
# Takes 5 files, the first is an FSA description, the second one is another FSA description of a different machine,
# the third one is the name of Union file of the Machines,
# the fourth one is the name of Intersection file of the Machines
# the fifth one is the name of Substraction file of the Machines.
# Check specifications document to understand the format of these documents

# IMPORTS #
import time, sys
import queue
from Minimize import *
from collections import deque


start = time.time()
#########################################################
#                       CLASSES                         #
#########################################################

class Machine:
    #Initialize values for the Machine
    def __init__(self, Num):
        self.vector_lines = []
        self.Alphabet = []
        self.States = []
        self.Accepting_States = []
        self.Transition_Function = []
        self.Possible = []
        self.Impossible = []
        self.Redundant = []
        self.Num = Num

    #Read values from FSA definition
    def ReadValues(self, Path):
        self.vector_lines, self.Alphabet, self.States, self.Accepting_States = ReadFSA(Path)

    #Create Transition Function Table
    def Create_Trans_Function(self):
        self.Transition_Function = Create_Table(self.vector_lines, self.Alphabet, self.States, self.Accepting_States)

    def Minimize_Calls (self, Alphabet, States, Accepting_States, Transition_Function, Possible, Impossible, Redundant):
        # Getting Rid of Unreachable States and Defining New Transition_Funtion, New States, and Accepting_States #
        self.Transition_Function, self.States, self.Accepting_States = Delete_Unreachable(self.Transition_Function, self.States, self.Accepting_States, 0) #Since I'm not keeping records of Minimization, just past a 0 as the last argument

        # Defining Initial Impossible and Possible States #
        self.Possible, self.Impossible = Define_Impossible(self.States, self.Accepting_States)
        
        # Finding Redundant States #
        self.Redundant = Find_Redundant(self.Possible, self.Impossible, self.Transition_Function, self.States, self.Alphabet)
            
        # Combining Redundant States #
        if len(self.Redundant) >= 2: #Only execute if two or more redundant states exist
            self.Transition_Function, self.States, self.Accepting_States = Delete_Redundant(self.Redundant, self.Transition_Function, self.States, self.Accepting_States, 0) #Since I'm not keeping records of Minimization, just past a 0 as the last argument
            
        print("\nMACHINE", self.Num , "IS: ")
        print(self.Transition_Function)

###############################
#      DRIVER FUNCTION       #
###############################
def main ():
    # Parameters Check #
    if len(sys.argv) != 6:
        print("\nUSAGE: Please enter 5 parameters in the following order:")
        print("1. An FSA definition file\n2. Another FSA definiton file \n3. The output file name for the UNION of the FSAs \n4. The output file name for the INTERSECTION of the FSAs \n5. The output file name for the SUBSTRACTION of the FSAs")
        exit()

    # Creating Machine Classes #
    M1 = Machine(1)
    M2 = Machine(2)

    # Calling ReadValues function in the class #
    M1.ReadValues(sys.argv[1])
    M2.ReadValues(sys.argv[2])

    # Calling the Create_Trans_Function function in the class #
    M1.Create_Trans_Function()
    M2.Create_Trans_Function()

    # Informing User of Succesful read of FSA #
    print("\nSUCCESFUL READ OF FSA DEFINITION FILES")
    print("-------------------------------------------")

    # Alphabet Checks #
    x = sorted(M1.Alphabet, key = str)
    y = sorted(M2.Alphabet, key = str)        
    if x != y:
        print("\nERROR:\nThe two machines have different alphabets")
        exit(0)

    # Minimizing Both Machines #
    print ("\nMINIMIZING BOTH MACHINES")
    M1.Minimize_Calls (M1.Alphabet, M1.States, M1.Accepting_States, M1.Transition_Function, M1.Possible, M1.Impossible, M1.Redundant)
    M2.Minimize_Calls (M2.Alphabet, M2.States, M2.Accepting_States, M2.Transition_Function, M2.Possible, M2.Impossible, M2.Redundant)

    # Initialize table with all values -1 and index list with [0,0] #
    Table = ['blank'] * M1.States
    for i in range (0, len(Table)):
        Table[i] = [-1] * M2.States
    Table[0][0] = 0 #Initialize the 0,0 in the table
    Indexes = [[0,0]] #Initialize Indexes list

    # Creating Merged Transition Function #
    Merged_Table, Indexes = New_Transition_Function(Table, Indexes, M1.Transition_Function, M2.Transition_Function, M1.Alphabet, M2.Alphabet) 
    print("\n-----------------------------------")
    print("-----------------------------------")
    print ("\nMERGING BOTH TRANSITION TABLES")
    print("\nFinal Merged Table is:")
    print(Merged_Table)
    print("\nFinal Index list is:")
    print (Indexes)
    print("\n-----------------------------------")
    print("-----------------------------------")

    # Performing Union, Intersection, and Substraction #
    Union (sys.argv[3], Indexes, M1.Accepting_States, M2.Accepting_States, Merged_Table, M1.Alphabet)
    print ("\nUNION operation completed.\nCheck the file", sys.argv[3])
    Intersection (sys.argv[4], Indexes, M1.Accepting_States, M2.Accepting_States, Merged_Table, M1.Alphabet)
    print ("\nINTERSECTION operation completed.\nCheck the file", sys.argv[4])
    Substraction (sys.argv[5], Indexes, M1.Accepting_States, M2.Accepting_States, Merged_Table, M1.Alphabet)
    print ("\nSUBSTRACTION operation completed.\nCheck the file", sys.argv[5])

    # Final Message #
    print ("\n-----------------------------------")
    print("-----------------------------------")
    print ("\nExecution time was: ", time.time() - start)
    
#########################################################
#                   PUBLIC FUNCTIONS                    #
#########################################################

def New_Transition_Function (Table, Indexes, Transition_Function_0, Transition_Function_1, Alphabet_1, Alphabet_2):
    # Initialize Variables #
    # 3-n nested list where n1 is the encapsulation
    # n2 is the line or the state
    # n3 is the ordered pair of where the state points
    # at each letter of the alphabet
    Merged = [['pair'] * len(Alphabet_1)]
    counter = 0 #Start counting on state 0

    while 1: #Infinite loop of execution 
        initial_len = len(Indexes) #Define initial len of Indexes[]
        
        #Loop through the alphabet
        for letter_M1 in range (0, len(Alphabet_1)):
            # If alphabets are different, Grab the index of the letter in Alphabet 2.
            if Alphabet_1 != Alphabet_2:
                letter_M2 = Get_Letter_Index(Alphabet_1[letter_M1], Alphabet_2)
            # Else, letter indexes are the same
            else:
                letter_M2 = letter_M1

            # This goes into the transition function of each machine,
            #grabs the state in the Indexes list defined by the counter
            #and grabs counter[0] for machine0 and counter[1] for machine1.
            Looking_At = [Transition_Function_0[Indexes[counter][0]][letter_M1], Transition_Function_1[Indexes[counter][1]][letter_M2]]

            # Check if that state already exists in the table #
            if Table[Looking_At[0]][Looking_At[1]] == -1: #If it hasn't been marked yet
                Table[Looking_At[0]][Looking_At[1]] = len(Indexes) #Mark it with the next index (which is the size of Indexes)
                Indexes.append(Looking_At) #Append the pair to the Indexes list
            
            
            # Add Looking_At to the merged transition function
            Merged[counter][letter_M1] = Looking_At
            
        # Breaking condition: if no more new pairs were found and all the previous lines have been completed, break
        if len(Indexes) == initial_len and Merged[len(Indexes)-1][len(Alphabet_1)-1] != 'pair':
            break
        # Else, append new pairs in Indexes to Merged Table and increase counter
        else:
            for i in range (initial_len, len(Indexes)): #This doesn't do anything if the size of Indexes didn't change, so no worries there
                Merged.append(['pair'] * len(Alphabet_1)) #Append a new line
            counter += 1

    # Call external function to get the final table indexes
    Merged = Get_Merged_Table_Final_Indexes (Merged, Indexes, Table)

    return Merged, Indexes

#################################################
#################################################

def Get_Letter_Index (letter, Alphabet_2):
    # Loop through the Alphabet of Machine 2
    for i in range (0, len(Alphabet_2)):
        # When finding a match for the letter, return the index
        if Alphabet_2[i] == letter:
            return i

#################################################
#################################################

def Get_Merged_Table_Final_Indexes (Merged, Indexes, Table):
    #Assign the index in Checking Table indicated
    # by the coordenates of the pair
    # to the value of each pair in the merged table
    for State in range(0, len(Merged)): #Loops through the table
        for Pair in range(0, len(Merged[State])): #Loops through the State
            Merged[State][Pair] = Table[Merged[State][Pair][0]][Merged[State][Pair][1]]
    
    return Merged

#################################################
#################################################

def Union (Path, Indexes, Accepting_States_1, Accepting_States_2, Merged_Table, Alphabet):
    # Initialize stuff #
    Union_Accepting_States = []
    Output = open(Path, "w")

    # Union of accepting States #
    for Pair_Index in range(0, len(Indexes)):
        #Using 'in' to check if any of the states is an accepting state
        if Indexes[Pair_Index][0] in Accepting_States_1 or Indexes[Pair_Index][1] in Accepting_States_2:
            Union_Accepting_States.append(Pair_Index) #Append the index, not the pair
    
    # Writing to Output File
    Output.write("%s\n" % Alphabet)
    Output.write("%s\n" % len(Indexes))
    for i in Union_Accepting_States:
        Output.write("%s " % i)
    Output.write("\n")
    for Line in Merged_Table:
        for State in Line:
            Output.write("%s " % State)
        Output.write("\n")
    Output.close()

#################################################
#################################################

def Intersection (Path, Indexes, Accepting_States_1, Accepting_States_2, Merged_Table, Alphabet):
    # Initialize stuff #
    Union_Accepting_States = []
    Output = open(Path, "w")

    # Union of accepting States #
    for Pair_Index in range(0, len(Indexes)):
        #Using 'in' to check if BOTH of the states are an accepting state
        if Indexes[Pair_Index][0] in Accepting_States_1 and Indexes[Pair_Index][1] in Accepting_States_2:
            Union_Accepting_States.append(Pair_Index) #Append the index, not the pair
    
    # Writing to Output File
    Output.write("%s\n" % Alphabet)
    Output.write("%s\n" % len(Indexes))
    for i in Union_Accepting_States:
        Output.write("%s " % i)
    Output.write("\n")
    for Line in Merged_Table:
        for State in Line:
            Output.write("%s " % State)
        Output.write("\n")
    Output.close()

#################################################
#################################################

def Substraction (Path, Indexes, Accepting_States_1, Accepting_States_2, Merged_Table, Alphabet):
    # Initialize stuff #
    Union_Accepting_States = []
    Output = open(Path, "w")

    # Union of accepting States #
    for Pair_Index in range(0, len(Indexes)):
        #Using 'in' to check if the first states is an accepting state and the second one isn't
        if Indexes[Pair_Index][0] in Accepting_States_1 and Indexes[Pair_Index][1] not in Accepting_States_2:
            Union_Accepting_States.append(Pair_Index) #Append the index, not the pair
    
    # Writing to Output File
    Output.write("%s\n" % Alphabet)
    Output.write("%s\n" % len(Indexes))
    for i in Union_Accepting_States:
        Output.write("%s " % i)
    Output.write("\n")
    for Line in Merged_Table:
        for State in Line:
            Output.write("%s " % State)
        Output.write("\n")
    Output.close()    

#################################################
#################################################
# Calling the main function first #
if __name__ == "__main__":
    main ()
#####################