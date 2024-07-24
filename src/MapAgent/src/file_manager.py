''' MAP CLASS '''
import logging
import h5py
import numpy as np
import os

def open_file(file_name:str) -> h5py.File:
    '''Opens an existing HDF5 file in Read Mode'''
    return h5py.File(file_name,'r')

def create_file(file_name:str) -> h5py.File:
    '''Creates a new file in Write Mode and stores it in the data folder'''
    file_name = './MapAgent/src/data/'+ file_name + '.hdf5'
    return h5py.File(file_name,'w')

def file_exists(start_path, target_file)-> bool:
    for root, dirs, files in os.walk(start_path):
        if target_file in files:
            return True

    return False

def file_add_dataset(file : h5py.File, dataset_name:str, dataset_content:np.array) -> h5py.Dataset: # type: ignore
    '''Adds a dataset into a HDF5 File'''
    file.create_dataset(dataset_name, data=dataset_content)
    return file.get(dataset_name) # type: ignore

def copy_attributes(new_dataset:h5py.Dataset, old_dataset:h5py.Dataset) -> None:
    '''Copies all the attributes from the old dataset to the new one'''
    attr_values = list(old_dataset.attrs.values())
    i=0
    for attr_name in list(old_dataset.attrs.keys()):
        new_dataset.attrs[attr_name] = attr_values[i]
        i+=1

def change_attribute(dataset:h5py.Dataset, name_attr:str, value) -> None:
    '''Changes the value of an attribute from a concrete dataset'''
    dataset.attrs[name_attr] = value

def get_datasets(file: h5py.File) -> list:
    '''Returns a list with all the datasets from the file'''
    datasets=[]
    for dataset_name in list(file.keys()):
        datasets.append(file.get(dataset_name))
    return datasets

def get_sorted_datasets(file:h5py.File) -> list:
    '''Returns a list with all the datasets from the file ordered by the ysup attribute'''
    max_y=[]
    datasets=[]
    for dataset_name in list(file.keys()):
        datasets.append(file.get(dataset_name))
    ordered_datasets=list()
    for dataset in datasets:
        max_y.append(get_attr(dataset,'ysup'))
    while max(max_y) != -1:
        next_id=max_y.index(max(max_y))
        ordered_datasets.append(file.get(list(file.keys())[next_id]))
        max_y[next_id]=-1
    
    return ordered_datasets

def get_dataset(file : h5py.File, dataset_name:str) -> h5py.Dataset:
    '''Returns a dataset from the file'''
    return file.get(dataset_name) # type: ignore

def get_dataset_with_id(file:h5py.File, dataset_id:int) -> h5py.Dataset:
    '''Returns a dataset from a self-made list of datasets from the provided file'''
    return file.get(list(file.keys())[dataset_id]) # type: ignore

def get_attr(dataset:h5py.Dataset, attr):
    '''Returns the value of an attribute from a concrete dataset'''
    return dataset.attrs[attr]

def read_value(dataset, cell) -> float:
    '''Returns the value of a concrete cell from a concrete dataset'''
    value = dataset[cell[0]][cell[1]]
    return value