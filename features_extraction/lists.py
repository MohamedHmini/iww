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





class Lists(DOM_Mapper):
    
    def __init__(self):
        
        
        
        pass
    
# =============================================================================
#     def vectorize(self, node):
#             
#         vect = self.reduce(node, fun1 = self.__init_vectorize, fun2 = self.__vectorize)
#         return vect
#     
#         pass
#     
#     
#     def __init_vectorize(self, node):
#         
#         vect = []
#         vect.append(node['LISTS']['relative'].values())
#         return vect
#     
#         pass
#     
#     def __vectorize(self, val, childval):
#         val += childval
#         return val
#     
#         pass
# =============================================================================
    
    
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
#        node['LISTS']['absolute']['top'] = node['bounds']['top']
#        node['LISTS']['absolute']['bottom'] = node['bounds']['bottom']
#        node['LISTS']['absolute']['left'] = node['bounds']['left']
#        node['LISTS']['absolute']['right'] = node['bounds']['right']
#        node['LISTS']['absolute']['x'] = node['bounds']['x']
#        node['LISTS']['absolute']['y'] = node['bounds']['y']
        
        
        node['LISTS']['absolute']['font-size'] = node['style']['font-size']
        
        node['LISTS']['absolute']['font-family'] = {}
        node['LISTS']['absolute']['font-family'][node['style']['font-family'].lower()] = 1
        
        node['LISTS']['absolute']['color'] = {}
        node['LISTS']['absolute']['color'][node['style']['color']] = 1
        
        node['LISTS']['absolute']['background-color'] = {}
        node['LISTS']['absolute']['background-color'][node['style']['background-color']] = 1
        
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
#        parent['LISTS']['absolute']['top'] += child['LISTS']['absolute']['top']
#        parent['LISTS']['absolute']['bottom'] += child['LISTS']['absolute']['bottom']
#        parent['LISTS']['absolute']['left'] += child['LISTS']['absolute']['left']
#        parent['LISTS']['absolute']['right'] += child['LISTS']['absolute']['right']
#        parent['LISTS']['absolute']['x'] += child['LISTS']['absolute']['x']
#        parent['LISTS']['absolute']['y'] += child['LISTS']['absolute']['y']
        
        
        parent['LISTS']['absolute']['font-size'] += child['LISTS']['absolute']['font-size']
        parent['LISTS']['absolute']['font-family'].update(child['LISTS']['absolute']['font-family'])
        parent['LISTS']['absolute']['background-color'].update(child['LISTS']['absolute']['background-color'])
        parent['LISTS']['absolute']['color'].update(child['LISTS']['absolute']['color'])
#        parent['LISTS']['absolute']['classes'].update(child['LISTS']['absolute']['classes'])

        
        parent['LISTS']['absolute']['bag-of-classes'] = self.mergeDicts(
                parent['LISTS']['absolute']['bag-of-classes'], 
                child['LISTS']['absolute']['bag-of-classes']
                )
        
        
        return parent, child
        
        pass
    
    
    def __end_absolute(self, node):
        
