import os
size_of_backpack = 5000
input_size=[1000,10000,500] # start end step

for i in range(input_size[0],input_size[1]+input_size[2],input_size[2]):
    for j in range(0,3):
        os.system(f"python kp_generate.py {i} {size_of_backpack} 100 {i}-{j}.txt")