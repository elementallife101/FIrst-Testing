import sys
import random
def read_file(name):
    #reads a sequence from a .fasta file of a given name and returns a list of the sequence's elements
    with open(name, "r") as file:
        sequence = file.read()
    sequenceList = [character for character in sequence if character != "\n"]
    return sequenceList

def count_bases(sequence):
    #takes a sequence as input and creates a dictionary with the amount of each base in the sequence
    dict = {"a":0, "t":0, "c":0, "g":0}
    for base in set(sequence):
        dict[base] = sequence.count(base)
    return dict

def swapComplements(char):
    #is passed a single nucleotide, returns its complement
    if char == "c":
        return "g"
    elif char == "g":
        return "c"
    elif char == "a":
        return "t"
    return "a"

def complement(list, reverse=False):
    #calculates the complement of each nucleotide in a sequence to find the complement of the sequence
    #if reverse is True, reverses the order of the list elements to calculate the reverse complement
    complementList = [swapComplements(item) for item in list]
    if reverse == True:
        reverseList = []
        for i in range(len(list), 0, -1):
            reverseList.append(complementList[i-1])
        return reverseList
    return complementList

def get_gc_content(dict):
    return ((dict["c"]+dict["g"])/sum(dict.values())*100)

'''
This function is designed for Step 5 of Task 3.
This module calculates the GC content for all windows.
If the GC content is above the threshold provided, then it will be printed back to the user.

Inputs:
Sequence - The DNA Sequence (ACGTGTGTCAGT...)
Window_Size - The size of each window for testing
GC_Threshold - The point at which GC levels above it count as an island

Output:
CPG_islands, a list containing all the known islands within the given sequence

'''
def detect_gc_islands(sequence, window_size, gc_threshold):
    island_positions = []
    ## Finds the appropriate windows to test
    if window_size > 1:
        for i in range(len(sequence) - (window_size - 2)):
            window = sequence[i:(i + window_size)]
            ## Tests the window for characters and checks if it is an island
            sequenceList = [character for character in window]
            dict = count_bases(sequenceList)
            while True:
                try:
                    test_value = get_gc_content(dict)
                    if test_value > gc_threshold:
                        island_positions.append([i, i+window_size])
                    break
                ## Ensures that "c" and "g" both have entries in the dictionary
                ## They must be set to 0 by default.
                except KeyError:
                    try:
                        if dict["c"] > -1:
                            dict["g"] = 0
                    except KeyError:
                        dict["c"] = 0
    ## Returns the positions of the islands
    return island_positions

#def main(infile):
    #seq = read_input_file(infile)
    #cpg_islands = detect_cpg_islands(seq, window_size=200, gc_threshold=50.0)
    #print("GC Islands:")
    #for start, end, gc_content in cpg_islands:
        #print(f"Start: {start}, End: {end}, GC Content: {gc_content:.2f}%")

"""
This module represents Step 6 of Task 3.
This calculates the gc_content of a sequence for a particular window size.

Input:
Sequence (The String, representing the actual sequence itself)
Window_Size (An integer, which represents the size of the window)

Output:
total/(i + 1) (This represents the mean value of the gc_content (Total / No of values))
"""
def calculate_mean_gc_content(sequence, window_size):
#takes a sequence list and a window size as input, returns a mean for the gc content of a given window
    if window_size > 1:
        total = 0
        # Loops through appropriate starting values of the window (leftmost)
        # Finds window and calculates gc_content
        for i in range(len(sequence) - (window_size - 1)):
            window = sequence[i:(i + window_size)]
            dict = count_bases(window)
            test_value = get_gc_content(dict)
            total += test_value
        ## Calculates the mean and returns it to the user.
        return total/(i + 1)
    
argNumber = -1
writeToFile = 0
output = []
window_size = 10
for argument in sys.argv:
    argNumber += 1
    if argument == "--input":
        #Take the next up the 3 arguments as text files to read sequences from unless there are less than 3 more arguments or a new command is detected
        sequences = []
        for i in range((argNumber+1),len(sys.argv)):
            arg = sys.argv[i]
            if arg[:2] != "--":
                sequences.append(read_file(arg))
            else:
                break
        if sequences == []:
            print("Error: No files provided")
    elif argument == "--output":
        #change variable WriteToFile to 1 for later when the output is processed
        writeToFile = 1
    elif argument == "--base-count":
        #outputs the base count of each inputted sequence
        output.append("Base Counts:")
        for sequence in sequences:
            output.append(count_bases(sequence))
    elif argument == "--reverse-complement":
        #Outputs the first 50 elements of each sequence and the first 50 elements of the reverse complement of each sequence
        output.append("First 50 elements of each sequence followed by first 50 elements of the reverse complement of that sequence:")
        for sequence in sequences:
            complementSequence = complement(sequence, True)
            output.append(sequence[:49])
            output.append(complementSequence[:49])
    elif argument == "--GC-content":
        #outputs gc content of each sequence
        output.append("GC content of each sequence:")
        for sequence in sequences:
            output.append(get_gc_content(sequence))
    elif argument == "--number-of-islands":
        #calculates the threshold as 1.5*(the mean gc content) and then outputs the number of islands and their positions.
        output.append("Number of GC islands and list of positions of islands")
        for sequence in sequences:
            mean = calculate_mean_gc_content(sequence, window_size)
            gc_threshold = 1.5*mean
            island_positions = detect_gc_islands(sequence, window_size, gc_threshold)
            output.append(len(island_positions))
            output.append(island_positions)
if writeToFile == 0:
    for item in output:
        print(item)
elif writeToFile == 1:
    #writes output to file with random name
    with open("Output" + str(random.randint(10000, 99999)) + ".txt", "x") as file:
        for item in output:
            file.write(str(item) + "\n")

        