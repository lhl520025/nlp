#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/19 14:36
# @Author  : LYC
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/19 13:44
# @Author  : LYC



import json


def write_by_lines(train_sent):
    """write the data"""
    with open('./train_ceshi.json', "a",encoding='utf-8') as outfile:
        # outfile.write(train_sent + "\n")
        outfile.write(str(train_sent).replace("'",'"') + "\n")



def data_format_edit(s_json):
    d_json = {}
    d_json['id'] = str(s_json['id'])
    # d_json['title'] = s_json['title']
    d_json['text'] = s_json['data'].replace(" ","")
    d_json['event_list'] = []
    arguments_list = s_json['label']
    arguments = []
    event_list = {}
    for var in arguments_list:
        event_ = {}
        event_['argument_start_index'] = var[0]
        event_['role'] = var[-1]
        lis = []
        for i in range(var[0],var[1]):
            lis.append(s_json['data'][i])
        event_['argument'] = "".join(lis)
        arguments.append(event_)
    event_list['arguments'] = arguments
    d_json['event_list'].append(event_list)
    # d_json = str(d_json).replace("'",'"')
    return d_json





with open('./all.jsonl', 'r', encoding='utf-8') as f:
    data = f.readlines()
    for i in data:
        s_json = json.loads(i)

        train_sent = data_format_edit(s_json)
        write_by_lines(train_sent)
