const puppeteer = require('puppeteer');
const fs = require('fs');
const commander = require('commander');



commander
  .version('0.1.0')
  .option('-s, --site [site]', 'The website URL address')
  .option('-f, --filedirectory [filedirectory]', 'The generated file directory location')
  .parse(process.argv);



(async() => {

        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.goto(commander.site);

        await page.setViewport({ width: 1600, height: 4000});

        const traversed_DOM_tree = await page.evaluate(()=>{
		
		var clean_style_properties = (styles) =>{

			styles['font-size'] = Number(styles['font-size'].split("px")[0])	


			return styles
		}


                var set_dimensions = (node)=>{
                        var dimensions = {}

                        dimensions['offsetWidth'] = node.offsetWidth;
                        dimensions['offsetHeight'] = node.offsetHeight;
                        dimensions['offsetTop'] = node.offsetTop;
                        dimensions['offsetLeft'] = node.offsetLeft;

                        dimensions['marginTop'] = node.style.marginTop
                        dimensions['marginBottom'] = node.style.marginBottom
                        dimensions['marginRight'] = node.style.marginRight
                        dimensions['marginLeft'] = node.style.marginLeft

                        dimensions['paddingTop'] = node.style.paddingTop
                        dimensions['paddingBottom'] = node.style.paddingBottom
                        dimensions['paddingRight'] = node.style.paddingRight
                        dimensions['paddingLeft'] = node.style.paddingLeft
                        
                        dimensions['borderRightWidth'] = node.style.borderRightWidth
                        dimensions['borderLeftWidth'] = node.style.borderLeftWidth
                        dimensions['borderBottomWidth'] = node.style.borderBottomWidth
                        dimensions['borderTopWidth'] = node.style.borderTopWidth

                        dimensions['top'] = node.style.top
                        dimensions['left'] = node.style.left
                        dimensions['scrollHeight'] = node.scrollHeight
                        dimensions['scrollWidth'] = node.scrollWidth
                        
                        dimensions['zIndex'] = node.style.zIndex


                        return dimensions;
                }


                var setAtts = (node)=>{

                        var atts = {};

                        for(i = 0;i < node.attributes.length;i++){
                        
                                var name = node.attributes[i].name;
                                var value = node.attributes[i].value;
                        
                                if(name == "class")
                                    value = value.split(" ")
                        
                                atts[name] = value
                        } 

                        return atts;
                }


                var setComputedSyles = (node)=>{

                        var computed_styles = {};
                        var acquired_computed_styles = document.defaultView.getComputedStyle(node);
                        var len = acquired_computed_styles.length;

                        for(i = 0;i < len;i++){

                                var name = acquired_computed_styles.item(i);
                                var value = acquired_computed_styles.getPropertyValue(name);

                                computed_styles[name] = value
                        } 

                        return computed_styles;
                }

                
                var traverse_DOM_tree = (node, xpath = "",index = "", real_xpath = "", real_index = "")=>{

                        var childs = node.childNodes;
                        var num_of_childs = childs.length;
                        var atts = setAtts(node);
                        var dimensions = set_dimensions(node)
                        var computed_styles = setComputedSyles(node);                        
                        computed_styles = clean_style_properties(computed_styles)
                        
                        var doc = {
                                "tagName":node.tagName,
                                "children":[],
                                "text":node.innerText,
                                "atts":atts,
                                "style":computed_styles,
                                "dimensions":dimensions,
                                "bounds":node.getBoundingClientRect().toJSON(),
                                "xpath":xpath+"/"+node.tagName+index,
                                "parent_xpath":xpath,
                                "real_xpath":real_xpath+"/"+node.tagName+real_index,
                        }

                        var counter = 0
                        var real_counter = 0

                        childs.forEach(child=>{
                                // consider NOSCRIPT & BR!
                                if(child.nodeType == 1 && child.tagName != "SCRIPT" && child.tagName != "STYLE" && child.tagName != "NOSCRIPT"){
                                        
                                        var doc_child = traverse_DOM_tree(
                                                node = child,
                                                xpath = doc.xpath,
                                                index = "["+counter+"]", 
                                                real_xpath = doc.real_xpath, 
                                                real_index = "["+real_counter+"]"
                                        )                                        
                                        
                                        
                                        doc.children.push(doc_child)
                                        counter++
                                }

                                real_counter++
                        })
                        
                
                        return doc;
                }

                return traverse_DOM_tree(document.body)
                
                
        })


        var meta_data = await page.evaluate(()=>{


                var description_nodes = [];
                var page_title_nodes = []
                var keywords_nodes = [];
                var content_type_nodes = [];
                var site_name_nodes = [];

                var selector = 'title'

                document.querySelectorAll(selector).forEach(title =>{
                        page_title_nodes.push(title.innerText)
                })

                selector = 'meta[name="og:title"], meta[property="og:title"], meta[name="twitter:title"], meta[property="twitter:title"]'

                document.querySelectorAll(selector).forEach(title=>{
                        page_title_nodes.push(title.content)
                })

                selector = 'meta[name="description"], meta[name="og:description"], meta[property="og:description"], meta[name="twitter:description"], meta[property="twitter:description"]'


                document.querySelectorAll(selector).forEach(desc=>{
                        description_nodes.push(desc.content)
                })

                selector = 'meta[property="og:type"], meta[property="twitter:type"]'


                document.querySelectorAll(selector).forEach(type=>{
                        content_type_nodes.push(type.content)
                })


                selector = 'meta[property="og:site_name"], meta[property="twitter:site"]'


                document.querySelectorAll(selector).forEach(site=>{
                        site_name_nodes.push(site.content)
                })


                selector = 'meta[name="keywords"]'

                document.querySelectorAll(selector).forEach(keywords=>{
                        var keys = keywords.content.split(", ");
                        var result = keys.length > 0 ? keys : []
                        
                        result.forEach(keyword=>keywords_nodes.push(keyword))
                        
                })

                return {
                        "page_title":page_title_nodes,
                        "description":description_nodes,
                        "keywords":keywords_nodes,
                        "content_type":content_type_nodes,
                        "site_names": site_name_nodes
                }

                
        })

        var document = {
		"DOM":traversed_DOM_tree,
                "meta_data":meta_data,
                "webpage_url":commander.site
        }

        fs.writeFile(commander.filedirectory,JSON.stringify(document),(err)=>{})

        // console.log(document)
	await browser.close();
	
})();






