from hmac import new
import math
import logging
import file_manager as fm
import numpy as np

logging.basicConfig(level=logging.INFO)
class Map:
    '''Class used for representing a map'''
    def __init__(self,file_name) -> None:
        '''Constructor'''
        self.f = fm.open_file(file_name)
        _sample_dataset=fm.get_dataset_with_id(self.f,1)
        _min_x,_min_y,_max_x,_max_y = self.__calculate_corners__()
        # Class Attrs
        self.nodata_value = fm.get_attr(_sample_dataset,'nodata_value')
        self.size_cell = fm.get_attr(_sample_dataset,'cellsize') 
        self.file_name = file_name
        self.up_left = (_min_x,_max_y)
        self.down_right = (_max_x,_min_y)
        self.dim = ((_max_x-_min_x)/self.size_cell,(_max_y-_min_y)/self.size_cell) # type: ignore

    def __calculate_corners__(self):
        '''Function that calculates the corners of the map'''
        max_x = 0
        max_y = 0
        min_x = 0
        min_y = 0
        init=False
        datasets=fm.get_datasets(self.f)
        for dataset in datasets:
            if not init:
                min_x = fm.get_attr(dataset,'xinf')
                min_y = fm.get_attr(dataset,'yinf')
                max_x = fm.get_attr(dataset,'xsup')
                max_y = fm.get_attr(dataset,'ysup')
                init=True
            else:
                min_x = min(fm.get_attr(dataset,'xinf'),min_x)
                min_y = min(fm.get_attr(dataset,'yinf'),min_y)
                max_x = max(fm.get_attr(dataset,'xsup'),max_x)
                max_y = max(fm.get_attr(dataset,'ysup'),max_y)
        return min_x,min_y,max_x,max_y


    def umt_yx(self,y,x) -> float:
        '''Function that locates the coordinates and outputs the corresponding value'''
        ordered_datasets = fm.get_sorted_datasets(self.f)
        chosen_dataset=None
        for dataset in ordered_datasets:
            if fm.get_attr(dataset,'yinf')<=y<fm.get_attr(dataset,'ysup') and fm.get_attr(dataset,'xinf')<x<fm.get_attr(dataset,'xsup'):
                chosen_dataset=dataset
                break
        if chosen_dataset is None:
            return self.nodata_value # type: ignore
        num_cell = self.umt_to_cell(chosen_dataset,y,x)
        return float(fm.read_value(chosen_dataset,num_cell))

    def resize(self,factor,transform,name):
        '''Function that resizes a map by a factor and applies that factor to the values, transforming them'''
        if factor == 1:
            return self
        if factor <=0:
            return None
        new_cellsize = self.size_cell*factor

        if fm.file_exists("./MapAgent/src/data",name + ".hdf5"):
            file_name = "./MapAgent/src/data/"+ name + ".hdf5"
            new_map_file = fm.open_file(file_name)
        else:
            new_map_file = fm.create_file(name)

            old_datasets = fm.get_datasets(self.f)
            for old_dataset in old_datasets:
                old_dataset_content = np.array(old_dataset)
                new_dataset_content = np.zeros((math.ceil(old_dataset.shape[0]/factor),math.ceil(old_dataset.shape[1]/factor)))
                new_row = 0
                for old_row in range(0, old_dataset.shape[0], factor):
                    new_column = 0
                    for old_column in range(0, old_dataset.shape[1], factor):
                        masked_old_dataset_content = old_dataset_content[old_row:old_row + factor,old_column:old_column + factor]
                        if np.all(masked_old_dataset_content == self.nodata_value):
                            new_dataset_content[new_row, new_column] = self.nodata_value
                        else:
                            new_dataset_content[new_row,new_column] = transform(masked_old_dataset_content[masked_old_dataset_content != self.nodata_value])
                        new_column = new_column + 1
                    new_row = new_row + 1
                new_dataset = fm.file_add_dataset(new_map_file,old_dataset.name,new_dataset_content)
                fm.copy_attributes(new_dataset,old_dataset)
                fm.change_attribute(new_dataset, 'cellsize', new_cellsize)
        return Map(new_map_file.filename)
    
    def umt_to_cell(self,dataset,y,x) -> tuple:
        '''Function that converts umt coordinates to the corresponding map cell'''
        cell_x=math.floor((x-fm.get_attr(dataset,'xinf'))/self.size_cell)
        cell_y=math.floor((fm.get_attr(dataset,'ysup')-y)/self.size_cell)
        
        if x==fm.get_attr(dataset,'xsup'):
            cell_x-=1

        if y==fm.get_attr(dataset,'ysup'):
            cell_y-=1
        cell=(cell_y,cell_x)
        return cell # type: ignore
