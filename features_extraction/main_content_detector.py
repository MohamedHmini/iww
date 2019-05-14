import sys
import os
import numpy as np
import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 100)



#sys.path.append(os.path.realpath(os.path.abspath('../')))

from iww.features_extraction.cetd import CETD
from iww.utils.dom_mapper import DOM_Mapper
import iww.utils.pairwise as pw





################   MAIN CONTENT DETECTOR   ########################
class MCD(DOM_Mapper):



    def __init__(self):

        pass
    
    
    
    def apply(self, node, min_ratio_threshold = 0.0, nbr_nodes_threshold = 1):
        
        self.nbr_nodes_threshold = nbr_nodes_threshold
        self.min_ratio_threshold = min_ratio_threshold
        
        cetd = CETD()
        cetd.count_tags(node)
        
        self.origin(node)
        self.relative(node)
        
        
        features = ['xpath','MCD.width','MCD.height','MCD.area','MCD.closeness','MCD.deepness']
        self.expected_vect = np.full(len(features) -1, 1)
    
        arr = self.flatten(node, features)
        X = arr[:,1:]
        xpaths = arr[:,0]
        
        self.get_final_results(xpaths, X)
        
        self.mark_results(node)
            
        pass
    
    
    def __remove_main_nodes(self, node):
        
        node['MCD']['main_node'] = "0"
            
        return node
        pass
    
    def __prepare_integrator_dataframe(self, node, nbr_nodes, condition_features):
        
        features = ["xpath", "MCD.mark", "MCD.iscontent"] + [feature for feature,val in condition_features]
        arr = self.flatten(node, features)
        df = pd.DataFrame(arr, columns = features)
        
        for feature, val in condition_features:
            df = df[df[feature] == val]
        
        df = df.sort_values(['MCD.iscontent'], ascending = False)[:nbr_nodes]
        
        return df
        
        pass
    
    def __ancestry_based_integration(self, node, df):
        
        for element in df.values:                
            is_main_content = element[1] == "1"
                
            if is_main_content == False:
                xpath_details = self.xpath_reader(element[0])
                result = self.__integrate_other_algorithms_results(root = node, parent_xpath = xpath_details['parent_xpath'])
                if result == True:
                    DOM_element = self.xpath_based_node_search(node, element[0])
                    DOM_element["MCD"]["main_node"] = "1"
            else:
                DOM_element = self.xpath_based_node_search(node, element[0])
                DOM_element["MCD"]["main_node"] = "1"
        
        pass
    
    
    def __self_only_based_integration(self, node, df):
        
        df = df[df["MCD.mark"] == "1"]
            
        for element in df.values:
            DOM_element = self.xpath_based_node_search(node, element[0])
            DOM_element["MCD"]["main_node"] = "1"

            pass
        
        pass
    
    def integrate_other_algorithms_results(self, node, nbr_nodes = -1, mode = "ancestry", condition_features = [("LISTS.mark","1")]):
        
        self.map(node = node, fun1 = self.__remove_main_nodes)
        
        df = self.__prepare_integrator_dataframe(node, nbr_nodes, condition_features)
        
        if mode == "ancestry":
            self.__ancestry_based_integration(node, df)                    
        elif mode == "self-only":            
            self.__self_only_based_integration(node, df)            
            
        
        pass
    
    
    def __integrate_other_algorithms_results(self, root, parent_xpath):
        
        parent_node = self.xpath_based_node_search(root, parent_xpath)
        
        if parent_node['MCD']['mark'] == "1":
            print(print(parent_node['xpath']))
            return True
       
        if parent_node['parent_xpath'] != '':
            return self.__integrate_other_algorithms_results(root, parent_node['parent_xpath'])            
        
        return False
        
        pass
    
    
    
    def origin(self, node):
        
        node['bounds']['centerX'] = node['bounds']['width'] / 2
        node['bounds']['centerY'] = node['bounds']['height'] / 2
        
        pass
    
    
    def relative(self, node):
        
        self.map(node, fun1 = self.__relative)
        
        pass
    
    
    def __relative(self, node):
        
        node['MCD'] = {}
        node['MCD']['width'] = node['bounds']['width'] / self.DOM['bounds']['width'] if self.DOM['bounds']['width'] != 0 else 1
        node['MCD']['height'] = node['bounds']['height'] / self.DOM['bounds']['height'] if self.DOM['bounds']['height'] != 0 else 1
        node['MCD']['area'] = (node['bounds']['width']*node['bounds']['height']) / (self.DOM['bounds']['width']*self.DOM['bounds']['height'])
        
        self.origin(node)
        
        node['MCD']['closeness'] = 1 - pw.simple_euclidean_similarity(
                [
                        node['bounds']['centerX'],
                        node['bounds']['centerY']
                ],
                [
                        self.DOM['bounds']['centerX'],
                        self.DOM['bounds']['centerY']  
                ]
                )
        
        
        node['MCD']['deepness'] = 1 - (node['CETD']['tagsCount'] / self.DOM['CETD']['tagsCount'])

        
        return node
        
        pass
    
    
    def get_final_results(self, xpaths, X):
        
        nbr_nodes = len(xpaths)
        
        for i in range(nbr_nodes):
            node = self.xpath_based_node_search(self.DOM, xpaths[i])
            euclidean_sim = pw.similarity(self.expected_vect, X[i,:], max_val = 0)
            node['MCD']['iscontent'] = str(euclidean_sim)
                    
        
        pass
    
    
    
    
    def mark_results(self, node):
        
        self.map(node, fun1 = self.__mark_results)
        
        features = ["xpath", "MCD.iscontent"]
        arr = self.flatten(node, features)
                
        df = pd.DataFrame(arr, columns = features)
        df["MCD.iscontent"] = pd.to_numeric(df["MCD.iscontent"])
        df = df[df['MCD.iscontent'] > self.min_ratio_threshold]
        df = df.sort_values(['MCD.iscontent'], ascending = False)[:self.nbr_nodes_threshold]
        
        for element in df.values:
            
            DOM_node = self.xpath_based_node_search(node, element[0])
            DOM_node['MCD']['mark'] = "1"
                        
            pass
        
        
        pass
    
    
    def __mark_results(self,node):
                
        node['MCD']['mark'] = "0"
        
        return node



    pass




if __name__ == "__main__":

    mcd = MCD()
    mcd.retrieve_DOM_tree(os.path.realpath('../datasets/extracted_data/0007.json'))
#    mcd.apply(mcd.DOM, nbr_nodes_threshold = 1)
    mcd.mark_main_nodes(node = mcd.DOM, mode = "ancestry")
#    print(mcd.webpage_url)
#     mcd.apply(mcd.DOM, min_ratio_threshold = 0.5, nbr_nodes_threshold = 3)
    
#    mcd.update_DOM_tree()
    
    arr = mcd.flatten(mcd.DOM, features = ['xpath', 'MCD.main_node'])
    print(arr[arr[:,1] == "1"])
    

    pass
