import sys
import os

sys.path.append(os.path.realpath(os.path.abspath('../utilities')))


from dom_mapper import DOM_Mapper




class CETD(DOM_Mapper):
    
    
    def __init__(self):
        super().__init__()
        pass
    
    
    
    def count_tags(self, node):
        
        node['tagsCount'] = len(node['children'])
        
        for child in node['children']:
            self.count_tags(child)
            node['tagsCount'] += child['tagsCount']
            
        
        pass
    
    
    def text_density(self, node):
        tagsCount = (node['tagsCount'] if node['tagsCount'] > 0 else 1)
        node['textDensity'] = len(node['text'])/tagsCount
        
        return node
        
        pass
    
    
    def density_sum(self, node):
          
        node['densitySum'] = 0
        for child in node['children']:            
            self.density_sum(child)
            node['densitySum'] += child['textDensity']
        
        pass
    
    
    def thresholding(self, node):
        #...        
        pass
    
    
    def mark_content(self, node):
        #...
        pass
    
    
    
    def visual_importance(self, node):
        #...
        pass
    
    
    def hybrid_text_density(self, node):
        
        
        pass
    
    
    pass


if __name__ == '__main__':
    
    #cetd = CETD()
    #cetd.retrieve_DOM_tree(os.path.realpath('../datasets/extracted_data/0000.json'))
    #cetd.count_tags(cetd.DOM)
    
    #cetd.map(node = cetd.DOM, fun1 = cetd.text_density)
    #cetd.update_DOM_tree()
    #cetd.density_sum(cetd.DOM)
    
    pass



