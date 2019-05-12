import sys
import os
import pandas as pd
import numpy as np
from cetd import CETD
import itertools
from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 100)



sys.path.append(os.path.realpath(os.path.abspath('../utilities')))


from dom_mapper import DOM_Mapper
import pairwise as pw





class Lists_Detector(DOM_Mapper):
    
    def __init__(self):
        
#        self.expected_vect = [1,1,1,1,1,1,1,1,1]
        
        pass
    
    
    def apply(self, 
              node, 
              coherence_threshold = (0.95,1), 
              sub_tags_threshold = 2, 
              mode = "full"):
        
        self.coherence_threshold = coherence_threshold
        self.sub_tags_threshold = sub_tags_threshold
        
        cetd = CETD()
        cetd.apply(self.DOM)

        self.absolute(node)
        self.relative(node)
        self.adjust(node)
        
        features = [
            'xpath','LISTS.adjust.width', 'LISTS.adjust.height', 'LISTS.adjust.area', 
            'LISTS.adjust.font-size', 'LISTS.adjust.font-family', 'LISTS.adjust.background-color', 
            'LISTS.adjust.color', 'LISTS.adjust.bag-of-classes-coherence','LISTS.adjust.tagsCount']
        
        self.expected_vect = np.full(len(features)-1,1)
    
        arr = self.flatten(node, features = features)
        self.xpaths = arr[:,0]
        self.X= arr[:,1:]
        
        self.get_final_results(self.xpaths, self.X)
        self.mark_results(node)
        
        pass
    
    
    def original(self):
        
        self.map(self.DOM, fun1 = self.__init_original)
        
        pass
    
    
    def __init_original(self, node):
        
        node['bounds']['centerX'] = node['bounds']['width']/2
        node['bounds']['centerY'] = node['bounds']['height']/2
        
        return node
        
        pass
    
    
    
    def absolute(self, node):
        
        self.map(
                node, 
                fun1 = self.__init_absolute, 
                fun3 = self.__absolute, 
                fun4 = self.__end_absolute
                )
        
        pass
    
    
    def __init_absolute(self, node):
        
        node['LISTS'] = {}
        node['LISTS']['absolute'] = {}
        node['LISTS']['absolute']['width'] = node['bounds']['width']
        node['LISTS']['absolute']['height'] = node['bounds']['height']
        node['LISTS']['absolute']['area'] = node['bounds']['width']*node['bounds']['height']
        
        node['LISTS']['absolute']['font-size'] = {node['style']['font-size']:1}
        node['LISTS']['absolute']['font-family'] = {node['style']['font-family'].lower():1}
        node['LISTS']['absolute']['color'] = {node['style']['color']:1}
        node['LISTS']['absolute']['background-color'] = {node['style']['background-color']:1}
        node['LISTS']['absolute']['bag-of-classes'] = { c: 1 for c in node['atts']['class'] } if 'class' in node['atts'].keys() else {}
        
        
        
        return node
        
        pass
    
    
    def mergeDicts(self, parent, child):
        
        parent = dict([
                (pi, pv+child[pi]) if pi in child.keys() else (pi, pv)
                for pi, pv in parent.items()                
        ])
        
        cv = child.copy()
        cv.update(parent)
        parent = cv
        
        return parent
        
        pass
    
    
    def __absolute(self, parent, child):
        
        parent['LISTS']['absolute']['width'] += child['LISTS']['absolute']['width']
        parent['LISTS']['absolute']['height'] += child['LISTS']['absolute']['height']
        parent['LISTS']['absolute']['area'] += child['LISTS']['absolute']['area']
        
        parent['LISTS']['absolute']['font-size'] = self.mergeDicts(
                parent['LISTS']['absolute']['font-size'],
                child['LISTS']['absolute']['font-size']
                )
        
        parent['LISTS']['absolute']['font-family'] = self.mergeDicts(
                parent['LISTS']['absolute']['font-family'],
                child['LISTS']['absolute']['font-family']
                )
        
        parent['LISTS']['absolute']['color'] = self.mergeDicts(
                parent['LISTS']['absolute']['color'],
                child['LISTS']['absolute']['color']
                )

        parent['LISTS']['absolute']['background-color'] = self.mergeDicts(
                parent['LISTS']['absolute']['background-color'],
                child['LISTS']['absolute']['background-color']
                )
        
        parent['LISTS']['absolute']['bag-of-classes'] = self.mergeDicts(
                parent['LISTS']['absolute']['bag-of-classes'], 
                child['LISTS']['absolute']['bag-of-classes']
                )
        
        
        return parent, child
        
        pass
    
    
    def __end_absolute(self, node):

        
        return node
        
        pass
    
       
    
    
    def relative(self, node):
        
        self.map(
                self.DOM,
                fun1 = self.__init_relative,
                fun2 = self.__relative
                 )
        
        pass
    
    
    def __init_relative(self, node):
        
        
        return node
        pass
    
    
    
    def child_parent_ratio(self, child, parent):
        
        return child / parent if  parent != 0 else 0
    
        pass
    
    
    def to_bag_of(self, child, parent):
        
        ratios = [ child[pi]/pv if (pi in child.keys()) == True else 0 for pi,pv in parent.items()]
        
        return ratios
        
        pass
    
    
    
    def __relative(self, parent, child):
        
        child['LISTS']['relative'] = {}
        child['LISTS']['relative']['width'] = self.child_parent_ratio(child['LISTS']['absolute']['width'],  parent['LISTS']['absolute']['width'])
        child['LISTS']['relative']['height'] = child['LISTS']['absolute']['height'] / parent['LISTS']['absolute']['height'] if  parent['LISTS']['absolute']['height'] != 0 else 0
        child['LISTS']['relative']['area'] = child['LISTS']['absolute']['area'] / parent['LISTS']['absolute']['area'] if  parent['LISTS']['absolute']['area'] != 0 else 0


        child['LISTS']['relative']['tagsCount'] = child['CETD']['tagsCount'] / parent['CETD']['tagsCount'] if  parent['CETD']['tagsCount'] != 0 else 0

        
        child['LISTS']['relative']['font-size'] = self.to_bag_of(
                child['LISTS']['absolute']['font-size'],
                parent['LISTS']['absolute']['font-size']
                )
        
        child['LISTS']['relative']['font-family'] = self.to_bag_of(
                child['LISTS']['absolute']['font-family'],
                parent['LISTS']['absolute']['font-family']
                )
        
        child['LISTS']['relative']['color'] = self.to_bag_of(
                child['LISTS']['absolute']['color'],
                parent['LISTS']['absolute']['color']
                )
        
        child['LISTS']['relative']['background-color'] = self.to_bag_of(
                child['LISTS']['absolute']['background-color'],
                parent['LISTS']['absolute']['background-color']
                )

        child['LISTS']['relative']['bag-of-classes'] = self.to_bag_of(
                child['LISTS']['absolute']['bag-of-classes'],
                parent['LISTS']['absolute']['bag-of-classes']
                )

        
        return parent, child
    
        pass
    
    
    
    def adjust(self, node):
        
        self.map(
                node, 
                fun1 = self.__init_adjust, 
                fun2 = self.__adjust, 
                fun4 = self.__end_adjust
                )
        
        pass
    
    def isListTag(self, tagname):
        
        return True if tagname == 'UL' or tagname == 'TR' else False
        
        pass
    
    

    def feature_coherence(self, node, absolute_feature, relative_feature):
        
        abs_val = self.get_feature_by_path(node, absolute_feature)
        
        nbr_children = len(node['children'])
        nbr_elements = len(abs_val)
        expected_vect =  np.full(nbr_elements, float(1/float(nbr_children)) if nbr_children !=0 else 0)       
        
        feature_coherence = pw.vectors_coherence(
                expected_vect,
                [
                        self.get_feature_by_path(child, relative_feature) 
                        for child in node['children']
                ]
                )
        
        
        return feature_coherence
        
        
        pass
    
    
    
    def __init_adjust(self, node):
        
        nbr_children = len(node['children'])
        expected_vect = np.full(nbr_children, float(1/float(nbr_children)) if nbr_children !=0 else 0)
        
        
        node['LISTS']['adjust'] = {}
        node['LISTS']['adjust']['expected_vect'] = expected_vect
        node['LISTS']['adjust']['bag-of-classes-coherence'] = self.feature_coherence(node, 'LISTS.absolute.bag-of-classes', 'LISTS.relative.bag-of-classes')
        node['LISTS']['adjust']['width'] = []
        node['LISTS']['adjust']['height'] = []
        node['LISTS']['adjust']['area'] = []
        node['LISTS']['adjust']['background-color'] = self.feature_coherence(node, 'LISTS.absolute.background-color', 'LISTS.relative.background-color')
        node['LISTS']['adjust']['font-size'] = self.feature_coherence(node, 'LISTS.absolute.font-size', 'LISTS.relative.font-size')
        node['LISTS']['adjust']['font-family'] = self.feature_coherence(node, 'LISTS.absolute.font-family', 'LISTS.relative.font-family')
        node['LISTS']['adjust']['color'] = self.feature_coherence(node, 'LISTS.absolute.color', 'LISTS.relative.color')

        node['LISTS']['adjust']['tagsCount'] = []
             
        
        node['LISTS']['adjust']['multi-tag-subtree'] = 1 if len(node['children']) >= 2 else 0
        node['LISTS']['adjust']['standard-list-tag'] = 1 if self.isListTag(node['tagName']) else 0
        
        return node
        
        pass
    
    
    def __adjust(self, parent, child):
        
        
        parent['LISTS']['adjust']['width'].append(child['LISTS']['relative']['width'])
        parent['LISTS']['adjust']['height'].append(child['LISTS']['relative']['height'])
        parent['LISTS']['adjust']['area'].append(child['LISTS']['relative']['area'])
        
        parent['LISTS']['adjust']['tagsCount'].append(child['LISTS']['relative']['tagsCount'])
        
        return parent, child
        
        pass
    
    
    def __end_adjust(self, node):
        
        if node['LISTS']['adjust']['expected_vect'].shape[0] != 0:
            node['LISTS']['adjust']['width'] = 1- euclidean_distances([node['LISTS']['adjust']['width']], [node['LISTS']['adjust']['expected_vect']])[0][0]
            node['LISTS']['adjust']['height'] = 1- euclidean_distances([node['LISTS']['adjust']['height']], [node['LISTS']['adjust']['expected_vect']])[0][0]
            node['LISTS']['adjust']['area'] = 1- euclidean_distances([node['LISTS']['adjust']['area']], [node['LISTS']['adjust']['expected_vect']])[0][0]
            node['LISTS']['adjust']['tagsCount'] = 1- euclidean_distances([node['LISTS']['adjust']['tagsCount']], [node['LISTS']['adjust']['expected_vect']])[0][0]

        else:
            
            node['LISTS']['adjust']['width'] = 0
            node['LISTS']['adjust']['height'] = 0
            node['LISTS']['adjust']['area'] = 0
            node['LISTS']['adjust']['tagsCount'] = 0

            
            pass
        
