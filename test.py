import os
from iww.extractor import extractor
from iww.detector import detector
from iww.features_extraction.lists_detector import Lists_Detector as LD
from iww.features_extraction.main_content_detector import MCD


url = "https://stackoverflow.com/questions/66102275/commanderjs-i-cant-get-value-from-option"

full_path = os.path.realpath(__file__)
json_file = f"{os.path.dirname(full_path)}/test.json"

extractor.extract(
    url = url, 
    destination = json_file
)

from iww.utils.dom_mapper import DOM_Mapper as DM

dm = DM()
dm.retrieve_DOM_tree("./test.json")
# print("total number of nodes : {}".format(dm.DOM['CETD']['tagsCount']))

ld = LD()
ld.retrieve_DOM_tree(file_path = "./test.json")
ld.apply(
    node = ld.DOM, 
    coherence_threshold= (0.75,1), 
    sub_tags_threshold = 2
)
ld.update_DOM_tree()

detector.detect(
    input_file = "./test.json", 
    output_file = "./test_ld.png",
    mark_path = "LISTS.mark", 
    mark_value = "1"
)

mcd = MCD()
mcd.retrieve_DOM_tree("./test.json")
mcd.apply(
    node = mcd.DOM, 
    min_ratio_threshold = 0.0, 
    nbr_nodes_threshold = 1
)
mcd.update_DOM_tree()

detector.detect(
    input_file = "./test.json", 
    output_file = "./test_mcd.png",
    mark_path = "MCD.mark", 
    mark_value = "1"
)


mcd.integrate_other_algorithms_results(
    node = mcd.DOM, 
    nbr_nodes = 1,
    mode = "ancestry", 
    condition_features = [("LISTS.mark","1")])

mcd.update_DOM_tree()


detector.detect(
    input_file = "./test.json", 
    output_file = "./test_main_list.png",
    mark_path = "MCD.main_node", 
    mark_value = "1"
)