# =============================================================================
#         node['LISTS']['absolute']['width'] /= (len(node['children']) + 1)
#         node['LISTS']['absolute']['height'] /= (len(node['children']) + 1)
#         node['LISTS']['absolute']['area'] /= (len(node['children']) + 1)
#         node['LISTS']['absolute']['top'] /= (len(node['children']) + 1)
#         node['LISTS']['absolute']['bottom'] /= (len(node['children']) + 1)
#         node['LISTS']['absolute']['left'] /= (len(node['children']) + 1)
#         node['LISTS']['absolute']['right'] /= (len(node['children']) + 1)
#         node['LISTS']['absolute']['x'] /= (len(node['children']) + 1)
#         node['LISTS']['absolute']['y'] /= (len(node['children']) + 1)
# =============================================================================
        node['LISTS']['absolute']['font-family-count'] = len(node['LISTS']['absolute']['font-family'])
        node['LISTS']['absolute']['background-color-count'] = len(node['LISTS']['absolute']['background-color'])
        node['LISTS']['absolute']['color-count'] = len(node['LISTS']['absolute']['color'])

        
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
    
    
    def create_bag_of_classes_ratios_list(self, child, parent):
        
        ratios = [ child[pi]/pv if (pi in child.keys()) == True else 0 for pi,pv in parent.items()]
        
        return ratios
        
        pass
    
    
    
    def __relative(self, parent, child):
        
        child['LISTS']['relative'] = {}
        child['LISTS']['relative']['width'] = self.child_parent_ratio(child['LISTS']['absolute']['width'],  parent['LISTS']['absolute']['width'])
        child['LISTS']['relative']['height'] = child['LISTS']['absolute']['height'] / parent['LISTS']['absolute']['height'] if  parent['LISTS']['absolute']['height'] != 0 else 0
        child['LISTS']['relative']['area'] = child['LISTS']['absolute']['area'] / parent['LISTS']['absolute']['area'] if  parent['LISTS']['absolute']['area'] != 0 else 0
#        child['LISTS']['relative']['top'] = child['LISTS']['absolute']['top'] / parent['LISTS']['absolute']['top'] if  parent['LISTS']['absolute']['top'] != 0 else 0
#        child['LISTS']['relative']['bottom'] = child['LISTS']['absolute']['bottom'] / parent['LISTS']['absolute']['bottom'] if  parent['LISTS']['absolute']['bottom'] != 0 else 0
#        child['LISTS']['relative']['left'] = child['LISTS']['absolute']['left'] / parent['LISTS']['absolute']['left'] if  parent['LISTS']['absolute']['left'] != 0 else 0
#        child['LISTS']['relative']['right'] = child['LISTS']['absolute']['right'] / parent['LISTS']['absolute']['right'] if  parent['LISTS']['absolute']['right'] != 0 else 0
#        child['LISTS']['relative']['x'] = child['LISTS']['absolute']['x'] / parent['LISTS']['absolute']['x'] if  parent['LISTS']['absolute']['x'] != 0 else 0
#        child['LISTS']['relative']['y'] = child['LISTS']['absolute']['y'] / parent['LISTS']['absolute']['y'] if  parent['LISTS']['absolute']['y'] != 0 else 0
#        child['LISTS']['relative']['centerX'] = child['LISTS']['absolute']['centerX'] / parent['LISTS']['absolute']['centerX'] if  parent['LISTS']['absolute']['centerX'] != 0 else 0
#        child['LISTS']['relative']['centerY'] = child['LISTS']['absolute']['centerY'] / parent['LISTS']['absolute']['centerY'] if  parent['LISTS']['absolute']['centerY'] != 0 else 0
        
        child['LISTS']['relative']['font-size'] = child['LISTS']['absolute']['font-size'] / parent['LISTS']['absolute']['font-size'] if  parent['LISTS']['absolute']['font-size'] != 0 else 0
        child['LISTS']['relative']['background-color-count'] = self.child_parent_ratio(child['LISTS']['absolute']['background-color-count'], parent['LISTS']['absolute']['background-color-count'])
        child['LISTS']['relative']['color-count'] = self.child_parent_ratio(child['LISTS']['absolute']['color-count'], parent['LISTS']['absolute']['color-count'])
        child['LISTS']['relative']['font-family-count'] = self.child_parent_ratio(child['LISTS']['absolute']['font-family-count'], parent['LISTS']['absolute']['font-family-count'])


        child['LISTS']['relative']['tagsCount'] = child['tagsCount'] / parent['tagsCount'] if  parent['tagsCount'] != 0 else 0
