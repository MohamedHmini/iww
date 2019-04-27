# this file is an example of how the IWW library should be used.

from IWW import IWW
from utilities.dom_mapper import DOM_Mapper as DM
from configs import Configs
import os





#project_path = os.path.realpath(os.path.abspath(os.path.dirname(__file__)))
#urls_dataset_path = os.path.realpath(os.path.join(project_path, 'datasets/webpages_urls.txt'))
#extractor_generated_data_directory_path = os.path.realpath(os.path.join(project_path, 'datasets/extracted_data'))







#configs = Configs()
#configs.set_configs(current_file_directory = __file__, default = True)

#iww = IWW(configs)


iww = IWW()

iww.configs.set_configs(current_file_directory = __file__, default = True)
#iww.extract(edge = 2)


def display(node):
    print(node['tagName'])
    return node


dm = DM()
dm.retrieve_dom_tree(os.path.realpath('datasets/extracted_data/0000.json'))
dm.map(node = dm.DOM, fun = display, option = 'DEPTH')

