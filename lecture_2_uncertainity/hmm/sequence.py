from model import model

# hmm means hidden Markov model
# Observed data
observations = [
    "umbrella",
    "umbrella",
    "no umbrella",
    "umbrella",
    "umbrella",
    "umbrella",
    "umbrella",
    "no umbrella",
    "no umbrella"
]

# Predict underlying states 
# prdict the corresponding states for observed data
predictions = model.predict(observations)
for prediction in predictions:
    print(model.states[prediction].name)
