import os
import random
import string


def rand_string(length=3):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


test_mode = [0, 1, 2, 4, 5, 6]
test_name = f"pp_{rand_string()}"
for i in test_mode:
    os.system(f"screen -dmS {test_name}_mode{i}")
    os.system(f"screen -x -S {test_name}_mode{i} -p 0 -X stuff 'python3 test.py python large hashset {i}\n'")
