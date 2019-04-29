import sys
import os

sys.path.append(os.path.realpath(os.path.abspath('../utilities')))


from dom_mapper import DOM_Mapper




class CETD(DOM_Mapper):
    
    max_density_sum = 0    
    
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
            
        self.max_density_sum =  node['densitySum'] if node['densitySum'] > self.max_density_sum else self.max_density_sum
        
        pass
    
    
    
    def mark_DOM_node(self, node, mark):
        
        node['mark'] = mark        
        
        for child in node['children']:
            self.mark_DOM_node(child, mark)
        
        pass
     
    
    
    def thresholding(self):
        
        threshold = -1.0
        node = self.search_DOM_node(self.DOM, att = 'densitySum', value = self.max_density_sum)
        threshold = node['textDensity']
        self.mark_DOM_node(node, 1)
        
        parent = self.xpath_based_node_search(self.DOM, node['parent_xpath'])
        
        while parent != None:        
            if (threshold - parent['textDensity']) > -1:
                threshold = parent['textDensity']
                
            self.mark_DOM_node(parent, 2)
            
            parent = self.xpath_based_node_search(self.DOM, parent['parent_xpath'])
            pass
        
        self.threshold = threshold
        
        return self.threshold
        
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
    
    cetd = CETD()
    cetd.retrieve_DOM_tree(os.path.realpath('../datasets/extracted_data/0000.json'))
    cetd.count_tags(cetd.DOM)
    
    cetd.map(node = cetd.DOM, fun1 = cetd.text_density)
    #cetd.update_DOM_tree()
    cetd.density_sum(cetd.DOM)
    #arr = cetd.toArray(['tagName','textDensity','densitySum','parent_xpath'])
    
    print(cetd.thresholding())
    pass



