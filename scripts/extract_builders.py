# -*- coding: utf-8 -*-
import json

data = json.load(open(r'D:\AI创意大赛\【桥见千年】中国古代桥梁智慧可视化平台\backend\data\bridges.json', 'r', encoding='utf-8'))

builders = []
for b in data:
    if b.get('builder') and b['builder'].get('name') and b['builder']['name'] != '佚名':
        builders.append({
            'name': b['builder']['name'],
            'dynasty': b['builder'].get('dynasty', ''),
            'intro': b['builder'].get('intro', ''),
            'bridge': b['name'],
            'bridge_id': b['id']
        })

for b in builders:
    print(f"{b['name']} - {b['dynasty']} - {b['bridge']}")
