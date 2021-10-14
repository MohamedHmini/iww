import os
import json
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 100)




class DotDict(dict):
    def __getattr__(self, item):
        if item in self:
            return self[item]
        raise AttributeError

    def __setattr__(self, key, value):
        if key in self:
            self[key] = value
            return
        raise AttributeError



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
        self.webpage_url = page_data['webpage_url']
        
        file.close()
        
        pass
    
    
    def update_DOM_tree(self):
        
        file = open(self.DOM_file_path, 'w', encoding = 'UTF-8')
        
        DOM_str = json.dumps({
                'DOM':self.DOM,
                'meta_data':self.meta_data,
                'webpage_url':self.webpage_url
                })
        
        file.write(DOM_str)
        
        file.close()
        
        pass
    
    
    def toDotDict(self):
        
        self.map(self.DOM, fun1 = self.__toDotDict) 
        
        pass
    
    
    def __toDotDict(self, node):
        
        node = DotDict(node)
        #node.atts = DotDict(node.atts)
        #node.style = DotDict(node.style)
        node.bounds = DotDict(node.bounds)
        node['test'] = "works"
        node.dimensions = DotDict(node.dimensions)
        
        return node
        
        pass
    
    
    
    ###################### MAPPER : ##########################

    
    def map(self, node = None, 
            fun1 = (lambda x: x), 
            fun2 = (lambda x, y: (x,y)), 
            fun3 = (lambda x, y: (x,y)), 
            fun4 = (lambda x: x), 
            args = [],
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
            fun2 = (lambda x,y : x),
            option = 'DEPTH'):
        
        if option == 'DEPTH':
            return self.depth_reducer(node, fun1, fun2)
        elif option == 'BREADTH':
            return self.breadth_reducer(node, fun1, fun2)
        else:
            print('ERR: option "%(option)s" is not available!' % {'option':option})
        
        pass
    
    
    def depth_reducer(self, node, fun1, fun2):
        
        val = fun1(node)
        
        for child in node['children']:   
            child_val = self.depth_reducer(child, fun1, fun2)
            val = fun2(val, child_val)
            
             
        return val
        
        pass
    
    
    
    
    def breadth_reducer(self, node, fun1, fun2):
        # ...
        pass
    
    ###########################################################
  
    
    
    def relative_position(self, node):
        # ...
        pass
    
    
    def getFeature(self, path):
        #...
        pass
    
    
    def flatten_single_node(self, node, features):
        
        features_values = []
        
        for feature in features:
            
            feature_val = self.get_feature_by_path(node, feature)
            features_values.append(feature_val)
            
            pass
        
        arr = np.array([features_values])    
        
        return arr
        
        pass
    
    
    def flatten(self, node, features):
        
        self.DOM_arr_features = features
        self.DOM_arr = np.array([])
        self.map(node = node, fun1 = self.__flatten)
        
        return self.DOM_arr
        
        pass
    
    
    def __flatten(self, node):
        
        features_values = []
        
        for feature in self.DOM_arr_features:
            
            feature_val = self.get_feature_by_path(node, feature)
            features_values.append(feature_val)
            
            pass
        
        arr = np.array([features_values])    
        
        if self.DOM_arr.shape == (0,):
            self.DOM_arr = arr            
        else:
            self.DOM_arr = np.concatenate((self.DOM_arr,arr), axis = 0)
        
        return node
        
        pass
    
    
    def get_feature_by_path(self, node, feature_path):
        
        try:
            feature_seq = feature_path.split(".")
            feature_val = node.copy()
            
            for feature in feature_seq:
                
                feature_val = feature_val[feature]
                
                pass
        except:
            return np.nan
            pass
        
        
        return feature_val        
        
        pass
    
    
    def set_feature_by_path(self, node, feature_path, feature_value):
        
        try:
            feature_seq = feature_path.split(".")
            feature_container = feature_seq[-2]
            needed_feature = feature_seq[-1]
            feature_node = node.copy()
            
            for feature in feature_container:
                
                feature_node = feature_node[feature]
                
                pass
        except:
            pass
        
        
        feature_node[needed_feature] = feature_value
        
        pass
    
    
    ##################    NEEDS AN UPDATE!!    #####################
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
    
    
    def search_DOM_node(self, node, att, value):
        
        if self.get_feature_by_path(node, att) == value:
            return node
        
        for child in node['children']:
            found = self.search_DOM_node(child, att, value)
            if found != None:
                return found
            
        return None
        
        pass
    
    
    def xpath_based_node_search(self, node, searched_xpath, current_xpath_position = "/BODY"):
        
        
        if searched_xpath == '':
            return None
        
        return self.__xpath_based_node_search(node, searched_xpath, current_xpath_position)
        
        pass
    
    
    def __xpath_based_node_search(self, node, searched_xpath, current_xpath_position = "/BODY"):
        
        elements = searched_xpath.split(current_xpath_position)
        
        if elements[1] == '':
            return node
        
        next_node = elements[1].split("/")[1]
        next_node_pos = next_node.split("[")
        next_node_pos = (next_node_pos[0], int(next_node_pos[1].split("]")[0]))
        
        found = self.xpath_based_node_search(node['children'][next_node_pos[1]], searched_xpath, current_xpath_position + "/" + next_node)
        
        return found
        
        pass
    
    
    
    
    def siblings(self, node):
        
        siblings = []
        parent = self.xpath_based_node_search(self.DOM, node['parent_xpath'])
        
        for child in parent['children']:
            if child['xpath'] != node['xpath']:
                siblings.append(child)
            pass
        
        return siblings
        
        pass
    
    
    
    def nextNode(self, node, option = "DEPTH"):
        #...
        pass
    
    
    
    def depth_first_next_node(self, node):
        #...    
        pass
    
    
    
