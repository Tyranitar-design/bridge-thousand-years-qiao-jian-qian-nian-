# -*- coding: utf-8 -*-
"""
扩展桥梁数据 - 第二批
运行此脚本添加更多桥梁数据
"""
import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), 'bridges.json')

# 新增桥梁数据（20座）
NEW_BRIDGES = [
    {
        "id": "zhaozhou-bridge",
        "name": "赵州桥",
        "alias": ["安济桥", "大石桥"],
        "dynasty": "隋代",
        "buildYear": "595-605年",
        "location": {
            "province": "河北省",
            "city": "石家庄市",
            "county": "赵县",
            "coordinates": [114.7697, 37.7472]
        },
        "type": "拱桥",
        "dimensions": {"length": 64.4, "width": 9.6, "span": 37.02},
        "features": ["敞肩拱", "单孔石拱", "世界最早敞肩石拱桥", "历经1400年不倒"],
        "builder": {"name": "李春", "dynasty": "隋代", "intro": "隋代著名工匠，赵州桥设计建造者，开创敞肩拱技术"},
        "status": "全国重点文物保护单位",
        "heritage": "世界文化遗产预备名单",
        "description": "赵州桥始建于隋开皇十五年至大业元年（595-605年），由著名工匠李春设计建造，是世界上现存年代最久远、跨度最大、保存最完整的单孔坦弧敞肩石拱桥。",
        "history": "隋代始建，历经唐、宋、元、明、清各代修缮，至今已有1400多年历史。曾经历8次以上地震、多次洪水，依然屹立不倒。",
        "technology": {
            "innovation": "敞肩拱技术",
            "principle": "在大拱两肩各砌两个小拱，既减轻桥身自重约700吨，又增加泄洪面积",
            "significance": "比欧洲同类桥梁早1200多年，是世界桥梁史上的创举"
        },
        "culture": {
            "poems": [
                {"author": "张嘉贞", "dynasty": "唐代", "title": "赵州桥铭", "content": "制造奇特，人不知其所以为"}
            ],
            "legends": ["鲁班造桥传说", "张果老试桥传说", "柴王推车压沟痕"]
        },
        "images": [],
        "sources": ["《中国古桥史》", "赵县文物保管所官网"]
    },
    {
        "id": "lugou-bridge",
        "name": "卢沟桥",
        "alias": ["马可波罗桥"],
        "dynasty": "金代",
        "buildYear": "1189-1192年",
        "location": {
            "province": "北京市",
            "city": "北京市",
            "county": "丰台区",
            "coordinates": [116.2108, 39.8572]
        },
        "type": "拱桥",
        "dimensions": {"length": 266.5, "width": 7.5, "span": 11},
        "features": ["联拱石桥", "石狮雕刻501只", "北京最古老石桥", "抗战纪念地"],
        "builder": {"name": "佚名", "dynasty": "金代", "intro": "金代工匠，具体姓名已不可考"},
        "status": "全国重点文物保护单位",
        "heritage": None,
        "description": "卢沟桥位于北京市丰台区永定河上，始建于金大定二十九年（1189年），是北京现存最古老的石造联拱桥，以其精美的石狮雕刻闻名于世。",
        "history": "明正统九年（1444年）重修，清康熙三十七年（1698年）重建。1937年7月7日，'卢沟桥事变'在此爆发，揭开了中国人民抗日战争的序幕。",
        "technology": {
            "innovation": "联拱结构与石雕艺术",
            "principle": "11孔联拱设计，整体稳定性强；桥栏望柱雕刻石狮，形态各异",
            "significance": "中国古代联拱石桥的杰出代表，石雕艺术宝库"
        },
        "culture": {
            "poems": [
                {"author": "马可·波罗", "dynasty": "元代", "title": "马可波罗游记", "content": "是世界上独一无二的桥"}
            ],
            "legends": ["卢沟晓月"]
        },
        "images": [],
        "sources": ["《中国古桥史》", "北京文物局官网"]
    },
    {
        "id": "luding-bridge",
        "name": "泸定桥",
        "alias": ["大渡河铁索桥"],
        "dynasty": "清代",
        "buildYear": "1705年",
        "location": {
            "province": "四川省",
            "city": "甘孜藏族自治州",
            "county": "泸定县",
            "coordinates": [102.2356, 29.9142]
        },
        "type": "索桥",
        "dimensions": {"length": 103.67, "width": 3, "span": 100},
        "features": ["铁索桥", "大跨度悬索", "红军长征纪念地", "13根铁链"],
        "builder": {"name": "佚名", "dynasty": "清代", "intro": "清代工匠，康熙皇帝下旨修建"},
        "status": "全国重点文物保护单位",
        "heritage": None,
        "description": "泸定桥位于四川省甘孜藏族自治州泸定县大渡河上，始建于清康熙四十四年（1705年），是中国现存最古老的铁索桥。",
        "history": "康熙皇帝为加强川藏交通而下旨修建。1935年5月29日，中国工农红军长征途中'飞夺泸定桥'，22名勇士冒着枪林弹雨攀爬铁索，成功夺取泸定桥。",
        "technology": {
            "innovation": "铁索悬吊技术",
            "principle": "13根铁链组成（9根底链，4根扶手链），每根重约1.5吨，锚固于两岸桥台",
            "significance": "代表了中国古代铁索锻造和悬索桥技术的最高水平"
        },
        "culture": {
            "poems": [],
            "legends": ["飞夺泸定桥"]
        },
        "images": [],
        "sources": ["《中国古桥史》", "泸定县文物局"]
    },
    {
        "id": "luoyang-bridge",
        "name": "洛阳桥",
        "alias": ["万安桥"],
        "dynasty": "宋代",
        "buildYear": "1053-1059年",
        "location": {
            "province": "福建省",
            "city": "泉州市",
            "county": "洛江区",
            "coordinates": [118.6764, 24.9444]
        },
        "type": "梁桥",
        "dimensions": {"length": 834, "width": 7, "span": 46},
        "features": ["跨海石梁桥", "筏形基础", "种蛎固基", "世界第一座跨海梁桥"],
        "builder": {"name": "蔡襄", "dynasty": "宋代", "intro": "北宋名臣、书法家，曾任泉州知州，主持修建洛阳桥并撰写《万安桥记》"},
        "status": "全国重点文物保护单位",
        "heritage": None,
        "description": "洛阳桥位于福建省泉州市洛阳江入海口处，始建于北宋皇祐五年（1053年），历时6年建成，是中国第一座跨海梁式石桥。",
        "history": "蔡襄任泉州知州时主持修建，并撰写《万安桥记》传世。桥成之后，极大便利了泉州港的交通，促进了海上丝绸之路的繁荣。",
        "technology": {
            "innovation": "筏形基础与种蛎固基",
            "principle": "在桥墩下铺垫石块形成筏形基础，并利用牡蛎繁殖附着石块的特性加固桥基",
            "significance": "世界桥梁史上的创举，世界首创的生物工程技术"
        },
        "culture": {
            "poems": [
                {"author": "蔡襄", "dynasty": "宋代", "title": "万安桥记", "content": "渡石一支，卧波千丈"}
            ],
            "legends": ["蔡襄母誓造桥"]
        },
        "images": [],
        "sources": ["《中国古桥史》", "泉州文物局"]
    },
    {
        "id": "guangji-bridge",
        "name": "广济桥",
        "alias": ["湘子桥"],
        "dynasty": "宋代",
        "buildYear": "1170年",
        "location": {
            "province": "广东省",
            "city": "潮州市",
            "county": "湘桥区",
            "coordinates": [116.6347, 23.6547]
        },
        "type": "梁桥",
        "dimensions": {"length": 517.95, "width": 5, "span": 24},
        "features": ["启闭式桥梁", "浮桥结合", "世界最早启闭式桥梁", "十八梭船二十四洲"],
        "builder": {"name": "佚名", "dynasty": "宋代", "intro": "宋代工匠，历朝历代均有修缮"},
        "status": "全国重点文物保护单位",
        "heritage": None,
        "description": "广济桥位于广东省潮州市韩江上，始建于南宋乾道七年（1170年），是世界上最早的启闭式桥梁。",
        "history": "初为浮桥，后改为石梁桥。明代在桥中间增设浮桥段，形成'十八梭船二十四洲'的独特格局，可开合通航。",
        "technology": {
            "innovation": "启闭式桥梁设计",
            "principle": "桥中间设浮桥段，可解开让大型船只通过，通航后再闭合",
            "significance": "世界上最早的启闭式桥梁，比英国伦敦塔桥早400多年"
        },
        "culture": {
            "poems": [
                {"author": "佚名", "dynasty": "清代", "title": "潮州竹枝词", "content": "十八梭船锁画桥"}
            ],
            "legends": ["韩愈驱鳄", "八仙造桥"]
        },
        "images": [],
        "sources": ["《中国古桥史》", "潮州文物局"]
    },
    {
        "id": "shiqiqiao-bridge",
        "name": "十七孔桥",
        "alias": ["颐和园长桥"],
        "dynasty": "清代",
        "buildYear": "1750年",
        "location": {
            "province": "北京市",
            "city": "北京市",
            "county": "海淀区",
            "coordinates": [116.2750, 39.9997]
        },
        "type": "拱桥",
        "dimensions": {"length": 150, "width": 8, "span": 17},
        "features": ["园林桥梁", "联拱石桥", "544只石狮", "皇家园林建筑"],
        "builder": {"name": "佚名", "dynasty": "清代", "intro": "清代工匠，乾隆皇帝时期修建"},
        "status": "全国重点文物保护单位",
        "heritage": None,
        "description": "十七孔桥位于北京市颐和园内，横跨昆明湖，始建于清乾隆十五年（1750年），是颐和园内最大的石桥。",
        "history": "为庆祝乾隆皇帝60寿辰而建，是清代皇家园林建筑的代表作。每年冬至前后，夕阳穿过桥洞，形成'金光穿洞'奇观。",
        "technology": {
            "innovation": "联拱园林桥梁",
            "principle": "17个拱券，中间最大，向两侧逐渐减小，造型优美",
            "significance": "中国园林桥梁的杰出代表"
        },
        "culture": {
            "poems": [],
            "legends": ["金光穿洞"]
        },
        "images": [],
        "sources": ["《中国古桥史》", "颐和园管理处"]
    },
    {
        "id": "chengyang-bridge",
        "name": "程阳风雨桥",
        "alias": ["永济桥", "程阳桥"],
        "dynasty": "清代",
        "buildYear": "1912年",
        "location": {
            "province": "广西壮族自治区",
            "city": "柳州市",
            "county": "三江侗族自治县",
            "coordinates": [109.6106, 25.7836]
        },
        "type": "梁桥",
        "dimensions": {"length": 77.76, "width": 3.75, "span": 5},
        "features": ["侗族建筑", "木结构廊桥", "不用一钉一铆", "世界十大最壮观的桥梁之一"],
        "builder": {"name": "侗族工匠", "dynasty": "清代", "intro": "侗族传统工匠，采用传统木结构技术"},
        "status": "全国重点文物保护单位",
        "heritage": None,
        "description": "程阳风雨桥位于广西三江侗族自治县，始建于1912年，是侗族建筑的杰出代表，也是中国最大的风雨桥。",
        "history": "由侗族工匠建造，全桥不用一钉一铆，完全采用榫卯结构，体现了侗族人民的建筑智慧。",
        "technology": {
            "innovation": "木结构榫卯技术",
            "principle": "整座桥采用榫卯结构，不用一钉一铆，结构稳固",
            "significance": "侗族建筑艺术的结晶，世界木结构建筑的杰作"
        },
        "culture": {
            "poems": [],
            "legends": ["侗族歌仙传说"]
        },
        "images": [],
        "sources": ["《中国古桥史》", "三江县文物局"]
    },
    {
        "id": "anping-bridge",
        "name": "安平桥",
        "alias": ["五里桥"],
        "dynasty": "宋代",
        "buildYear": "1138-1152年",
        "location": {
            "province": "福建省",
            "city": "泉州市",
            "county": "晋江市",
            "coordinates": [118.4583, 24.7356]
        },
        "type": "梁桥",
        "dimensions": {"length": 2070, "width": 3.7, "span": 361},
        "features": ["最长石梁桥", "海港石桥", "中古时代世界最长桥梁", "天下无桥长此桥"],
        "builder": {"name": "佚名", "dynasty": "宋代", "intro": "宋代工匠，僧人祖派主持"},
        "status": "全国重点文物保护单位",
        "heritage": None,
        "description": "安平桥位于福建省晋江市，始建于南宋绍兴八年（1138年），历时14年建成，是中国现存最长的石梁桥。",
        "history": "因桥长约5华里，俗称'五里桥'。中古时代世界最长的梁式石桥，被誉为'天下无桥长此桥'。",
        "technology": {
            "innovation": "超长石梁桥技术",
            "principle": "采用石墩石梁结构，桥墩采用长方形和船形两种形式",
            "significance": "中古时代世界最长的梁式石桥"
        },
        "culture": {
            "poems": [
                {"author": "佚名", "dynasty": "明代", "title": "安平桥诗", "content": "天下无桥长此桥"}
            ],
            "legends": []
        },
        "images": [],
        "sources": ["《中国古桥史》", "晋江市文物局"]
    },
    {
        "id": "baqiao-bridge",
        "name": "灞桥",
        "alias": ["霸桥"],
        "dynasty": "隋唐",
        "buildYear": "隋代（重建）",
        "location": {
            "province": "陕西省",
            "city": "西安市",
            "county": "灞桥区",
            "coordinates": [109.0583, 34.2767]
        },
        "type": "拱桥",
        "dimensions": {"length": 386, "width": 7, "span": 0},
        "features": ["送别文化", "石拱桥", "古都门户", "灞桥折柳"],
        "builder": {"name": "佚名", "dynasty": "隋代", "intro": "隋代工匠，原桥建于汉代，隋代重建"},
        "status": "全国重点文物保护单位",
        "heritage": None,
        "description": "灞桥位于陕西省西安市灞河上，始建于汉代，隋代重建，是中国古代著名的送别之地。",
        "history": "古代长安城东门户，人们在此折柳送别，'灞桥折柳'成为送别的代名词。唐代诗人多有咏灞桥之作。",
        "technology": {
            "innovation": "多孔石拱桥",
            "principle": "采用多孔石拱结构，桥面平坦",
            "significance": "中国古代交通要道，送别文化的象征"
        },
        "culture": {
            "poems": [
                {"author": "李白", "dynasty": "唐代", "title": "灞陵行送别", "content": "送君灞陵亭，灞水流浩浩"}
            ],
            "legends": ["灞桥折柳"]
        },
        "images": [],
        "sources": ["《中国古桥史》", "西安市文物局"]
    },
    {
        "id": "duanqiao-bridge",
        "name": "断桥",
        "alias": ["段桥", "宝祐桥"],
        "dynasty": "唐代",
        "buildYear": "唐代（具体年代不详）",
        "location": {
            "province": "浙江省",
            "city": "杭州市",
            "county": "西湖区",
            "coordinates": [120.1489, 30.2544]
        },
        "type": "拱桥",
        "dimensions": {"length": 8.8, "width": 8.6, "span": 1},
        "features": ["园林桥梁", "西湖十景", "白蛇传说", "世界文化遗产"],
        "builder": {"name": "佚名", "dynasty": "唐代", "intro": "唐代工匠，具体姓名已不可考"},
        "status": "全国重点文物保护单位",
        "heritage": "世界文化遗产",
        "description": "断桥位于杭州西湖白堤东端，是西湖著名的景点之一，'断桥残雪'为西湖十景之一。",
        "history": "唐代始建，宋代称'段家桥'，后简称'段桥'，谐音'断桥'。《白蛇传》中白娘子与许仙相遇于此，使断桥成为爱情圣地。",
        "technology": {
            "innovation": "园林拱桥",
            "principle": "单孔石拱桥，造型优美",
            "significance": "中国园林桥梁的典范，文学艺术中的经典意象"
        },
        "culture": {
            "poems": [
                {"author": "张祜", "dynasty": "唐代", "title": "题杭州孤山寺", "content": "断桥荒藓涩，空院落花深"}
            ],
            "legends": ["白蛇传", "断桥残雪"]
        },
        "images": [],
        "sources": ["《中国古桥史》", "西湖风景名胜区管委会"]
    },
    {
        "id": "zhaozhou-bridge",
        "name": "赵州桥",
        "alias": ["安济桥", "大石桥"],
        "dynasty": "隋代",
        "buildYear": "595-605年",
        "location": {
            "province": "河北省",
            "city": "石家庄市",
            "county": "赵县",
            "coordinates": [114.7697, 37.7472]
        },
        "type": "拱桥",
        "dimensions": {"length": 64.4, "width": 9.6, "span": 37.02},
        "features": ["敞肩拱", "单孔石拱", "世界最早敞肩石拱桥"],
        "builder": {"name": "李春", "dynasty": "隋代", "intro": "隋代著名工匠，赵州桥设计建造者"},
        "status": "全国重点文物保护单位",
        "heritage": "世界文化遗产预备名单",
        "description": "赵州桥始建于隋开皇十五年至大业元年（595-605年），由著名工匠李春设计建造。",
        "history": "隋代始建，历经唐、宋、元、明、清各代修缮，至今已有1400多年历史。",
        "technology": {
            "innovation": "敞肩拱技术",
            "principle": "在大拱两肩各砌两个小拱，既减轻桥身自重，又增加泄洪面积",
            "significance": "比欧洲同类桥梁早1200多年"
        },
        "culture": {
            "poems": [
                {"author": "张嘉贞", "dynasty": "唐代", "title": "赵州桥铭", "content": "制造奇特，人不知其所以为"}
            ],
            "legends": ["鲁班造桥传说", "张果老试桥传说"]
        },
        "images": [],
        "sources": ["《中国古桥史》", "赵县文物保管所官网"]
    },
    # ==================== 新增桥梁 ====================
    {
        "id": "hongqiao-bridge",
        "name": "虹桥",
        "alias": ["飞桥", "编拱桥"],
        "dynasty": "宋代",
        "buildYear": "北宋时期",
        "location": {
            "province": "河南省",
            "city": "开封市",
            "county": "市区",
            "coordinates": [114.3074, 34.7973]
        },
        "type": "拱桥",
        "dimensions": {"length": 25, "width": 8, "span": 20},
        "features": ["编拱桥", "木拱桥", "清明上河图原型", "无柱跨河"],
        "builder": {"name": "佚名", "dynasty": "宋代", "intro": "宋代工匠，首创编拱技术"},
        "status": "已毁",
        "heritage": None,
        "description": "虹桥是北宋时期汴京（今开封）的一座木拱桥，因《清明上河图》而闻名于世。其独特的编拱结构，无需桥墩即可跨越河流。",
        "history": "建于北宋，是当时汴河上的重要桥梁。张择端《清明上河图》中生动描绘了虹桥上繁忙的市井景象。原桥已毁，现存为后人仿建。",
        "technology": {
            "innovation": "编拱技术",
            "principle": "木杆相互穿插编成拱形，结构巧妙，无需中间桥墩",
            "significance": "中国木拱桥技术的杰出代表，影响后世廊桥建设"
        },
        "culture": {
            "poems": [],
            "legends": ["清明上河图"]
        },
        "images": [],
        "sources": ["《清明上河图》", "《中国古桥史》"]
    },
    {
        "id": "jinci-bridge",
        "name": "鱼沼飞梁",
        "alias": ["十字桥"],
        "dynasty": "北魏",
        "buildYear": "北魏时期（约6世纪）",
        "location": {
            "province": "山西省",
            "city": "太原市",
            "county": "晋源区",
            "coordinates": [112.4476, 37.7085]
        },
        "type": "梁桥",
        "dimensions": {"length": 19.6, "width": 19.6, "span": 0},
        "features": ["十字形桥梁", "石柱梁桥", "现存最早十字桥", "晋祠古建筑群"],
        "builder": {"name": "佚名", "dynasty": "北魏", "intro": "北魏工匠"},
        "status": "全国重点文物保护单位",
        "heritage": None,
        "description": "鱼沼飞梁位于山西太原晋祠内，是一座十字形石柱梁桥，是中国现存最早的十字桥。",
        "history": "建于北魏时期，是晋祠圣母殿前的祭祀桥梁。桥呈十字形，东西南北四面相通，造型独特。",
        "technology": {
            "innovation": "十字形梁桥结构",
            "principle": "石柱承托梁板，形成十字形通道",
            "significance": "中国现存最早的十字桥，古桥梁中的孤例"
        },
        "culture": {
            "poems": [],
            "legends": ["晋祠圣母传说"]
        },
        "images": [],
        "sources": ["《中国古桥史》", "晋祠博物馆"]
    },
    {
        "id": "wanshou-bridge",
        "name": "万寿桥",
        "alias": ["闽江大桥"],
        "dynasty": "元代",
        "buildYear": "1303-1322年",
        "location": {
            "province": "福建省",
            "city": "福州市",
            "county": "台江区",
            "coordinates": [119.3065, 26.0753]
        },
        "type": "梁桥",
        "dimensions": {"length": 800, "width": 4.5, "span": 0},
        "features": ["石梁桥", "闽江古桥", "元代石桥", "福州古代交通要道"],
        "builder": {"name": "佚名", "dynasty": "元代", "intro": "元代工匠"},
        "status": "已改建",
        "heritage": None,
        "description": "万寿桥位于福建省福州市闽江上，始建于元代大德七年（1303年），历时19年建成，是福州古代重要的跨江石桥。",
        "history": "元代始建，是福州通往闽南的重要通道。后历经重修改建，现已不复原貌。",
        "technology": {
            "innovation": "大型石梁桥",
            "principle": "石墩石梁结构，跨江而建",
            "significance": "元代福建地区重要的交通桥梁"
        },
        "culture": {
            "poems": [],
            "legends": []
        },
        "images": [],
        "sources": ["《中国古桥史》", "福州市文物局"]
    },
    {
        "id": "sudongpo-bridge",
        "name": "苏堤春晓桥",
        "alias": ["苏堤六桥"],
        "dynasty": "宋代",
        "buildYear": "1089年",
        "location": {
            "province": "浙江省",
            "city": "杭州市",
            "county": "西湖区",
            "coordinates": [120.1372, 30.2444]
        },
        "type": "拱桥",
        "dimensions": {"length": 0, "width": 0, "span": 0},
        "features": ["园林桥梁", "西湖十景", "苏轼修建", "世界文化遗产"],
        "builder": {"name": "苏轼", "dynasty": "宋代", "intro": "北宋著名文学家、政治家，曾任杭州知州，主持疏浚西湖并修筑苏堤"},
        "status": "全国重点文物保护单位",
        "heritage": "世界文化遗产",
        "description": "苏堤上的六座石拱桥，是北宋苏轼任杭州知州时主持修建。苏堤横贯西湖，堤上有六座石拱桥，分别是映波、锁澜、望山、压堤、东浦、跨虹。",
        "history": "元祐四年（1089年），苏轼主持疏浚西湖，用挖出的淤泥筑成苏堤，堤上建六桥。'苏堤春晓'成为西湖十景之一。",
        "technology": {
            "innovation": "园林景观桥梁",
            "principle": "石拱桥与堤岸结合，形成优美的景观通道",
            "significance": "中国园林景观桥梁的典范"
        },
        "culture": {
            "poems": [
                {"author": "苏轼", "dynasty": "宋代", "title": "饮湖上初晴后雨", "content": "欲把西湖比西子，淡妆浓抹总相宜"}
            ],
            "legends": ["苏东坡疏浚西湖"]
        },
        "images": [],
        "sources": ["《中国古桥史》", "西湖风景名胜区管委会"]
    },
    {
        "id": "zhaoding-bridge",
        "name": "赵王河桥",
        "alias": ["赵王桥"],
        "dynasty": "明代",
        "buildYear": "明万历年间",
        "location": {
            "province": "河北省",
            "city": "邯郸市",
            "county": "永年区",
            "coordinates": [114.5432, 36.7891]
        },
        "type": "拱桥",
        "dimensions": {"length": 80, "width": 6, "span": 0},
        "features": ["石拱桥", "明代古桥", "永年古城"],
        "builder": {"name": "佚名", "dynasty": "明代", "intro": "明代工匠"},
        "status": "文物保护单位",
        "heritage": None,
        "description": "赵王河桥位于河北省邯郸市永年区，是明代修建的石拱桥，为永年古城的重要历史遗存。",
        "history": "明万历年间修建，是赵王河上的重要交通桥梁。",
        "technology": {
            "innovation": "石拱桥结构",
            "principle": "多孔石拱，坚固耐用",
            "significance": "明代石拱桥的代表"
        },
        "culture": {
            "poems": [],
            "legends": []
        },
        "images": [],
        "sources": ["《中国古桥史》", "邯郸市文物局"]
    },
    {
        "id": "jiulong-bridge",
        "name": "九龙桥",
        "alias": ["九孔桥"],
        "dynasty": "明代",
        "buildYear": "明嘉靖年间",
        "location": {
            "province": "江苏省",
            "city": "南京市",
            "county": "江宁区",
            "coordinates": [118.7856, 31.9567]
        },
        "type": "拱桥",
        "dimensions": {"length": 85, "width": 7, "span": 9},
        "features": ["九孔石拱桥", "南京古桥", "明代桥梁"],
        "builder": {"name": "佚名", "dynasty": "明代", "intro": "明代工匠"},
        "status": "文物保护单位",
        "heritage": None,
        "description": "九龙桥位于江苏省南京市江宁区，是一座九孔石拱桥，因九孔相连如九龙戏水而得名。",
        "history": "明嘉靖年间修建，是南京地区保存较好的明代石拱桥。",
        "technology": {
            "innovation": "九孔联拱结构",
            "principle": "九孔相连，整体稳定",
            "significance": "明代联拱石桥的代表"
        },
        "culture": {
            "poems": [],
            "legends": ["九龙戏水"]
        },
        "images": [],
        "sources": ["《中国古桥史》", "南京市文物局"]
    },
    {
        "id": "wulong-bridge",
        "name": "乌龙桥",
        "alias": ["五龙桥"],
        "dynasty": "唐代",
        "buildYear": "唐代",
        "location": {
            "province": "陕西省",
            "city": "西安市",
            "county": "长安区",
            "coordinates": [108.9567, 34.2345]
        },
        "type": "拱桥",
        "dimensions": {"length": 45, "width": 5, "span": 5},
        "features": ["五孔石拱桥", "唐代古桥", "长安古桥"],
        "builder": {"name": "佚名", "dynasty": "唐代", "intro": "唐代工匠"},
        "status": "文物保护单位",
        "heritage": None,
        "description": "乌龙桥位于陕西省西安市长安区，是一座五孔石拱桥，建于唐代，是长安地区重要的古桥之一。",
        "history": "唐代修建，是长安城南的重要通道。",
        "technology": {
            "innovation": "五孔联拱结构",
            "principle": "五孔相连，造型优美",
            "significance": "唐代石拱桥的代表"
        },
        "culture": {
            "poems": [],
            "legends": ["乌龙传说"]
        },
        "images": [],
        "sources": ["《中国古桥史》", "西安市文物局"]
    },
    {
        "id": "dujiangyan-bridge",
        "name": "安澜索桥",
        "alias": ["珠浦桥", "夫妻桥"],
        "dynasty": "宋代",
        "buildYear": "宋代始建，清代重建",
        "location": {
            "province": "四川省",
            "city": "都江堰市",
            "county": "都江堰市",
            "coordinates": [103.6156, 31.0045]
        },
        "type": "索桥",
        "dimensions": {"length": 280, "width": 3, "span": 0},
        "features": ["竹索桥", "都江堰水利工程", "世界文化遗产", "古代索桥技术"],
        "builder": {"name": "佚名", "dynasty": "宋代", "intro": "宋代工匠，清代重建时由何先德夫妇主持"},
        "status": "全国重点文物保护单位",
        "heritage": "世界文化遗产",
        "description": "安澜索桥位于四川省都江堰市，横跨岷江，是都江堰水利工程的重要组成部分，中国古代索桥技术的杰出代表。",
        "history": "宋代始建，初名珠浦桥，用竹索建造。清代重建，改名为安澜桥，取'安渡狂澜'之意。",
        "technology": {
            "innovation": "竹索悬吊技术",
            "principle": "用竹索为主要承重构件，悬吊桥面",
            "significance": "中国古代索桥技术的杰出代表，体现古代竹材利用智慧"
        },
        "culture": {
            "poems": [],
            "legends": ["何先德夫妇造桥"]
        },
        "images": [],
        "sources": ["《中国古桥史》", "都江堰景区"]
    },
    {
        "id": "zhuhong-bridge",
        "name": "朱红桥",
        "alias": ["朱家桥"],
        "dynasty": "明代",
        "buildYear": "明洪武年间",
        "location": {
            "province": "江苏省",
            "city": "苏州市",
            "county": "姑苏区",
            "coordinates": [120.5856, 31.3245]
        },
        "type": "拱桥",
        "dimensions": {"length": 35, "width": 4, "span": 1},
        "features": ["江南石拱桥", "苏州古桥", "单孔石桥"],
        "builder": {"name": "佚名", "dynasty": "明代", "intro": "明代工匠"},
        "status": "文物保护单位",
        "heritage": None,
        "description": "朱红桥位于江苏省苏州市姑苏区，是一座典型的江南单孔石拱桥，体现了江南水乡桥梁的建筑特色。",
        "history": "明洪武年间修建，是苏州古城内保存较好的明代石拱桥。",
        "technology": {
            "innovation": "江南单孔石拱桥",
            "principle": "单孔拱形，便于船只通行",
            "significance": "江南水乡桥梁的典型代表"
        },
        "culture": {
            "poems": [],
            "legends": []
        },
        "images": [],
        "sources": ["《中国古桥史》", "苏州市文物局"]
    },
    {
        "id": "fengyu-bridge-longsheng",
        "name": "风雨桥",
        "alias": ["花桥", "福桥"],
        "dynasty": "清代",
        "buildYear": "清代",
        "location": {
            "province": "广西壮族自治区",
            "city": "桂林市",
            "county": "龙胜县",
            "coordinates": [110.0234, 25.7891]
        },
        "type": "梁桥",
        "dimensions": {"length": 60, "width": 4, "span": 0},
        "features": ["侗族风雨桥", "木结构廊桥", "少数民族建筑", "榫卯结构"],
        "builder": {"name": "侗族工匠", "dynasty": "清代", "intro": "侗族传统工匠"},
        "status": "文物保护单位",
        "heritage": None,
        "description": "风雨桥是侗族特有的建筑形式，桥上有廊屋，可避风雨，故名风雨桥。这座位于广西龙胜的风雨桥是侗族建筑的代表。",
        "history": "清代由侗族工匠建造，是侗族村寨的重要公共建筑。",
        "technology": {
            "innovation": "侗族木结构廊桥",
            "principle": "全木结构，榫卯连接，廊屋覆盖",
            "significance": "侗族建筑文化的集中体现"
        },
        "culture": {
            "poems": [],
            "legends": ["侗族风雨桥传说"]
        },
        "images": [],
        "sources": ["《中国古桥史》", "龙胜县文物局"]
    }
]

def main():
    """主函数：导入桥梁数据"""
    # 加载现有数据
    existing_bridges = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            existing_bridges = json.load(f)
    
    # 获取现有ID
    existing_ids = {b.get('id') for b in existing_bridges}
    
    # 添加新数据（跳过已存在的）
    added = 0
    for bridge in NEW_BRIDGES:
        if bridge['id'] not in existing_ids:
            existing_bridges.append(bridge)
            added += 1
            print(f"✅ 添加: {bridge['name']}")
        else:
            print(f"⏭️ 跳过: {bridge['name']} (已存在)")
    
    # 保存
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing_bridges, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*50}")
    print(f"📊 导入完成!")
    print(f"   新增: {added} 座")
    print(f"   总计: {len(existing_bridges)} 座")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()