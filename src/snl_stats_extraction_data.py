import itertools
import re
import os, sys
script_path = os.path.realpath(os.path.dirname("IBPY"))
os.chdir(script_path)
sys.path.append("..")
import json
import pympi
import numpy as np
from IBPY.interaction_analysis import *
from .preprocessing import *
from IBPY.utils import *
from IBPY.db import *
from IBPY.extract_data import *
import pandas as pd
from scipy.stats import pearsonr 
from .json_creation import create_json_from_directory

#JSON_________________________________________________________

# Creates JSON file with the directory structure and annotation information
create_json_from_directory()

current_dir = os.getcwd()
json_file_path = os.path.join(current_dir, 'data.json')
print(json_file_path)
# Check if the JSON file exists
if os.path.exists(json_file_path):
    # Read the data from the JSON file
    with open(json_file_path, 'r') as f:
        parameters = json.load(f)
else:
    # Handle the case when the JSON file doesn't exist
    print("data.json file not found.")

#____________________________________________________________________
DIR=parameters["FOLDER_PATHS"]["DIR"]
databases_pair_paths = parameters["DATABASES_PAIR_PATHS"]
databases_paths = parameters["DATABASES_PATHS"]
tier_lists = parameters["TIER_LISTS"]

#____________________________________________________________________
databases = {}
databases_pairs = {}
tiers = {}
# Parcours des jeux de données pair
for db_name, db_path in databases_pair_paths.items():
    databases_pairs[db_name] = db_path

# Parcours des jeux de données
for db_name, db_path in databases_paths.items():
    databases[db_name] = db_path

# Parcours des tiers d'expressions
for tier_name, tier_list in tier_lists.items():
    tiers[f"intensity_{tier_name.lower()}"] = tier_list
#____________________________________________________________________


def correct_dict_role_smiles(dict_,listpaths,string):
    """This function set to 0 intensities that doesn't exist in our eaf files for smiles.

    Args:
        dict_ (list): list of the tuple we have to fix
        listpaths (list): list of eaf paths of a database
        string (str): nae of the database concerned

    Returns:
        A list with previously non-existent intensities set to 0.    
    """
    dict_sub=[]
    dict_present_subject=[]
    label_present_subject=[]
    
    # print(len(dict_))
    # print(dict_[0])
    #Si un sujet n'existe pas, on l'ajoute et on mets tous ses labels à 0
    subjects=[i for i in range(1,len(listpaths)+1)]
    #print(subjects)
    for _ in dict_:dict_sub.append(_[0])
    for subject in subjects:
        if subject not in dict_sub:
            for i in tier_lists["Smiles"]:
                dict_.append((subject,string,i,0,0,dict_[0][5]))
        else:
            #Si un sujet existe 
            for _ in dict_: 
                if _[0]==subject: 
                    dict_present_subject.append(_) 
                    for i in dict_present_subject : label_present_subject.append(i[2]) #je prends les labels du sujet qui existe que je stocke 
            #Si un des labels normaux n'est pas dans cette liste de label, on le mets à 0
                    for l in tier_lists["Smiles"] :
                        if l not in label_present_subject :
                            dict_.append((subject, string,l,0,0,dict_[0][5]))# dict_=list(df_to_correct.to_records(index=False))
    #print(len(dict_))

    return dict_

def correct_dict_role_laughs(dict_,listpaths,string):
    """This function set to 0 intensities that doesn't exist in our eaf files for laughs.

    Args:
        dict_ (list): list of the tuple we have to fix
        listpaths (list): list of eaf paths of a database
        string (str): nae of the database concerned

    Returns:
        A list with previously non-existent intensities set to 0.    
    """
    dict_sub=[]
    dict_present_subject=[]
    label_present_subject=[]
    
    # print(len(dict_))
    # print(dict_[0])
    #Si un sujet n'existe pas, on l'ajoute et on mets tous ses labels à 0
    subjects=[i for i in range(1,len(listpaths)+1)]
    #print(subjects)
    for _ in dict_:dict_sub.append(_[0])
    for subject in subjects:
        if subject not in dict_sub:
            for i in tier_lists["Laughs"]:
                dict_.append((subject,string,i,0,0,dict_[0][5]))
        else:
            #Si un sujet existe 
            for _ in dict_: 
                if _[0]==subject: 
                    dict_present_subject.append(_) 
                    for i in dict_present_subject : label_present_subject.append(i[2]) #je prends les labels du sujet qui existe que je stocke 
            #Si un des labels normaux n'est pas dans cette liste de label, on le mets à 0
                    for l in tier_lists["Laughs"] :
                        if l not in label_present_subject :
                            dict_.append((subject, string,l,0,0,dict_[0][5]))# dict_=list(df_to_correct.to_records(index=False))
    #print(len(dict_))

    return dict_


def get_SLdict(root):
    """
    Return a list of S&L with the label corresponding to the Smiles_0 and Laughs_0 dictionnaries

    Args :
        root (str) -> Path of the file
    """
    lst1 = get_Sdict(root)
    lst2 = get_Ldict(root)
    to_dict = read_eaf_to_dict (root, mark=True, tiers=None)
    lst=to_dict["S&L_0"]

    nb=0
    for _ in range (0, len(lst),1): 
        for j in lst1:
            if (lst[_][0] == j[0]) and (lst[_][1] == j[1]):
                nb+=1
                y=list(lst[_])
                y[2]='S'
                lst[_]=tuple(y)
    #print(f"Nb smiles in S&L : {nb}", lst)
    nb=0
    for _ in range (0, len(lst),1): 
        for j in lst2:
            if (lst[_][0] == j[0]) and (lst[_][1] == j[1]):
                nb+=1
                y=list(lst[_])
                y[2]='L'
                lst[_]=tuple(y)
    #print(f"Nb laughs in S&L : {nb}", lst)
    return lst

def get_Sdict(root):
    """
    Give the list of smiles from a file.
    Arg : root (str) -> path of the file
    """
    to_dict = read_eaf_to_dict (root, mark=True, tiers=None)
    lst = to_dict["Smiles_0"]
    return lst

def get_Ldict(root):
    """
    Give the laughs's list from a file
    Arg : root (str) -> path of the file
    """
    to_dict = read_eaf_to_dict (root, mark=True, tiers=None)
    lst = to_dict["Laughs_0"]
    return lst

def get_Rdict(root):
    """
    Give the role's list from a file
    Arg : root (str) -> path of the file
    """
    to_dict = read_eaf_to_dict (root, mark=True, tiers=None)
    lst = to_dict["Role"]
    return lst

def get_tier_dict(root, tier):
    """
    Retrieve the list of a specific tier from a file.

    Args:
        root (str): Path of the file.
        tier (str): Tier name.

    Returns:
        list: List of the specified tier from the file.
    """
    to_dict = read_eaf_to_dict(root, mark=True, tiers=None)
    lst = None
    if tier not in to_dict:
        tier = tier + '_0'
    lst = to_dict[tier]
    return lst

def get_IR_list(root,expression, intensity):
    """
    Give the list of tier from a file for a given intensity or a given role
    Args :
        root (str) -> path of the file
        expression (str) -> tier name
        intensity (str) -> intensity or role of the tier
    """
    tier= get_tier_from_file(root, expression, intensity)
    lst= tier[expression]

    return lst

def get_tier_dict_folder(filespaths, database, tier):
    """
    Retrieve the dataframe of a specified tier from a folder.
    Args:
        filespaths (list): List of file paths in the folder.
        database (str): Database name (e.g., "ccdb", "ifadv", "ndc").
        tier (str): Tier name to retrieve the data from.
    Returns:
        A list of tuples and the column names.
    """
    startime, endtime, label, subject, duration = ([] for _ in range(5))
    s = 1
    for file in filespaths:
        lst_ = get_tier_dict(file, tier)
        eaf = pympi.Elan.Eaf(file)
        c = check_duration(eaf)
        for i in range(len(lst_)):
            subject.append(s)
            startime.append(lst_[i][0])
            endtime.append(lst_[i][1])
            label.append(lst_[i][2])
            duration.append(c)

        s += 1  
    df=pd.DataFrame({'database': list_of_words(f"{database}", len(subject)),'subject':subject,'startime':startime, 
    'endtime':endtime,'label':label,'duration':duration})
    df['diff_time']=df['endtime']-df['startime']

    df.columns = ['database', 'subject', 'startime', 'endtime', 'label', 'duration', 'diff_time']
    df = df.reindex(columns=['startime', 'endtime', 'label', 'subject', 'diff_time', 'duration', 'database'])

    lst = df_to_list(df)
    col = ['startime', 'endtime', 'label', 'subject', 'diff_time', 'duration', 'database']

    return lst, col

def get_smiles_dict_folder(filespaths,database):
    """
    Give the dataframe of smiles from a folder.
    Args : 
        filespaths (list) -> Cointain the filespath of the folder
        database (str) -> ccdb, ifadv or ndc
    Return :
        A list of tuple and the list L = ['startime','endtime','label', 'subject', 'diff_time', 'duration','database'] 
    """
    startime, endtime, label, subject,duration = ([] for _ in range(5))
    s=1
    for _ in filespaths:
        lst_ = get_Sdict(_)
        eaf = pympi.Elan.Eaf(_)
        c=check_duration(eaf)
        for i in range(len(lst_)):
            subject.append(s)
            startime.append(lst_[i][0])
            endtime.append(lst_[i][1])
            label.append(lst_[i][2])
            duration.append(c)

        s+=1

    df=pd.DataFrame({'database': list_of_words(f"{database}", len(subject)),'subject':subject,'startime':startime, 
    'endtime':endtime,'label':label,'duration':duration})
    df['diff_time']=df['endtime']-df['startime']
   
    df.columns=['database','subject','startime','endtime','label','duration','diff_time']
    #df.drop(df.columns[[2,3,4]], axis=1, inplace=True)
    df=df.reindex(columns=['startime','endtime','label','subject','diff_time', 'duration','database'])

    lst=df_to_list(df)
    col=['startime','endtime','label', 'subject','diff_time', 'duration','database']

    return lst,col

def get_laughs_dict_folder(filespaths,database):
    """
    Give the dataframe of laughs from a folder.
    Args : 
        filespaths (list) -> Cointain the filespath of the folder
    Return :
        A list of tuple and the list L = ['startime','endtime','label', 'subject', 'diff_time', 'duration','database'] 
    """
    startime, endtime, label, subject , duration= ([] for _ in range(5))
    s=1
    n=1
    for _ in filespaths:
        lst_ = get_Ldict(_)
        eaf = pympi.Elan.Eaf(_)
        c=check_duration(eaf)
        for i in range(len(lst_)):
            subject.append(s)
            startime.append(lst_[i][0])
            endtime.append(lst_[i][1])
            label.append(lst_[i][2])
            duration.append(c)
            n+=1

        s+=1

    df=pd.DataFrame({'database': list_of_words(f"{database}", len(subject)),'subject':subject, 'startime':startime, 
    'endtime':endtime,'label':label,'duration':duration})
    df['diff_time']=df['endtime']-df['startime']
    df.columns=['database','subject','startime','endtime','label','duration','diff_time']
    #df.drop(df.columns[[2,3,4]], axis=1, inplace=True)

    df=df.reindex(columns=['startime','endtime','label', 'subject','diff_time', 'duration','database'])
    lst=df_to_list(df)
    col=['startime','endtime','label', 'subject','diff_time', 'duration','database']

    return lst,col

def get_smiles_dict_conv_folder(filespaths,database):
    """
    Give the dataframe of smiles from a folder.
    Args : 
        filespaths (list) -> Cointain the filespath of the folder
        database (str) -> ccdb, ifadv or ndc
    Return a list of tuple and the list L =['startime','endtime','label', 'subject','diff_time', 'duration','database'] 
    """
    startime, endtime, label, subject,duration = ([] for _ in range(5))
    s=1
    n=0
    for _ in range (len(filespaths)):
        #print("file ",_,"duration n°",n)
        lst_ = get_Sdict(filespaths[_])
        eaf = pympi.Elan.Eaf(filespaths[n])
        eaf2= pympi.Elan.Eaf(filespaths[n+1])
        c=check_duration(eaf)
        c2= check_duration(eaf2)
        for i in range(len(lst_)):
            subject.append(s)
            startime.append(lst_[i][0])
            endtime.append(lst_[i][1])
            label.append(lst_[i][2])
            duration.append(max(c,c2))

        s+=1

        if ((s-1)%2==0):
            n+=2

    df=pd.DataFrame({'database': list_of_words(f"{database}", len(subject)),'subject':subject, 'startime':startime, 
    'endtime':endtime,'label':label,'duration':duration})
    df['diff_time']=df['endtime']-df['startime']
    df.columns=['database','subject','startime','endtime','label','duration','diff_time']
    df=df.reindex(columns=['startime','endtime','label', 'subject','diff_time', 'duration','database' ])

    lst=df_to_list(df)
    col=['startime','endtime','label', 'subject','diff_time', 'duration','database' ]
    return lst,col

def get_laughs_dict_conv_folder(filespaths,database):
    """
    Give the dataframe of laughs from a folder.
    Args : 
        filespaths (list) -> Cointain the filespath of the folder
        database (str) -> ccdb, ifadv or ndc
    Return a list of tuple and the list L =['startime','endtime','label', 'subject','diff_time', 'duration','database'] 
    """
    startime, endtime, label, subject,duration = ([] for _ in range(5))
    s=1
    n=0
    for _ in range (len(filespaths)):
        #print("file ",_,"duration n°",n)
        lst_ = get_Ldict(filespaths[_])
        eaf = pympi.Elan.Eaf(filespaths[n])
        eaf2= pympi.Elan.Eaf(filespaths[n+1])
        c=check_duration(eaf)
        c2= check_duration(eaf2)
        for i in range(len(lst_)):
            subject.append(s)
            startime.append(lst_[i][0])
            endtime.append(lst_[i][1])
            label.append(lst_[i][2])
            duration.append(max(c,c2))

        s+=1
        if ((s-1)%2==0):
            n+=2

    df=pd.DataFrame({'database': list_of_words(f"{database}", len(subject)),'subject':subject, 'startime':startime, 
    'endtime':endtime,'label':label,'duration':duration})
    df['diff_time']=df['endtime']-df['startime']
   
    df.columns=['database','subject','startime','endtime','label','duration','diff_time']
    df=df.reindex(columns=['startime','endtime','label', 'subject','diff_time', 'duration','database' ])

    lst=df_to_list(df)
    col=['startime','endtime','label', 'subject','diff_time', 'duration','database' ]
    return lst,col

