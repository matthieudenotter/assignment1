def similarity(set_1, set_2, outfile):
    """
    Calculates list similarities between corresponding lists in set of lists 
    >parameters
    ----------
    set_1, set_2: text files with lines, containing a set of intervals [x1,y1],[x2,y2]...[xn,yn]
    >output
    ------
    outfile with value mean list similarity between corresponding lists in two sets parameters
    """
    if (set1 := read_data_from_file(set_1)) and (set2 := read_data_from_file(set_2)):
        if ((set_length := len(set1)) != len(set2)):
            print('Error: number of sets has to be equal in each file!')
        list_similarity = 0
        for i in range(len(set1)):
        # iterate list symetric similarities between all corresponding lists in sets (i.e. first lists in sets, second lists etc....)
            list_similarity += list_similarity_symetric(set1[i], set2[i])
        # write result to outfile
        outf = open(outfile, 'w')
        outf.write("{:.2f}".format(list_similarity/set_length))
        outf.close()
        return True
    else:
        print("No files could not be read")

def read_data_from_file(filename):
    """ 
    Reads from .txt file with lists of intervals, seperated by newlines
    Returns a set of lists containing lists with two integers (start and end of interval)
    """
    try: 
        txt = open(filename)
        data = txt.read()
        txt.close()
        lines = data.split('\n')
        set_length = len(lines)
        lists = [[]*set_length]*set_length
        for i in range(set_length):
        # iterate all lines in set
            lines[i] = lines[i].replace("],[","]$[") # introduce seperation character $ between intervals
            lines[i] = lines[i].replace("]",""); lines[i] = lines[i].replace("[","") # remove unnecessary brackets
            lists[i] = lines[i].split("$") # split on new split character
            for j in range(len(lists[i])):
            # iterate all sets
                lists[i][j] = lists[i][j].split(",") # split on comma
                lists[i][j] = [ int(x) for x in lists[i][j]] # convert all characters to integers
        return(lists)
    except: 
        print(filename, "not in folder")
        return False

def list_similarity_symetric(list1,list2):
    """
    Returns symetric similarity (assignment description) between two lists by averaging the LS12 and LS21
    """
    similarity_forward = list_similarity(list1,list2)
    similarity_backward = list_similarity(list2,list1)
    return (similarity_forward+similarity_backward)/2

def list_similarity(list1, list2):
    """
    Returns asymetric similarity (assignment description) between two lists.
    """
    list_similarity = 0
    for i in range(len(list1)):
    # iterate intervals from list1
        # check for overlap in intervals with list
        if overlap(list1[i],list2):
            list_similarity += 1
    return list_similarity/max(len(list1), len(list2))

def overlap(interval, list):
    """
    Returns boolean overlap=True if there is an overlap in list with interval
    >parameters
    ----------
    interval: list with two values(start and stop value of interval). list: list of intervals
    >output
    ------
    Boolean: true if overlap
    >algorithm
    ---------
    For each interval in list, calculate the sum of the spans of the intervals. If this sum is larger or equals than the joint interval span, there must be an overlap
    eg: [1,2] and [3,4]. Joint interval: [1:4]. (2-1)+(4-3)) < (4-3) so no overlap
    eg: [1,2] and [2,4]. Joint interval: [1:4]. 1+2 >= 3 overlap
    eg: [5,10] and [6,7]. Joint interval: [5:10]. 5+2 >= 5 so overlap
    eg: [1,2] and [8,9]. Joint interval: [1:9]. 1+1 < 8 so no overlap
    """
    list_length = len(list)
    overlap = False # default False
    index_list = 0
    span_interval = interval[1]-interval[0] # span of the interval
    while index_list<list_length and not overlap and interval[1] >= list[index_list][0]:
    # iterate intervals in list. Stop if overlap found. Third condition: exit loop if interval below list interval (only possible because lists are sorted!!)
        if span_interval + list[index_list][1] - list[index_list][0] >= max(list[index_list][1],interval[1])-min(list[index_list][0],interval[0]):
            overlap = True
        index_list += 1
    return overlap