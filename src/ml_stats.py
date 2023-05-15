import numpy as np
from .preprocessing import setup_label_database, divide_seq_to_frames

#Machine learning Stats
def get_element_count(lst, split=False):
    """This function calculates the occurence of each element of the given list.

    Args:
        lst (list): It's a list of elements [x, y, ..., z]
    Returns:
        dictionnary : A dictionnary like that -> { element A : count of element A ; element B : count of element B ; ..... }
    """
    dct={}
    if split==True :
        M=[]
        lst=[i.split("_") for i in lst]
        for i in lst:
            M+=i
        lst=M
    else :
        pass

    for i in lst :
        if type(i) == list:
            i="_".join(i)
        else:
            pass

        if i not in dct:
                dct[i]=1
        else:
            dct[i]+=1
            
    return dct

def get_mixedconstant_count(L, threshold, split=True):
    """This function calculates the count of constant element and mixed element in a list L.
    Args :
        L (list): list of elements. The elements have same length.
        threshold (numeric): a float value that help to consider a list as constant or not.
        split(bool): Indicates if we want to split our elements with a separator already 
        included in the elements of L. Default to True.
    Returns :
        dictionnary, [constant lists, mixed lists] : ( {constant lists : count of constant lists ; mixed lists : count of mixed lists }  ,  [constant lists, mixed lists] )
    
    """
    #A list is constant when we have the same element in the list
    dct={}
    constant_count=0
    constant_lists=[]
    mixed_count=0
    mixed_lists=[]
    c=0
    list_pct=[]
    #__________We check lengths of each element of L
    len_=[]
    M=[]

    if split==True:
        for i in L:
            M.append(i.split("_"))
        L=M
    else:
        pass

    
    for lst in L:
        len_.append(len(lst))
    lst2=list(np.unique(len_))
    if len(lst2)!=len(len_):
        for i in len_:
            if i==lst2[0]:
                c+=1
    #____________________
        if c== len(len_):       #If we have same lengths
            #We calculate constant count
            for element in L:
                j=0
                l=list(np.unique(element))
                for k in element :
                    if k==l[0] :
                        j+=1
                if j == len(element):
                    constant_count+=1
                    constant_lists.append(element)
                else:
                    constant_count+=0
            
            #We calculate mixed count
            """
            Process:
            We calculate the percentage of each element of the list where the lenght !=1
            We take the max one and we make 100% - this percentage = pct
            If pct > threshold : increase mixed_count
            """
            for element in L:
                if len(list(np.unique(element)))!=1:
                    #calculate the percentage of each element of the list
                    list_pct=[ (element.count(x)/ len(element))  for x in list(np.unique(element)) ]
                    #print(list_pct)
                    max_pct=max(list_pct)

                    if (1-max_pct)> threshold:
                        mixed_count+=1
                        mixed_lists.append(element)
                    else:
                        constant_count+=1
                        constant_lists.append(element)
                        
            dct={'Constant list ': constant_count, 'Mixed list ': mixed_count}
            
            return dct,[constant_lists, mixed_lists]
            
        else:  #If not
            a='The given list has to contain lists of same lengths'
            return a

def database_creation(PATH_IN, PATH_OUT, FRAME_LEN, FRAME_TSTEP):
    """This function creates all input and output frames for the database chosen.
    The arguments are input (path of person1 in conversation) and output (path of person2 in conversation) paths relative to this database.

    Args:
        PATH_IN (str):  full input path of eaf datas 
        PATH_OUT (str):  full output path of eaf datas 
        FRAME_LEN (numeric) : Length of a frame (in ms) for one sequence
        FRAME_TSTEP (numeric) : How many ms the frame move between each record

    Returns:
        tuple: input frames, output frames
    """
    new_lst, data_in, data_out =([] for _ in range(3))

    level=0
    for _ in reversed(list(enumerate(PATH_IN))):
        if PATH_IN[_[0]]== '\\':
            level=_[0]
            break
    a=PATH_IN[:level]
    level=0
    for _ in reversed(list(enumerate(a))):
        if a[_[0]]== '\\':
            level=_[0]
            break

    b=a[level+1:]
    for i in range(len(b)):
        if b[i]=='_':
            level=i
            break

    format=b[:level]

    labelled_data=setup_label_database(PATH_IN, PATH_OUT,format)
    lst=list(labelled_data.keys())
    
    for _ in lst:
        if len(_)==7:
            new_lst.append(_[-1:])
        else:
            new_lst.append(_[-2:])
    print(new_lst)
    for nb in new_lst:
        data_sequenced=divide_seq_to_frames(labelled_data[f"video_{nb}"], FRAME_LEN, FRAME_TSTEP)
        data = data_sequenced[0]
        data_in.append(data[0].tolist())
        data_out.append(data[1].tolist())

    #database=[data_in, data_out]
    #print(database)
    return data_in, data_out

