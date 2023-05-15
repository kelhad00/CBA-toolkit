import os, sys
script_path = os.path.realpath(os.path.dirname("IBPY"))
os.chdir(script_path)
sys.path.append("..")

from  IBPY.processing import *
from  IBPY.extract_data import *
from .settings import *
from IBPY.db import *

import os
import numpy as np
import Levenshtein

def findIndexes(str, search):
  lst = []
  for i in range(len(str)):
      if (str[i] == search):
          lst.append(i)
  return lst

def one_hot_encode(elt, nb_exprs):
  """
  Args:
    elt : class we need to encode
    nb_exprs : total number of classes gettable
  """
  ohe_elt = [0 for _ in range(nb_exprs)]
  ohe_elt[elt] = 1
  ohe_elt = np.asanyarray(ohe_elt)
  return ohe_elt

def one_hot_decode(encoded_seq):
  return [np.argmax(vec) for vec in encoded_seq]

def class_to_label(c):
  """
  Args: 
    c : the class code we want to labelize. ! Need to be shape [role, expr] !
  """
  if c[0] == 0:
    label = "None_"
  elif c[0] == 1:
    label = "S_"
  elif c[0] == 2:
    label = "L_"
  if c[1] == 0: label = label + "None_None"
  elif c[1] == 1: label = label + "S_s"
  elif c[1] == 2: label = label + "S_l"
  elif c[1] == 3: label = label + "S_m"
  elif c[1] == 4: label = label + "S_h"
  elif c[1] == 5: label = label + "L_l"
  elif c[1] == 6: label = label + "L_m"
  elif c[1] == 7: label = label + "L_h"
  return label

def seq_encoded_to_labels(datas):
  """
  Args:
    datas : must be 3 dimension sequence with shape (nbr_sequences, sequence_len, [role, expr])
  
  Return: the sequence (seq) labelized
  """
  datas_labeled = []
  for seq in range(len(datas)):
    datas_labeled.append([class_to_label(x) for x in datas[seq]])
  return np.array(datas_labeled)

def divide_seq_to_frames(seq, f_len, f_step):
  """ Take a raw sequence (exemple: full video sequence) and divide it in multiple sub sequences
    Args: 
      seq : the sequence we want to split to frames
      f_len : is FRAME_LEN defined in settings.py
      f_step : is FRAME_STEP defined in settings.py

    Return : The same sequence from args but framed
  """
  div_seq = []
  cur_seq_ind = 0
  shift = int(f_step/REC_TSTEP)
  sample_count = int(f_len/REC_TSTEP)    # Number of samples in one frame
  while (cur_seq_ind+shift) < len(seq):
    div_seq.append([seq[x] for x in range(cur_seq_ind, cur_seq_ind+sample_count)])
    cur_seq_ind = cur_seq_ind+shift
  if sample_count > len(seq):     #Special case if frame bigger than datas length then we only have one sequence 
    div_seq = [seq]
  return np.asanyarray(div_seq)

def dict_to_seq(dct, steps, ohe):
  """
    Args:
    dct : dictionnary we want to transform in a sequence
    steps : step (in ms) between each sample of the video defined in settings variable
    ohe : option for one hot encoding to encode the datas extracted

    Return: full sequence of couple (expressions, roles) extracted from dct
  """
  seq = []

  role_class = {
    'spk': 1,
    'lsn' : 2
  }
  smile_class = {
    'subtle': 1,
    'low': 2,
    'medium': 3,
    'high': 4
  }
  laugh_class = {
    'low': 5,
    'medium': 6,
    'high': 7
  }

  try:
    roles = [role_class[x] if x != None else 0 for x in tuple_to_sequence(dct["Role"], steps, steps)]
  except:
    print("WARNING:: No role detected, putting initial value to 0")
    roles = [0]
  try:
    smiles = [smile_class[x] if x != None else 0 for x in tuple_to_sequence(dct["Smiles_0"], steps, steps)]
  except:
    print("WARNING:: No smile detected, putting initial value to 0")
    smiles = [0]
  try:
    laughs = [laugh_class[x] if x != None else 0 for x in tuple_to_sequence(dct["Laughs_0"], steps, steps)]
  except:
    print("WARNING:: No laugh detected, putting initial value to 0")
    laughs = [0]

  if len(smiles) > len(laughs):
    laughs = laughs+[0]*(len(smiles) - len(laughs))
  elif len(smiles) < len(laughs):
    smiles = smiles+[0]*(len(laughs) - len(smiles))

  if len(smiles) < len(roles):
    smiles = smiles + [0] * (len(roles) - len(smiles))
    laughs = laughs + [0] * (len(roles) - len(laughs))
  elif len(smiles) > len(roles):
    smiles = smiles[:len(roles)]
    laughs = laughs[:len(roles)]

  seq_size = min(len(roles), len(smiles))
  expr = 0
  for i in range(seq_size):
    if smiles[i] != 0:
      expr = smiles[i]
    elif laughs[i] != 0:
      expr = laughs[i]
    else:
      expr = 0
    seq.append(np.concatenate((one_hot_encode(roles[i], len(role_class)+1), one_hot_encode(expr, len(smile_class)+len(laugh_class)+1)), axis=None)) if ohe else seq.append([roles[i], expr])

  return np.array(seq)


