import sys
import os
import pandas as pd
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 100)

sys.path.append(os.path.realpath(os.path.abspath('../utilities')))


from dom_mapper import DOM_Mapper



class CLG(DOM_Mapper):
    
    FEATURES_LABELS = ['POS_LEFT', 'POS_RIGHT', 'POS_TOP', 'POS_BOTTOM', 'POS_X', 'POS_Y', 'POS_DIST', 
                        'AREA_SIZE', 'AREA_DIST', 'FONT_COLOR_POPULARITY', 'FONT_SIZE', 'FONT_SIZE_POPULARITY', 
                        'VISIBLE_CHAR', 'TEXT_RATIO', 'TAG_SCORE','TAG_DENSITY', 'LINK_DENSITY']
    
    
    def __init__(self):
        #...
        pass


    def absolute(self):
              
        self.map(self.DOM, fun1 = self.__absolute)
        
        pass
    
    
    def __absolute(self, node):
        
        top = self.reduce(node, fun = lambda x,y: x if x['bounds']['top'] < y['bounds']['top'] else y)
        bottom = self.reduce(node, fun = lambda x,y: x if x['bounds']['bottom'] < y['bounds']['bottom'] else y)
        left = self.reduce(node, fun = lambda x,y: x if x['bounds']['left'] < y['bounds']['left'] else y)
        right = self.reduce(node, fun = lambda x,y: x if x['bounds']['right'] < y['bounds']['right'] else y)
        
        node['CLG'] = {
                'absolute_top':top['bounds']['top'],
                'absolute_bottom':bottom['bounds']['bottom'],
                'absolute_left':left['bounds']['left'],
                'absolute_right':right['bounds']['right'],                
        }
    
        
        return node        
        
        pass

    
    
    pass





if __name__ == '__main__':
    
    clg = CLG()
    clg.retrieve_DOM_tree(os.path.realpath('../datasets/extracted_data/0000.json'))
    #arr = clg.toArray(features = ['tagName','xpath'])
    #print(arr)
    clg.absolute()
    print((clg.DOM['children'][0]['children'][13]['children'][0]['CLG']))
    pass