#By file
#Here, the get_overlapping_seg function (defined in interaction_analysis.py) makes directly intersection between the segments.
def get_smiles_from_spk(root):
    """
    Give a list of smiles when the subject is a speaker.
    Args :
        root (str) -> file path
    Return :
        A list of tuple and the list L =  startime, endtime, label, duration, diff_time, subject
    """
    """
    Process: 
    We want the overlap of speaker's segments and smiles segments
    """
    spk_lst = get_IR_list(root,"Role","spk")
    smiles_lst = get_Sdict(root)
    startime, endtime, label,duration, diff_time, subject= ([] for _ in range(6))
   
    b=get_overlapping_seg(spk_lst, smiles_lst)
    sub=1
    eaf = pympi.Elan.Eaf(root)
    c=check_duration(eaf)

    for _ in range(0,len(b),1):     
        startime.append(b[_][0])
        endtime.append(b[_][1])
        diff_time.append(b[_][1] - b[_][0])
        label.append(b[_][2])
        duration.append(c)
        subject.append(sub)
        sub+=1

    # lst=df_to_list(df)
    lst=[(i,j,k,l,m,n) for i,j,k,l,m,n in zip(startime,endtime, label,duration, diff_time, subject)]
    col=['startime', 'endtime', 'label','duration','diff_time','subject']

    return lst,col

def get_smiles_from_lsn(root):
    """
    Give a list of smiles when the subject is a listener
    Args :
        root (str) -> file path
    Return :
        A list of tuple and the list L =  startime, endtime, label, duration, diff_time, subject
    """
    lsn_lst = get_IR_list(root,"Role","lsn")
    lst = get_Sdict(root)
    startime, endtime, label,duration, diff_time, subject= ([] for _ in range(6))
    
    b=get_overlapping_seg(lsn_lst, lst)
    sub=1
    eaf = pympi.Elan.Eaf(root)
    c=check_duration(eaf)

    for _ in range(0,len(b),1):     
        startime.append(b[_][0])
        endtime.append(b[_][1])
        diff_time.append(b[_][1] - b[_][0])
        label.append(b[_][2])
        duration.append(c)
        subject.append(sub)
        sub+=1

    # lst=df_to_list(df)
    lst=[(i,j,k,l,m,n) for i,j,k,l,m,n in zip(startime,endtime, label,duration, diff_time, subject)]
    col=['startime', 'endtime', 'label','duration','diff_time','subject']

    return lst,col

def get_laughs_from_spk(root):
    """
    Give a list of laughs when the subject is a speaker
    Args :
        root (str) -> file path
    Return :
        A list of tuple and the list L =  startime, endtime, label, duration, diff_time, subject
    """
    spk_lst = get_IR_list(root,"Role","spk")
    lst = get_Ldict(root)
    startime, endtime, label,duration, diff_time, subject= ([] for _ in range(6))
    
    b=get_overlapping_seg(spk_lst, lst)
    eaf = pympi.Elan.Eaf(root)
    c=check_duration(eaf)
    sub=1
    for _ in range(0,len(b),1):     
        startime.append(b[_][0])
        endtime.append(b[_][1])
        diff_time.append(b[_][1] - b[_][0])
        label.append(b[_][2])
        duration.append(c)
        subject.append(sub)
        sub+=1
    
    # lst=df_to_list(df)
    lst=[(i,j,k,l,m,n) for i,j,k,l,m,n in zip(startime,endtime, label,duration, diff_time, subject)]
    col=['startime', 'endtime', 'label','duration','diff_time','subject']
    return lst,col

def get_laughs_from_lsn(root):
    """
    Give a list of laughs when the subject is a listener
    Args :
        root (str) -> file path
    Return :
        A list of tuple and the list L =  startime, endtime, label, duration, diff_time, subject
    """
    lsn_lst = get_IR_list(root,"Role","lsn")
    lst = get_Ldict(root)

    startime, endtime, label,duration, diff_time, subject= ([] for _ in range(6))
   
    b=get_overlapping_seg(lsn_lst, lst)
    eaf = pympi.Elan.Eaf(root)
    c=check_duration(eaf)
    sub=1
    for _ in range(0,len(b),1):     
        startime.append(b[_][0])
        endtime.append(b[_][1])
        diff_time.append(b[_][1] - b[_][0])
        label.append(b[_][2])
        duration.append(c)
        subject.append(sub)
        sub+=1

    # lst=df_to_list(df)
    lst=[(i,j,k,l,m,n) for i,j,k,l,m,n in zip(startime,endtime, label,duration, diff_time, subject)]
    col=['startime', 'endtime', 'label','duration','diff_time','subject']
    return lst,col

#Here, the get_overlapping_segments function (defined in interaction_analysis.py) doesn't make directly intersection between the segments.
def get_smiles_from_spk2(root):
    """
    Give a list of smiles when the subject is a speaker.
    Args :
        root (str) -> file path
    Return :
        A list of tuple and the list L =  'startime', 'endtime', 'label','duration'
    """
    """
    Process: 
    We want the overlap of speaker's segments and smiles segments
    """
    spk_lst = get_IR_list(root,"Role","spk")
    smiles_lst = get_Sdict(root)
    startime, endtime, label, nsmile, role_ind , duration= ([] for _ in range(6))

    b=list(get_overlapping_segments(spk_lst, smiles_lst).values())
    b=list(itertools.chain(*b))
    
    eaf = pympi.Elan.Eaf(root)
    c=check_duration(eaf)

    for _ in range(0,len(b),1):     
        startime.append(b[_][0])
        endtime.append(b[_][1])
        label.append(b[_][2])
        duration.append(c)

    # lst=df_to_list(df)
    lst=[(i,j,k,l) for i,j,k,l in zip(startime,endtime, label,duration)]
    col=['startime', 'endtime', 'label','duration']


    return lst,col

def get_smiles_from_lsn2(root):
    """
    Give a list of smiles when the subject is a listener
    Args :
        root (str) -> file path
    Return :
        A list of tuple and the list L =  'startime', 'endtime', 'label','duration'
    """
    lsn_lst = get_IR_list(root,"Role","lsn")
    lst = get_Sdict(root)
    startime, endtime, label, duration = ([] for _ in range(4))
    
    b=list(get_overlapping_segments(lsn_lst, lst).values())
    b=list(itertools.chain(*b))

    eaf = pympi.Elan.Eaf(root)
    c=check_duration(eaf)

    for _ in range(0,len(b),1):     
        startime.append(b[_][0])
        endtime.append(b[_][1])
        label.append(b[_][2])
        duration.append(c)

    # lst=df_to_list(df)
    lst=[(i,j,k,l) for i,j,k,l in zip(startime,endtime, label,duration)]
    col=['startime', 'endtime', 'label','duration']


    return lst,col

def get_laughs_from_spk2(root):
    """
    Give a list of laughs when the subject is a speaker
    Args :
        root (str) -> file path
    Return :
        A list of tuple and the list L =  'startime', 'endtime', 'label','duration'
    """
    spk_lst = get_IR_list(root,"Role","spk")
    lst = get_Ldict(root)

    startime, endtime, label, duration = ([] for _ in range(4))
    
    b=list(get_overlapping_segments(spk_lst, lst).values())
    b=list(itertools.chain(*b))
    
    eaf = pympi.Elan.Eaf(root)
    c=check_duration(eaf)

    for _ in range(0,len(b),1):     
        startime.append(b[_][0])
        endtime.append(b[_][1])
        label.append(b[_][2])
        duration.append(c)

    # lst=df_to_list(df)
    lst=[(i,j,k,l) for i,j,k,l in zip(startime,endtime, label,duration)]
    col=['startime', 'endtime', 'label','duration']

    return lst,col

def get_laughs_from_lsn2(root):
    """
    Give a list of laughs when the subject is a listener
    Args :
        root (str) -> file path
    Return :
        A list of tuple and the list L =  'startime', 'endtime', 'label','duration'
    """
    lsn_lst = get_IR_list(root,"Role","lsn")
    lst = get_Ldict(root)

    startime, endtime, label,duration = ([] for _ in range(4))
   
    b=list(get_overlapping_segments(lsn_lst, lst).values())
    b=list(itertools.chain(*b))
 
    
    eaf = pympi.Elan.Eaf(root)
    c=check_duration(eaf)
    for _ in range(0,len(b),1):     
        startime.append(b[_][0])
        endtime.append(b[_][1])
        label.append(b[_][2])
        duration.append(c)

    # lst=df_to_list(df)
    lst=[(i,j,k,l) for i,j,k,l in zip(startime,endtime, label,duration)]
    col=['startime', 'endtime', 'label','duration']

    return lst,col

def get_tier_from_lsn2(root, tier):
    """
    Retrieve a specified tier from an LSN file when the subject is a listener.
    
    Args:
        root (str): File path.
        tier (str): Name of the tier to retrieve.
        
    Returns:
        tuple: A list of tuples representing the specified tier and the list of column names.
    """
    lsn_lst = get_IR_list(root, "Role", "lsn")
    lst = get_tier_dict(root, tier)
    startime, endtime, label, duration = ([] for _ in range(4))
   
    b = list(get_overlapping_segments(lsn_lst, lst).values())
    b = list(itertools.chain(*b))
    
    eaf = pympi.Elan.Eaf(root)
    duration = check_duration(eaf)
    
    for item in b:     
        startime.append(item[0])
        endtime.append(item[1])
        label.append(item[2])
    
    lst = [(i, j, k, duration) for i, j, k in zip(startime, endtime, label)]
    columns = ['startime', 'endtime', 'label', 'duration']

    return lst, columns

def get_tier_from_spk2(root, tier):
    """
    Retrieve a specified tier from an SPK file when the subject is a speaker.
    
    Args:
        root (str): File path.
        tier (str): Name of the tier to retrieve.
        
    Returns:
        tuple: A list of tuples representing the specified tier and the list of column names.
    """
    spk_lst = get_IR_list(root, "Role", "spk")
    lst = get_tier_dict(root, tier)
    startime, endtime, label, duration = ([] for _ in range(4))
   
    b = list(get_overlapping_segments(spk_lst, lst).values())
    b = list(itertools.chain(*b))
    
    eaf = pympi.Elan.Eaf(root)
    duration = check_duration(eaf)
    
    for item in b:     
        startime.append(item[0])
        endtime.append(item[1])
        label.append(item[2])
    
    lst = [(i, j, k, duration) for i, j, k in zip(startime, endtime, label)]
    columns = ['startime', 'endtime', 'label', 'duration']

    return lst, columns

#By folder
def get_smiles_from_spk_folder(listpaths,string):
    """
    Same as get_smiles_from_spk but from a folder
    Args : listpaths (list) -> list of folder's filespath 
    Return :
        A list of tuple and the list L =  'subject','diff_time','label','duration','database'
    """
    L=[]
    subject=[]
    i=1
    for _ in listpaths:
        df0=list_to_df(get_smiles_from_spk2(_)[0], get_smiles_from_spk2(_)[1])
        #df0.drop(df0.columns[[4,5]], axis=1, inplace=True)
        subject.append(list_of_words(i,len(df0['startime'])))
        L.append(df0)
        i+=1
    S=[]
    for _ in subject:
        S=S+_
    df=pd.concat([L[_] for _ in range (len(L))])
    df['subject']=S
    df['database']=list_of_words(string, len(df['subject']))

    df['diff_time']=df['endtime']-df['startime']

    df.drop(df.columns[[0,1]], axis=1, inplace=True)
    df=df.reindex(columns=['subject','diff_time','label','duration','database'])
    lst=df_to_list(df)
    columns=['subject','diff_time','label','duration','database']
    return lst,columns

def get_smiles_from_lsn_folder(listpaths, string):
    """
    Same as get_smiles_from_spk but from a folder
    Args : listpaths (list) -> list of folder's filespath 
    Return :
        A list of tuple and the list L =  'subject','diff_time','label','duration','database'
    """

    L=[]
    subject=[]
    
    i=1
    for _ in listpaths:
        df0=list_to_df(get_smiles_from_lsn2(_)[0], get_smiles_from_lsn2(_)[1])
        #df0.drop(df0.columns[[4,5]], axis=1, inplace=True)
        subject.append(list_of_words(i,len(df0['startime'])))
        L.append(df0)
        i+=1
    S=[]
    for _ in subject:
        S=S+_
    df=pd.concat([L[_] for _ in range (len(L))])
    df['subject']=S
    df['database']=list_of_words(string, len(df['subject']))
    df['diff_time']=df['endtime']-df['startime']

    df.drop(df.columns[[0,1]], axis=1, inplace=True)
    df=df.reindex(columns=['subject','diff_time','label','duration','database'])
    lst=df_to_list(df)
    columns=['subject','diff_time','label','duration','database']
    return lst,columns

def get_laughs_from_spk_folder(listpaths,string):
    """
    Same as get_smiles_from_spk but from a folder
    Args : listpaths (list) -> list of folder's filespath 
    Return :
        A list of tuple and the list L =  'subject','diff_time','label','duration','database'
    """
    L=[]
    subject=[]
    
    i=1
    for _ in listpaths:
        df0=list_to_df(get_laughs_from_spk2(_)[0], get_laughs_from_spk2(_)[1])
        #df0.drop(df0.columns[[4,5]], axis=1, inplace=True)
        subject.append(list_of_words(i,len(df0['startime'])))
        L.append(df0)
        i+=1
    S=[]
    for _ in subject:
        S=S+_
    df=pd.concat([L[_] for _ in range (len(L))])
    df['subject']=S
    df['database']=list_of_words(string, len(df['subject']))
    df['diff_time']=df['endtime']-df['startime']

    df.drop(df.columns[[0,1]], axis=1, inplace=True)
    df=df.reindex(columns=['subject','diff_time','label','duration','database'])
    lst=df_to_list(df)
    columns=['subject','diff_time','label','duration','database']
    return lst,columns

