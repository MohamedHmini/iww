import os
import sys
import subprocess
import iww



project_path = os.path.realpath(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..'))




def get_urls(urls_path, edge):
    
    urls_dataset_file = open(urls_path,'r')    
    urls_dataset = urls_dataset_file.readlines()
    urls_dataset = [url[:-1] if url[-1] == '\n' else url for url in urls_dataset[:edge]]
    urls_dataset_file.close()
    
    return urls_dataset

    pass



def CMD(script, url, file):
    
    cmd = 'node "%(script)s" -s "%(url)s" -f "%(file)s"' % {
                'script': script,
                'url': url,
                'file': file,
            }
            
            
    subprocess.call(cmd, shell=True)
    
    pass



def extract(url, destination):
    
    if os.path.exists(destination) == False:
    
        file_path = os.path.realpath(destination)
        full_path = os.path.realpath(__file__)

        print(f'{os.path.dirname(full_path)}/resources_extractor.js', url, file_path)

        CMD(f'{os.path.dirname(full_path)}/resources_extractor.js', url, file_path)
        
        pass
    
    pass



def feed_extractor(urls_path, destination_directory, edge):
    
    urls_dataset = get_urls(urls_path, edge)
        
    enumerated = enumerate(urls_dataset)
    
    for index, url in enumerated:
                    
            
        file_name = "%04d.json" % index
        destination = os.path.realpath(os.path.join(destination_directory,file_name))
        
        extract(url, destination)
        
        pass
    
    
    pass





if __name__ == '__main__':
    
#    destination_path = os.path.realpath(os.path.join(project_path, 'datasets/extracted_data'))
#    feed_extractor(urls_path = "../datasets/webpages_urls.txt", destination_directory = destination_path, 1)
    
    pass



