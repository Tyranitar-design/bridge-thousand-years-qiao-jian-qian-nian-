# -*- coding: utf-8 -*-
"""
桥梁数据导入脚本
用于批量导入和管理桥梁数据
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import os
from datetime import datetime

# 数据文件路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, 'bridges.json')

def load_bridges():
    """加载现有桥梁数据"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_bridges(bridges):
    """保存桥梁数据"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(bridges, f, ensure_ascii=False, indent=2)
    print(f"✅ 已保存 {len(bridges)} 座桥梁数据")

def add_bridge(bridge_data):
    """添加单座桥梁"""
    bridges = load_bridges()
    
    # 检查是否已存在
    existing_ids = [b.get('id') for b in bridges]
    if bridge_data.get('id') in existing_ids:
        print(f"⚠️ 桥梁 {bridge_data.get('name')} 已存在，跳过")
        return False
    
    bridges.append(bridge_data)
    save_bridges(bridges)
    print(f"✅ 已添加: {bridge_data.get('name')}")
    return True

def add_bridges_batch(bridges_list):
    """批量添加桥梁"""
    bridges = load_bridges()
    existing_ids = [b.get('id') for b in bridges]
    
    added = 0
    skipped = 0
    for bridge in bridges_list:
        if bridge.get('id') in existing_ids:
            skipped += 1
            continue
        bridges.append(bridge)
        added += 1
    
    save_bridges(bridges)
    print(f"✅ 批量导入完成: 新增 {added} 座，跳过 {skipped} 座")
    return added

def get_bridge_template():
    """获取桥梁数据模板"""
    return {
        "id": "bridge-id",
        "name": "桥梁名称",
        "alias": ["别名1", "别名2"],
        "dynasty": "朝代",
        "buildYear": "建造年份",
        "location": {
            "province": "省份",
            "city": "城市",
            "county": "区县",
            "coordinates": [经度, 纬度]
        },
        "type": "拱桥/梁桥/索桥/浮桥",
        "dimensions": {
            "length": 0,
            "width": 0,
            "span": 0
        },
        "features": ["特点1", "特点2"],
        "builder": {
            "name": "建造者姓名",
            "dynasty": "朝代",
            "intro": "简介"
        },
        "status": "保护级别",
        "heritage": "世界遗产状态",
        "description": "详细描述",
        "history": "历史沿革",
        "technology": {
            "innovation": "技术创新",
            "principle": "技术原理",
            "significance": "历史意义"
        },
        "culture": {
            "poems": [
                {"author": "作者", "dynasty": "朝代", "title": "标题", "content": "内容"}
            ],
            "legends": ["传说故事"]
        },
        "images": [],
        "sources": ["资料来源"]
    }

def export_to_markdown():
    """导出为 Markdown 格式"""
    bridges = load_bridges()
    
    md_content = "# 中国古代桥梁数据\n\n"
    md_content += f"> 数据更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    md_content += f"> 桥梁总数：{len(bridges)} 座\n\n"
    
    for bridge in bridges:
        md_content += f"## {bridge.get('name', '未知')}\n\n"
        md_content += f"- **别名**：{', '.join(bridge.get('alias', [])) or '无'}\n"
        md_content += f"- **朝代**：{bridge.get('dynasty', '未知')}\n"
        md_content += f"- **类型**：{bridge.get('type', '未知')}\n"
        md_content += f"- **地点**：{bridge.get('location', {}).get('province', '')} {bridge.get('location', {}).get('city', '')}\n"
        md_content += f"- **简介**：{bridge.get('description', '')[:100]}...\n\n"
        md_content += "---\n\n"
    
    export_file = os.path.join(SCRIPT_DIR, 'bridges_export.md')
    with open(export_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"✅ 已导出到: {export_file}")

def show_statistics():
    """显示数据统计"""
    bridges = load_bridges()
    
    print("\n" + "="*50)
    print("📊 桥梁数据统计")
    print("="*50)
    print(f"桥梁总数：{len(bridges)} 座\n")
    
    # 类型统计
    types = {}
    for b in bridges:
        t = b.get('type', '未知')
        types[t] = types.get(t, 0) + 1
    
    print("按类型分布：")
    for t, count in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  - {t}: {count} 座")
    
    # 朝代统计
    dynasties = {}
    for b in bridges:
        d = b.get('dynasty', '未知')
        dynasties[d] = dynasties.get(d, 0) + 1
    
    print("\n按朝代分布：")
    for d, count in sorted(dynasties.items(), key=lambda x: -x[1]):
        print(f"  - {d}: {count} 座")
    
    # 地区统计
    provinces = {}
    for b in bridges:
        p = b.get('location', {}).get('province', '未知')
        provinces[p] = provinces.get(p, 0) + 1
    
    print("\n按地区分布：")
    for p, count in sorted(provinces.items(), key=lambda x: -x[1]):
        print(f"  - {p}: {count} 座")
    
    print("="*50 + "\n")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python import_bridges.py stats      # 显示统计")
        print("  python import_bridges.py export     # 导出为Markdown")
        print("  python import_bridges.py template   # 显示数据模板")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == 'stats':
        show_statistics()
    elif command == 'export':
        export_to_markdown()
    elif command == 'template':
        template = get_bridge_template()
        print(json.dumps(template, ensure_ascii=False, indent=2))
    else:
        print(f"未知命令: {command}")