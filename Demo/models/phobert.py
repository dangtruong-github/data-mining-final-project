from .phobert_init import predict

def phobert_no_pred_predict(text):
    return predict(mode="model0", text=text)

def phobert_5_pred_predict(text):
    return predict(mode="model5", text=text)

def phobert_10_pred_predict(text):
    return predict(mode="model10", text=text)