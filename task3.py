with open("sequence.fasta", "r") as file:
    sequence = file.read()
sequenceList = [character for character in sequence]
dict = {nucl:sequenceList.count(nucl) for nucl in set(sequenceList)}
def swapComplements(char):
    if char == "c":
        return "g"
    elif char == "g":
        return "c"
    elif char == "a":
        return "t"
    return "a"
def complement(list, reverse=False):
    complementList = [swapComplements(item) for item in list]
    if reverse == True:
        reverseList = []
        for i in range(len(list), 0, -1):
            reverseList.append(complementList[i])
        return reverseList
    return complementList
def get_gc_content(dict):
    return ((dict["c"]+dict["g"])/sum(dict.values())*100)
print(dict)
print(get_gc_content(dict))