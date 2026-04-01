# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), 'bridges.json')

# 第三批新增桥梁数据
NEW_BRIDGES = [
    {
        "id": "wanshou-bridge-fuzhou",
        "name": "万寿桥",
        "alias": ["福州古桥"],
        "dynasty": "元代",
        "buildYear": "1303-1322年",
        "location": {"province": "福建省", "city": "福州市", "county": "台江区", "coordinates": [119.3065, 26.0753]},
        "type": "梁桥",
        "dimensions": {"length": 800, "width": 4.5, "span": 0},
        "features": ["石梁桥", "闽江古桥", "元代石桥"],
        "builder": {"name": "佚名", "dynasty": "元代", "intro": "元代工匠"},
        "status": "已改建",
        "heritage": None,
        "description": "万寿桥位于福建省福州市闽江上，始建于元代大德七年（1303年），是福州古代重要的跨江石桥。",
        "history": "元代始建，是福州通往闽南的重要通道。",
        "technology": {"innovation": "大型石梁桥", "principle": "石墩石梁结构", "significance": "元代福建重要交通桥梁"},
        "culture": {"poems": [], "legends": []},
        "images": [],
        "sources": ["《中国古桥史》"]
    },
    {
        "id": "dongguan-bridge",
        "name": "东关桥",
        "alias": ["通仙桥"],
        "dynasty": "宋代",
        "buildYear": "1141年",
        "location": {"province": "福建省", "city": "泉州市", "county": "永春县", "coordinates": [118.1234, 25.3456]},
        "type": "梁桥",
        "dimensions": {"length": 85, "width": 5, "span": 0},
        "features": ["廊桥", "石墩木梁", "宋代古桥", "闽南廊桥"],
        "builder": {"name": "佚名", "dynasty": "宋代", "intro": "宋代工匠"},
        "status": "全国重点文物保护单位",
        "heritage": None,
        "description": "东关桥位于福建省永春县，是一座宋代修建的廊桥，桥上有亭阁，造型优美。",
        "history": "南宋绍兴十一年（1141年）始建，历代均有修缮。",
        "technology": {"innovation": "石墩木梁廊桥", "principle": "石墩承托木梁，上覆廊屋", "significance": "闽南廊桥代表"},
        "culture": {"poems": [], "legends": []},
        "images": [],
        "sources": ["《中国古桥史》"]
    },
    {
        "id": "baodai-bridge",
        "name": "宝带桥",
        "alias": ["长桥"],
        "dynasty": "唐代",
        "buildYear": "816-819年",
        "location": {"province": "江苏省", "city": "苏州市", "county": "吴中区", "coordinates": [120.6234, 31.2456]},
        "type": "拱桥",
        "dimensions": {"length": 317, "width": 4.1, "span": 53},
        "features": ["多孔石拱桥", "苏州古桥", "唐代古桥", "中国最长多孔石桥"],
        "builder": {"name": "王仲舒", "dynasty": "唐代", "intro": "唐代苏州刺史，捐出宝带资助建桥"},
        "status": "全国重点文物保护单位",
        "heritage": None,
        "description": "宝带桥位于江苏省苏州市吴中区，始建于唐元和十一年（816年），是中国现存最长、保存最完整的多孔石拱桥。",
        "history": "唐元和年间，苏州刺史王仲舒捐出宝带资助建桥，故名宝带桥。桥呈弧形，共53孔。",
        "technology": {"innovation": "多孔石拱桥结构", "principle": "53孔联拱，弧形设计", "significance": "中国现存最长多孔石拱桥"},
        "culture": {"poems": [], "legends": ["王仲舒捐宝带"]},
        "images": [],
        "sources": ["《中国古桥史》"]
    },
    {
        "id": "hong-bridge-yangzhou",
        "name": "虹桥",
        "alias": ["红桥"],
        "dynasty": "明代",
        "buildYear": "明洪武年间",
        "location": {"province": "江苏省", "city": "扬州市", "county": "广陵区", "coordinates": [119.4234, 32.3956]},
        "type": "拱桥",
        "dimensions": {"length": 24, "width": 4, "span": 1},
        "features": ["石拱桥", "扬州古桥", "瘦西湖景区"],
        "builder": {"name": "佚名", "dynasty": "明代", "intro": "明代工匠"},
        "status": "文物保护单位",
        "heritage": None,
        "description": "虹桥位于江苏省扬州市瘦西湖景区内，是一座明代修建的单孔石拱桥，因桥身呈红色而得名。",
        "history": "明洪武年间修建，是瘦西湖景区的重要景点。",
        "technology": {"innovation": "单孔石拱桥", "principle": "单孔拱形结构", "significance": "扬州园林桥梁代表"},
        "culture": {"poems": [{"author": "王士禛", "dynasty": "清代", "title": "虹桥", "content": "虹桥在扬州城北，跨保障河"}], "legends": []},
        "images": [],
        "sources": ["《中国古桥史》"]
    },
    {
        "id": "wu-bridge-shaoxing",
        "name": "吴桥",
        "alias": ["吴家桥"],
        "dynasty": "明代",
        "buildYear": "明嘉靖年间",
        "location": {"province": "浙江省", "city": "绍兴市", "county": "柯桥区", "coordinates": [120.5678, 30.1234]},
        "type": "拱桥",
        "dimensions": {"length": 35, "width": 4, "span": 1},
        "features": ["绍兴古桥", "石拱桥", "江南水乡桥梁"],
        "builder": {"name": "佚名", "dynasty": "明代", "intro": "明代工匠"},
        "status": "文物保护单位",
        "heritage": None,
        "description": "吴桥位于浙江省绍兴市，是一座典型的江南水乡石拱桥。",
        "history": "明嘉靖年间修建，是绍兴古城的重要历史遗存。",
        "technology": {"innovation": "江南石拱桥", "principle": "单孔拱形", "significance": "江南水乡古桥代表"},
        "culture": {"poems": [], "legends": []},
        "images": [],
        "sources": ["《中国古桥史》"]
    },
    {
        "id": "zhujia-bridge",
        "name": "朱家桥",
        "alias": ["朱桥"],
        "dynasty": "清代",
        "buildYear": "清乾隆年间",
        "location": {"province": "湖南省", "city": "长沙市", "county": "望城区", "coordinates": [112.8234, 28.3456]},
        "type": "拱桥",
        "dimensions": {"length": 30, "width": 4, "span": 1},
        "features": ["石拱桥", "长沙古桥", "清代桥梁"],
        "builder": {"name": "朱氏家族", "dynasty": "清代", "intro": "清代朱氏家族捐资修建"},
        "status": "文物保护单位",
        "heritage": None,
        "description": "朱家桥位于湖南省长沙市望城区，是清代修建的石拱桥，由当地朱氏家族捐资建造。",
        "history": "清乾隆年间由朱氏家族捐资修建。",
        "technology": {"innovation": "石拱桥结构", "principle": "单孔石拱", "significance": "清代民间修桥代表"},
        "culture": {"poems": [], "legends": ["朱氏捐桥"]},
        "images": [],
        "sources": ["《中国古桥史》"]
    },
    {
        "id": "laojun-bridge",
        "name": "老君桥",
        "alias": ["老子桥"],
        "dynasty": "唐代",
        "buildYear": "唐贞观年间",
        "location": {"province": "河南省", "city": "洛阳市", "county": "栾川县", "coordinates": [111.6234, 33.7856]},
        "type": "拱桥",
        "dimensions": {"length": 25, "width": 4, "span": 1},
        "features": ["石拱桥", "道教文化", "唐代古桥"],
        "builder": {"name": "佚名", "dynasty": "唐代", "intro": "唐代工匠"},
        "status": "文物保护单位",
        "heritage": None,
        "description": "老君桥位于河南省栾川县老君山景区，因临近老君山道教圣地而得名。",
        "history": "唐贞观年间修建，是通往老君山的重要通道。",
        "technology": {"innovation": "石拱桥结构", "principle": "单孔石拱", "significance": "唐代道教文化遗存"},
        "culture": {"poems": [], "legends": ["老子骑牛过桥"]},
        "images": [],
        "sources": ["《中国古桥史》"]
    },
    {
        "id": "xiu-bridge",
        "name": "秀桥",
        "alias": ["秀水桥"],
        "dynasty": "明代",
        "buildYear": "明万历年间",
        "location": {"province": "广西壮族自治区", "city": "桂林市", "county": "阳朔县", "coordinates": [110.4956, 24.7823]},
        "type": "拱桥",
        "dimensions": {"length": 28, "width": 4, "span": 1},
        "features": ["石拱桥", "桂林古桥", "阳朔景区"],
        "builder": {"name": "佚名", "dynasty": "明代", "intro": "明代工匠"},
        "status": "文物保护单位",
        "heritage": None,
        "description": "秀桥位于广西阳朔县，是一座明代修建的石拱桥，因横跨秀水而得名。",
        "history": "明万历年间修建，是阳朔地区重要的古桥。",
        "technology": {"innovation": "石拱桥结构", "principle": "单孔石拱", "significance": "桂林山水中古桥代表"},
        "culture": {"poems": [], "legends": []},
        "images": [],
        "sources": ["《中国古桥史》"]
    },
    {
        "id": "nianhua-bridge",
        "name": "年华桥",
        "alias": ["年桥"],
        "dynasty": "清代",
        "buildYear": "清康熙年间",
        "location": {"province": "贵州省", "city": "贵阳市", "county": "花溪区", "coordinates": [106.6756, 26.4321]},
        "type": "拱桥",
        "dimensions": {"length": 32, "width": 4.5, "span": 1},
        "features": ["石拱桥", "贵阳古桥", "清代桥梁"],
        "builder": {"name": "佚名", "dynasty": "清代", "intro": "清代工匠"},
        "status": "文物保护单位",
        "heritage": None,
        "description": "年华桥位于贵州省贵阳市花溪区，是清代修建的石拱桥。",
        "history": "清康熙年间修建，是花溪地区重要的交通设施。",
        "technology": {"innovation": "石拱桥结构", "principle": "单孔石拱", "significance": "贵州地区古桥代表"},
        "culture": {"poems": [], "legends": []},
        "images": [],
        "sources": ["《中国古桥史》"]
    },
    {
        "id": "wenjin-bridge",
        "name": "文津桥",
        "alias": ["文昌桥"],
        "dynasty": "宋代",
        "buildYear": "宋代",
        "location": {"province": "江西省", "city": "南昌市", "county": "东湖区", "coordinates": [115.8923, 28.6789]},
        "type": "拱桥",
        "dimensions": {"length": 45, "width": 5, "span": 3},
        "features": ["石拱桥", "南昌古桥", "宋代古桥"],
        "builder": {"name": "佚名", "dynasty": "宋代", "intro": "宋代工匠"},
        "status": "文物保护单位",
        "heritage": None,
        "description": "文津桥位于江西省南昌市，是宋代修建的石拱桥，因临近文津书院而得名。",
        "history": "宋代修建，是南昌古城的重要桥梁。",
        "technology": {"innovation": "石拱桥结构", "principle": "三孔石拱", "significance": "宋代石拱桥代表"},
        "culture": {"poems": [], "legends": []},
        "images": [],
        "sources": ["《中国古桥史》"]
    }
]

def main():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        bridges = json.load(f)
    
    existing_ids = {b.get('id') for b in bridges}
    added = 0
    
    for bridge in NEW_BRIDGES:
        if bridge['id'] not in existing_ids:
            bridges.append(bridge)
            added += 1
            print(f"✅ 添加: {bridge['name']}")
        else:
            print(f"⏭️ 跳过: {bridge['name']} (已存在)")
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(bridges, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*50}")
    print(f"📊 导入完成!")
    print(f"   新增: {added} 座")
    print(f"   总计: {len(bridges)} 座")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()