def split_dict_to_seq(dct, steps, ohe):       # DEPRECATED
  """
  # DEPRECATED
    Args:
      dct : dictionnary we want to transform in a sequence
      steps : step (in ms) between each sample of the video defined in settings variable
      ohe : option for one hot encoding to encode the datas extracted

    Return: full sequence of couple (expressions, roles) extracted from dct 

  """
  counter = 0
  role = 0
  expr = 0
  has_smile = False
  has_laugh = False
  seq = []              #shape seq = [[0, 4], [1, 5]] -> 0 being role class and 4 emotion class
  cur_role_ind = 0      # tuple list position in the dict
  cur_smile_ind = 0
  cur_laugh_ind = 0
  
  while counter <= dct['Role'][-1][1]:
    # ROLE CLASS SELECTION
    if dct['Role'][cur_role_ind][1] <= counter-steps/2 and cur_role_ind != len(dct['Role'])-1:
      cur_role_ind += 1
    if dct['Role'][cur_role_ind][2] == 'spk':
      role = 0
    else:
       role = 1

    # EMOTION CLASS SELECTION
    if cur_smile_ind == 0:     # Detect the first expression
      if counter+steps/2 >= dct['Smiles_0'][cur_smile_ind][0]:
        has_smile = True
         
    if dct['Smiles_0'][cur_smile_ind][1] <= counter+steps/2 and cur_smile_ind != len(dct['Smiles_0'])-1:    # middle smiles
      if dct['Smiles_0'][cur_smile_ind+1][0] <= counter+steps/2:
        cur_smile_ind += 1
        has_smile = True
      else:
        has_smile = False
    elif cur_smile_ind == len(dct['Smiles_0'])-1 and dct['Smiles_0'][cur_smile_ind][1] < counter+steps/2:   # Last smile
      has_smile = False

    if has_smile:
      if dct['Smiles_0'][cur_smile_ind][2] == 'subtle':
        expr = 1
      elif dct['Smiles_0'][cur_smile_ind][2] == 'low':
        expr = 2
      elif dct['Smiles_0'][cur_smile_ind][2] == 'medium':
        expr = 3
      elif dct['Smiles_0'][cur_smile_ind][2] == 'high':
        expr = 4

    if len(dct['Laughs_0']) > 0:      # Video without laughs can exist
      if cur_laugh_ind == 0:
        if counter+steps/2 >= dct['Laughs_0'][cur_laugh_ind][0]:
          has_laugh = True

      if dct['Laughs_0'][cur_laugh_ind][1] <= counter+steps/2 and cur_laugh_ind != len(dct['Laughs_0'])-1:    # middle laughs
        if dct['Laughs_0'][cur_laugh_ind+1][0] <= counter+steps/2:
          cur_laugh_ind += 1
          has_laugh = True
        else:
          has_laugh = False
      elif cur_laugh_ind == len(dct['Laughs_0'])-1 and dct['Laughs_0'][cur_laugh_ind][1] < counter+steps/2:   # last laugh
        has_laugh = False

      if has_laugh:
        if dct['Laughs_0'][cur_laugh_ind][2] == 'low':
          expr = 5
        elif dct['Laughs_0'][cur_laugh_ind][2] == 'medium':
          expr = 6
        elif dct['Laughs_0'][cur_laugh_ind][2] == 'high':
          expr = 7

    if not has_smile and not has_laugh:
      expr = 0

    #One hot encoding option in action
    if not ohe:
      seq.append([role, expr])
    else:
      seq.append([role, one_hot_encode(expr, 8)])

    counter = counter+steps
  return np.array(seq)

def dict_preprocess(input_dct, output_dct):
  """
    Arg : 
      input_dct : takes raw dict extracted from eaf as input
      output_dct : takes raw dict extracted from eaf as input

      Return : input/output tuple of smiles and laughs with tsteps between each emotion for one video
  """
  keys_to_del = []

  for k in input_dct:
    if '_0' not in k and k != 'Role':
      keys_to_del.append(k)
  for k in keys_to_del:
    input_dct.pop(k)
    output_dct.pop(k)

  #Evaluate max length of the video to synchro datas and delete exceeding samples
  input_seq = dict_to_seq(input_dct, REC_TSTEP, OHE)
  output_seq = dict_to_seq(output_dct, REC_TSTEP, OHE)

  if len(input_seq) > len(output_seq):
    input_seq = input_seq[:len(output_seq)]
  elif len(input_seq) < len(output_seq):
    output_seq = output_seq[:len(input_seq)]

  # Frame dividing here ? -> or in main.py to be customed

  return (input_seq, output_seq)