# =============================================================================
#         features = [
#             'xpath','LISTS.adjust.width', 'LISTS.adjust.height', 'LISTS.adjust.area', 
#             'LISTS.adjust.font-size', 'LISTS.adjust.font-family', 'LISTS.adjust.background-color', 
#             'LISTS.adjust.color', 'LISTS.adjust.classes-coherence','LISTS.adjust.tagsCount']
#         
#         final_expected_vect = [1,1,1,1,1,1,1,1,1]
#                 
#         self.flatten_single_node(features)
# =============================================================================
            
        return node
        
        pass
    
    
    def get_final_results(self, xpaths, X):
        
        nbr_nodes = len(xpaths)
        
        for i in range(nbr_nodes):
            node = self.xpath_based_node_search(self.DOM, xpaths[i])
            euclidean_sim = pw.similarity(self.expected_vect, X[i,:], max_val = 0)
            node['LISTS']['coherence'] = str(euclidean_sim)
                    
        
        pass
    
    
    
    def mark_results(self, node):
        
        
        self.map(node, fun1 = self.__mark_results)
        
        pass
    
    
    def __mark_results(self,node):
               
        node['LISTS']['mark'] = "1" if float(node['LISTS']['coherence']) >= self.coherence_threshold[0] and float(node['LISTS']['coherence']) <= self.coherence_threshold[1] and len(node['children']) > self.sub_tags_threshold else "0"
        
        return node
        
        pass
    
    
    
    def markAll(self, xpaths, labels):
        
        for xpath in range(len(xpaths)):
            
            node = self.xpath_based_node_search(self.DOM, xpaths[xpath])
            node['LISTS']['mark'] = str(labels[xpath])