# =============================================================================
#     def display(self, node, att):
#         self.map(node, fun1 = self.__display, args = [att])
#         pass
#     
#     def __display(self, node, args):
#         
#         print(node[args[0]])
#         
#         return node
#         pass
# =============================================================================
 
    def xpath_reader(self, xpath):
                
        xpath_splited = xpath.split("/")
        node = xpath_splited[-1]
        
        if node == "BODY":
            node = {
                'node':node,
                'tagName': node,
                'tagIndex': 0,
                'parent_xpath': ""
            } 
            
        else:
        
            node = {
                    'node':node,
                    'tagName': node.split("[")[0],
                    'tagIndex': int(node.split("[")[-1].split("]")[0]),
                    'parent_xpath': str.join("/",xpath_splited[:-1])
            }
        
        return node
        
        pass
    
    
    
#    def map_all(self, node, att, value):
#        
#        self.map(node, fun1 = self.__map_all, args = [att, value])
#        
#        pass
#    
#    
#    def __map_all(self, node, args):
#        
#        
#        
#        return node
#        
#        pass
    
    
    pass




if __name__ == '__main__':
    
#    dr = DOM_Mapper()
#
#    dr.retrieve_DOM_tree('../datasets/extracted_data/0007.json')
    print(dr.DOM.keys())
    #df = pd.DataFrame(dr.toArray(['tagName','mark']))
    #print(df)
    #dr.map(dr.DOM, fun1 = lambda x: x if print(x['xpath']) else x)
    
    #dr.toDotDict()
    
    #dr.map(node = dr.DOM, fun1 = p) 
    #dr.map(node = dr.DOM, fun = )
    #dom_copy = dr.DOM.copy()
    
    #dr.map(node = dr.DOM, fun1 = dr.toArray)
    
    #columns = ['tagName','xpath']
    
    #arr = dr.toArray(columns)
    #dr.update_DOM_arr_file(arr = dr.DOM_arr, directory = '../datasets/DOM_arrs/')
    
    #arr = pd.read_csv(os.path.realpath('../datasets/DOM_arrs/0000.csv'))
    
    #arr = dr.retrieve_DOM_arr_file('../datasets/DOM_arrs/0000.csv')
    #print(dr.DOM_arr_features)
    
    
    #print(dr.xpath_based_node_search(dr.DOM, "/BODY/DIV[0]/NOSCRIPT[17]"))
    
    #print(pd.DataFrame(dr.DOM_arr, columns = columns))
    
    pass
