from model import model

# Calculate probability for a given observation
probability = model.probability([["none", "no", "on time", "attend"]]) #find probability of this sample

print(probability)
