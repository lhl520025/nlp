# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import argparse
import time

import paddle
from paddlenlp import Taskflow

from flask import Flask, request, jsonify
import json
def parse_args():
    parser = argparse.ArgumentParser()

    # yapf: disable
    parser.add_argument("--max_seq_len", default=128, type=int,
                        help="The maximum total input sequence length after tokenization. Sequences longer than this will be truncated, sequences shorter will be padded.", )
    parser.add_argument("--batch_size", default=64, type=int, help="Batch size per GPU/CPU for training.", )
    parser.add_argument("--device", default="gpu", type=str, choices=["cpu", "gpu", "xpu"],
                        help="The device to select to train the model, is must be cpu/gpu/xpu.")
    # yapf: enable

    args = parser.parse_args()
    return args
def print_arguments(args):
    """print arguments"""
    print('-----------  Configuration Arguments -----------')
    for arg, value in sorted(vars(args).items()):
        print('%s: %s' % (arg, value))
    print('------------------------------------------------')

app = Flask(__name__)
args = parse_args()
print_arguments(args)
paddle.set_device(args.device)
print("开始加载模型：" + str(time.time()))
wordtag = Taskflow(
    "knowledge_mining",
    model="wordtag",
    # task="ner",
    batch_size=args.batch_size,
    max_seq_length=args.max_seq_len,
    params_path="C:\\Users\\Administrator\\DataspellProjects\\PaddleNLP\\examples\\text_to_knowledge\\ernie-ctm/output/model_300/model_state.pdparams",
    tag_path="C:\\Users\\Administrator\\DataspellProjects\\PaddleNLP\\examples\\text_to_knowledge\\ernie-ctm/data/tags.txt",
    linking=True,
    term_schema_path="d:/termtree/new/termtree_type.csv", term_data_path="d:/termtree/new/termtree_data")
print("模型加载完毕：" + str(time.time()))

def do_predict(txts):
    print("预测开始：" + str(time.time()))
    try:
        res = wordtag(txts)
    except:
        with open('D:\log.txt','a+') as f :
            f.write("text: "+str(txts))
            f.write('\n')
    # txts = txts.split('。')
    # res_list = []
    # for par in txts:
    #     if par=='':
    #         continue
    #     par=par+'。'
    #     res = wordtag(par)
    #     res_list.append(res[0])
    print("预测完毕：" + str(time.time()))
    return res
'D:\dsprojects\lib\site-packages\paddle\text\viterbi_decode.py"'
@app.route('/paddlenlp/ner/', methods=['post'])
def api_use():
    if not request.data:
        return 'fail'
    text = request.data.decode('utf-8')
    # print(text)
    text_json = json.loads(text)
    if text_json['text'].strip()!='':
    # txts=[]
    # txts.append(text_json['text'])
    # print(txts)
        args = parse_args()
        print_arguments(args)
        data_list = do_predict(text_json['text'])
    else:
        data_list=[{
            "items": [],
            "text": ""
        }]
    # print(data_list)
    data_dict = {
        'data': data_list
    }
    return jsonify(data_dict)


if __name__ == "__main__":
    app.run(host='192.168.200.244', port=1234, debug=True)
