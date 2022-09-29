import string
import random

length=40
number=1000000

for i in range(number):
  print(''.join(random.choices(string.ascii_lowercase, k=length)))
