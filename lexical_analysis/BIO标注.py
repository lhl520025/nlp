#!/usr/bin/env python
# @Time    : 2021/12/17 8:29
# @Author  : LYC



import json

enum_role = "环节"

def read_by_lines(path):
    """读取train_ceshi.json文件"""
    result = list()
    with open(path, "r" , encoding="utf-8") as infile:
        for line in infile:
            result.append(line.strip())
    print(result)
    return result


def data_process(path, model="role", is_predict=False):
    sentences = []
    output = ["text_a"] if is_predict else ["text_a\tlabel"]
    for line in read_by_lines(path):
        print(line)
        d_json = json.loads(line)
        _id = d_json["id"]
        text_a = [
            "，" if t == " " or t == "\n" or t == "\t" else t
            for t in list(d_json["text"].lower())
        ]
        if is_predict:
            sentences.append({"text": d_json["text"], "id": _id})
            output.append('\002'.join(text_a))
        else:
            if model == u"role":
                for event in d_json.get("event_list", []):
                    labels = ["O"] * len(text_a)
                    for arg in event["arguments"]:
                        role_type = arg["role"]
                        argument = arg["argument"]
                        start = arg["argument_start_index"]
                        # 开始标注
                        # labels = label_data(labels,start,len(argument), role_type)
                        for i in range(start, start + len(argument)):
                            suffix = "-B" if i == start else "-I"
                            # print(suffix, role_type)
                            labels[i] = "{}{}".format(role_type,suffix)
                    output.append("{}\t{}".format('\002'.join(text_a),'\002'.join(labels)))
    return output

train_tri = data_process("format_conversion.json", "role")
print(train_tri)

def write_by_lines(data):
    """写入 train_ceshi.tsv文件"""
    with open('train_ceshi.tsv', "w" ,encoding='utf-8') as outfile:
        [outfile.write(d + "\n") for d in data]
        print('train_ceshi.tsv写入成功')
write_by_lines(train_tri)
