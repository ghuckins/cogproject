import numpy as np
from node import Node
import os 
import glob 
import h5py
import pickle 



class DataStruct(object):
    """
    Generates a simplified R struct (data format used by NPTL) from 
    a Node object. 
    """
    def __init__(self, node):
        self.speechLabel = node.R_out.speechLabel
        self.audio       = node.R_out.audio
        self.audioFs     = node.R_out.audioFs
        self.spikeRaster = node.R_out.spikeRaster
        
        self.timeCue     = node.R_out.timeCue
        self.timeSpeech  = node.R_out.timeSpeech
        self.trialStart  = node.R_out.trialStart
        self.goCue       = node.R_out.goCue
        self.HLFP        = node.R_out.HLFP
        
        
def combineDataStructs(struct_list):
  '''
  Given a list of DataStruct objects, combine them into one.
  '''
  
  numstructs  = len(struct_list)
  base_struct = struct_list[0]
  
  for struct in range(1, numstructs):
    for attr, val in base_struct.__dict__.items():
      append_val    = getattr(struct_list[struct], attr)
      extended_attr = np.append(val, append_val)
      setattr(base_struct, attr, extended_attr)
      
  return base_struct

        
        
def Mat2Python(mat_path):
    '''
    Given path to a V7.3 mat file, generate a 
    DataStruct instance.
    '''
    f        = h5py.File(mat_path, mode= 'r')
    data     = Node(f)
    data_out = DataStruct(data)
    return data_out
  
  
  
def generateDataset():
  '''
  Goes through each .mat file in data/raw/ and generates the resultant DataStruct instance 
  in data/processed/. Note: we assume the project directory structure is:
  
  Requires original dataset be placed in root/data/raw/. Will generate processed/ if need be.
  '''
  
  if not os.path.isdir('../data/processed/'):
    os.system('mkdir processed/')

  datafiles = glob.glob('../data/raw/*.mat')
  for file in datafiles:
    save_fname = file 
    save_fname = save_fname.replace('raw', 'processed')
    save_fname = save_fname.replace('mat', 'pickle')
    if not os.path.isfile(save_fname):
      print(file)
      data_out = Mat2Python(file)
      with open(save_fname, 'wb') as handle:
        pickle.dump(data_out, handle, protocol = pickle.HIGHEST_PROTOCOL)
        print(save_fname, 'saved.')

    
  

        