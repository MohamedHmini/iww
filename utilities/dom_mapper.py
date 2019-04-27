import os
import json




class DOM_Mapper:
    
    
    DOM = {}
    meta_data = {}
    
    
    def __init__(self):
        # ...
        pass
    
    
    def retrieve_DOM_tree(self, file_path):
    
        self.DOM_file_path = os.path.realpath(file_path)
        
        file = open(file_path, 'r', encoding = 'UTF-8')
        page_data = json.load(file)
        self.DOM = page_data['DOM']
        self.meta_data = page_data['meta_data']
        
        file.close()
        pass
    
    
    
    def map(self, node = None, 
            fun1 = (lambda x: x), 
            fun2 = (lambda x, y: (x,y)), 
            fun3 = (lambda x, y: (x,y)), 
            fun4 = (lambda x: x), 
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
    
    
    
    def update_DOM_tree(self):
        
        file = open(self.DOM_file_path, 'w', encoding = 'UTF-8')
        
        DOM_str = json.dumps({
                'DOM':self.DOM,
                'meta_data':self.meta_data
                })
        
        file.write(DOM_str)
        
        file.close()
        
        pass
    
    
    def test(self, arg):
        print("from parent : {}".format(arg))
        
    
        
        pass
    
    
    pass


def p(node):
    
    print(node['tagName'])
    return node


if __name__ == '__main__':
    
    dr = DOM_Mapper()

    dr.retrieve_DOM_tree('../datasets/extracted_data/0000.json')
    
    dr.map(node = dr.DOM, fun1 = p) 
    #dr.map(node = dr.DOM, fun = )
    
    
    pass