def get_laughs_from_lsn_folder(listpaths, string):
    """
    Same as get_smiles_from_spk but from a folder
    Args : listpaths (list) -> list of folder's filespath 
    Return :
        A list of tuple and the list L =  'subject','diff_time','label','duration','database'
    """
    L=[]
    subject=[]
    i=1
    for _ in listpaths:
        df0=list_to_df(get_laughs_from_lsn2(_)[0], get_laughs_from_lsn2(_)[1])
        #df0.drop(df0.columns[[4,5]], axis=1, inplace=True)
        subject.append(list_of_words(i,len(df0['startime'])))
        L.append(df0)
        i+=1
    S=[]
    for _ in subject:
        S=S+_
    df=pd.concat([L[_] for _ in range (len(L))])
    df['subject']=S
    df['database']=list_of_words(string, len(df['subject']))
    df['diff_time']=df['endtime']-df['startime']

    df.drop(df.columns[[0,1]], axis=1, inplace=True)
    df=df.reindex(columns=['subject','diff_time','label','duration','database'])
    lst=df_to_list(df)
    columns=['subject','diff_time','label','duration','database']
    return lst,columns

def get_tier_from_spk_folder(listpaths, string, tier):
    """
    Retrieve specified tiers from SPK files in a folder.
    
    Args:
        listpaths (list): List of folder file paths.
        string (str): String to be used as the 'database' value.
        tier (str): Name of the tier to retrieve.
        
    Returns:
        tuple: A list of tuples representing the specified tier and the list of column names.
    """
    L = []
    subject = []
    i = 1
    for path in listpaths:
        df0 = list_to_df(get_tier_from_spk2(path, tier)[0], get_tier_from_spk2(path, tier)[1])
        subject.append(list_of_words(i, len(df0['startime'])))
        L.append(df0)
        i += 1
    S = []
    for _ in subject:
        S=S+_
    df=pd.concat([L[_] for _ in range (len(L))])
    df['subject'] = S
    df['database'] = list_of_words(string, len(df['subject']))
    df['diff_time'] = df['endtime'] - df['startime']
    
    df.drop(df.columns[[0, 1]], axis=1, inplace=True)
    df = df.reindex(columns=['subject', 'diff_time', 'label', 'duration', 'database'])
    lst = df_to_list(df)
    columns = ['subject', 'diff_time', 'label', 'duration', 'database']
    return lst, columns

def get_tier_from_lsn_folder(listpaths, string, tier):
    """
    Retrieve specified tiers from LSN files in a folder.
    
    Args:
        listpaths (list): List of folder file paths.
        string (str): String to be used as the 'database' value.
        tier (str): Name of the tier to retrieve.
        
    Returns:
        tuple: A list of tuples representing the specified tier and the list of column names.
    """
    L = []
    subject = []
    i = 1
    for path in listpaths:
        df0 = list_to_df(get_tier_from_lsn2(path, tier)[0], get_tier_from_lsn2(path, tier)[1])
        subject.append(list_of_words(i, len(df0['startime'])))
        L.append(df0)
        i += 1
    S=[]
    for _ in subject:
        S=S+_
    df=pd.concat([L[_] for _ in range (len(L))])
    df['subject'] = S
    df['database'] = list_of_words(string, len(df['subject']))
    df['diff_time'] = df['endtime'] - df['startime']
    
    df.drop(df.columns[[0, 1]], axis=1, inplace=True)
    df = df.reindex(columns=['subject', 'diff_time', 'label', 'duration', 'database'])
    lst = df_to_list(df)
    columns = ['subject', 'diff_time', 'label', 'duration', 'database']
    
    return lst, columns

#Roles versus 
def get_smiles_from_spk_vs_lsn_folder(listpaths,string):
    """This function gives the list of smiles when a speaker is in front of a listener.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database

    Returns:
        list of tuple and a description of what is inside the tuple : (list of tuple, ['conv','role','label','subject','diff_time','duration','database'])
    """
    df=list_to_df(get_smiles_from_spk_folder(listpaths,string)[0], get_smiles_from_spk_folder(listpaths,string)[1])
    #df.drop(df.columns[[0,1]], axis = 1, inplace = True)     
    df['role']=list_of_words('spk',len(df['label'])) 
    #print(list(np.unique((df.subject))))

    dg=list_to_df(get_smiles_from_lsn_folder(listpaths,string)[0], get_smiles_from_lsn_folder(listpaths,string)[1])
    #dg.drop(dg.columns[[0,1]], axis = 1, inplace = True)     
    dg['role']=list_of_words('lsn',len(dg['label'])) 
    #print(list(np.unique((dg.subject))))

    #Some corrections
    df=df.loc[:,['subject', 'database','label','duration','diff_time','role']]
    dict_=list(df.to_records(index=False))
    dg=dg.loc[:,['subject', 'database','label','duration','diff_time','role']]
    dict_2=list(dg.to_records(index=False))

    df=correct_dict_role_smiles(dict_,listpaths,string)
    dg=correct_dict_role_smiles(dict_2,listpaths,string)
    
    df=pd.DataFrame.from_records(df, columns=['subject', 'database','label','duration','diff_time','role'])
    dg=pd.DataFrame.from_records(dg, columns=['subject', 'database','label','duration','diff_time','role'])
    
    L1=[]
    L2=[]
    subj = list(np.unique((df.subject)))
    for i in subj:
        if i%2!=0 :     #if the number of the subject is unpair
            L1.append(df[df.subject.eq(i)])
        else:
            L2.append(dg[dg.subject.eq(i)])
    
    df=pd.concat(L1)
    dg=pd.concat(L2)
    
    #Put together these dataframes ordered by subject
    db=pd.concat([df,dg])
    db=pd.DataFrame(db.loc[:,['label','duration','diff_time','subject','database','role']]).reset_index()
    db=db.drop(['index'],axis=1)
    db=db.sort_values(['subject'], ascending=[True])
    
    c=1
    conv=[]
    for i in range (1, len(db.duration),2):
        values=[i,i+1]
        dgg= db[db.subject.isin(values)]
        conv+=list_of_words(c, len(dgg.subject))
        c+=1
    db['conv']=conv

    #If subject change, take duration
    duration=[]
    for _ in list(np.unique((db.subject))) :
        duration+=(list(np.unique(db.loc[db.subject.eq(_),'duration'])))
    #duration=list(np.unique((db.duration)))
    #print(duration)

    if 0 not in duration : pass
    else : duration.remove(0)
    #print(duration, len(duration))
    
    conv=list(np.unique((db.conv)))
    d=[]
    for _ in range(0,len(duration),2):
        d.append((duration[_], duration[_+1]))

    d=list(reversed(d))
    for i,j in zip (conv,d):
        db.loc[db.conv.eq(i),'duration']=max(j)
    
    db=db.reindex(columns=['conv','role','label','subject','diff_time','duration','database'])
    lst=df_to_list(db)
    col=['conv','role','label','subject','diff_time','duration','database']

    return lst,col

def get_smiles_from_lsn_vs_spk_folder(listpaths,string):
    """This function gives the list of smiles when a listener is in front of a speaker.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database

    Returns:
        list of tuple and a description of what is inside the tuple : (list of tuple, ['conv','role','label','subject','diff_time','duration','database'])
    """
    df=list_to_df(get_smiles_from_lsn_folder(listpaths,string)[0], get_smiles_from_lsn_folder(listpaths,string)[1])
    #df.drop(df.columns[[0,1]], axis = 1, inplace = True) 
    df['role']=list_of_words('lsn',len(df['subject'])) 
    df=pd.DataFrame(df).reset_index()
    df.drop(df.columns[[0]], axis = 1, inplace = True) 
    #print(list(np.unique((df.subject))))

    dg=list_to_df(get_smiles_from_spk_folder(listpaths,string)[0], get_smiles_from_spk_folder(listpaths,string)[1])
    #dg.drop(dg.columns[[0,1]], axis = 1, inplace = True)     
    dg['role']=list_of_words('spk',len(dg['subject'])) 
    dg=pd.DataFrame(dg).reset_index()
    dg.drop(dg.columns[[0]], axis = 1, inplace = True) 
    #print(list(np.unique((dg.subject))))

    #Some corrections
    df=df.loc[:,['subject', 'database','label','duration','diff_time','role']]
    dict_=list(df.to_records(index=False))
    dg=dg.loc[:,['subject', 'database','label','duration','diff_time','role']]
    dict_2=list(dg.to_records(index=False))

    df=correct_dict_role_smiles(dict_,listpaths,string)
    dg=correct_dict_role_smiles(dict_2,listpaths,string)
    
    df=pd.DataFrame.from_records(df, columns=['subject', 'database','label','duration','diff_time','role'])
    dg=pd.DataFrame.from_records(dg, columns=['subject', 'database','label','duration','diff_time','role'])
    
    L1=[]
    L2=[]
    subj = list(np.unique((df.subject)))
    for i in subj:
        if i%2!=0 :     #if the number of the subject is unpair
            L1.append(df[df.subject.eq(i)])
        else:
            L2.append(dg[dg.subject.eq(i)])
    
    df=pd.concat(L1)
    dg=pd.concat(L2)
    
    #Put together these dataframes ordered by subject
    db=pd.concat([df,dg])
    db=pd.DataFrame(db.loc[:,['label','duration','diff_time','subject','database','role']]).reset_index()
    db=db.drop(['index'],axis=1)
    db=db.sort_values(['subject'], ascending=[True])
    

    c=1
    conv=[]
    for i in range (1, len(db.duration),2):
        values=[i,i+1]
        dgg= db[db.subject.isin(values)]
        conv+=list_of_words(c, len(dgg.subject))
        c+=1
    db['conv']=conv

    #If subject change, take duration
    duration=[]
    for _ in list(np.unique((db.subject))) :
        duration+=(list(np.unique(db.loc[db.subject.eq(_),'duration'])))
    #duration=list(np.unique((db.duration)))
    #print(duration)

    if 0 not in duration : pass
    else : duration.remove(0)
    #print(duration, len(duration))
    
    conv=list(np.unique((db.conv)))
    d=[]
    for _ in range(0,len(duration),2):
        d.append((duration[_], duration[_+1]))

    d=list(reversed(d))
    for i,j in zip (conv,d):
        db.loc[db.conv.eq(i),'duration']=max(j)
    db=db.reindex(columns=['conv','role','label','subject','diff_time','duration','database'])
    lst=df_to_list(db)
    col=['conv','role','label','subject','diff_time','duration','database']

    return lst,col

def get_laughs_from_spk_vs_lsn_folder(listpaths,string):
    """This function gives the list of laughs when a speaker is in front of a listener.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database

    Returns:
        list of tuple and a description of what is inside the tuple : (list of tuple, ['conv','role','label','subject','diff_time','duration','database'])
    """
    df=list_to_df(get_laughs_from_spk_folder(listpaths,string)[0], get_laughs_from_spk_folder(listpaths,string)[1])
    #df.drop(df.columns[[0,1]], axis = 1, inplace = True)     
    df['role']=list_of_words('spk',len(df['label'])) 
    df=pd.DataFrame(df).reset_index()
    df.drop(df.columns[[0]], axis = 1, inplace = True) 

    dg=list_to_df(get_laughs_from_lsn_folder(listpaths,string)[0], get_laughs_from_lsn_folder(listpaths,string)[1])
    #dg.drop(dg.columns[[0,1]], axis = 1, inplace = True)     
    dg['role']=list_of_words('lsn',len(dg['label'])) 
    dg=pd.DataFrame(dg).reset_index()
    dg.drop(dg.columns[[0]], axis = 1, inplace = True) 

    #Some corrections
    df=df.loc[:,['subject', 'database','label','duration','diff_time','role']]
    dict_=list(df.to_records(index=False))
    dg=dg.loc[:,['subject', 'database','label','duration','diff_time','role']]
    dict_2=list(dg.to_records(index=False))

    df=correct_dict_role_smiles(dict_,listpaths,string)
    dg=correct_dict_role_smiles(dict_2,listpaths,string)
    
    df=pd.DataFrame.from_records(df, columns=['subject', 'database','label','duration','diff_time','role'])
    dg=pd.DataFrame.from_records(dg, columns=['subject', 'database','label','duration','diff_time','role'])
    
    L1=[]
    L2=[]
    subj = list(np.unique((df.subject)))
    for i in subj:
        if i%2!=0 :     #if the number of the subject is unpair
            L1.append(df[df.subject.eq(i)])
        else:
            L2.append(dg[dg.subject.eq(i)])
    
    df=pd.concat(L1)
    dg=pd.concat(L2)
    
    #Put together these dataframes ordered by subject
    db=pd.concat([df,dg])
    db=pd.DataFrame(db.loc[:,['label','duration','diff_time','subject','database','role']]).reset_index()
    db=db.drop(['index'],axis=1)
    db=db.sort_values(['subject'], ascending=[True])

    c=1
    conv=[]
    for i in range (1, len(db.duration),2):
        values=[i,i+1]
        dgg= db[db.subject.isin(values)]
        conv+=list_of_words(c, len(dgg.subject))
        c+=1
    db['conv']=conv

    #If subject change, take duration
    duration=[]
    for _ in list(np.unique((db.subject))) :
        duration+=(list(np.unique(db.loc[db.subject.eq(_),'duration'])))
    #duration=list(np.unique((db.duration)))
    #print(duration)

    if 0 not in duration : pass
    else : duration.remove(0)
    #print(duration, len(duration))
    
    conv=list(np.unique((db.conv)))
    d=[]
    for _ in range(0,len(duration),2):
        if (_+1) < len(duration) : 
            d.append((duration[_], duration[_+1]))

    d=list(reversed(d))
    for i,j in zip (conv,d):
        db.loc[db.conv.eq(i),'duration']=max(j)
    db=db.reindex(columns=['conv','role','label','subject','diff_time','duration','database'])
    lst=df_to_list(db)
    col=['conv','role','label','subject','diff_time','duration','database']

    return lst,col

