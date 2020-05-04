from Classes.SeqAlgorithm import SequentialAlgorithm
import os
import csv
import numpy as np

filename = "MyData.csv"
folder = os.path.join(os.getcwd(), "Data")
path = os.path.abspath(os.path.join(folder, filename))
print(path)
assert os.path.exists(path), "Incorrect name of file or path"
temp_list = list()
with open(path, "r") as f_obj:
    reader = csv.reader(f_obj)
    for row in reader:
        temp_list.append([int(x) for x in row])

N = 6
M = 5

crystal = np.zeros(30).reshape(N, M)

seq = SequentialAlgorithm(np.array(temp_list), crystal)
seq.start_seq()
seq.start_iter()
