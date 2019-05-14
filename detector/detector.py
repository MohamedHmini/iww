import os
import sys
import subprocess








def CMD(script, input_file, output_file, mark_path, mark_value):
    
    cmd = 'node "%(script)s" -i "%(input_file)s" -o "%(output_file)s" -m "%(mark_path)s" -v "%(mark_value)s"' % {
                'script': script,
                'input_file': input_file,
                'output_file': output_file,
                'mark_path':mark_path,
                'mark_value':mark_value
            }
            
            
    subprocess.call(cmd, shell=True)
    
    pass



def detect(input_file, output_file, mark_path = "CETD.mark", mark_value = "1"):
    
    if os.path.exists(input_file) == True:
    
        input_file = os.path.realpath(input_file)
        output_file = os.path.realpath(output_file)
        CMD(
	'c:\\users\\mohamedhmini\\data_analysis_doodlings\\iww\\iww\\detector\\webpage_filter.js', 
	input_file, 
	output_file, 
	mark_path = mark_path, 
	mark_value = mark_value)
        
        pass
    
    pass






if __name__ == "__main__" :
    
    
    
    pass




