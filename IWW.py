import extractor.extractor_feeder as ef
from configs import Configs
import os



class IWW:
    

    def __init__(self, configs = Configs()):
        
        self.configs = configs
        
        pass
    


    def extract(self, edge = -1):
    
        ef.feed_extractor(
                self.configs.urls_dataset_path,
                self.configs.extractor_generated_data_directory_path, 
                edge)
        #print(self.configs.extractor_generated_data_directory_path)
        	
        pass
    
    
    
    pass








