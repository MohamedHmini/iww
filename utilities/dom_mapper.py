import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 100)



class DOM_Mapper:
    
    
    DOM = {}
    meta_data = {}
    
    DOM_arr = np.array([])
    
    
    def __init__(self):
        # ...
        pass
    
    
    def retrieve_DOM_tree(self, file_path):
    
        self.DOM_file_path = os.path.realpath(file_path)        
        self.DOM_file_name = os.path.basename(self.DOM_file_path).split('.json')[0]
        
        file = open(self.DOM_file_path, 'r', encoding = 'UTF-8')
        page_data = json.load(file)
        self.DOM = page_data['DOM']
        self.meta_data = page_data['meta_data']
        
        file.close()
        
        pass
    
    
    def update_DOM_tree(self):
        
        file = open(self.DOM_file_path, 'w', encoding = 'UTF-8')
        
        DOM_str = json.dumps({
                'DOM':self.DOM,
                'meta_data':self.meta_data
                })
        
        file.write(DOM_str)
        
        file.close()
        
        pass
    
    
    
    ###################### MAPPER : ##########################

    
    def map(self, node = None, 
            fun1 = (lambda x: x), 
            fun2 = (lambda x, y: (x,y)), 
            fun3 = (lambda x, y: (x,y)), 
            fun4 = (lambda x: x), 
            option = 'DEPTH'):
        
        if option == 'DEPTH':
            self.depth_mapper(node, fun1, fun2, fun3, fun4)
        elif option == 'BREADTH':
            self.breadth_mapper(node, fun1, fun2, fun3, fun4)
        else:
            print('ERR: option "%(option)s" is not available!' % {'option':option})
        
        pass
    
    
    
    def depth_mapper(self, node, fun1, fun2, fun3, fun4):
        
        node = fun1(node)
        
        for child in node['children']:
            node, child = fun2(node, child)
            self.depth_mapper(child, fun1, fun2, fun3, fun4)
            node, child = fun3(node, child)
            
        node = fun4(node)
        
        pass
    
    
    
    
    def breadth_mapper(self, node, fun1, fun2, fun3, fun4):
        # ...
        pass
    
    ###########################################################
    
    
    
    ###################### REDUCER : ##########################
    def reduce(self, node = None, 
            fun1 = (lambda x: x), 
            fun2 = (lambda x: x), 
            option = 'DEPTH'):
        
        if option == 'DEPTH':
            self.depth_reducer(node, fun1, fun2)
        elif option == 'BREADTH':
            self.breadth_reducer(node, fun1, fun2)
        else:
            print('ERR: option "%(option)s" is not available!' % {'option':option})
        
        pass
    
    
    def depth_reducer(self, node, fun1, fun2):
        
        node = fun1(node)
        
        for child in node['children']:
            self.depth_reducer(child, fun1, fun2)
            
        node = fun2(node)
        
        pass
    
    
    
    
    def breadth_reducer(self, node, fun1, fun2):
        # ...
        pass
    
    ###########################################################
  
    
    
    def relative_position(self, node):
        # ...
        pass
    
    
    def toArray(self, DOM_arr_features):
        
        self.DOM_arr_features = DOM_arr_features
        self.map(node = self.DOM, fun1 = self.__toArray)
        
        return self.DOM_arr
        
        pass
    
    
    def __toArray(self, node):
        
        features_values = []
        
        for feature in self.DOM_arr_features:
            
            features_values.append(node[feature])
            
            pass
        
        arr = np.array([features_values])    
        
        if self.DOM_arr.shape == (0,):
            self.DOM_arr = arr            
        else:
            self.DOM_arr = np.concatenate((self.DOM_arr,arr), axis = 0)
        
        return node
        
        pass
    
    
    def retrieve_DOM_arr_file(self, file_path):
        
        df = pd.read_csv(file_path)
        
        self.DOM_file_name = os.path.basename(file_path).split(".csv")[0]
        self.DOM_arr_features = df.columns[1:]
        self.DOM_arr = df.values[:,1:]
        
        return self.DOM_arr
        
        pass
    
    
    def update_DOM_arr_file(self, arr, directory, file_name = None):
        
        if file_name == None:
            file_name = self.DOM_file_name + ".csv"
        
        
        file_path = os.path.realpath(os.path.join(os.path.abspath(directory), file_name))
        
        df = pd.DataFrame(arr, columns = self.DOM_arr_features)
        df.to_csv(file_path)
    
        
        pass
    
    
    
    pass




if __name__ == '__main__':
    
    dr = DOM_Mapper()

    #dr.retrieve_DOM_tree('../datasets/extracted_data/0000.json')
    
    #dr.map(node = dr.DOM, fun1 = p) 
    #dr.map(node = dr.DOM, fun = )
    #dom_copy = dr.DOM.copy()
    
    #dr.map(node = dr.DOM, fun1 = dr.toArray)
    
    #columns = ['tagName','tagsCount', 'textDensity', 'densitySum']
    
    #dr.toArray(columns)
    #dr.update_DOM_arr_file(arr = dr.DOM_arr, directory = '../datasets/DOM_arrs/')
    
    #arr = pd.read_csv(os.path.realpath('../datasets/DOM_arrs/0000.csv'))
    
    arr = dr.retrieve_DOM_arr_file('../datasets/DOM_arrs/0000.csv')
    print(dr.DOM_arr_features)
    print(arr)
    
    #print(pd.DataFrame(dr.DOM_arr, columns = columns))
    
    pass