def get_laughs_from_lsn_vs_spk_folder(listpaths,string):
    """This function gives the list of laughs when a listener is in front of a speaker.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database

    Returns:
        list of tuple and a description of what is inside the tuple : (list of tuple, ['conv','role','label','subject','diff_time','duration','database'])
    """
    df=list_to_df(get_laughs_from_lsn_folder(listpaths,string)[0], get_laughs_from_lsn_folder(listpaths,string)[1])
    #df.drop(df.columns[[0,1]], axis = 1, inplace = True)     
    df['role']=list_of_words('lsn',len(df['label'])) 
    
    dg=list_to_df(get_laughs_from_spk_folder(listpaths,string)[0], get_laughs_from_spk_folder(listpaths,string)[1])
    #dg.drop(dg.columns[[0,1]], axis = 1, inplace = True)     
    dg['role']=list_of_words('spk',len(dg['label'])) 

    #Some corrections
    df=df.loc[:,['subject', 'database','label','duration','diff_time','role']]
    dict_=list(df.to_records(index=False))
    dg=dg.loc[:,['subject', 'database','label','duration','diff_time','role']]
    dict_2=list(dg.to_records(index=False))

    df=correct_dict_role_smiles(dict_,listpaths,string)
    dg=correct_dict_role_smiles(dict_2,listpaths,string)
    
    df=pd.DataFrame.from_records(df, columns=['subject', 'database','label','duration','diff_time','role'])
    dg=pd.DataFrame.from_records(dg, columns=['subject', 'database','label','duration','diff_time','role'])
    
    L1=[]
    L2=[]
    subj = list(np.unique((df.subject)))
    for i in subj:
        if i%2!=0 :     #if the number of the subject is unpair
            L1.append(df[df.subject.eq(i)])
        else:
            L2.append(dg[dg.subject.eq(i)])
    
    df=pd.concat(L1)
    dg=pd.concat(L2)
    
    #Put together these dataframes ordered by subject
    db=pd.concat([df,dg])
    db=pd.DataFrame(db.loc[:,['label','duration','diff_time','subject','database','role']]).reset_index()
    db=db.drop(['index'],axis=1)
    db=db.sort_values(['subject'], ascending=[True])
    

    c=1
    conv=[]
    for i in range (1, len(db.duration),2):
        values=[i,i+1]
        dgg= db[db.subject.isin(values)]
        conv+=list_of_words(c, len(dgg.subject))
        c+=1
    db['conv']=conv

    #If subject change, take duration
    duration=[]
    for _ in list(np.unique((db.subject))) :
        duration+=(list(np.unique(db.loc[db.subject.eq(_),'duration'])))
    #duration=list(np.unique((db.duration)))
    #print(duration)

    if 0 not in duration : pass
    else : duration.remove(0)
    #print(duration, len(duration))
    
    conv=list(np.unique((db.conv)))
    d=[]
    for _ in range(0,len(duration),2):
        if (_+1) < len(duration) : 
            d.append((duration[_], duration[_+1]))

    d=list(reversed(d))
    for i,j in zip (conv,d):
        db.loc[db.conv.eq(i),'duration']=max(j)
    db=db.reindex(columns=['conv','role','label','subject','diff_time','duration','database'])
    lst=df_to_list(db)
    col=['conv','role','label','subject','diff_time','duration','database']

    return lst,col

#Mean, Std, median from all datasets
def get_rd_stats(df):
    """This function calculate the mean, median and standard deviation of the relative duration of three lists of tuple.
    Args:
        df1, df2 and df3 (list): They are lists of tuple

    Returns:
        list of tuple and a description of what is inside the tuple : (list of tuple, ['database','label','mean_p','median_p','std_p','min_p','max_p']))
    """

    dg1=df.loc[:,['subject','database','label','duration','diff_time']]
    dg1=dg1.groupby(['subject','database','label','duration']).sum().reset_index()
    dg1['percentage']=(dg1['diff_time']/dg1['duration'])*100
    # dg1.columns=['subject','database','label','duration','sum_time','percentage']
    dg1 = dg1.drop(['subject', 'duration', 'diff_time'], axis=1)

    dg=dg1.loc[:,['database','label','percentage']]
    df_mean=dg1.loc[:,['database','label','percentage']]
    df_mean=df_mean.groupby(['database','label']).mean().reset_index()
    
    df_median=dg1.loc[:,['database','label','percentage']]
    df_median=df_median.groupby(['database','label']).median().reset_index()
    
    df_std=dg1.loc[:,['database','label','percentage']]
    df_std=df_std.groupby(['database','label']).std().reset_index()
    
    df_min = dg1.loc[:, ['database', 'label', 'percentage']]
    df_min = df_min.groupby(['database', 'label']).min().reset_index()

    df_max = dg1.loc[:, ['database', 'label', 'percentage']]
    df_max = df_max.groupby(['database', 'label']).max().reset_index()

    df_mean.columns=['database','label','mean_p']
    df_median.columns = ['database', 'label', 'median_p']
    df_std.columns = ['database', 'label', 'std_p']
    df_min.columns = ['database', 'label', 'min_p']
    df_max.columns = ['database', 'label', 'max_p']

    dg = df_mean.merge(df_median, on=['database', 'label'])
    dg = dg.merge(df_std, on=['database', 'label'])
    dg = dg.merge(df_min, on=['database', 'label'])
    dg = dg.merge(df_max, on=['database', 'label'])
    
    lst=df_to_list(dg)
    col = ['database', 'label', 'mean_p', 'median_p', 'std_p', 'min_p', 'max_p']
    return lst,col

def get_rd_stats_byrole(df):
    """This function calculate the mean, median and standard deviation of the relative duration of three lists of tuple filtered by role.
    Args:
        df1, df2 and df3 (list): They are lists of tuple

    Returns:
        list of tuple and a description of what is inside the tuple : (list of tuple, ['database','label','mean_p','median_p','std_p','min_p','max_p'])
    """
    dg1=df.loc[:,['subject','database','label','duration','diff_time']]
    dg1=dg1.groupby(['subject','database','label','duration']).sum().reset_index()
    dg1['percentage']=(dg1['diff_time']/dg1['duration'])*100
    # dg1.columns=['subject','database','label','duration','sum_time','percentage']
    dg1 = dg1.drop(['subject', 'duration', 'diff_time'], axis=1)

    dg=dg1.loc[:,['database','label','percentage']]
    df_mean=dg1.loc[:,['database','label','percentage']]
    df_mean=df_mean.groupby(['database','label']).mean().reset_index()
    
    df_median=dg1.loc[:,['database','label','percentage']]
    df_median=df_median.groupby(['database','label']).median().reset_index()
    
    df_std=dg1.loc[:,['database','label','percentage']]
    df_std=df_std.groupby(['database','label']).std().reset_index()
    
    df_min = dg1.loc[:, ['database', 'label', 'percentage']]
    df_min = df_min.groupby(['database', 'label']).min().reset_index()

    df_max = dg1.loc[:, ['database', 'label', 'percentage']]
    df_max = df_max.groupby(['database', 'label']).max().reset_index()

    df_mean.columns=['database','label','mean_p']
    df_median.columns = ['database', 'label', 'median_p']
    df_std.columns = ['database', 'label', 'std_p']
    df_min.columns = ['database', 'label', 'min_p']
    df_max.columns = ['database', 'label', 'max_p']

    dg = df_mean.merge(df_median, on=['database', 'label'])
    dg = dg.merge(df_std, on=['database', 'label'])
    dg = dg.merge(df_min, on=['database', 'label'])
    dg = dg.merge(df_max, on=['database', 'label'])
    
    lst=df_to_list(dg)
    col = ['database', 'label', 'mean_p', 'median_p', 'std_p', 'min_p', 'max_p']
    return lst,col

#Intra
def get_intra_smiles_absolute_duration_folder(listpaths,string):
    """This function calculates absolute duration for smiles in a database considering one person.
    Args:
        listpaths (list): list of filespath
        string (str): name of the database
    Returns:
        Tuple: (list of tuple , description of tuples) -> ([], ['subject','database','label','sum_time','time'])
    """
    df1=list_to_df(get_smiles_dict_folder(listpaths,string)[0], get_smiles_dict_folder(listpaths,string)[1])

    dg1=df1.loc[:,['subject','database','label','diff_time']]
    dg1=dg1.groupby(['subject','database','label']).sum().reset_index()
    dg1['time']=seconds_to_hmsms_list(dg1['diff_time'])
    dg1.columns=['subject','database','label','sum_time','time']

    lst=df_to_list(dg1)
    col=['subject','database','label','sum_time','time']

    return lst,col

def get_intra_laughs_absolute_duration_folder(listpaths,string):
    """This function calculates absolute duration for laughs in a database considering one person.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database
    Returns:
        Tuple: (list of tuple , description of tuples) -> ([], ['subject','database','label','sum_time','time'])
    """
    df2=list_to_df(get_laughs_dict_folder(listpaths,string)[0], get_laughs_dict_folder(listpaths,string)[1])

    dg2=df2.loc[:,['subject','database','label','diff_time']]
    dg2=dg2.groupby(['subject','database','label']).sum().reset_index()
    dg2['time']=seconds_to_hmsms_list(dg2['diff_time'])
    dg2.columns=['subject','database','label','sum_time','time']
    lst=df_to_list(dg2)
    col=['subject','database','label','sum_time','time']

    return lst,col

def get_intra_smiles_relative_duration_folder(listpaths,string):
    """This function calculates relative duration for smiles in a database considering one person.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database
    Returns:
        Tuple: (list of tuple , description of tuples) -> ([], ['subject','database','label','duration','sum_time','percentage'])
    """
    df1=list_to_df(get_smiles_dict_folder(listpaths,string)[0], get_smiles_dict_folder(listpaths,string)[1])

    dg1=df1.loc[:,['subject','database','label','duration','diff_time']]
    dg1=dg1.groupby(['subject','database','label','duration']).sum().reset_index()
    dg1['percentage']=round(((dg1['diff_time']/dg1['duration'])*100),2)
    dg1.columns=['subject','database','label','duration','sum_time','percentage']
    lst=df_to_list(dg1)
    col=['subject','database','label','duration','sum_time','percentage']

    return lst,col

def get_intra_laughs_relative_duration_folder(listpaths,string):
    """This function calculates relative duration for laughs in a database considering one person.
    Args:
        listpaths (list): list of filespath
        string (str): name of the database
    Returns:
        Tuple: (list of tuple , description of tuples) -> ([], ['subject','database','label','duration','sum_time','percentage'])
    """
    df2=get_laughs_dict_folder(listpaths,string)
    df2=list_to_df(df2[0], df2[1])
    dg2=df2.loc[:,['subject','database','label','duration','diff_time']]
    dg2=dg2.groupby(['subject','database','label','duration']).sum().reset_index()
    dg2['percentage']=round(((dg2['diff_time']/dg2['duration'])*100),2)
    dg2.columns=['subject','database','label','duration','sum_time','percentage']
    lst=df_to_list(dg2)
    col=['subject','database','label','duration','sum_time','percentage']

    return lst,col


#By roles
def get_intra_smiles_ad_from_lsn_folder(listpaths,string):
    """This function calculates absolute duration for smiles in a database considering one person who is listener.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database

    Returns:
        Tuple: (list of tuple , description of tuples) -> ([], ['subject','database','label','sum_time','time'])
    """
    df1=list_to_df(get_smiles_from_lsn_folder(listpaths,string)[0], get_smiles_from_lsn_folder(listpaths,string)[1])

    dg1=df1.loc[:,['subject','database','label','diff_time']]
    dg1=dg1.groupby(['subject','database','label']).sum().reset_index()
    dg1['time']=seconds_to_hmsms_list(dg1['diff_time'])
    dg1.columns=['subject','database','label','sum_time','time']
    lst=df_to_list(dg1)
    col=['subject','database','label','sum_time','time']
    return lst,col

def get_intra_smiles_rd_from_lsn_folder(listpaths,string):
    """This function calculates relative duration for smiles in a database considering one person who is listener.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database
    Returns:
        Tuple: (list of tuple , description of tuples) -> ([], ['subject','database','label','percentage'])
    """
    df1=list_to_df(get_smiles_from_lsn_folder(listpaths,string)[0], get_smiles_from_lsn_folder(listpaths,string)[1])
    dg1=df1.loc[:,['subject','database','label','duration','diff_time']]
    dg1=dg1.groupby(['subject','database','label','duration']).sum().reset_index()
    dg1['percentage']=round(((dg1['diff_time']/dg1['duration'])*100),2)
    dg1.columns=['subject','database','label','duration','sum_time','percentage']
    dg1.drop(dg1.columns[[3,4]], axis=1, inplace=True)
    lst=df_to_list(dg1)
    col=['subject','database','label','percentage']
    return lst,col

def get_intra_smiles_ad_from_spk_folder(listpaths,string):
    """This function calculates absolute duration for smiles in a database considering one person who is speaker.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database

    Returns:
        Tuple: (list of tuple , description of tuples) -> ([], ['subject','database','label','sum_time','time'])
    """
    df1=list_to_df(get_smiles_from_spk_folder(listpaths,string)[0], get_smiles_from_spk_folder(listpaths,string)[1])
    dg1=df1.loc[:,['subject','database','label','diff_time']]
    dg1=dg1.groupby(['subject','database','label']).sum().reset_index()
    dg1['time']=seconds_to_hmsms_list(dg1['diff_time'])
    dg1.columns=['subject','database','label','sum_time','time']
    lst=df_to_list(dg1)
    col=['subject','database','label','sum_time','time']
    return lst,col

