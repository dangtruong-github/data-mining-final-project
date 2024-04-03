import pickle
import json
import sklearn

def predict(mode, text):
    fill = [mode, 5 if mode == "5_freq" else 10]
    prob = []

    threshold = None

    with open("./models/svc_models/threshold.json", "r") as file:
        f = json.load(file)
        threshold = f[mode]

    for i in range(1, 9):
        PATH = "./models/svc_models/{}/clf{}_for_tag_{}.pkl".format(fill[0], fill[1], i)
        with open(PATH, 'rb') as f:
            clf = pickle.load(f)
            prob_temp = clf.predict(text)
            prob.append(prob_temp)
    
    return prob, threshold

def svc_5_predict(text):
    return predict(mode="5_freq", text=text)

def svc_10_predict(text):
    return predict(mode="10_freq", text=text)