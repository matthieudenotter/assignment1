def similarity(set_1, set_2, outfile):
    """
    Calculates list similarities between corresponding lists in set of lists 
        parameters
        ----------
        set_1, set_2: text files with lines, containing a set of intervals [x1,y1],[x2,y2]...[xn,yn]
    
        output
        ------
        outfile with value mean list similarity between corresponding lists in two sets parameters
    """
    if (set1 := read_data_from_file(set_1)) and (set2 := read_data_from_file(set_2)):
        if ((set_length := len(set1)) != len(set2)):
            print('Error: number of sets has to be equal in each file!')
        
        list_similarity = 0
        # iterate list symetric similarities between all corresponding lists in sets (i.e. first lists in sets, second lists etc....)
        for i in range(len(set1)):
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
    except: 
        print(filename, "not in folder")
        return False

def list_similarity_symetric(list1,list2):
    """
    Returns symetric similarity between two lists by averaging the LS12 and LS21
    """
    similarity_forward = list_similarity(list1,list2)
    similarity_backward = list_similarity(list2,list1)
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
        while index_list < list_length and not overlap and index_interval>list[index_list][0]:
            # loop over all intervals in list. If overlap found exit loop. 
            # third condition: exit loop if interval end < start value of interval from list
            # only possible if intervals are sorted => reduce order n^2
            index_list_interval = list[index_list][0] # start with start value from interval
            while index_list_interval <= list[index_list][1] and not overlap:
                # loop over all values in interval. If overlap found exit loop
                if index_interval == index_list_interval:
                    overlap = True
                index_list_interval += 1
            index_list += 1
        index_interval += 1
    return overlap