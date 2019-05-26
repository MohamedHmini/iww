# IWW-IntelliWebWrapper- [development phase] 🖖🐼

an AI based web-mining library for web-content-extraction using machine learning algorithms.

currently, the library offers many functionalities to be exploited & some interesting algos to look at:

  - DOM extractor, mapper, reducer and flattening functionality...
  - DoC, degree of coherence, a euclidean distance based similarity.
  - LD, Lists detector algorithm.
  - MCD, Main content detector algorithm.
  - MCD algorithms results integrator method.
  - CETD algorithm.
  - DOM tags detector script (highlighting the chosen nodes).

P.S : 
   - the documentation isn't available yet.
   - LD & MCD algorithms are to be released as a research article in the near future.

## USE CASE EXAMPLE :

### 1- extraction :

```
from iww.extractor import extractor
from iww.detector import detector
from iww.features_extraction.lists_detector import Lists_Detector as LD
from iww.features_extraction.main_content_detector import MCD
```

```
url = "https://www.theiconic.com.au/catalog/?q=kids%20sunglasses"
json_file = "./iconic.json"

extractor.extract(
    url = url, 
    destination = json_file
)
```

### 2- data exploratory analysis :

```
from iww.utils.dom_mapper import DOM_Mapper as DM

dm = DM()
dm.retrieve_DOM_tree("./iconic.json")
print("total number of nodes : {}".format(dm.DOM['CETD']['tagsCount']))
```
> result : total numbre of nodes : 2098

![](/test/webpage.PNG)


### 3- LD algorithm :

```
ld = LD()
ld.retrieve_DOM_tree(file_path = "./iconic.json")
ld.apply(
    node = ld.DOM, 
    coherence_threshold= (0.75,1), 
    sub_tags_threshold = 2
)
ld.update_DOM_tree()
```

```
detector.detect(
    input_file = "./iconic.json", 
    output_file = "./iconic_ld.png",
    mark_path = "LISTS.mark", 
    mark_value = "1"
)
```

![](/test/ld.png)

### 4- MCD algorithm :

```
mcd = MCD()
mcd.retrieve_DOM_tree("./iconic.json")
mcd.apply(
    node = mcd.DOM, 
    min_ratio_threshold = 0.0, 
    nbr_nodes_threshold = 1
)
mcd.update_DOM_tree()
```

```
detector.detect(
    input_file = "./iconic.json", 
    output_file = "./iconic_mcd.png",
    mark_path = "MCD.mark", 
    mark_value = "1"
)
```

![](/test/mcd.png)

### 5- LD/MCD integration (main list detection) :

```
mcd.integrate_other_algorithms_results(
    node = mcd.DOM, 
    nbr_nodes = 1,
    mode = "ancestry", 
    condition_features = [("LISTS.mark","1")])

mcd.update_DOM_tree()
```

```
detector.detect(
    input_file = "./iconic.json", 
    output_file = "./iconic_main_list.png",
    mark_path = "MCD.main_node", 
    mark_value = "1"
)
```

![](/test/main_list.png)


**MOHAMED-HMINI**
