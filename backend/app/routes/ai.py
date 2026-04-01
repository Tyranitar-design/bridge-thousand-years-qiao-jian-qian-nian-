# -*- coding: utf-8 -*-
"""
AI智能问答API路由
"""
from flask import Blueprint, jsonify, request
import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

ai_bp = Blueprint('ai', __name__)

# GLM API配置（从环境变量读取）
GLM_API_KEY = os.environ.get('GLM_API_KEY', '')
GLM_API_URL = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'

# 预设推荐问题
SUGGESTED_QUESTIONS = [
    "赵州桥为什么能屹立1400年不倒？",
    "中国古代桥梁有哪些主要类型？",
    "敞肩拱技术是什么？有什么意义？",
    "卢沟桥的石狮有多少只？",
    "泸定桥的铁索是怎么制成的？",
    "中国古代有哪些著名的桥梁建造者？",
    "《营造法式》中记载了哪些桥梁技术？"
]

@ai_bp.route('/chat', methods=['POST'])
def chat():
    """AI问答"""
    data = request.get_json()
    question = data.get('question', '')
    history = data.get('history', [])
    
    if not question:
        return jsonify({
            'success': False,
            'message': '问题不能为空'
        }), 400
    
    # 构建上下文
    system_prompt = """你是【桥见千年】中国古代桥梁智慧可视化平台的AI助手。
你的专业知识范围包括：
1. 中国古代桥梁的历史、技术、文化
2. 桥梁建筑类型：拱桥、梁桥、索桥、浮桥
3. 著名古桥：赵州桥、卢沟桥、泸定桥、洛阳桥、广济桥等
4. 桥梁建造技术与工艺
5. 建造者传记与工匠精神
6. 与桥梁相关的诗词歌赋、典故传说

请用专业、准确、有温度的语言回答用户问题。如果问题超出你的知识范围，请诚实告知。"""

    messages = [{"role": "system", "content": system_prompt}]
    
    # 添加历史对话
    for h in history:
        messages.append({"role": h.get("role"), "content": h.get("content")})
    
    # 添加当前问题
    messages.append({"role": "user", "content": question})
    
    try:
        # 调用GLM API
        if GLM_API_KEY:
            response = requests.post(
                GLM_API_URL,
                headers={
                    'Authorization': f'Bearer {GLM_API_KEY}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'glm-4',
                    'messages': messages,
                    'temperature': 0.7,
                    'max_tokens': 1000
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                
                return jsonify({
                    'success': True,
                    'data': {
                        'answer': answer,
                        'sources': []  # RAG时添加来源
                    }
                })
            else:
                # API调用失败，使用备用回答
                return jsonify({
                    'success': True,
                    'data': {
                        'answer': get_fallback_answer(question),
                        'sources': [],
                        'note': '使用本地知识库'
                    }
                })
        else:
            # 无API Key，使用本地知识库
            return jsonify({
                'success': True,
                'data': {
                    'answer': get_fallback_answer(question),
                    'sources': [],
                    'note': '使用本地知识库'
                }
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'AI服务暂时不可用：{str(e)}'
        }), 500

@ai_bp.route('/suggestions', methods=['GET'])
def get_suggestions():
    """获取推荐问题"""
    return jsonify({
        'success': True,
        'data': SUGGESTED_QUESTIONS
    })

def get_fallback_answer(question):
    """备用问答（本地知识库）"""
    # 简单的关键词匹配
    qa_pairs = {
        '赵州桥': """赵州桥（又名安济桥）位于河北省赵县，始建于隋代（公元595-605年），由著名工匠李春设计建造。

**建筑成就：**
- 世界上现存最早、保存最完好的敞肩石拱桥
- 主拱跨径37.02米，在当时是世界之最
- 敞肩拱设计减轻桥身重量约700吨

**屹立千年不倒的原因：**
1. **敞肩拱技术**：大拱两肩各设两个小拱，既减轻自重，又增大泄洪面积
2. **合理选材**：使用本地优质青白色石灰岩，质地坚硬
3. **精湛工艺**：28道拱圈纵向并列砌筑，整体性强
4. **科学选址**：建在汶河河床坚硬的冲积层上

赵州桥比欧洲同类桥梁早1200多年，被誉为"天下第一桥"。""",

        '敞肩拱': """**敞肩拱技术**是中国古代桥梁建筑的重大创新，由隋代工匠李春在赵州桥首次应用。

**技术原理：**
在大拱两肩各砌筑两个小拱，形成"敞肩"结构。

**技术优势：**
1. **减轻自重**：四个小拱减少石材用量，减轻桥身重量约700吨
2. **增大泄洪**：洪水时可从四个小拱分流，减少水流冲击力
3. **节省材料**：减少石材使用，降低建造成本
4. **美观协调**：整体造型更加轻盈优美

**世界意义：**
敞肩拱技术比欧洲早1200多年，是世界桥梁史上的创举，体现了中国古代工匠的卓越智慧。""",

        '卢沟桥': """**卢沟桥**位于北京市丰台区，横跨永定河，始建于金大定二十九年（1189年），是北京现存最古老的石造联拱桥。

**建筑特色：**
- 全长266.5米，宽7.5米，11孔联拱结构
- 桥身全部用白石建成，造型优美

**艺术珍品——石狮：**
- 桥两侧石雕护栏各有140根望柱
- 每根望柱上雕刻石狮，共501只（一说485只）
- 石狮形态各异，无一雷同，是雕刻艺术宝库

**历史意义：**
1937年7月7日，"卢沟桥事变"在此爆发，揭开了中国人民抗日战争的序幕。""",

        '泸定桥': """**泸定桥**位于四川省甘孜藏族自治州泸定县，始建于清康熙四十四年（1705年），是中国现存最古老的铁索桥。

**建筑结构：**
- 全长103.67米，宽3米
- 由13根铁链组成（9根底链，4根扶手链）
- 每根铁链重约1.5吨，总重超过20吨

**技术成就：**
- 铁链锻造工艺精湛，在当时的冶炼条件下极为不易
- 铁链锚固于两岸桥台，结构稳固

**历史故事：**
1935年5月29日，中国工农红军长征途中"飞夺泸定桥"，22名勇士冒着枪林弹雨攀爬铁索，成功夺取泸定桥，成为长征史上的英雄壮举。""",

        '洛阳桥': """**洛阳桥**（原名万安桥）位于福建省泉州市，始建于北宋皇祐五年（1053年），历时6年建成，是中国第一座跨海梁式石桥。

**建筑成就：**
- 全长834米，宽7米，有46座桥墩
- **筏形基础**：在桥墩下铺垫石块，形成筏形基础，是世界桥梁史上的创举
- **种蛎固基**：利用牡蛎繁殖附着石块的特性，加固桥基，是世界首创的生物工程

**建造者：**
宋代名臣蔡襄任泉州知州时主持修建，并撰写《万安桥记》传世。

**文化价值：**
洛阳桥是"海上丝绸之路"的重要遗产，见证了泉州港的繁荣历史。"""
    }
    
    # 匹配关键词
    for keyword, answer in qa_pairs.items():
        if keyword in question:
            return answer
    
    # 默认回复
    return """感谢您的提问！我是【桥见千年】平台的AI助手，专注于中国古代桥梁知识。

我可以为您解答：
- 中国古代桥梁的历史、技术、文化
- 著名古桥介绍（赵州桥、卢沟桥、泸定桥等）
- 桥梁建造技术与工艺
- 建造者传记与工匠精神
- 与桥梁相关的诗词典故

请尝试问我关于古桥的问题，我会尽力为您解答！"""