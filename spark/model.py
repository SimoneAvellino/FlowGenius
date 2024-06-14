import torch
from transformers import PatchTSTForPrediction


def predict_problems(df):
    # load model
    model = PatchTSTForPrediction.from_pretrained("/opt/bitnami/spark/scripts/model")
    # dro the date column
    if "date" in df.columns:
        df = df.drop(columns=["date"])
    # convert the dataframe to a tensor
    past_values = torch.tensor(df.values).view(1, 8, 31).float()
    # predict the problems
    outputs = model(past_values=past_values)
    predictions_tensor = outputs.prediction_outputs[0]
    predictions = predictions_tensor.detach().numpy()

    # parse the results
    for i, pred in enumerate(predictions):
        predictions[i] = [int(x + 0.5) if x >= 0 else 0 for x in pred]

    return predictions