def get_intra_smiles_rd_from_spk_folder(listpaths,string):
    """This function calculates relative duration for smiles in a database considering one person who is speaker.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database

    Returns:
        Tuple: (list of tuple , description of tuples) -> ([], ['subject','database','label','percentage'])
    """
    df1=list_to_df(get_smiles_from_spk_folder(listpaths,string)[0], get_smiles_from_spk_folder(listpaths,string)[1])

    dg1=df1.loc[:,['subject','database','label','duration','diff_time']]
    dg1=dg1.groupby(['subject','database','label','duration']).sum().reset_index()
    dg1['percentage']=round(((dg1['diff_time']/dg1['duration'])*100),2)
    dg1.columns=['subject','database','label','duration','sum_time','percentage']
    dg1.drop(dg1.columns[[3,4]], axis=1, inplace=True)
    lst=df_to_list(dg1)
    col=['subject','database','label','percentage']
    return lst,col

def get_intra_laughs_ad_from_lsn_folder(listpaths,string):
    """This function calculates absolute duration for laughs in a database considering one person who is listener.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database
    Returns:
        Tuple: (list of tuple , description of tuples) -> ([], ['subject','database','label','sum_time','time'])
    """
    df1=list_to_df(get_laughs_from_lsn_folder(listpaths,string)[0], get_laughs_from_lsn_folder(listpaths,string)[1])

    dg1=df1.loc[:,['subject','database','label','diff_time']]
    dg1=dg1.groupby(['subject','database','label']).sum().reset_index()
    dg1['time']=seconds_to_hmsms_list(dg1['diff_time'])
    dg1.columns=['subject','database','label','sum_time','time']
    lst=df_to_list(dg1)
    col=['subject','database','label','sum_time','time']
    return lst,col

def get_intra_laughs_rd_from_lsn_folder(listpaths,string):
    """This function calculates relative duration for laughs in a database considering one person who is listener.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database
    Returns:
        Tuple: (list of tuple , description of tuples) -> ([], ['subject','database','label','percentage'])
    """
    df1=list_to_df(get_laughs_from_lsn_folder(listpaths,string)[0], get_laughs_from_lsn_folder(listpaths,string)[1])
    dg1=df1.loc[:,['subject','database','label','duration','diff_time']]
    dg1=dg1.groupby(['subject','database','label','duration']).sum().reset_index()
    dg1['percentage']=round(((dg1['diff_time']/dg1['duration'])*100),2)
    dg1.columns=['subject','database','label','duration','sum_time','percentage']
    dg1.drop(dg1.columns[[3,4]], axis=1, inplace=True)
    lst=df_to_list(dg1)
    col=['subject','database','label','percentage']
    return lst,col

def get_intra_laughs_ad_from_spk_folder(listpaths,string):
    """This function calculates absolute duration for laughs in a database considering one person who is speaker.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database
    Returns:
        Tuple: (list of tuple , description of tuples) -> ([], ['subject','database','label','sum_time','time'])
    """
    df1=list_to_df(get_laughs_from_spk_folder(listpaths,string)[0], get_laughs_from_spk_folder(listpaths,string)[1])
    dg1=df1.loc[:,['subject','database','label','diff_time']]
    dg1=dg1.groupby(['subject','database','label']).sum().reset_index()
    dg1['time']=seconds_to_hmsms_list(dg1['diff_time'])
    dg1.columns=['subject','database','label','sum_time','time']
    lst=df_to_list(dg1)
    col=['subject','database','label','sum_time','time']
    return lst,col

def get_intra_laughs_rd_from_spk_folder(listpaths,string):
    """This function calculates relative duration for laughs in a database considering one person who is speaker.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database

    Returns:
        Tuple: (list of tuple , description of tuples) -> ([], ['subject','database','label','percentage'])
    """
    df1=list_to_df(get_laughs_from_spk_folder(listpaths,string)[0], get_laughs_from_spk_folder(listpaths,string)[1])

    dg1=df1.loc[:,['subject','database','label','duration','diff_time']]
    dg1=dg1.groupby(['subject','database','label','duration']).sum().reset_index()
    dg1['percentage']=round(((dg1['diff_time']/dg1['duration'])*100),2)
    dg1.columns=['subject','database','label','duration','sum_time','percentage']
    dg1.drop(dg1.columns[[3,4]], axis=1, inplace=True)
    lst=df_to_list(dg1)
    col=['subject','database','label','percentage']
    return lst,col

#Inter
#By folder
def get_inter_smiles_absolute_duration_folder(listpaths,string):
    """This function calculates absolute duration for smiles in a database considering one interaction.
    Args:
        listpaths (list): list of filespath
        string (str): name of the database
    Returns:    
        Tuple: (list of tuple , description of tuples) ->(list, ['conv','label','duration','database','time'])
    """
    df=get_smiles_dict_conv_folder(listpaths,string)
    df=list_to_df(df[0], df[1])
    dg1=df.loc[:,['subject','database','label','diff_time']]
    dg1=dg1.groupby(['subject','database','label']).sum().reset_index()
    dg1['time']=seconds_to_hmsms_list(dg1['diff_time'])
    dg1.columns=['subject','database','label','sum_time','time']

    c=1
    conv=[]
    
    for i in range (1, len(listpaths),2):
        values=[i,i+1]
        dgg= dg1[dg1.subject.isin(values)]
        conv+=list_of_words(c, len(dgg.subject))
        c+=1
 
    dg1['conv']=conv
    dg1.columns=['subject','database','label','sum_time','time','conv']
    
    roles=[]
    
    for r in range(1,len(listpaths),2):
        dgf= dg1[dg1.subject.eq(r)]
        roles+=list_of_words("A", len(dgf.subject))
        r+=1
        dgf= dg1[dg1.subject.eq(r)]
        roles+=list_of_words("B", len(dgf.subject))

    dg1['roles']=roles
    dg1.columns=['subject','database','label','sum_time','time','conv','roles']

    #correct lines (replace the row in A which is not in B and same in te other sens with 0)
    #print(dg1.loc[0])
    dg1=dg1.loc[:,['label','sum_time','conv','roles']]
    dg1= dg1.reindex(columns=['conv', 'label','sum_time','roles'])
    dict_=list(dg1.to_records(index=False))

    conv = list(np.unique(conv))
    labels=tier_lists["Smiles"]
    for a in conv:
        #print("For conv n°",a)
        J_A=[]
        J_B=[]
        label_B=[]
        label_A=[]
        for _ in dict_:
            if _[0]==a and _[3]=='A':
                J_A.append(_)
            if _[0]==a and _[3]=='B':
                J_B.append(_)
        # print(J_A)
        # print(J_B)
        for i in J_B:label_B.append(i[1])
        for j in J_A :label_A.append(j[1])
        #print(label_B)
        for _ in labels :
            if _ in label_B:
                pass
            else:
                dict_.append((a, _ , 0 , 'B'))
            if _ in label_A:
                pass
            else :
                dict_.append((a, _ , 0 , 'A'))
    
    #print(dict_)
    #print(len(dict_))
    conv=[]
    label=[]
    sum_time=[]
    roles=[]
    for _ in range (len(dict_)):
        conv.append(dict_[_][0])
        label.append(dict_[_][1])
        sum_time.append(dict_[_][2])
        roles.append(dict_[_][3])

    dg1 = pd.DataFrame({'conv':conv,'label':label,'sum_time':sum_time,'roles':roles})
    dg1=dg1.sort_values(['conv','label'], ascending=[True,True]).reset_index()
    dg1.drop(dg1.columns[[0]], axis = 1, inplace = True) 
    #print(dg1)

    dfA= dg1[dg1.roles.eq('A')]
    dfB= dg1[dg1.roles.eq('B')]
    
    difA=pd.DataFrame(dfA).reset_index()
    difB=pd.DataFrame(dfB).reset_index()
    
    dg= difA.merge(difB,how='left', left_index=True, right_index=True)
    diff_time=[]
    for i,j in zip (dg.sum_time_x, dg.sum_time_y):
        diff_time.append(max(i,j)-min(i,j))
    dg['diff_time']=diff_time
    dg.drop(dg.columns[[0,3,4,5,6,7,8,9]], axis = 1, inplace = True) 
    dg['database']=list_of_words(string,len(dg.conv_x))
    dg.columns=['conv','label','duration','database']
    dg['time']=seconds_to_hmsms_list(dg['duration'])
    dg.columns=['conv','label','duration','database','time']

    lst=df_to_list(dg)
    col=['conv','label','duration','database','time']

    return lst,col

def get_inter_smiles_relative_duration_folder(listpaths,string):
    """This function calculates relative duration for smiles in a database considering one interaction.
    Args:
        listpaths (list): list of filespath
        string (str): name of the database
    Returns:        
        Tuple: (list of tuple , description of tuples) ->(list, ['conv','label','percentage','database'])
    """

    df1=get_smiles_dict_conv_folder(listpaths,string)
    df1=list_to_df(df1[0],df1[1])

    dg1=df1.loc[:,['subject','database','label','duration','diff_time']]
    dg1=dg1.groupby(['subject','database','label','duration']).sum().reset_index()
    dg1['percentage']=round(((dg1['diff_time']/dg1['duration'])*100),2)
    dg1.columns=['subject','database','label','duration','sum_time','percentage']

    c=1
    conv=[]
    for i in range (1, len(listpaths),2):
        values=[i,i+1]
        dgg= dg1[dg1.subject.isin(values)]
        conv+=list_of_words(c, len(dgg.subject))
        c+=1
    dg1['conv']=conv
    dg1.columns=['subject','database','label','duration','sum_time','percentage','conv']

    roles=[]
    for r in range(1,len(listpaths),2):
        dgf= dg1[dg1.subject.eq(r)]
        roles+=list_of_words("A", len(dgf.subject))
        r+=1
        dgf= dg1[dg1.subject.eq(r)]
        roles+=list_of_words("B", len(dgf.subject))
    dg1['roles']=roles
    dg1.columns=['subject','database','label','duration','sum_time','percentage','conv','roles']

    #correct lines (replace the row in A which is not in B and same in te other sens with 0)
    #print(dg1.loc[0])
    dg1=dg1.loc[:,['label','percentage','conv','roles']]
    dg1= dg1.reindex(columns=['conv', 'label','percentage','roles'])
    dict_=list(dg1.to_records(index=False))


    conv = list(np.unique(conv))
    labels=tier_lists["Smiles"]
    for a in conv:
        #print("For conv n°",a)
        J_A=[]
        J_B=[]
        label_B=[]
        label_A=[]
        for _ in dict_:
            if _[0]==a and _[3]=='A':
                J_A.append(_)
            if _[0]==a and _[3]=='B':
                J_B.append(_)
        # print(J_A)
        # print(J_B)
        for i in J_B:label_B.append(i[1])
        for j in J_A :label_A.append(j[1])
        #print(label_B)
        for _ in labels :
            if _ in label_B:
                pass
            else:
                dict_.append((a, _ , 0 , 'B'))
            if _ in label_A:
                pass
            else :
                dict_.append((a, _ , 0 , 'A'))
    
    #print(dict_)
    #print(len(dict_))
    conv=[]
    label=[]
    pct=[]
    roles=[]
    for _ in range (len(dict_)):
        conv.append(dict_[_][0])
        label.append(dict_[_][1])
        pct.append(dict_[_][2])
        roles.append(dict_[_][3])

    dg1 = pd.DataFrame({'conv':conv,'label':label,'percentage':pct,'roles':roles})
    dg1=dg1.sort_values(['conv','label'], ascending=[True,True]).reset_index()
    dg1.drop(dg1.columns[[0]], axis = 1, inplace = True) 
    #print(dg1)

    dfA= dg1[dg1.roles.eq('A')]
    dfB= dg1[dg1.roles.eq('B')]
    
    difA=pd.DataFrame(dfA).reset_index()
    difB=pd.DataFrame(dfB).reset_index()
    
    dg= difA.merge(difB,how='left', left_index=True, right_index=True)
    #print(dg)
    diff_pct=[]
    for i,j in zip (dg.percentage_x, dg.percentage_y):
        diff_pct.append(max(i,j)-min(i,j))
    dg['diff_pct']=diff_pct
    #print(dg)
    dg.drop(dg.columns[[0,3,4,5,6,7,8,9]], axis = 1, inplace = True) 
    dg['database']=list_of_words(string,len(dg.conv_x))
    dg.columns=['conv','label','percentage','database']

    lst=df_to_list(dg)
    col=['conv','label','percentage','database']

    return lst,col

