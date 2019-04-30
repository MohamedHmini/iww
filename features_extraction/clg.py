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

    
    
    pass





if __name__ == '__main__':
    
    clg = CLG()
    clg.retrieve_DOM_tree(os.path.realpath('../datasets/extracted_data/0000.json'))
    arr = clg.toArray(features = ['tagName','xpath'])
    print(arr)
    
    pass