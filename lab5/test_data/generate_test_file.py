import os
size_of_items = 10000
input_size=[500,15000,500] # start end step

for i in range(input_size[0],input_size[1]+input_size[2],input_size[2]):
    for j in range(0,2):
        os.system(f"python3 kp_generate.py {size_of_items} {i} 200 {i}-{j}.txt")