def get_inter_laughs_absolute_duration_folder(listpaths,string):
    """This function calculates absolute duration for laughs in a database considering one interaction.
    Args:
        listpaths (list): list of filespath
        string (str): name of the database
    Returns:    
        Tuple: (list of tuple , description of tuples) ->(list, ['conv','label','duration','database','time'])
    """
    df=get_laughs_dict_conv_folder(listpaths,string)
    df=list_to_df(df[0], df[1])
    dg1=df.loc[:,['subject','database','label','diff_time']]
    dg1=dg1.groupby(['subject','database','label']).sum().reset_index()
    dg1['time']=seconds_to_hmsms_list(dg1['diff_time'])
    dg1.columns=['subject','database','label','sum_time','time']

    c=1
    conv=[]
    
    for i in range (1, len(listpaths),2):
        values=[i,i+1]
        dgg= dg1[dg1.subject.isin(values)]
        conv+=list_of_words(c, len(dgg.subject))
        c+=1

    dg1['conv']=conv
    dg1.columns=['subject','database','label','sum_time','time','conv']
   
    roles=[]
    
    for r in range(1,len(listpaths),2):
        dgf= dg1[dg1.subject.eq(r)]
        roles+=list_of_words("A", len(dgf.subject))
        r+=1
        dgf= dg1[dg1.subject.eq(r)]
        roles+=list_of_words("B", len(dgf.subject))

    dg1['roles']=roles
    dg1.columns=['subject','database','label','sum_time','time','conv','roles']

    #correct lines (replace the row in A which is not in B and same in te other sens with 0)
    dg1=dg1.loc[:,['label','sum_time','conv','roles']]
    dg1= dg1.reindex(columns=['conv', 'label','sum_time','roles'])
    dict_=list(dg1.to_records(index=False))

    #print(dict_)
    conv = list(np.unique(conv))
    labels=tier_lists["Laughs"]
    for a in conv:
        #print("For conv n°",a)
        J_A=[]
        J_B=[]
        label_B=[]
        label_A=[]
        for _ in dict_:
            if _[0]==a and _[3]=='A':
                J_A.append(_)
            if _[0]==a and _[3]=='B':
                J_B.append(_)
        #print(J_A)
        #print(J_B)
        for i in J_B:label_B.append(i[1])
        for j in J_A :label_A.append(j[1])
        #print(label_B)
        for _ in labels :
            if _ in label_B:
                pass
            else:
                dict_.append((a, _ , 0 , 'B'))
            if _ in label_A:
                pass
            else :
                dict_.append((a, _ , 0 , 'A'))
    
    #print(dict_)
    #print(len(dict_))

    # for a in conv:
    #     print("For conv n°",a)
    #     J_A=[]
    #     J_B=[]
    #     label_B=[]
    #     for _ in dict_:
    #         if _[0]==a and _[3]=='A':
    #             J_A.append(_)
    #         if _[0]==a and _[3]=='B':
    #             J_B.append(_)
    #     print(J_A)
    #     print(J_B)

    conv=[]
    label=[]
    sum_time=[]
    roles=[]
    for _ in range (len(dict_)):
        conv.append(dict_[_][0])
        label.append(dict_[_][1])
        sum_time.append(dict_[_][2])
        roles.append(dict_[_][3])

    dg1 = pd.DataFrame({'conv':conv,'label':label,'sum_time':sum_time,'roles':roles})
    dg1=dg1.sort_values(['conv','label'], ascending=[True,True]).reset_index()
    dg1.drop(dg1.columns[[0]], axis = 1, inplace = True) 
    #print(dg1)

    dfA= dg1[dg1.roles.eq('A')]
    dfB= dg1[dg1.roles.eq('B')]
    
    difA=pd.DataFrame(dfA).reset_index()
    difB=pd.DataFrame(dfB).reset_index()
    
    dg= difA.merge(difB,how='left', left_index=True, right_index=True)
    diff_time=[]
    for i,j in zip (dg.sum_time_x, dg.sum_time_y):
        diff_time.append(max(i,j)-min(i,j))
    dg['diff_time']=diff_time
    dg.drop(dg.columns[[0,3,4,5,6,7,8,9]], axis = 1, inplace = True) 
    dg['database']=list_of_words(string,len(dg.conv_x))
    dg.columns=['conv','label','duration','database']
    dg['time']=seconds_to_hmsms_list(dg['duration'])
    dg.columns=['conv','label','duration','database','time']

    lst=df_to_list(dg)
    col=['conv','label','duration','database','time']

    return lst,col

def get_inter_laughs_relative_duration_folder(listpaths,string):
    """This function calculates relative duration for laughs in a database considering one interaction.
    Args:
        listpaths (list): list of filespath
        string (str): name of the database
    Returns:        
        Tuple: (list of tuple , description of tuples) ->(list, ['conv','label','percentage','database'])
    """

    df1=get_laughs_dict_conv_folder(listpaths,string)
    df1=list_to_df(df1[0],df1[1])
    dg1=df1.loc[:,['subject','database','label','duration','diff_time']]
    dg1=dg1.groupby(['subject','database','label','duration']).sum().reset_index()
    dg1['percentage']=round(((dg1['diff_time']/dg1['duration'])*100),2)
    dg1.columns=['subject','database','label','duration','sum_time','percentage']

    c=1
    conv=[]
    for i in range (1, len(listpaths),2):
        values=[i,i+1]
        dgg= dg1[dg1.subject.isin(values)]
        conv+=list_of_words(c, len(dgg.subject))
        c+=1

    dg1['conv']=conv
    dg1.columns=['subject','database','label','duration','sum_time','percentage','conv']
    #print(dg1)

    roles=[]
    for r in range(1,len(listpaths),2):
        dgf= dg1[dg1.subject.eq(r)]
        roles+=list_of_words("A", len(dgf.subject))
        r+=1
        dgf= dg1[dg1.subject.eq(r)]
        roles+=list_of_words("B", len(dgf.subject))

    dg1['roles']=roles
    dg1.columns=['subject','database','label','duration','sum_time','percentage','conv','roles']

    #correct lines (replace the row in A which is not in B and same in te other sens with 0)
    #print(dg1.loc[0])
    dg1=dg1.loc[:,['label','percentage','conv','roles']]
    dg1= dg1.reindex(columns=['conv', 'label','percentage','roles'])
    dict_=list(dg1.to_records(index=False))


    labels=tier_lists["Laughs"]
    for a in conv:
        #print("For conv n°",a)
        J_A=[]
        J_B=[]
        label_B=[]
        label_A=[]
        for _ in dict_:
            if _[0]==a and _[3]=='A':
                J_A.append(_)
            if _[0]==a and _[3]=='B':
                J_B.append(_)
        #print(J_A)
        #print(J_B)
        for i in J_B:label_B.append(i[1])
        for j in J_A :label_A.append(j[1])
        #print(label_B)
        for _ in labels :
            if _ in label_B:
                pass
            else:
                dict_.append((a, _ , 0 , 'B'))
            if _ in label_A:
                pass
            else :
                dict_.append((a, _ , 0 , 'A'))
    
    #print(len(dict_))
    conv=[]
    label=[]
    pct=[]
    roles=[]
    for _ in range (len(dict_)):
        conv.append(dict_[_][0])
        label.append(dict_[_][1])
        pct.append(dict_[_][2])
        roles.append(dict_[_][3])

    dg1 = pd.DataFrame({'conv':conv,'label':label,'percentage':pct,'roles':roles})
    dg1=dg1.sort_values(['conv','label'], ascending=[True,True]).reset_index()
    dg1.drop(dg1.columns[[0]], axis = 1, inplace = True) 
    #print(dg1)

    dfA= dg1[dg1.roles.eq('A')]
    dfB= dg1[dg1.roles.eq('B')]
    
    difA=pd.DataFrame(dfA).reset_index()
    difB=pd.DataFrame(dfB).reset_index()
    
    dg= difA.merge(difB,how='left', left_index=True, right_index=True)
    #print(dg)
    diff_pct=[]
    for i,j in zip (dg.percentage_x, dg.percentage_y):
        diff_pct.append(max(i,j)-min(i,j))
    dg['diff_pct']=diff_pct
    #print(dg)
    dg.drop(dg.columns[[0,3,4,5,6,7,8,9]], axis = 1, inplace = True) 
    dg['database']=list_of_words(string,len(dg.conv_x))
    dg.columns=['conv','label','percentage','database']

    lst=df_to_list(dg)
    col=['conv','label','percentage','database']

    return lst,col

#By roles
#Smiles
def get_inter_smiles_ad_spk_vs_lsn_folder(listpaths,string):
    """This function calculates absolute duration for smiles when a speaker is in front of a listener.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database

    Return :
        Tuple (list, description of the list) -> (list, ['database','conv','role','label','sum_time','time']) """
    df=get_smiles_from_spk_vs_lsn_folder(listpaths,string)
    df=list_to_df(df[0], df[1])

    dg1=df.loc[:,['database','conv','role','label','diff_time']]
    dg1=dg1.groupby(['database','conv','role','label']).sum().reset_index()
    dg1['time']=seconds_to_hmsms_list(dg1['diff_time'])
    dg1.columns=['database','conv','role','label','sum_time','time']
    
    lst=df_to_list(dg1)
    col=['database','conv','role','label','sum_time','time']
    return lst,col

def get_inter_smiles_rd_spk_vs_lsn_folder(listpaths,string):
    """This function calculates relative duration for smiles when a speaker is in front of a listener.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database
    Return :
        Tuple (list, description of the list) -> (list, ['database','conv','label','percentage','role'])"""
    df=get_smiles_from_spk_vs_lsn_folder(listpaths,string)
    df=list_to_df(df[0], df[1])

    dg1=df.loc[:,['database','label','duration','conv','role','diff_time']]
    dg1=dg1.groupby(['database','label','duration','conv','role']).sum().reset_index()
    dg1['percentage']=round(((dg1['diff_time']/dg1['duration'])*100),2)
    dg1.columns=['database','label','duration','conv','role','sum_time','percentage']

    dg1.drop(dg1.columns[[2,5]], axis=1, inplace=True)
    dg1=dg1.reindex(columns=['database','conv','label','percentage','role'])

    lst=df_to_list(dg1)
    col=['database','conv','label','percentage','role']

    return lst,col

def get_inter_smiles_ad_lsn_vs_spk_folder(listpaths,string):
    """This function calculates absolute duration for smiles when a listener is in front of a speaker.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database
    Return :
        Tuple (list, description of the list) -> (list, [ 'database','label','conv','role','sum_time','time']) """
    
    df=get_smiles_from_lsn_vs_spk_folder(listpaths,string)
    df=list_to_df(df[0], df[1])

    dg1=df.loc[:,['database','label','conv','role','diff_time']]
    dg1=dg1.groupby(['database','label','conv','role']).sum().reset_index()
    dg1['time']=seconds_to_hmsms_list(dg1['diff_time'])
    dg1.columns=['database','label','conv','role','sum_time','time']
    lst=df_to_list(dg1)
    col=['database','label','conv','role','sum_time','time']
    return lst,col

def get_inter_smiles_rd_lsn_vs_spk_folder(listpaths,string):
    """This function calculates relative duration for smiles when a listener is in front of a speaker.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database
    Return :
        Tuple (list, description of the list) -> (list, ['database','conv','label','percentage','role'])"""
    df=get_smiles_from_lsn_vs_spk_folder(listpaths,string)
    df=list_to_df(df[0], df[1])
    dg1=df.loc[:,['database','label','duration','conv','role','diff_time']]
    dg1=dg1.groupby(['database','label','duration','conv','role']).sum().reset_index()
    dg1['percentage']=round(((dg1['diff_time']/dg1['duration'])*100),2)
    dg1.columns=['database','label','duration','conv','role','sum_time','percentage']
    dg1.drop(dg1.columns[[2,5]], axis=1, inplace=True)
    dg1=dg1.reindex(columns=['database','conv','label','percentage','role'])

    lst=df_to_list(dg1)
    col=['database','conv','label','percentage','role']

    return lst,col


#Laughs
def get_inter_laughs_ad_spk_vs_lsn_folder(listpaths,string):
    """This function calculates absolute duration for laughs when a speaker is in front of a listener.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database

    Return :
        Tuple (list, description of the list) -> (list, ['database','label','conv','role','sum_time','time']) """
    df=get_laughs_from_spk_vs_lsn_folder(listpaths,string)
    df=list_to_df(df[0], df[1])
    dg1=df.loc[:,['database','label','conv','role','diff_time']]
    dg1=dg1.groupby(['database','label','conv','role']).sum().reset_index()
    dg1['time']=seconds_to_hmsms_list(dg1['diff_time'])
    dg1.columns=['database','label','conv','role','sum_time','time']
    lst=df_to_list(dg1)
    col=['database','label','conv','role','sum_time','time']
    return lst,col

def get_inter_laughs_rd_spk_vs_lsn_folder(listpaths,string):
    """This function calculates relative duration for laughs when a speaker is in front of a listener.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database
    Return :
        Tuple (list, description of the list) -> (list, ['database','conv','label','percentage','role'])"""
    df=get_laughs_from_spk_vs_lsn_folder(listpaths,string)
    df=list_to_df(df[0], df[1])
    dg1=df.loc[:,['database','label','duration','conv','role','diff_time']]
    dg1=dg1.groupby(['database','label','duration','conv','role']).sum().reset_index()
    dg1['percentage']=round(((dg1['diff_time']/dg1['duration'])*100),2)
    dg1.columns=['database','label','duration','conv','role','sum_time','percentage']
    dg1.drop(dg1.columns[[2,5]], axis=1, inplace=True)
    dg1=dg1.reindex(columns=['database','conv','label','percentage','role'])

    lst=df_to_list(dg1)
    col=['database','conv','label','percentage','role']

    return lst,col

def get_inter_laughs_ad_lsn_vs_spk_folder(listpaths,string):
    """This function calculates absolute duration for laughs when a listener is in front of a speaker.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database

    Return :
        Tuple (list, description of the list) -> (list, ['database','label','conv','role','sum_time','time']) """
    
    df=get_laughs_from_lsn_vs_spk_folder(listpaths,string)
    df=list_to_df(df[0], df[1])
    dg1=df.loc[:,['database','label','conv','role','diff_time']]
    dg1=dg1.groupby(['database','label','conv','role']).sum().reset_index()
    dg1['time']=seconds_to_hmsms_list(dg1['diff_time'])
    dg1.columns=['database','label','conv','role','sum_time','time']
    lst=df_to_list(dg1)
    col=['database','label','conv','role','sum_time','time']
    return lst,col

def get_inter_laughs_rd_lsn_vs_spk_folder(listpaths,string):
    """This function calculates relative duration for laughs when a listener is in front of a speaker.

    Args:
        listpaths (list): list of filespath
        string (str): name of the database
    Return :
        Tuple (list, description of the list) -> (list, ['database','conv','label','percentage','role'])"""
    df=get_laughs_from_lsn_vs_spk_folder(listpaths,string)
    df=list_to_df(df[0], df[1])
    dg1=df.loc[:,['database','label','duration','conv','role','diff_time']]
    dg1=dg1.groupby(['database','label','duration','conv','role']).sum().reset_index()
    dg1['percentage']=round(((dg1['diff_time']/dg1['duration'])*100),2)
    dg1.columns=['database','label','duration','conv','role','sum_time','percentage']
    dg1.drop(dg1.columns[[2,5]], axis=1, inplace=True)
    dg1=dg1.reindex(columns=['database','conv','label','percentage','role'])

    lst=df_to_list(dg1)
    col=['database','conv','label','percentage','role']

    return lst,col


