import os





class Configs:
    
    project_path = ""
    urls_dataset_path = ""
    extractor_generated_data_directory_path = ""
    
    def __init__(self):
        
        pass
    
    
    def set_configs(
            self, 
            current_file_directory = '',
            project_path = '', 
            urls_dataset_path = '', 
            extractor_generated_data_directory_path = '', 
            default = False):
    
    
        if default == True:
            
                self.project_path = os.path.realpath(os.path.abspath(os.path.dirname(current_file_directory)))
                self.urls_dataset_path = os.path.realpath(os.path.join(self.project_path, 'datasets/webpages_urls.txt'))
                self.extractor_generated_data_directory_path = os.path.realpath(os.path.join(self.project_path, 'datasets/extracted_data'))
            
        elif default == False:
            
                self.project_path = project_path
                self.urls_dataset_path = urls_dataset_path
                self.extractor_generated_data_directory_path = extractor_generated_data_directory_path
            
            
        
        pass
    
    
    pass


