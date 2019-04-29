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

                var set_dimensions = (node)=>{
                        var bounds = {}

                        bounds['offsetWidth'] = node.offsetWidth;
                        bounds['offsetHeight'] = node.offsetHeight;
                        bounds['offsetTop'] = node.offsetTop;
                        bounds['offsetLeft'] = node.offsetLeft;

                        bounds['marginTop'] = node.style.marginTop
                        bounds['marginBottom'] = node.style.marginBottom
                        bounds['marginRight'] = node.style.marginRight
                        bounds['marginLeft'] = node.style.marginLeft

                        bounds['paddingTop'] = node.style.paddingTop
                        bounds['paddingBottom'] = node.style.paddingBottom
                        bounds['paddingRight'] = node.style.paddingRight
                        bounds['paddingLeft'] = node.style.paddingLeft

                        bounds['top'] = node.style.top
                        bounds['left'] = node.style.left
                        bounds['scrollHeight'] = node.scrollHeight
                        bounds['scrollWidth'] = node.scrollWidth


                        return bounds;
                }


                var setAtts = (node)=>{

                        var atts = [];

                        for(i = 0;i < node.attributes.length;i++){
                                atts.push({
                                        "name":node.attributes[i].name,
                                        "value":node.attributes[i].value
                                })
                        } 

                        return atts;
                }


                var setComputedSyles = (node)=>{

                        var computed_styles = [];
                        var acquired_computed_styles = document.defaultView.getComputedStyle(node);
                        var len = acquired_computed_styles.length;

                        for(i = 0;i < len;i++){

                                var name = acquired_computed_styles.item(i);
                                var value = acquired_computed_styles.getPropertyValue(name);

                                computed_styles.push({
                                        "name":name,
                                        "value":value
                                })
                        } 

                        return computed_styles;
                }

                
                var traverse_DOM_tree = (node, xpath = "",index = "")=>{

                        var childs = node.childNodes;
                        var num_of_childs = childs.length;
                        var atts = setAtts(node);
                        var dimensions = set_dimensions(node)
                        var computed_styles = setComputedSyles(node);                        
                        

                        var doc = {
                                "tagName":node.tagName,
                                "children":[],
                                "text":node.innerText,
                                "atts":atts,
                                "style":computed_styles,
                                "dimensions":dimensions,
                                "xpath":xpath+"/"+node.tagName+index,
                                "parent_xpath":xpath
                        }

                        var counter = 0
                        childs.forEach(child=>{
                                // consider NOSCRIPT & BR!
                                if(child.nodeType == 1 && child.tagName != "SCRIPT" && child.tagName != "STYLE"){
                                        var doc_child = traverse_DOM_tree(child,doc.xpath,"["+counter+"]")
                                        doc.children.push(doc_child)
                                        counter++
                                }
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
                "meta_data":meta_data
        }

        fs.writeFile(commander.filedirectory,JSON.stringify(document),(err)=>{})

        // console.log(document)
	await browser.close();
})();






