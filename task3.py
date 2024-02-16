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
So this function is designed for Step 5 - HAS PARTIALLY STOPPED WORKING DUE TO EARLIER CODE CHANGES.
Inputs:
Sequence - The DNA Sequence (ACGTGTGTCAGT...)
Window_Size - The size of each window for testing
GC_Threshold - The point at which GC levels above it count as an island

Output:CPG_islands, a list containing all the known islands within the given sequence

'''
def detect_gc_islands(sequence, window_size, gc_threshold):
    #Takes a sequence list, the size of the window and the gc threshold as inputs, returns a list of island positions.
    island_positions = []
    
    if window_size > 1:
        for i in range(len(sequence) - (window_size - 2)):
            window = sequence[i:(i + window_size)]
            sequenceList = [character for character in window]
            dict = count_bases(sequenceList)
            while True:
                try:
                    test_value = get_gc_content(dict)
                    if test_value > gc_threshold:
                        island_positions.append([i, i+window_size])
                    break
                except KeyError:
                    try:
                        if dict["c"] > -1:
                            dict["g"] = 0
                    except KeyError:
                        dict["c"] = 0
    return island_positions

#def main(infile):
    #seq = read_input_file(infile)
    #cpg_islands = detect_cpg_islands(seq, window_size=200, gc_threshold=50.0)
    #print("GC Islands:")
    #for start, end, gc_content in cpg_islands:
        #print(f"Start: {start}, End: {end}, GC Content: {gc_content:.2f}%")

"""
This version of task 6 works.
"""
def calculate_mean_gc_content(sequence, window_size):
#takes a sequence list and a window size as input, returns a mean for the gc content of a given window
    if window_size > 1:
        total = 0
        for i in range(len(sequence) - (window_size - 1)):
            window = sequence[i:(i + window_size)]
            print(window)
            dict = count_bases(window)
            test_value = get_gc_content(dict)
            total += test_value
    return total/(i + 1)
    
argNumber = -1
writeToFile = 0
output = []
window_size = 10
for argument in sys.argv:
    argNumber += 1
    if argument == "--input":
        #if input is detected as a command line argument, 
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
        writeToFile = 1
    elif argument == "--base-count":
        output.append("Base Counts:")
        for sequence in sequences:
            output.append(count_bases(sequence))
    elif argument == "--reverse-complement":
        output.append("First 50 elements of each sequence followed by first 50 elements of the reverse complement of that sequence:")
        for sequence in sequences:
            complementSequence = complement(sequence, True)
            output.append(sequence[:49])
            output.append(complementSequence[:49])
    elif argument == "--GC-content":
        output.append("GC content of each sequence:")
        for sequence in sequences:
            output.append(get_gc_content(sequence))
    elif argument == "--number-of-islands":
        output.append("Number of GC islands and list of positions of islands")
        for sequence in sequences:
            mean = calculate_mean_gc_content(sequence, window_size)
            gc_threshold = 1.5*mean
            print(gc_threshold)
            island_positions = detect_gc_islands(sequence, window_size, gc_threshold)
            print(len(island_positions))
            print(island_positions)
if writeToFile == 0:
    for item in output:
        print(item)
elif writeToFile == 1:
    with open("Output" + str(random.randint(10000, 99999)) + ".txt", "x") as file:
        for item in output:
            file.write(str(item) + "\n")

        