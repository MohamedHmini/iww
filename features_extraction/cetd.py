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
    
    
    def calculate_text_density(self, node):
        
        node['textDensity'] = len(node['text'])/(node['tagsCount'] if node['tagsCount'] > 0 else 1)  
        return node
        
        pass
    
    
    def calculate_density_sum(self, node):
          
        node['densitySum'] = 0
        for child in node['children']:            
            self.calculate_density_sum(child)
            node['densitySum'] += child['textDensity']
            
            
        
        pass
    
    
    
    pass


if __name__ == '__main__':
    
    #cetd = CETD()
    #cetd.retrieve_DOM_tree(os.path.realpath('../datasets/extracted_data/0000.json'))
    #cetd.count_tags(cetd.DOM)
    
    #cetd.map(node = cetd.DOM, fun1 = cetd.calculate_text_density)
    #cetd.update_DOM_tree()
    #cetd.calculate_density_sum(cetd.DOM)
    
    pass