#            node['LISTS'] = {}
            
            pass
                
        
        pass
    
    
    def remove(self, node):
        
        self.map(node, fun1 = self.__remove)
        pass
    
    
    def __remove(self, node):
        
        if len(node['children']) < 4:
            node['LISTS']['mark'] = "-1"
        
        return node
        pass
            
    
    pass






if __name__ == '__main__':
    
#    lists = Lists_Detector()
#    cetd = CETD()
#    lists.retrieve_DOM_tree(os.path.realpath('../datasets/extracted_data/0000.json'))
#    lists.detectLists(lists.DOM, coherence_threshold = (0.80,1), sub_tags_threshold = 1)
#    lists.coherence_threshold =(0.80,1)
#    lists.get_final_results(lists.xpaths, lists.X)
#    lists.mark_results(lists.DOM)
    lists.update_DOM_tree()
#    print(lists.DOM['tagsCount'])
#    DOM = lists.DOM
#    meta = lists.meta_data
#    cetd.count_tags(lists.DOM)
#    cetd.text_density(lists.DOM)
#    cetd.density_sum(lists.DOM)
#    lists.absolute(lists.DOM)
#    lists.relative(lists.DOM)
#    lists.adjust(lists.DOM)
#    print(lists.DOM['children'][0]['children'][0]['children'][0]['LISTS']['adjust']['font-size'])
#    print(len(lists.DOM['children'][0]['children']))
#    features = [
#            'xpath','LISTS.adjust.width', 'LISTS.adjust.height', 'LISTS.adjust.area', 
#            'LISTS.adjust.font-size', 'LISTS.adjust.font-family', 'LISTS.adjust.background-color', 
#            'LISTS.adjust.color', 'LISTS.adjust.bag-of-classes-coherence','LISTS.adjust.tagsCount']
#    features = ['xpath','LISTS.adjust.bag-of-classes-coherence']
#    
#    arr = lists.flatten(lists.DOM, features = features)
#    xpaths = arr[:,0]
#    X= arr[:,1:]
#    print(X)
#    lists.get_final_results(xpaths, X)
#    lists.mark_results(lists.DOM)
#    print(lists.DOM['children'][0]['children'][4]['LISTS']['adjust']['classes-coherence'])
#    print(lists.DOM['children'][0]['children'][4]['LISTS']['adjust']['bag-of-classes'])
#    print(lists.DOM['children'][0]['textDensity'])
#    print(lists.DOM['children'][0]['textDensity'])
#    print(lists.DOM['children'][1]['textDensity'])

#    lists.DOM['LISTS']['relative'] = {}
#    vect = lists.vectorize(node = lists.DOM)
#    print(vect.shape)
    
#    tsne = TSNE(n_components=2).fit_transform(X)
#    km = KMeans(n_clusters = 2)
#    results = km.fit(X)
    
#    fig = plt.figure()
#    ax = fig.add_subplot(111, projection='3d')  
    
#    plt.scatter(tsne[:,0], tsne[:,1], c = results.labels_)
#    lists.markAll(xpaths, results.labels_)
    
     # heuristic based method :
#    lists.remove(lists.DOM)
#    lists.update_DOM_tree()
#    df = pd.DataFrame(X)
#    print(df)
    
    pass
