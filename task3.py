import sys
def read_file(name):
    #reads a sequence from a .fasta file of a given name and returns a list of the sequence's elements
    with open(name, "r") as file:
        sequence = file.read()
    sequenceList = [character for character in sequence if character != "\n"]
    return sequenceList

def count_bases(sequence):
    #takes a sequence as input and creates a dictionary with the amount of each base in the sequence
    dict = {"a":0, "t":0, "c":0, "g":0}
    dict = {nucl:sequence.count(nucl) for nucl in set(sequence)}
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
So this function is designed for Step 5 - UNTESTED.
Inputs:
Sequence - The DNA Sequence (ACGTGTGTCAGT...)
Window_Size - The size of each window for testing
GC_Threshold - The point at which GC levels above it count as an island

Output:CPG_islands, a list containing all the known islands within the given sequence

'''
def detect_gc_islands(sequence, window_size, gc_threshold):
    cpg_islands = []
    
    if window_size > 1:
        for i in range(len(sequence) - (window_size - 2)):
            window = sequence[i:(i + window_size - 1)]
            sequenceList = [character for character in window]
            dict = {nucl:sequenceList.count(nucl) for nucl in set(sequenceList)}
            test_value = get_gc_content(dict)
            if test_value > gc_threshold:
                cpg_islands.append(window)

    return cpg_islands

#def main(infile):
    #seq = read_input_file(infile)
    #cpg_islands = detect_cpg_islands(seq, window_size=200, gc_threshold=50.0)
    #print("GC Islands:")
    #for start, end, gc_content in cpg_islands:
        #print(f"Start: {start}, End: {end}, GC Content: {gc_content:.2f}%")

def mean(list):
    return sum(list) / len(list)

def calculate_mean_gc_content(sequence, window_size):
    if window_size > 1:
        mean_list = []
        for i in range(len(sequence) - (window_size - 2)):
            window = sequence[i:(i + window_size - 1)]
            sequenceList = [character for character in window]
            dict = {nucl:sequenceList.count(nucl) for nucl in set(sequenceList)}
            test_value = get_gc_content(dict)
            mean_list.append(test_value)
        return mean(mean_list)
    
argNumber = -1
writeToFile = 0
output = []
for argument in sys.argv:
    argNumber += 1
    if argument == "--input":
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
    
if writeToFile == 0:
    for item in output:
        print(item)
        
        