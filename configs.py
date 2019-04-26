import os





class Configs:
    
    project_path = ""
    urls_dataset_path = ""
    extractor_generated_data_directory_path = ""
    
    def __init__(self):
        
        pass
    
    
    def set_configs(self, current_file_directory, default = False):
    
    
        if default == True:
            
                self.project_path = os.path.realpath(os.path.abspath(os.path.dirname(current_file_directory)))
                self.urls_dataset_path = os.path.realpath(os.path.join(self.project_path, 'datasets/webpages_urls.txt'))
                self.extractor_generated_data_directory_path = os.path.realpath(os.path.join(self.project_path, 'datasets/extracted_data'))
            
        elif default == False:
            
            pass
        
        pass
    
    pass