def get_model_datas_eaf(input_path, output_path, format):
  """_summary_

  Args:
      input_path (string): videos of person1 in conversation. serves as input
      output_path (string): videos of person2 in conversation. serves as output
      format (string): type of video datas (ifadv, ccbd, ndc)

  Returns:
      dict: A dict with sequece ordered by couple of videos (shape: {video_0: (input_seq_vid0, output_seq_vid0), video_1: (input_seq_video1, output_seq_vid1), ...})
  """
  eaf_files = get_all_filepaths(input_path, 'eaf') + get_all_filepaths(output_path, 'eaf')
  eaf_files_short = []
  all_videos_datas = {}
  for file in eaf_files:
    eaf_files_short.append(file[findIndexes(file, '\\')[-1]+1:])
  eaf_files_short_copy = eaf_files_short.copy()
  eaf_pairs = EAF_FORMATS[format](eaf_files_short)
  eaf_files_short = eaf_files_short_copy
  for couple in eaf_pairs:
    input = eaf_files[eaf_files_short.index(couple[0])]
    output = eaf_files[eaf_files_short.index(couple[1])]
    print(input, output)
    model_datas = dict_preprocess(read_eaf_to_dict(input), read_eaf_to_dict(output))
    all_videos_datas['video_'+str(len(all_videos_datas))] = model_datas

  return all_videos_datas

def get_model_datas_ifadv(input_path, output_path):
  """
    Args:
      input_path: videos of person1 in conversation. serves as input
      output_path: videos of person2 in conversation. serves as output

    Return:
      A dict with sequece ordered by couple of videos (shape: {video_0: (input_seq_vid0, output_seq_vid0), video_1: (input_seq_video1, output_seq_vid1), ...})
  """
  eaf_files_input = get_all_filepaths(input_path, 'eaf')
  eaf_files_output = get_all_filepaths(output_path, 'eaf')
  all_videos_datas = {}
  for file1 in eaf_files_input:     # Search for couple of people talking
    for file2 in eaf_files_output:
      print(file1, file2)
      if Levenshtein.distance(file1[findIndexes(file1, '\\')[-1]+1:-4], file2[findIndexes(file2, '\\')[-1]+1:-4]) == 2:       #recover file name without ext and path to avoid particular case and determinate if files are associated (for ifadv videos)
        print("INFO:: IFADV eaf couple detected")
        print("INFO:: input datas", file1, "and output datas", file2, "treatment in progress.")
        
        model_datas = dict_preprocess(read_eaf_to_dict(file1), read_eaf_to_dict(file2))
        all_videos_datas['video_'+str(len(all_videos_datas))] = model_datas

      elif len(findIndexes(file1, '_')) != 0 and len(findIndexes(file2, '_')) != 0 and file1[findIndexes(file1, '\\')[-1]+1:findIndexes(file1, '_')[-1]] == file2[findIndexes(file2, '\\')[-1]+1:findIndexes(file2, '_')[-1]]:    # recover couple of eaf files (for ccbd videos)
        print("INFO:: CCDB eaf couple detected")
        print("INFO:: input datas", file1, "and output datas", file2, "treatment in progress.")

        model_datas = dict_preprocess(read_eaf_to_dict(file1), read_eaf_to_dict(file2))
        all_videos_datas['video_'+str(len(all_videos_datas))] = model_datas

  return all_videos_datas

def seq_to_crf_dict(in_seq, out_seq, propagation_count):
  """
  Used for crf purpose only. Create features dict for crf model training with class labels associated.
  Args: 
    in_seq : Sequence of expressions from the person the AI talk with. Also input of our model.
    out_seq : Our output sequence wich is ideal AI response to the person. Needed to recover past expressions from AI. 
  """
  crf_dict_list = []
  crf_dict_seq_list = []
  output_labels = []
  output_seq_labels = []
  for n in range(len(in_seq)):
    crf_dict_seq_list = []
    output_seq_labels = []
    for m in range(len(in_seq[n])):
      # Building features dict for crf model training
      features = {
        'role': in_seq[n][m][0],
        'state': in_seq[n][m][1]
      }
      if n > propagation_count:
        for p in range(1, propagation_count+1):
          features.update({'-'+str(p)+'state': in_seq[n][m-p][1]})
          features.update({'-'+str(p)+'other_state': out_seq[n][m-p][1]})
      crf_dict_seq_list.append(features)
      output_seq_labels.append(class_to_label(out_seq[n][m]))
    crf_dict_list.append(crf_dict_seq_list)
    output_labels.append(output_seq_labels)
  return (crf_dict_list, output_labels)

def setup_label_database(path_in, path_out, format):
  """Transform a filepath with eaf files to labeled sequence dictionnary ordered by videos
      For now it only works on ifadv eaf files

  Args:
      path_in (string): full input path of eaf datas 
      path_out (string): full output path of eaf datas 

  Returns:
      dict: shape of the returned dict :: video_0:
                                            0 (input_datas): [sequence]
                                            1 (output_datas): [sequence]
                                          video_1: ...
  """
  #raw_datas = get_model_datas_eaf(path_in, path_out, 'ifadv')
  raw_datas = get_model_datas_eaf(path_in, path_out, format)
  label_datas = {}
  for video in raw_datas:
    label_datas[video] = ([class_to_label(raw_datas[video][0][x]) for x in range(len(raw_datas[video][0]))], [class_to_label(raw_datas[video][1][x]) for x in range(len(raw_datas[video][1]))])
    
  return label_datas