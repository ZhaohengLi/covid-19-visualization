# user_id not available, merely use semantic infomation
import os
import pickle
import torch
from sklearn.metrics import classification_report
from src.rumor.model.GLAN import GLAN
from src.rumor.dataset.preprocess import build_input_data
from flask import Flask, request, Response
import numpy
app = Flask(__name__)
model = GLAN
os.environ["CUDA_VISIBLE_DEVICES"] = ""
task = 'weibo'
config = {
    'reg':0,
    'batch_size':50,
    'nb_filters':100,
    'kernel_sizes':[3, 4, 5],
    'dropout':0.5,
    'maxlen':50,
    'epochs':20,
    'num_classes':4,
    'target_names':['NR', 'FR', 'UR', 'TR']
}
print("task: ", task)
app.debug = False
    
if task == 'weibo':
    config['num_classes'] = 2
    config['target_names'] = ['NR', 'FR']
def load_dataset(task):
    X_train_tid, X_train, y_train, word_embeddings, adj = pickle.load(open("./rumor/dataset/"+task+"/train.pkl", 'rb'))
    X_dev_tid, X_dev, y_dev = pickle.load(open("./rumor/dataset/"+task+"/dev.pkl", 'rb'))
    X_test_tid, X_test, y_test = pickle.load(open("./rumor/dataset/"+task+"/test.pkl", 'rb'))
    config['embedding_weights'] = word_embeddings
    print("#nodes: ", adj.shape[0])
    print("adj",adj)
    return X_train_tid, X_train, y_train, \
           X_dev_tid, X_dev, y_dev, \
           X_test_tid, X_test, y_test, adj


@app.route('/judge')
def test():
    sentence = request.args.get('sentence')
    model_suffix = model.__name__.lower().strip("text")
    config['save_path'] = 'checkpoint/weights.best.' + task + "." + model_suffix
    w2v = pickle.load(open("./rumor/dataset/"+task+"/vocab.pkl", 'rb'))
    _ ,X_train, y_train, \
    _, X_dev, y_dev, \
    _, X_test, y_test, _ = load_dataset(task)
    tf=[sentence]*50 #padding
    tfg = build_input_data(tf,w2v)
    nn = model(config)
   # nn.fit(X_train, y_train,
    #       X_dev, y_dev)
    nn.load_state_dict(torch.load(config['save_path']))
    y_pred = nn.predict(tfg)
    rt = '倾向于判断不是谣言' if y_pred[0]==0 else '倾向于判断是谣言'
    #print(classification_report(y_test, y_pred, target_names=config['target_names'], digits=3))
    return rt


def is_rumor(sentence):
    model_suffix = model.__name__.lower().strip("text")
    config['save_path'] = './rumor/checkpoint/weights.best.' + task + "." + model_suffix
    w2v = pickle.load(open("./rumor/dataset/" + task + "/vocab.pkl", 'rb'))
    _, X_train, y_train, \
    _, X_dev, y_dev, \
    _, X_test, y_test, _ = load_dataset(task)
    tf = [sentence] * 50  # padding
    tfg = build_input_data(tf, w2v)
    nn = model(config)
    nn.load_state_dict(torch.load(config['save_path']))
    y_pred = nn.predict(tfg)
    return y_pred[0] == 0

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000)
    #train_and_test(model, task)
    

