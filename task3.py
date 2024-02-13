import sys
def read_file(name):
    #reads a sequence from a .fasta file of a given name and returns a list of the sequence's elements
    with open(name, "r") as file:
        sequence = file.read()
    sequenceList = [character for character in sequence]
    return sequenceList

sequenceList = read_file("sequence.fasta")

def count_bases(sequence):
    #takes a sequence as input and creates a dictionary with the amount of each base in the sequence
    dict = {"a":0, "t":0, "c":0, "g":0}
    dict = {nucl:sequence.count(nucl) for nucl in set(sequence)}
    return dict
dict = count_bases(sequenceList)

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
            reverseList.append(complementList[i])
        return reverseList
    return complementList

def get_gc_content(dict):
    return ((dict["c"]+dict["g"])/sum(dict.values())*100)

argNumber = -1
writeToFile = 0
output = []
for argument in sys.argv:
    argNumber += 1
    if argument == "--input":
        sequences = []
        for i in range((argNumber+1),len(sys.argv)):
            arg = sys.argv[i]
            if arg[:1] != "--":
                sequences.append(read_file(arg))
            else:
                break
        if sequences == []:
            print("Error: No files provided")
            sequences = [sequenceList]
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
        
        