#        child['LISTS']['relative']['densitySum'] = child['densitySum'] / parent['densitySum'] if  parent['densitySum'] != 0 else 0
        

        child['LISTS']['relative']['bag-of-classes'] = self.create_bag_of_classes_ratios_list(
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
    
    
    def __init_adjust(self, node):
        
        nbr_children = len(node['children'])
        expected_vect = np.full(nbr_children, float(1/float(nbr_children)) if nbr_children !=0 else 0)
        
        nbr_classes = len(node['LISTS']['absolute']['bag-of-classes'])
        classes_expected_vect = np.full(nbr_classes, float(1/float(nbr_children)) if nbr_children !=0 else 0)

        
        classes_coherence = pw.vectors_coherence(
                classes_expected_vect,
                [
                        child['LISTS']['relative']['bag-of-classes'] 
                        for child in node['children']
                ]
                )
        
        
        node['LISTS']['adjust'] = {}
        node['LISTS']['adjust']['expected_vect'] = expected_vect
        node['LISTS']['adjust']['classes-expected-vect'] = classes_expected_vect
        node['LISTS']['adjust']['bag-of-classes'] = []
        node['LISTS']['adjust']['bag-of-classes-coherence'] = classes_coherence
        node['LISTS']['adjust']['width'] = []
        node['LISTS']['adjust']['height'] = []
        node['LISTS']['adjust']['area'] = []
        node['LISTS']['adjust']['font-size'] = []
        node['LISTS']['adjust']['background-color-count'] = []
        node['LISTS']['adjust']['color-count'] = []
        node['LISTS']['adjust']['font-family-count'] = []
        node['LISTS']['adjust']['font-size'] = []
        node['LISTS']['adjust']['tagsCount'] = []
#        node['LISTS']['adjust']['densitySum'] = []
        
        
        
        
        node['LISTS']['adjust']['multi-tag-subtree'] = 1 if len(node['children']) >= 2 else 0
        node['LISTS']['adjust']['standard-list-tag'] = 1 if self.isListTag(node['tagName']) else 0
        
        return node
        
        pass
    
    
    def __adjust(self, parent, child):
        
        
        parent['LISTS']['adjust']['width'].append(child['LISTS']['relative']['width'])
        parent['LISTS']['adjust']['height'].append(child['LISTS']['relative']['height'])
        parent['LISTS']['adjust']['area'].append(child['LISTS']['relative']['area'])
        parent['LISTS']['adjust']['font-size'].append(child['LISTS']['relative']['font-size'])
        parent['LISTS']['adjust']['font-family-count'].append(child['LISTS']['relative']['font-family-count'])
        parent['LISTS']['adjust']['background-color-count'].append(child['LISTS']['relative']['background-color-count'])
        parent['LISTS']['adjust']['color-count'].append(child['LISTS']['relative']['color-count'])
        parent['LISTS']['adjust']['tagsCount'].append(child['LISTS']['relative']['tagsCount'])
#        parent['LISTS']['adjust']['densitySum'].append(child['LISTS']['relative']['densitySum'])
        
        classes_sim = 1
        
        try:
        
            classes_sim = cosine_similarity(
                    [child['LISTS']['relative']['bag-of-classes']],
                    [parent['LISTS']['adjust']['classes-expected-vect']])[0][0]
        except:
            pass
        
        
        
        parent['LISTS']['adjust']['bag-of-classes'].append(classes_sim)
        
        return parent, child
        
        pass
    
    
    def __end_adjust(self, node):
        
        if node['LISTS']['adjust']['expected_vect'].shape[0] != 0:
            node['LISTS']['adjust']['width'] = 1- euclidean_distances([node['LISTS']['adjust']['width']], [node['LISTS']['adjust']['expected_vect']])[0][0]
            node['LISTS']['adjust']['height'] = 1- euclidean_distances([node['LISTS']['adjust']['height']], [node['LISTS']['adjust']['expected_vect']])[0][0]
            node['LISTS']['adjust']['area'] = 1- euclidean_distances([node['LISTS']['adjust']['area']], [node['LISTS']['adjust']['expected_vect']])[0][0]
            node['LISTS']['adjust']['font-size'] = 1- euclidean_distances([node['LISTS']['adjust']['font-size']], [node['LISTS']['adjust']['expected_vect']])[0][0]
            node['LISTS']['adjust']['font-family-count'] = 1- euclidean_distances([node['LISTS']['adjust']['font-family-count']], [node['LISTS']['adjust']['expected_vect']])[0][0]
            node['LISTS']['adjust']['background-color-count'] = 1- euclidean_distances([node['LISTS']['adjust']['background-color-count']], [node['LISTS']['adjust']['expected_vect']])[0][0]
            node['LISTS']['adjust']['color-count'] = 1- euclidean_distances([node['LISTS']['adjust']['color-count']], [node['LISTS']['adjust']['expected_vect']])[0][0]
            node['LISTS']['adjust']['tagsCount'] = 1- euclidean_distances([node['LISTS']['adjust']['tagsCount']], [node['LISTS']['adjust']['expected_vect']])[0][0]
#            node['LISTS']['adjust']['densitySum'] = cosine_similarity([node['LISTS']['adjust']['densitySum']], [node['LISTS']['adjust']['expected_vect']])[0][0]

        else:
            
            node['LISTS']['adjust']['width'] = 0
            node['LISTS']['adjust']['height'] = 0
            node['LISTS']['adjust']['area'] = 0
            node['LISTS']['adjust']['font-size'] = 0
            node['LISTS']['adjust']['font-family-count'] = 0
            node['LISTS']['adjust']['background-color-count'] = 0
            node['LISTS']['adjust']['color-count'] = 0
            node['LISTS']['adjust']['tagsCount'] = 0
#            node['LISTS']['adjust']['densitySum'] = 0

            
            pass
        
        
        expected_val = len(node['LISTS']['adjust']['bag-of-classes'])
        expected_val = expected_val if expected_val != 0 else 1
        node['LISTS']['adjust']['classes-coherence'] = (sum(node['LISTS']['adjust']['bag-of-classes']) * 100)/expected_val
        
            
        return node
        
        pass
    
    
    
    
    def markAll(self, xpaths, labels):
        
        for xpath in range(len(xpaths)):
            
            node = self.xpath_based_node_search(self.DOM, xpaths[xpath])
            node['mark'] = str(labels[xpath])
            node['LISTS']={}
            
            pass
                
        
        pass
    
    
    def remove(self, node):
        
        self.map(node, fun1 = self.__remove)
        pass
    
    
    def __remove(self, node):
        
        if len(node['children']) < 4:
            node['mark'] = "-1"
        
        return node
        pass
            
    
    pass






if __name__ == '__main__':
    
#    lists = Lists()
#    cetd = CETD()
#    lists.retrieve_DOM_tree(os.path.realpath('../datasets/extracted_data/0003.json'))
#
#    cetd.count_tags(lists.DOM)
#    cetd.text_density(lists.DOM)
#    cetd.density_sum(lists.DOM)
#    lists.absolute(lists.DOM)
#    lists.relative(lists.DOM)
#    lists.adjust(lists.DOM)
#    print(lists.DOM['children'][0]['LISTS']['relative']['bag-of-classes'])
#    features = [
#            'xpath','LISTS.adjust.width', 'LISTS.adjust.height', 'LISTS.adjust.area', 
#            'LISTS.adjust.font-size', 'LISTS.adjust.font-family-count', 'LISTS.adjust.background-color-count', 
#            'LISTS.adjust.color-count', 'LISTS.adjust.classes-coherence','LISTS.adjust.tagsCount', 
#            'LISTS.adjust.multi-tag-subtree', 'LISTS.adjust.standard-list-tag']
#    features = ['xpath','LISTS.adjust.bag-of-classes-coherence']
###    
#    arr = lists.flatten(lists.DOM, features = features)
#    xpaths = arr[:,0]
#    X= arr[:,1:]
#    print(X)
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
#    
#    lists.update_DOM_tree()
#    df = pd.DataFrame(X, columns = features[1:])
#    print(df[df['LISTS.adjust.bag-of-classes-coherence'] >= 0.8])
    
    pass