#S&L track 
def fill_sl_track(track, check, folder):
    """This function fill some lists where we put previous and next expressions concerning a tracked expression.

    Args:
        track (string): L or S for laugh or smile
        check (string): L or S for laugh or smile
        folder (list): eaf paths

    Returns:
        tuple: (database concerned, number of the expression, list of previous expressions, list of next expressions). Each element of the tuple is a list.
    """
    if folder==databases_paths["ccdb_paths"]:
        string='ccdb'
    if folder==databases_paths["ifadv_paths"]:
        string='ifadv'
    if folder==databases_paths["ndc_paths"]:
        string='ndc'

    track_p,track_f,sl_number,subjects=([] for _ in range(4))

    for root in range (0,len(folder),1):
        #lst=read_eaf_to_dict (folder[root], mark=True, tiers=None)
        sl_lst=get_SLdict(folder[root])

        track_lst=eval('get_'+track+'dict')(folder[root])
        #s_lst=lst["Smiles_0"]
        
        #On prends le stt et le stp d'un élément de Laughs_0 (on répètera l'action pour tous les éléments de Laughs_0).
        #Pour tous les éléments de track_lst
        i=1
        for _ in range(0, len(track_lst),1):
            stt = track_lst[_][0]
            stp = track_lst[_][1]
            subjects.append(string)
            #je repère d'abord mon stt et stp dans la liste S&L
            for _ in range(0, len(sl_lst),1):
                if (sl_lst[_][0] == stt) and (sl_lst[_][1] == stp):
                    #print(sl_lst[_])
                    if (sl_lst[_] == sl_lst[0]):    #we check if we are with the first element of the list
                            track_p.append('non')
                    else:
                        if (sl_lst[_-1][2]==check):           #je repère si j'ai un sourire avant ou non
                            track_p.append('oui')
                        else :
                            track_p.append('non')
                    
                    if (sl_lst[_] == sl_lst[len(sl_lst)-1]):    #we check if we are with the last element of the list
                        track_f.append('non')
                    else :
                        if (sl_lst[_+1][2]==check):       #je repère si j'ai un sourire après ou non
                            track_f.append('oui')
                        else :
                            track_f.append('non')

                    sl_number.append(i)     
            i+=1 

    return subjects,sl_number,track_p, track_f

def fill_trackfp_byIR(folder,string,function_to_lst_check, function_to_lst_track,case,special=bool):
    """This function fill some lists where we put previous and next expressions concerning a tracked expression filtered by intensity

    Args:
        folder (function):  list of filespath
        string (str): name of the database
        function_to_lst_check (function): _description_
        function_to_lst_track (function): _description_
        case (str): Can be S for smiles or L for laughs. For example, if we are tracking laughs, it's L
        special (str, optional): . Defaults to bool.

    Returns:
        tuple -> (database,current_level,track_number,trackp,trackf). Each element of the tuple is a list

    """
    """
    Now, we want to now what we have function of the intensity of the laugh.
    So we do the process below for each level of laugh.
    For example : intensity high.
    We take the corresponding dictionnary to this intensity.
    For each element of this dict, for example for laugh n°1 :
        * Check this laugh in the S&L dict (1) | Particularity : By role, we maybe wont find the laugh in the dict because of overlapping function.
        * Take the smile before/after      (2)
        * Check this smile in the smiles_dict   (3)
        * Put this unique smile's intensity in a list (trackp (previous) / trackf (followed) ) (4)
    Return two databases : for previous and next smiles
    """

    #Variables
    trackp, trackf, track_number, current_level, database= ([] for _ in range(5))
    
    for root in folder :
        n=1
        sl_lst=get_SLdict(root)
        lst_check=apply_funct2(function_to_lst_check,keep_info,root,special)
        lst_track=apply_funct2(function_to_lst_track,keep_info,root,special)
        if case=="L":
            low_lst=keep_info_with_lab(lst_track, 'low',2)
            med_lst=keep_info_with_lab(lst_track, 'medium',2)
            high_lst=keep_info_with_lab(lst_track, 'high',2)
            level_list=low_lst+ med_lst+ high_lst
            current_level=current_level+list_of_words("low",len(low_lst))+list_of_words("med",len(med_lst))+list_of_words("high",len(high_lst))
        if case=='S':
            subtle_lst=keep_info_with_lab(lst_track, 'subtle',2)
            low_lst=keep_info_with_lab(lst_track, 'low',2)
            med_lst=keep_info_with_lab(lst_track, 'medium',2)
            high_lst=keep_info_with_lab(lst_track, 'high',2)
            level_list=subtle_lst+low_lst+med_lst+high_lst
            current_level=current_level+list_of_words("subtle",len(subtle_lst))+list_of_words("low",len(low_lst))+list_of_words("med",len(med_lst))+list_of_words("high",len(high_lst))
        
        #print("\n Root =",root,"\n S&L : ", sl_lst, "\n\n List to check : ", lst_check, "\n\n List to track :", level_list)
        
        all_stt_s=[k[0] for k in lst_check]
        #all_stp_s=[k[1] for k in lst_check]
        if len(level_list)== 0:
            pass
        else :
            for j in level_list:
                stt_l = j[0]
                stp_l = j[1]
                database.append(string)
                for _ in range(0, len(sl_lst),1):
                    if (sl_lst[_][0] == stt_l) and (sl_lst[_][1] == stp_l):     #(1)
                        #print(sl_lst[_])
                        if (sl_lst[_] == sl_lst[0]):    #we check if we are with the first element of the list
                            trackp.append('null')
                        else:
                            if (sl_lst[_-1][2]=='S'):  #(2)
                                index_=0
                                stt_s=0
                                for k in all_stt_s:
                                    if sl_lst[_-1][0] in all_stt_s:
                                        if sl_lst[_-1][0] == k :
                                            stt_s=k
                                    else:
                                        pass
                                if len(lst_check)== 0:
                                    pass
                                else:
                                    for i in range (len(lst_check)):
                                        if stt_s==lst_check[i][0]:
                                            index_=lst_check.index(lst_check[i])
                                    if stt_s == lst_check[index_][0]: 
                                        trackp.append(lst_check[index_][2])   #(4) 
                                    else : 
                                        trackp.append('null')
                                     
                            else :
                                trackp.append('null')

                        if (sl_lst[_] == sl_lst[len(sl_lst)-1]):    #we check if we are with the last element of the list
                            trackf.append('null')
                        else :
                            if (sl_lst[_+1][2]=='S'):       #(2)
                                index_=0
                                stt_s=0
                                for k in all_stt_s:
                                    if sl_lst[_+1][0] in all_stt_s:
                                        if sl_lst[_+1][0] == k :
                                            stt_s=k
                                    else:
                                        pass
                                if len(lst_check)== 0:
                                    pass
                                else:
                                    for i in range (len(lst_check)):
                                        if stt_s==lst_check[i][0]:
                                            index_=lst_check.index(lst_check[i])
                                    if stt_s == lst_check[index_][0]: 
                                        trackf.append(lst_check[index_][2])   #(4) 
                                    else : 
                                        trackf.append('null')                                
                            else :
                                trackf.append('null')

                        track_number.append(n)
                    
                n+=1
                #print("trackp :",trackp)#," |  trackf ",trackf)
    # for i in [database,current_level,track_number,trackp,trackf]:
    #     print(len(i), i)

    return database,current_level,track_number,trackp,trackf

def SL_track(check, track,dir):
    """This function determines the previous and next expressions we have concerning a tracked expression.

    Args:
        check (str): L or S for laugh or smile. It's the expression which preced or follow.
        track (str): L or S for laugh or smile. It's the expression of which we want to know what is before and after.
        dir (str) : path of the folder containing all databases.

    Returns:
        database : A database containing the quantity of previous and next expressions.
    """
    dg=[]
    n =0
    L =[]
    for path in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, path)):
            n+=1
            data=["ccdb","ifadv","ndc"]
            for i in data:
                if path==i:
                    L.append(get_all_filepaths((os.path.join(dir, path)), "eaf", None))   

    for i in range (len(L)) :

        a=fill_sl_track(track, check,L[i])
        # Check list lengths
        if len(a[0]) == len(a[1]) == len(a[2]) == len(a[3]):
            df1 = pd.DataFrame({'Database': a[0], 'N°' + track: a[1], 'Trackp': a[2], 'Trackf': a[3]})
            dg.append(df1)
        else:
            desired_length = min(len(a[0]), len(a[1]), len(a[2]), len(a[3]))  # Desired length based on existing listings
            # Create a new tuple with the first desired length elements
            a = (a[0][:desired_length], a[1][:desired_length], a[2][:desired_length], a[3][:desired_length])
            df1 = pd.DataFrame({'Database': a[0], 'N°' + track: a[1], 'Trackp': a[2], 'Trackf': a[3]})
            dg.append(df1)

    df= pd.concat(dg)

    #Previous smile's track    
    df_g = df.groupby(['Trackp', 'Database']).size().reset_index()
    df_g.columns = ['Trackp', 'Database', 'Countp']
    df_t=df_g.groupby(['Database'])['Countp'].sum().reset_index()
    tot=[]
    for _ in list(df_g["Database"]):
        for i in list(df_t['Database']):
            if _ == i:
                tot.append(int(df_t[df_t.Database.eq(_)]['Countp']))
    df_g['tot']=tot
    df_g['Percentagep'] = round(((df_g["Countp"]/df_g['tot'])*100),2)
    #df_g['percentage'] = df.groupby(['Trackp', 'Database']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
    df_g.columns = ['Trackp', 'Databasep', 'Countp','tot','Percentagep']


    # #Following smile's track 
    df1_g = df.groupby(['Trackf', 'Database']).size().reset_index()
    df1_g.columns = ['Trackf', 'Database', 'Countf']
    df_t1=df1_g.groupby(['Database'])['Countf'].sum().reset_index()
    tot=[]
    for _ in list(df1_g["Database"]):
        for i in list(df_t1['Database']):
            if _ == i:
                tot.append(int(df_t1[df_t1.Database.eq(_)]['Countf']))
    df1_g['tot']=tot
    df1_g['Percentagef'] = round(((df1_g["Countf"]/df1_g['tot'])*100),2)
    df1_g.columns = ['Trackf', 'Databasef', 'Countf','tot','Percentagef']   

    dg= pd.concat([df_g, df1_g],axis=1)

    # a_list= df_to_list(dg)
    # col=dg.columns.values.tolist()

    return dg

def SL_track_byI(check, track, dir):
    """This function determines the previous and next expression taking into account the intensities.
    Args :
        check (str): L or S for laugh or smile. It's the expression which preced or follow.
        track (str): L or S for laugh or smile. It's the expression of which we want to know what is before and after.
        dir (str) : path of the folder containing all databases.
    Returns:
        tuple: (database for previous expressions, database for next expressions)
    """
    
    #Variables
    dg=[]
    n =0
    L =[]
    for path in os.listdir(DIR):
        if os.path.isdir(os.path.join(DIR, path)):
            n+=1
            data=["ccdb","ifadv","ndc"]
            for i in data:
                if path==i:
                    L.append((get_all_filepaths((os.path.join(DIR, path)), "eaf", None), path))

    for i in range (len(L)) :
        a=fill_trackfp_byIR(L[i][0], L[i][1], eval('get_'+check+'dict'), eval('get_'+track+'dict'), track, False )
        # Check list lengths
        if len(a[0]) == len(a[1]) == len(a[2]) == len(a[3]) == len(a[4]):
            df1 = pd.DataFrame({'Database':a[0],'Current_level_'+track : a[1], 'N°'+track: a[2],'Intensityp': a[3],
    'Intensityf':a[4]}) 
            dg.append(df1)
        else:
            desired_length = min(len(a[0]), len(a[1]), len(a[2]), len(a[3]), len(a[4]))  # Desired length based on existing listings
            # Create a new tuple with the first desired length elements
            a = (a[0][:desired_length], a[1][:desired_length], a[2][:desired_length], a[3][:desired_length], a[4][:desired_length])
            df1 = pd.DataFrame({'Database':a[0],'Current_level_'+track : a[1], 'N°'+track: a[2],'Intensityp': a[3],
    'Intensityf':a[4]}) 
            dg.append(df1)

    df= pd.concat(dg)
    
    #Previous smiles
    df_g = df.groupby(['Intensityp', 'Database', 'Current_level_'+track]).size().reset_index()
    df_g.columns = ['Intensityp', 'Database', 'Current_level_'+track, 'Count']
    df_t=df_g.groupby(['Database','Current_level_'+track])['Count'].sum().reset_index()

    tot=[]
    for _,j in zip (list(df_g["Database"]), list(df_g['Current_level_'+track])):
        for i,k in zip (list(df_t['Database']),list(df_t['Current_level_'+track])):
            if _ == i and j==k:
                #print(df_t[df_t.Database.eq(_)]['Count'])
                tot.append(int(df_t[df_t.Database.eq(_) & df_t['Current_level_'+track].eq(j)]['Count']))
    df_g['tot']=tot
    df_g['Percentage'] = round(((df_g["Count"]/df_g['tot'])*100),2)
    #df_g['percentage'] = df.groupby(['Trackp', 'Database']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
    df_g.columns = ['Intensityp', 'Databasep', 'Current_level_'+track+'p', 'Countp','tot','Percentagep']

    #Following smiles
    df1_g = df.groupby(['Intensityf', 'Database', 'Current_level_'+track]).size().reset_index()
    df1_g.columns = ['Intensityf', 'Database', 'Current_level_'+track,'Count']
    df_t1=df1_g.groupby(['Database','Current_level_'+track])['Count'].sum().reset_index()
    tot=[]
    for _,j in zip (list(df1_g["Database"]), list(df1_g['Current_level_'+track ])):
        for i,k in zip (list(df_t1['Database']),list(df_t1['Current_level_'+track ])):
            if _ == i and j==k:
                tot.append(int(df_t1[df_t1.Database.eq(_) & df_t1['Current_level_'+track].eq(j)]['Count']))
    df1_g['tot']=tot
    df1_g['Percentage'] = round(((df1_g["Count"]/df1_g['tot'])*100),2)
    df1_g.columns = ['Intensityf', 'Databasef', 'Current_level_'+track+'f','Countf','tot','Percentagef'] 

    #dg= pd.concat([df_g, df1_g],axis=1)

    return df_g, df1_g

