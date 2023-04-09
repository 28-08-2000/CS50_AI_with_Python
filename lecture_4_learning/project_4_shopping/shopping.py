import csv
import sys 

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# ratio of test set and training set
TEST_SIZE = 0.4  


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """ 
    month_conv = {
        'Jan' : 0,
        'Feb' : 1,
        'Mar' : 2,
        'April' : 3,
        'May' : 4,
        'June' : 5,
        'Jul' : 6,
        'Aug' : 7,
        'Sep' : 8 ,
        'Oct' : 9,
        'Nov' : 10, 
        'Dec' : 11
    } 
    Bool_conv = {
        'FALSE' : 0,
        'TRUE' : 1
    }
    Visitor_conv = {
        'Returning_Visitor' : 1,
        'New_Visitor' : 0,
        'Other' : 0
    }
    # open the csv file
    with open('shopping.csv','r') as csv_file:
        csv_reader = csv.reader(csv_file) 

        next(csv_reader)  #leave the first line

        evidences_list = [] 
        labels = []  

        for line in csv_reader:  
            # make the labels list 
            # column 17 of line is label convert it 0 or 1
            labels.append(Bool_conv[line[17]])  
            
           # make the evidence list for this line 
            evidences = []
            for i in range(17): 
                column = line[i] 
                if i == 0 or i == 2 or i == 4 or i == 11 or i == 12 or i == 13 or i == 14:
                    evidences.append(int(column)) 
                elif i == 10: 
                    evidences.append(month_conv[column])
                elif i == 15:
                    evidences.append(Visitor_conv[column])
                elif i == 16:
                    evidences.append(Bool_conv[column])
                else:
                    evidences.append(float(column))
            evidences_list.append(evidences) 
        # print(labels)
        # print(evidences_list) 
        return (evidences_list, labels) 
    #raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """ 
    """train a k neighbor classifier model on training set""" 
    # choose model
    model = KNeighborsClassifier(n_neighbors = 1)  
    # apply model or training 
    model.fit(evidence, labels) 

    return model
    # raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """ 
    """calculate true positive rate and true negative rate 
       based on predictons""" 
    total_identified_pos = 0   # identified positive labes
    total_identified_neg = 0   # identified negative labels
    total_pos = 0              # total positive labels  
    total_neg = 0              # total negative labels
    for i in range(len(predictions)):
        if labels[i] == predictions[i]:
            if labels[i] == 1:
                total_identified_pos += 1
            else:
                total_identified_neg += 1  
        if labels[i] == 1:
            total_pos += 1
        else:
            total_neg += 1

   
    sensitivity = total_identified_pos/total_pos   # sensitivity 
    specificity = total_identified_neg/total_neg  # specifity
    
    return (sensitivity, specificity)
    # raise NotImplementedError


if __name__ == "__main__":
    main()
