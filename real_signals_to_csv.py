import json
import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt
import os

# simulated signals are stored here:
base_path = "/Volumes/T7 1TB/csv/"
neural_signals = os.listdir(base_path)
# pre-allocate array to cut down on runtime
files_contents = np.full(fill_value=None, shape=len(neural_signals))

for i in range(len(neural_signals)):
    # print(base_path+neural_signals[i])
    nparr = genfromtxt(fname=base_path+neural_signals[i], delimiter='\x0a')
    if len(nparr) < 1000:
        print("%s has length length %d" % (neural_signals[i], len(nparr)))
    for j in range(len(nparr)):
        if nparr[j] != 0:
            # print(nparr[j])
            break
        if j == len(nparr)-1:
            # print("all zeros")
            os._exit(1)

    file_content = nparr.tolist()
    files_contents[i] = file_content

# os._exit(1)

sig_dict = {"sigs": {},
            "n_sigs": len(files_contents),
            "users": {},
            "params": {}}

for i in range(len(files_contents)):
    print("real %d " % i)
    sig_dict["sigs"]["sig_"+str(i)] = files_contents[i]
    print(type(files_contents[i]))
    plt.figure()
    plt.plot(np.linspace(0, len(files_contents[i]), len(
        files_contents[i])), files_contents[i])
    sig_dict["ground_truth"] = None
# plt.show()

# print(sig_dict)


simulated_signals = json.load(open("signals_2024_22_4.json"))
print(type(simulated_signals))

print([*simulated_signals["sigs"].keys()])
for k in simulated_signals["sigs"].keys():
    sig_dict["sigs"][k] = simulated_signals["sigs"][k]
sig_dict["ground_truth"] = simulated_signals["ground_truth"]
sig_dict["params"] = simulated_signals["params"]

# real_sigs=49, sim_sigs=50
sig_dict["n_sigs"] = sig_dict["n_sigs"]+simulated_signals["n_sigs"]
print(sig_dict["n_sigs"])
# exit(2)

print([*sig_dict["sigs"].keys()])
# plt.show()
with open("real_signals_20240422.json", "w") as f:
    json.dump(sig_dict, f)
