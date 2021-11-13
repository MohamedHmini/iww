# IWW-IntelliWebWrapper

![](/iww2.png)<br/>
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub version](https://badge.fury.io/gh/Naereen%2FStrapDown.js.svg)](https://github.com/Naereen/StrapDown.js)
[![Generic badge](https://img.shields.io/badge/docs-passing-<green>.svg)](https://shields.io/)
[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://GitHub.com/Naereen/ama)


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
   - the pip package of iww will be available online as soon as possible.



## USE CASE EXAMPLE :

### 1- extraction :

```python
from iww.extractor import extractor
from iww.detector import detector
from iww.features_extraction.lists_detector import Lists_Detector as LD
from iww.features_extraction.main_content_detector import MCD
```

```python
url = "https://www.theiconic.com.au/catalog/?q=kids%20sunglasses"
json_file = "./iconic.json"

extractor.extract(
    url = url, 
    destination = json_file
)
```

### 2- data exploratory analysis :

```python
from iww.utils.dom_mapper import DOM_Mapper as DM

dm = DM()
dm.retrieve_DOM_tree("./iconic.json")
print("total number of nodes : {}".format(dm.DOM['CETD']['tagsCount']))
```
> total numbre of nodes : 2098

![](iww/test/webpage.PNG)


### 3- LD algorithm :

```python
ld = LD()
ld.retrieve_DOM_tree(file_path = "./iconic.json")
ld.apply(
    node = ld.DOM, 
    coherence_threshold= (0.75,1), 
    sub_tags_threshold = 2
)
ld.update_DOM_tree()
```

```python
detector.detect(
    input_file = "./iconic.json", 
    output_file = "./iconic_ld.png",
    mark_path = "LISTS.mark", 
    mark_value = "1"
)
```

![](iww/test/ld.png)

### 4- MCD algorithm :

```python
mcd = MCD()
mcd.retrieve_DOM_tree("./iconic.json")
mcd.apply(
    node = mcd.DOM, 
    min_ratio_threshold = 0.0, 
    nbr_nodes_threshold = 1
)
mcd.update_DOM_tree()
```

```python
detector.detect(
    input_file = "./iconic.json", 
    output_file = "./iconic_mcd.png",
    mark_path = "MCD.mark", 
    mark_value = "1"
)
```

![](iww/test/mcd.png)

### 5- LD/MCD integration (main list detection) :

```python
mcd.integrate_other_algorithms_results(
    node = mcd.DOM, 
    nbr_nodes = 1,
    mode = "ancestry", 
    condition_features = [("LISTS.mark","1")])

mcd.update_DOM_tree()
```

```python
detector.detect(
    input_file = "./iconic.json", 
    output_file = "./iconic_main_list.png",
    mark_path = "MCD.main_node", 
    mark_value = "1"
)
```

![](iww/test/main_list.png)


## License
[MIT](https://choosealicense.com/licenses/mit/)

**MOHAMED-HMINI 2019**
