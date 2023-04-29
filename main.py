def read_data_from_file(filename):
    """ 
    Reads from .txt file with lists of intervals, seperated by newlines
    Returns a set of lists containing lists with two integers (start and end of interval)
    """
    txt = open(filename)
    data = txt.read()
    txt.close()
    lines = data.split('\n')
    set_length = len(lines)
    lists = [[]*set_length]*set_length
    # iterate all lines in set
    for i in range(set_length):
        lines[i] = lines[i].replace("],[","]$[") # introduce seperation character $ between intervals
        lines[i] = lines[i].replace("]",""); lines[i] = lines[i].replace("[","") # remove unnecessary brackets
        lists[i] = lines[i].split("$") # split on new split character
        # iterate all sets
        for j in range(len(lists[i])):
            lists[i][j] = lists[i][j].split(",") # split on comma
            lists[i][j] = [ int(x) for x in lists[i][j]] # convert all characters to integers
    return(lists)

def similarity(set1, set2):
    """
    Returns mean list similarity between corresponding lists in two sets
    """
    set_length = len(set1)
    list_similarity = 0
    for i in range(len(set1)):
        list_similarity += list_similarity_symetric(set1[i], set2[i])
    return list_similarity/set_length

def list_similarity_symetric(list1,list2):
    """
    Returns symetric similarity between two lists by averaging the LS12 and LS21
    """
    similarity_forward = list_similarity(list1,list2)
    similarity_backward = list_similarity(list2,list1)
    print("LS12: {:3.2f}   LS21: {:3.2f}".format(similarity_forward, similarity_backward))
    return (similarity_forward+similarity_backward)/2

def list_similarity(list1, list2):
    """
    Returns asymetric similarity between two lists
    """
    list_similarity = 0
    # iterate intervals of list1
    for i in range(len(list1)):
        # check for overlap in intervals with list
        if overlap(list1[i],list2):
            list_similarity += 1
    max_list_length = max(len(list1), len(list2))
    return list_similarity/max_list_length

def overlap(interval, list):
    """
    Returns boolean overlap=True if there is an overlap in list with interval
    """
    index_interval = interval[0] # start with first element in interval
    list_length = len(list)
    overlap = False
    
    while index_interval <= interval[1] and not overlap:
        # iterate all values in interval. If overlap found exit loop
        index_list = 0 # start with first interval in list
        while index_list < list_length and not overlap:
            # loop over all intervals in list. If overlap found exit loop
            index_list_interval = list[index_list][0] # start with start value from interval
            while index_list_interval <= list[index_list][1] and not overlap:
                # loop over all values in interval. If overlap found exit loop
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
    print("Mean similarity in set: {:3.2f}".format(similarity(set_of_lists1, set_of_lists2)))
