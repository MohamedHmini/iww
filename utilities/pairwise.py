import numpy as np
from sklearn.metrics.pairwise import euclidean_distances






def euclidean_similarity(vect1, vect2, max_distance):
    
    distance = euclidean_distances([vect1],[vect2])[0][0]
    euclidean_sim = 1 - ((distance / max_distance) if max_distance != 0 else 0)
    
    return euclidean_sim
    
    pass


def is_bunch_of_zeros(vect):
    
    bunch_of_zeros = True
    
    for i in vect:        
        if i != 0:
            bunch_of_zeros = False
            
    return bunch_of_zeros
    pass


def get_max_distance(expected_vect, max_val = 1):
    
    max_vect = np.full(len(expected_vect), max_val)
    max_distance = euclidean_distances([expected_vect],[max_vect])[0][0]
    
    return max_distance
        
    pass


def similarity(expected_vect, observed_vect,max_val = 1):
    
    max_distance = get_max_distance(expected_vect, max_val)
    euclidean_sim = euclidean_similarity(expected_vect, observed_vect, max_distance)
    
    return euclidean_sim
    
    pass


def vectors_coherence(expected_vect, observed_vects):
    
    if is_bunch_of_zeros(expected_vect) != True:
        
        max_distance = get_max_distance(expected_vect, max_val = 1)
        
        observed_vect = [
                euclidean_similarity(expected_vect, vect, max_distance) 
                for vect in observed_vects
                ]
        
        final_expected_vect = np.full(len(observed_vect), 1)
        
        final_max_distance = get_max_distance(final_expected_vect, max_val = 0)
        
#        print("EXPECTED VECTOR : {}".format(final_expected_vect))
#        print("OBSERVED VECTOR : {}".format(observed_vect))
        
        coherence = euclidean_similarity(final_expected_vect, observed_vect, final_max_distance)
        
#        print("COHERENCE : {}".format(coherence))
    
    else:
        return 0
    
        
    
    return coherence
    
    pass




def __vectors_coherence():
    
    
    pass




if __name__ == "__main__":
    
    
    vectors_coherence([1,1],[[1,1]])
    
    
    pass