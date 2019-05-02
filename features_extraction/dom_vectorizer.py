import sys
import os
import pandas as pd
import numpy as np
from cetd import CETD
import itertools
from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN

import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 100)

sys.path.append(os.path.realpath(os.path.abspath('../utilities')))


from dom_mapper import DOM_Mapper






class DOM_Vectorizer(DOM_Mapper):
    
    tagsNum = {}
    idsNum = {}
    classesNum = {}
    
    def __init__(self):
        
        pass
    
# =============================================================================
#     def vectorize(self, node):
#         
#         self.map(node, )
#         
#         pass
# =============================================================================
    
    
# =============================================================================
#     def vectorize(self, xpath):
#         
#         xpath_details = self.xpath_reader(xpath)
#                 
#         if xpath_details['parent_xpath'] != '':
#             self.vectorize(xpath_details['parent_xpath'])
#         
#         
#         if xpath_details['tagName'] not in self.tagsNum:
#             
#            self.tagsNum[xpath_details['tagName']] = len(self.tagsNum)
#             
#            pass
#         
#         pass
# =============================================================================
    
    
    def vectorize(self, node):
        
        node['vect'] = []
        
        self.map(node, fun1 = self.__init_vectorize, fun2 = self.__vectorize, fun4 = self.__end_vectorize)
        
        pass
    
    def get_basic_node_coordinates(self, node):
        
        vect = []
        
        xpath_details = self.xpath_reader(node['xpath'])  
        
        if xpath_details['tagName'] not in self.tagsNum:
            self.tagsNum[xpath_details['tagName']] = len(self.tagsNum)
        
        vect = [self.tagsNum[xpath_details['tagName']], xpath_details['tagIndex']]
        
        return vect
        
        pass
    
    def __init_vectorize(self, node):
        
        node['vect'] += self.get_basic_node_coordinates(node)
        
        return node

        pass
    
    
    def __vectorize(self, node, child):
        
        vect = node['vect'].copy()
        child['vect'] = vect
        
        return node, child
        
        pass
    
    
    def __end_vectorize(self, node):
        
        num_of_elements = (self.DOM['tagsCount'] * 2) - len(node['vect'])
        tail = itertools.repeat(-1, num_of_elements)
        
        node['vect'] += tail
        
        return node
        
        pass
    
    
    def similarity(self, vectors_matrix):
        
        pass
    
    
    def display(self):
        
        vect_mat = np.array(self.reduce(self.DOM, fun1 = self.__init_display, fun2 = self.__display))
        tsne = TSNE(n_components=2).fit_transform(vect_mat)
        return [tsne, vect_mat]
        
        
        pass
    
    def __init_display(self, node):
        
        return [node['vect']]
        pass
    
    def __display(self, val, child_val):
        val += child_val
        return val
        pass
    
    
    def vect2xpath(self, vect):
        
        tagsCoordinates =  [(vect[i*2], vect[(i*2)+1]) for i in range(int(len(vect)/2)) if i < len(vect)][1:]
        xpath = "/BODY"
        
        for tag, i in tagsCoordinates:
            xpath += "/" + list(self.tagsNum.keys())[tag] + "["+str(i)+"]"
            
        return xpath
        pass
    
    
    pass




if __name__ == '__main__':
    
#    vectorizer = DOM_Vectorizer()
#    cetd = CETD()
#    vectorizer.retrieve_DOM_tree('../datasets/extracted_data/0000.json')
#    cetd.count_tags(vectorizer.DOM)
#
#    vectorizer.vectorize(vectorizer.DOM)
    #tsne, mat = vectorizer.display()
    #clustering = DBSCAN(eps=2, min_samples=2).fit(mat)
    
    #plt.scatter(tsne[:,0], tsne[:,1],c = clustering.labels_)
    #con = clustering.labels_ == 80
    #print([i for i,val in enumerate(con) if val == True])
    0, 0, 1, 0, 1, 7, 1, 1, 1, 1, 1, 0, 6, 3, 1, 0, 1, 0
    0, 0, 1, 0, 1, 7, 1, 1, 1, 0, 1, 0, 6, 3, 1, 0, 1, 0
    0, 0, 1, 0, 1, 7, 1, 1, 1, 1, 1, 0, 6, 3, 1, 0, 1, 3
    0, 0, 1, 0, 1, 7, 1, 1, 1, 1, 1, 0, 6, 3, 1, 0, 1, 16
    print(vectorizer.vect2xpath([0, 0, 1, 0, 1, 7, 1, 1, 1, 1, 1, 0, 6, 3, 1, 0, 1, 0]))
    print(vectorizer.xpath_based_node_search(vectorizer.DOM, vectorizer.vect2xpath([0, 0, 1, 0, 1, 7, 1, 1, 1, 1, 1, 0, 6, 3, 1, 0, 1, 0]))['atts'])
    print(vectorizer.meta_data)
    #print(vectorizer.tagsNum)
    
    pass