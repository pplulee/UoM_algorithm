import pandas as pd
import os
import time
input_size=[500,15000,500] # start end step
test_result = pd.DataFrame(columns=["input_size","time"])
for i in range(input_size[0],input_size[1]+input_size[2],input_size[2]):
    for j in range(0,2):
        print(f"running test for {i}-{j}.txt")
        start_time=time.time()
        os.system(f"python3 dp_kp.py {i}-{j}.txt")
        end_time=time.time()
        time_count=end_time-start_time
        print(f"running time is {time_count}")
        test_result.loc[len(test_result)]=[i,end_time-start_time]

test_result.to_csv("result_dp.csv")