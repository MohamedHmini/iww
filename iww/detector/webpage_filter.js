const puppeteer = require('puppeteer');
const fs = require('fs');
const commander = require('commander');
const util = require('util')


commander
  .version('0.1.0')
  .option('-i, --inputFile [inputFile]', 'The webpage generated JSON file location')
  .option('-o, --outputFile [outputFile]', '')
  .option('-m, --markPath [markPath]', '')
  .option('-v, --markValue [markValue]', '')
  .parse(process.argv);



var getJsonizedDOM = (file) => {

  let rawdata = fs.readFileSync(file);  
  let webpage = JSON.parse(rawdata.toString());  
  let DOM = webpage.DOM
  let meta_data = webpage.meta_data
  let webpage_url = webpage.webpage_url

    console.log(webpage_url)

  return {
    'DOM':DOM,
    'meta_data':meta_data,
    'webpage_url':webpage_url
  }
  
}




(async() => {
      let options = commander.opts();      

        const browser = await puppeteer.launch();
        const page = await browser.newPage();

        var webpage_json = await getJsonizedDOM(options.inputFile)        
	var input_data = {
		"webpage_json":webpage_json,
		"commander":options
	}	

        await page.goto(webpage_json.webpage_url);
	console.log("HTTP RESPONSE!")        
        await page.setViewport({ width: 1600, height: 20000});
        

        var counter = await page.evaluate((input_data)=>{
          
	  var get_feature_with_path = (node, feature_path) =>{

		var feature_seq = feature_path.split(".");
		var feature_val = node;
		
		try{		

			feature_seq.forEach((feature)=>{
				
				feature_val = feature_val[feature]
			
			})
		}catch(e){}
		

		return feature_val

	  }

          var xpath_reader = (xpath) =>{
          
            var xpath_splited = xpath.split("/")
            var node = xpath_splited[xpath_splited.length - 1]
                  
            if(node == "BODY"){
              node = {
                  'node':node,
                  'tagName': node,
                  'tagIndex': 0,
                  'parent_xpath': ""
              } 
            }
            else{
              
              node = {
                      'node':node,
                      'tagName': node.split("[")[0],
                      'tagIndex': Number(node.split("[")[1].split("]")[0]),
                      'parent_xpath': xpath_splited.slice(0,xpath_splited.length-1).join("/")
              }
            }
            
            return node
          
          
          }

          var xpath_detacher = (xpath, details = []) =>{
          
            var xpath_details = xpath_reader(xpath)
            details.push(xpath_details)
          
            if(xpath_details.parent_xpath != "")    
              details = details.concat(xpath_detacher(xpath_details.parent_xpath))
          
            return details
          
          }

          var search_node = (node, searched_node = []) =>{

            if(searched_node.length == 0)
              return node
            
            next_node = searched_node.pop()
            return search_node(node.childNodes[next_node.tagIndex], searched_node)

          }

          var counter = '';
          var traverse_JSON_DOM_tree = (node) =>{
          
            var xpath_details = ''
            var DOM_node = NaN

            if(get_feature_with_path(node, input_data.commander.markPath) == input_data.commander.markValue){
              counter++
              xpath_details = xpath_detacher(node.real_xpath)
              xpath_details.pop()
		try{              
	      DOM_node = search_node(document.body, xpath_details)
              
	      DOM_node.style.border = "4px solid red"
		}catch(e){}
            }

            node.children.forEach(child=>{
              traverse_JSON_DOM_tree(child)
            })

            // xpath_details = xpath_detacher(node.children[0].real_xpath)
            // xpath_details.pop()
            // DOM_node = search_node(document.body, xpath_details)
            // DOM_node.style.border = "4px solid red"
          
          }


          traverse_JSON_DOM_tree(input_data.webpage_json.DOM)
          return counter
          
        }, input_data)

        console.log("NUMBER OF SELECTED NODES : " + counter)
        await page.screenshot({
          path:options.outputFile
        });



        // fs.writeFile("./test.txt", util.inspect(document),(err)=>{})
        
        //  console.log(await xpath_detacher("/BODY/DIV[4]/SPAN[7]"))

	await browser.close();
	
})();


