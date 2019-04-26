import IWW as iww
import os


project_path = os.path.realpath(os.path.abspath(os.path.dirname(__file__)))
urls_dataset_path = os.path.realpath(os.path.join(project_path, 'datasets/webpages_urls.txt'))
destination_directory_path = os.path.realpath(os.path.join(project_path, 'datasets/extracted_data'))




iww.extract(urls_dataset_path, destination_directory_path)
