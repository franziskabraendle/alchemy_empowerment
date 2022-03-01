import numpy as np


def get_empowerment(probability_table, element, outgoing_combinations, n_elements):
        """Returns predicted empowerment for single element depending on the calculation type. 

        Args:
            probability_table (DataFrame): Table with custom gametree probabilities.
            element (float): Element that empowerment is calculated for.
            outgoing_combinations (bool): True if calculation is based on outgoing combinations, False if it is based on children.
            n_elements (int): Number of elements.
            
        Returns: 
            list: Either list with single value if outgoing_combinations is True, else list with all resulting elements.
        """
        # check how many outgoing combinations with element are possible
        combinations = probability_table.query('first==@element | second==@element')
           
        # get successful combinations (probability of success > 0.5)
        successful_combination = combinations.query('predSuccess >= 0.5')
                 
        if outgoing_combinations is True:
            # get number of successful combinations
            element_empowerment_info = len(successful_combination.index)
        else:            
            # extract only element probability columns
            element_probabilities = successful_combination[successful_combination.columns[-n_elements:-1]]
            
            # get elements with maximum probability
            element_empowerment_info = element_probabilities.idxmax(axis='columns').astype(int).unique().tolist()
            
        return element_empowerment_info

def get_combination_empowerment(empowerment_outgoing_combinations, empowerment_children, combination_probabilities, n_elements):       
    """Returns predicted empowerment for combinations.

    Args:
        empowerment_outgoing_combinations (dict): Element empowerment info with caluclation type outgoing combinations.
        empowerment_children (dict): Element empowerment info with caluclation type children.
        combination_probabilities (DataFrame): Combination probabilities.
        n_elements (int): Number of elements

    Returns:
        ndarray(dtype=float, ndim=2)): Predicted empowerment values.
    """
    # get probability of success
    p_success = combination_probabilities['predSuccess'].values
    
    # initialize summed element probabilities
    p_sum = np.zeros((len(p_success), 4))
    
    for element in range(n_elements):
        # get empowerment value
        emp_out = empowerment_outgoing_combinations[element]
        emp_chi = len(empowerment_children[element])
        
        # get binary value
        if emp_out > 0:
            bin_out = 1
        else:
            bin_out = 0
            
        if emp_chi > 0:
            bin_chi = 1
        else:
            bin_chi= 0
        
        # get probability that this element is the result
        avg_element_probability = combination_probabilities[str(element)].values
        
        # multiply and add to sum
        p_sum[:,0] = p_sum[:,0] + avg_element_probability*emp_out
        p_sum[:,1] = p_sum[:,1] + avg_element_probability*emp_chi
        p_sum[:,2] = p_sum[:,2] + avg_element_probability*bin_out
        p_sum[:,3] = p_sum[:,3] + avg_element_probability*bin_chi
    
    # set empowerment value for combination
    return p_sum * p_success[:, None]
