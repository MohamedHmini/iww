import extractor.extractor_feeder as ef
from configs import Configs
import os



class IWW:
    
    configs = Configs()


    def __init__(self):
        
        pass
    


    def extract(self):
    
    	ef.feed_extractor(self.configs.urls_dataset_path,self.configs.extractor_generated_data_directory_path)
    
    	pass
    
    
    
    pass








