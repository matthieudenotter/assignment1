def read_data_from_file(filename):
    """ 
    Reads from .txt file with lists of intervals, seperated by newlines
    Returns a set of lists containing intervals
    """
    txt = open(filename)
    data = txt.read()
    txt.close()
    lines = data.split('\n')
    set_length = len(lines)
    lists = [[]*set_length]*set_length
    
    for i in range(set_length):
        lines[i] = lines[i].replace("],[","]$[")
        lines[i] = lines[i].replace("]",""); lines[i] = lines[i].replace("[","")
        lists[i] = lines[i].split("$")
        for j in range(len(lists[i])):
            lists[i][j] = lists[i][j].split(",")
            lists[i][j] = [ int(x) for x in lists[i][j]]
    return(lists)

def calculate_set_similarity(set1, set2):
    """
    Calculates mean list similarity between corresponding lists in two sets
    """
    set_length = len(set1)
    list_similarity = 0
    for i in range(len(set1)):
        list_similarity += calculate_list_similarity_symetric(set1[i], set2[i])
    return list_similarity/set_length

def calculate_list_similarity_symetric(list1,list2):
    """
    Calculates symetric similarity between two lists by averaging the LS12 and LS21
    """
    similarity_forward = calculate_list_similarity(list1,list2)
    similarity_backward = calculate_list_similarity(list2,list1)
    
    print(similarity_forward, similarity_backward)
    return (similarity_forward+similarity_backward)/2

def calculate_list_similarity(list1, list2):
    list_similarity = 0
    for i in range(len(list1)):
        if overlap(list1[i],list2):
            list_similarity += 1
    max_list_length = max(len(list1), len(list2))
    return list_similarity/max_list_length

def overlap(interval, list):
    index_interval = interval[0]    
    list_length = len(list)
    overlap = False
    while index_interval <= interval[1] and not overlap:
        index_list = 0
        while index_list < list_length and not overlap:
            index_list_interval = list[index_list][0]
            while index_list_interval <= list[index_list][1] and not overlap:
                if index_interval == index_list_interval:
                    overlap = True
                index_list_interval += 1
            index_list += 1
        index_interval += 1
    return overlap

# Main Code
set_of_lists1 = read_data_from_file('sample_set1.txt')
set_of_lists2 = read_data_from_file('sample_set2.txt')

if ((set_length := len(set_of_lists1)) != len(set_of_lists2)):
    print('Error: number of sets has to be equal in each file!')
else: 
    print(calculate_set_similarity(set_of_lists1, set_of_lists2))