#Probabilities mimicry
def give_mimicry(lA, lB, delta_t=0):
    """
    The function calculate the mimicry between two lists
    Args :
        lA (list): list of tuples (start, stop, label) of expressions mimicked.
        lB (list): list of tuples (start, stop, label) of expressions mimicking.
        delta_t (int, optional): Defaults to 0.
                                Time after which expression occuring still counts as mimicry.
                                Should be in the same unit as the times in lstA and lstB.    
    Returns:
        int: number of times B mimicked A (=len(the list described below)).
        float: probability of B mimick A
    """
    count_=count_mimicry(lA,lB,delta_t)
    return (count_[0], round((count_[0]/len(lB)),2))

def give_mimicry_folder1(function,folder,filter=None,label=None):
    """Calculate mimicry of interactions on a folder

    Args:
        function (function): It's a function giving the list of tuples (start, stop, label) of expressions mimicked and mimicking.
        folder (list): List of the .eaf files path 
        filter (string, optional): It has to be 'Intensity'. Defaults to None.
        label (string or list, optional): If it's a string, it represents the intensity we want and if it's a list, 
        it represents the intensities we want to keep. Defaults to None.

    Returns:
        list: A list of tuples [(count, probability),....]
    """
    if folder==databases_pair_paths["ccdb_pairs"]:
        string='ccdb'
    if folder==databases_pair_paths["ifadv_pairs"]:
        string='ifadv'
    if folder==databases_pair_paths["ndc_pairs"]:
        string='ndc'
    
    dt=apply_function1(function,folder,string)  
    dt2=keep_info(dt[0],4)
    df=list_to_df(dt2, dt[1][0:4])

    #print(df)
    LA=[]
    LB=[]
    count_proba=[]

    n=1
    for _ in range (int(len(folder)/2)) :
        
        if filter is None:    
            LA = df_to_list(df[df.subject.eq(n)])
            LB = df_to_list(df[df.subject.eq(n+1)])

        else:
            if filter=='Intensity':
                if type(label) is list:
                    LA = keep_info_with_lab(df_to_list(df[df.subject.eq(n)]), label[0], 2)
                    LB = keep_info_with_lab(df_to_list(df[df.subject.eq(n+1)]), label[1], 2)
                else:
                    LA = keep_info_with_lab(df_to_list(df[df.subject.eq(n)]), label, 2)
                    LB = keep_info_with_lab(df_to_list(df[df.subject.eq(n+1)]), label, 2)
            

        if len(LA)==0 :
            LA.append((0,0,0,0))
        if len(LB)==0:
            LB.append((0,0,0,0))
        #print(LA,"\n",LB)
        count_proba.append(give_mimicry(LA,LB))
        n+=2
    
    M=[]
    for i in count_proba :
        i+=(string,)
        M.append(i)
    return M

def give_mimicry_folder2(folder,function1,function2,filter=None,label=None):
    """
    Calculate mimicry of interactions on a folder.
    The particularity here is one of the lists contains smiles and the second, laughs.
    Args:
        folder (list): List of the .eaf files path 
        function1 (function): It's a function giving the list of tuples (start, stop, label) of expressions mimicked
        function2 (function): It's a function giving the list of tuples (start, stop, label) of expressions mimicking
        filter (string, optional): It has to be 'Intensity'. Defaults to None.
        label (string or list, optional): If it's a string, it represents the intensity we want and if it's a list, 
        it represents the intensities we want to keep. Defaults to None.

    Returns:
        list: A list of tuples [(count, probability),....]
    """
    if folder==databases_pair_paths["ccdb_pairs"]:
        string='ccdb'
    if folder==databases_pair_paths["ifadv_pairs"]:
        string='ifadv'
    if folder==databases_pair_paths["ndc_pairs"]:
        string='ndc'

    dA=apply_function1(function1,folder,string)
    dB=apply_function1(function2,folder,string)

    dA2=keep_info(dA[0],4)
    dB2=keep_info(dB[0],4)
    dfA=list_to_df(dA2, dA[1][0:4])
    dfB=list_to_df(dB2, dB[1][0:4])

    LA=[]
    LB=[]
    count_proba=[]
    lst=list(np.unique(list(dfA['subject'])))
    del lst[-1]
    
    n=1
    for _ in range (int(len(folder)/2)) :
        if filter is None:    
            LA = df_to_list(dfA[dfA.subject.eq(n)])
            LB = df_to_list(dfB[dfB.subject.eq(n+1)])

        else:
            if filter=='Intensity':
                if type(label) is list:
                    LA = keep_info_with_lab(df_to_list(dfA[dfA.subject.eq(n)]), label[0], 2)
                    LB = keep_info_with_lab(df_to_list(dfB[dfB.subject.eq(n+1)]), label[1], 2)
                else:
                    LA = keep_info_with_lab(df_to_list(dfA[dfA.subject.eq(n)]), label, 2)
                    LB = keep_info_with_lab(df_to_list(dfB[dfB.subject.eq(n+1)]), label, 2)
        
        if len(LA)==0 :
            LA.append((0,0,0,0))
        if len(LB)==0:
            LB.append((0,0,0,0))
        print(LA,"\n",LB)
        count_proba.append(give_mimicry(LA,LB))
        n+=2
    
    M=[]
    for i in count_proba :
        i+=(string,)
        M.append(i)
    return M

#Correlation
def get_correlation(lA,lB):
    """This function calculates correlation between two lists.

    Args:
        lA (list): list of numeric elements
        lB (list): list of numeric elements

    Returns:
        numeric : the value is the correlation between the two lists
    """
    # lA=tuple_to_int_sequence(rootA)
    # lB=tuple_to_int_sequence(rootB)
    if len(lA) ==0 or len(lB) ==0 :
        corr=0
    else:

        diff=max(len(lA),len(lB))-min(len(lA),len(lB))
        if max(len(lA),len(lB))==len(lA):
            lA=lA[:len(lA)-diff]
        else:
            if max(len(lA),len(lB))==len(lB):
                lB=lB[:len(lB)-diff]

        #Calculate mean
        mA = sum(lA)/len(lA)
        mB = sum(lB)/len(lB)
        #Calculate covariance
        cov = sum((a - mA) * (b - mB) for (a,b) in zip(lA,lB)) / (len(lA))
        #Calculate the standard deviation of each list
        stdA=np.std(lA)
        stdB=np.std(lB)
        #Calculate correlation
        corr=round(cov/(stdA*stdB),3)
        
        #corr=round(np.corrcoef(lA,lB)[0][1],3)
        #corr=round(pearsonr(lA,lB)[0],3)
    return corr

def get_correlation_folder(SL,folder, width, shift, SL2=None,role=False,which_role=None):
    """This function calculates the correlation in an interaction. 

    Args:
        SL (string): S for smiles or L for laughs
        folder (list): list of eaf paths in the database chosen
        width (numeric):  window width in ms
        shift (numeric):  window shift in ms
        role (bool, optional): To say if we want to dispatch by role or not. Defaults to False.

    Returns:
        list: List of values corresponding to the correlation of each interaction of the database
    """
    corr_l=[]
    for i in range(0,len(folder),2):
        L=[folder[i],folder[i+1]]

        if role==True:
            if SL=='S':
                a=eval('get_smiles_from_'+which_role)(L[0])[0]
                b=eval('get_smiles_from_'+which_role)(L[1])[0]
            if SL=='L':
                a=eval('get_laughs_from_'+which_role)(L[0])[0]
                b=eval('get_laughs_from_'+which_role)(L[1])[0]
        else:
            if SL2 is None:
                a=eval('get_'+SL+'dict')(L[0])
                b=eval('get_'+SL+'dict')(L[1])
            else:
                a=eval('get_'+SL+'dict')(L[0])
                b=eval('get_'+SL2+'dict')(L[1])
        #print(a, "  |  ",b)
        lst = [tuple_to_int_sequence(a, width=width, shift=shift), tuple_to_int_sequence(b, width=width, shift=shift)]
        c=get_correlation(lst[0],lst[1])
        corr_l.append(c)

    return corr_l

def get_correlation_byI(SL1,intensity1,folder, width, shift,SL2=None,intensity2=None):
    """This function calculates the correlation in an interaction filtered by intensity. 

    Args:
        SL1 (str): S for smiles or L for laughs.
        intensity1 (str): low, subtle, medium or high
        folder (list): list of eaf paths in the database chosen
        width (numeric):  window width in ms
        shift (numeric):  window shift in ms
        SL2 (str, optional): S for smiles or L for laughs. It's the second expression. Defaults to None.
        intensity2 (str, optional): low, subtle, medium or high. Defaults to None.

    Returns:
        list: List of values corresponding to the correlation of each interaction of the database
    """
    corr_l=[]
    for i in range(0,len(folder),2):
        L=[folder[i],folder[i+1]]
        a=get_IR_list(L[0], SL1, intensity1)  
        if SL2 is None :
            if intensity2 is None:
                b=get_IR_list(L[1], SL1, intensity1)
            else:
                b=get_IR_list(L[1], SL1, intensity2)
        else:
            if intensity2 is None:
                b=get_IR_list(L[1], SL2, intensity1)
            else:
                b=get_IR_list(L[1], SL2, intensity2)
        #print(a, "  |  ",b)
        lst = [tuple_to_int_sequence(a, width=width, shift=shift), tuple_to_int_sequence(b, width=width, shift=shift)]
        c=get_correlation(lst[0],lst[1])
        corr_l.append(c)

    return corr_l

#Others
def get_database_name(folder):
        """This function give the name of the database corresponding to the folder.
        Args:
            folder (list): list of eaf paths

        Returns:
            str: name of the database
        """
        level=0
        for _ in reversed(list(enumerate(folder[0]))):
            if folder[0][_[0]]== '\\':
                #print(folder[0][_[0]])
                level=_[0]
                break
        a=folder[0][:level]
        level=0
        for _ in reversed(list(enumerate(a))):
            if a[_[0]]== '\\':
                #print(a[_[0]])
                level=_[0]
                break
        return a[level+1:]
   
def expression_per_min(folder, expression, case=None):
    """
    This function calculates the number of one tier we have per minute.   
    Args:
        folder (list) -> list of all files paths
        expression (str) -> tiers_0
        case (int, optional): Express if you want to look into conversations ; for that, you put 2. Defaults to None.

    Returns:
        A list containing the number of smiles per minute for each subject of the folder and a list 
        containing the intensity of expression corresponding to the smiles.
    """
    L=[]
    M=[]
    tiers_=[]
    m = 60000
    m_multiples = [m, m*2, m*3, m*4, m*5, m*6, m*7]
    threshold_value = 20000

    if case is None :
        for j in range(0, len(folder),1):
            n=0
            nb=0                            #variable which represent the number of smiles by minute
            to_dict = read_eaf_to_dict (folder[j] , mark=True, tiers=None)
            lst = None
            if expression in to_dict:
               lst = to_dict[expression]
            else:
                match = re.search(r'^([a-zA-Z]+)', expression)
                if match:
                    word = match.group(1)
                lst = to_dict[word]
            n=len(lst)  #number of expression in the file

            eaf = pympi.Elan.Eaf(folder[j])
            duration_annotated=check_duration(eaf)

            #if the duration annotated is near one value of m_multiples, we divide n by the corresponding value (1 or 2 or 3 .... )
            for i in m_multiples:
                if( i-threshold_value < duration_annotated < i+threshold_value) :
                    nb=n/(i/m)
                    L.append(nb) 
                else :
                    pass
            
            for i in range(0, len(lst),1):
                M.append(lst[i])
            tiers_.append(M)
    else:
        for j in range(0, len(folder),2):
            n,n2, nb, nb2=0,0,0,0       # nb and nb2 are variables which represent the number of smiles by minute for person 1 and person 2
            to_dict = read_eaf_to_dict (folder[j] , mark=True, tiers=None)
            to_dict2 = read_eaf_to_dict (folder[j+1] , mark=True, tiers=None)
            lst = to_dict.get(expression)
            lst2 = to_dict2.get(expression)

            if lst is None:
                match = re.search(r'^([a-zA-Z]+)', expression)
                if match:
                    word = match.group(1)
                    lst = to_dict.get(word)
                    lst2 = to_dict2.get(word)
            n=len(lst)
            n2=len(lst2)

            eaf1 = pympi.Elan.Eaf(folder[j])
            duration_annotated=check_duration(eaf1)
            eaf2 = pympi.Elan.Eaf(folder[j+1])
            duration_annotated=check_duration(eaf2)

            #If the duration annotated is near one value of m_multiples, we divide n by the corresponding value (1 or 2 or 3 .... )
            for i in m_multiples:
                if( i-threshold_value < duration_annotated < i+threshold_value) :
                    nb=n/(i/m)
                    nb2=n2/(i/m)
                    L.append(nb+nb2) 
                else :
                    pass

            for j in range(0, len(lst),1):
                    M.append(lst[j])
            for k in range(0, len(lst2),1):
                    M.append(lst2[k])

            tiers_.append(M)
     
    return L, tiers_

def expression_per_min_I(folder, expression, intensity):
    """This function calculates the number of one tier we have per minute for one intensity.  
    Args:
        folder (list) -> list of all files paths
        expression (str) -> tiers
        intensity (str) -> This is the intensity we search. You can type : subtle, low, medium, high for smiles and same for laughs (without subtle)

    Returns:
        list, list : list of tuples ("start",'end','intensity','person'), ["start",'end','intensity','person']
    """
    m, n, nb = 60000, 0, 0
    L=[]
    m_multiples = [m, m*2, m*3, m*4, m*5, m*6, m*7]
    threshold_value = 20000
    count=[]
    for root in folder:
        lst=get_IR_list(root, expression, intensity)
        n = len(lst)
        eaf = pympi.Elan.Eaf(root)
        duration_annotated=check_duration(eaf)

        #if the duration annotated is near one value of m_multiples, we divide n by the corresponding value (1 or 2 or 3 .... )
        for i in m_multiples:
            if( i-threshold_value < duration_annotated < i+threshold_value) :
                nb=n/(i/m)
                count.append(nb) 
            else :
                pass
    
    return count 


