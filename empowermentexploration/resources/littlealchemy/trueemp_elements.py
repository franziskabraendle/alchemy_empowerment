#element_empowerment values
import empowermentexploration.utils.data_handle as data_handle
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

parents = data_handle.get_parent_table("alchemy2")
n_elements = 720
empowerment = np.zeros(n_elements)
for element_id in range(n_elements):
    if element_id in parents:
        empowerment[element_id] = len(parents[element_id])
    else:
        empowerment[element_id] = 0


print(empowerment)
print("number final:")
print(sum(i == 0 for i in empowerment))
