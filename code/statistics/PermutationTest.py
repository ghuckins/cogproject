import numpy as np 

def PermutationTest(group1, group2, permutations = 1000, tail = 'both'):
    '''
        Perform a permutation test of group means. Inputs are:
        
        group1/2 (np.array) - holds test data 
        permutations (int)  - number of permutations to run
        tail (str)          - tails to be tested; options are 'left', 'right', and
                              'both'

        example: test two gaussians with equal variance and different means 
        
        group1 = np.random.normal(0, 1, 1000)
        group2 = np.random.normal(1, 1, 1000)
        pval   = permutationTest(group1, group)  
    
        TODO:
            - optimize code 
    '''
    
    null_distribution = np.zeros((permutations,))

    if len(group1.shape) > 1:
        if (group1.shape[1] > group1.shape[0]):
            group1  = np.transpose(group1)
    if len(group2.shape) > 1:
        if (group2.shape[1] > group2.shape[0]):
            group2  = np.transpose(group2)

    grouped_data  = np.concatenate((group1, group2))  
    #print(len(grouped_data), len(group1))
    grp1_len      = len(group1)
    
    for run in range(permutations):
        randomized_data = grouped_data[np.random.permutation(len(grouped_data))]
        shuffle1_mean   = np.mean(randomized_data[0:grp1_len])
        shuffle2_mean   = np.mean(randomized_data[(grp1_len + 1):])
    
        null_distribution[run] = shuffle1_mean - shuffle2_mean
    
    
    # calculate p-value 
    observed = np.mean(group1) - np.mean(group2)
    
    if (tail == 'left'):
        pval = (np.sum(observed > null_distribution) + 1) / permutations
    elif (tail == 'right'):
        pval = (np.sum(observed < null_distribution) + 1) / permutations
    else:
        pval = (np.sum(np.abs(observed) < np.abs(null_distribution)) + 1) / permutations

    return pval 


