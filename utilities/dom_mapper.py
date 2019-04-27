import os
import json




class DOM_Mapper:
    
    
    DOM = {}
    meta_data = {}
    
    
    def __init__(self):
        
        pass
    
    
    def retrieve_dom_tree(self, file_path):
    
        file = open(file_path, 'r', encoding = 'UTF-8')
        page_data = json.load(file)
        self.DOM = page_data['DOM']
        self.meta_data = page_data['meta_data']
        
        print(self.meta_data)
        
        pass
    
    
    
    def map(self, node, fun, option = 'DEPTH'):
        
        if option == 'DEPTH':
            self.depth_mapper(node, fun)
        elif option == 'BREADTH':
            self.breadth_mapper(node, fun)
        else:
            print('ERR: option "%(option)s" is not available!' % {'option':option})
        
        pass
    
    
    
    def depth_mapper(self, node, fun):
        
        node = fun(node)
        
        for child in node['children']:
            self.map(node = child, fun = fun)
        
        pass
    
    
    
    
    def breadth_mapper(self, node, fun):
        # ...
        pass
    
    
    
    
    pass




if __name__ == '__main__':
    
    dr = DOM_Mapper()

    dr.retrieve_dom_tree('../datasets/extracted_data/0000.json')
    
    #dr.map(node = dr.DOM, fun = ) 
    #dr.map(node = dr.DOM, fun = )
    
    
    pass