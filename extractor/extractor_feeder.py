import os
import sys
import subprocess




project_path = os.path.realpath(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..'))



def feed_extractor(urls_path, destination_directory):
    
    urls_dataset_file = open(urls_path,'r')    
    urls_dataset = urls_dataset_file.readlines()
    urls_dataset = [url[:-1] if url[-1] == '\n' else url for url in urls_dataset]
    urls_dataset_file.close()
        
    
    for index, url in enumerate(urls_dataset):
        
            
        file_name = "%04d.json" % index
        destination = os.path.realpath(os.path.join(destination_directory,file_name))
        
        cmd = 'node resources_extractor.js -s "%(url)s" -f "%(destination)s"' % {
            'url': url,
            'destination': destination,
        }
        
        print(cmd)
        
        subprocess.call(cmd, shell=True)
        
        pass
    
    
    pass



if __name__ == '__main__':
    
    destination_path = os.path.realpath(os.path.join(project_path, 'datasets/extracted_data'))
    feed_extractor("../datasets/webpages_urls.txt",destination_path)
    
    pass



