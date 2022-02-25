#!/usr/bin/env python
# @Time    : 2021/12/17 8:29
# @Author  : LYC



import json



def read_by_lines(path):
    """读取train_ceshi.json文件"""
    result = list()
    result =""
    with open(path, "r" , encoding="utf-8") as infile:
        for line in infile:
            result+=line.strip()
    print(result)
    return result


def data_process(path, model="text", is_predict=False):
    output = ""
    a = read_by_lines(path)
    d_json = json.loads(a)
    for o in d_json:
        output += o[model]+"-B\n"
        output += o[model]+"-I\n"
    output += "O"
    with open('tag_ceshi.dic', "w", encoding='utf-8') as outfile:
        outfile.write(output)
    return output

train_tri = data_process("label_config.json", "text")
print(train_tri)

