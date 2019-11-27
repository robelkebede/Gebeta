
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.neural_network import MLPClassifier
import joblib

data = np.load("./data/game_data.npy",allow_pickle=True)

def preprocesses(data):
    
    feature = []
    tar = []
    features = data[:,0]
    target = data[:,1]
    for i in features:
        feature.append([i[0],i[1]])

    fea = np.array(feature)
    #one hot encoding [0,[0,0,0,0,0,1] (0,5)
    for t in target:
        #tar.append(t)
        if t[1] == 0:
            tar.append([1,0,0,0,0,0])
        elif t[1] == 1:
            tar.append([0,1,0,0,0,0])
        elif t[1] == 2:
            tar.append([0,0,1,0,0,0])
        elif t[1] == 3:
            tar.append([0,0,0,1,0,0])
        elif t[1] == 4:
            tar.append([0,0,0,0,1,0])
        elif t[1] == 5:
            tar.append([0,0,0,0,0,1])
    
    fea = np.array(feature)
    tar = np.array(tar)

    return fea,tar


def train():
    fea,target = preprocesses(data)
    fea = np.array([i for i in fea.reshape(fea.shape[0],6*2)])
    target = np.array([i for i in target])

    print(target)

    x_train,x_test,y_train,y_test = train_test_split(fea,target,test_size=0.2)

    network = MLPClassifier(early_stopping=False,hidden_layer_sizes=(100,),verbose=True)
    network.fit(x_train,y_train)

    predict = network.predict(x_test)
    
    #joblib.dump(network,"./model/gebeta_model_1")

    print(metrics.classification_report(predict,y_test))   


def main():
    train()


if __name__ == "__main__":
    main()
