# FiniteStateMachine_Merger
This is a Finite State Machine Merger. The program merges virtual machines and creates 3 new Machine Definition files (see description.pdf to understand the format of these files). The 3 new machine definition files are the Union, the Intersection, and the Substraction of each machine.

# Note
This program is a very good example of modularity and efficiency.
Not only is a very short program (less than 300 lines) performing a fairly complex operation, but the time complexity of the main algorith is O(1).
The only loops in the program are execution loops. In the main algorithm, there is no linear search happening, it all works through tabular lookup, making the main algorithm have an O(1) time complexity.

########################################################################
# Must-Knows & Pre-reqs
These are things you must know to understand the program:
1. Understand what a Finite State Machine is and how it functions.
2. Have a basic understanding of the merging process for Finite State Machines.
3. Have a basic knowledge of set operaitons.

########################################################################
# To Run the program:
1. Download the repository in a machine with Python installed.
2. Run the script from the command line using "python Merge.py"
3. Make sure the Merge.py file is in the same directory as the file Minimize.py. Merge.py includes and calls functions from Minimize.py. If both files are not in the same directory, the program will not run.
4. Pass in the proper arguments as listed below

########################################################################
# Arguments - Merge.py receives 5 command line arguments in the following order:
# A Definition File

This Definition File configures Machine 1, following the instructions in the Description file (description.pdf).
# Another Definition File

This Definition File configures Machine 2, following the instructions in the Description file (description.pdf).
# The output file name for the UNION Machine

This will be the file name containing the Definition File of the machine resulting from the UNION of both machines.
# The output file name for the INTERSECTION Machine

This will be the file name containing the Definition File of the machine resulting from the INTERSECTION of both machines.
# The output file name for the SUBSTRACTION Machine

This will be the file name containing the Definition File of the machine resulting from the SUBSTRACTION of Machine1 minus Machine2.

############################
############################

Any questions or comments just message me. Feel free to use my code for whatever the heck you want to.
