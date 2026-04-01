# -*- coding: utf-8 -*-
"""
统计数据API路由
"""
from flask import Blueprint, jsonify
import json
import os
from collections import Counter

stats_bp = Blueprint('statistics', __name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
BRIDGES_FILE = os.path.join(DATA_DIR, 'bridges.json')

def load_bridges():
    """加载桥梁数据"""
    if os.path.exists(BRIDGES_FILE):
        with open(BRIDGES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

@stats_bp.route('/overview', methods=['GET'])
def get_overview():
    """获取总览数据"""
    bridges = load_bridges()
    
    # 计算统计数据
    total = len(bridges)
    
    # 朝代范围
    dynasties = set()
    for b in bridges:
        dynasties.add(b.get('dynasty', '未知'))
    
    # 桥梁类型
    types = Counter(b.get('type', '未知') for b in bridges)
    
    # 地区分布
    provinces = Counter(b.get('location', {}).get('province', '未知') for b in bridges)
    
    # 世界遗产
    heritage_count = sum(1 for b in bridges if b.get('heritage'))
    
    return jsonify({
        'success': True,
        'data': {
            'totalBridges': total,
            'dynastyCount': len(dynasties),
            'typeDistribution': dict(types),
            'topProvinces': dict(provinces.most_common(5)),
            'heritageCount': heritage_count,
            'yearSpan': '2500+年'  # 春秋战国到清末
        }
    })

@stats_bp.route('/by-type', methods=['GET'])
def get_by_type():
    """按类型统计"""
    bridges = load_bridges()
    
    type_stats = {}
    for b in bridges:
        bridge_type = b.get('type', '未知')
        if bridge_type not in type_stats:
            type_stats[bridge_type] = {
                'count': 0,
                'bridges': []
            }
        type_stats[bridge_type]['count'] += 1
        type_stats[bridge_type]['bridges'].append({
            'id': b.get('id'),
            'name': b.get('name')
        })
    
    return jsonify({
        'success': True,
        'data': type_stats
    })

@stats_bp.route('/by-dynasty', methods=['GET'])
def get_by_dynasty():
    """按朝代统计"""
    bridges = load_bridges()
    
    dynasty_order = ['春秋战国', '秦汉', '魏晋南北朝', '隋唐', '宋代', '元代', '明代', '清代']
    dynasty_stats = {d: {'count': 0, 'bridges': []} for d in dynasty_order}
    dynasty_stats['其他'] = {'count': 0, 'bridges': []}
    
    for b in bridges:
        dynasty = b.get('dynasty', '其他')
        found = False
        for d in dynasty_order:
            if d in dynasty:
                dynasty_stats[d]['count'] += 1
                dynasty_stats[d]['bridges'].append({
                    'id': b.get('id'),
                    'name': b.get('name')
                })
                found = True
                break
        if not found:
            dynasty_stats['其他']['count'] += 1
            dynasty_stats['其他']['bridges'].append({
                'id': b.get('id'),
                'name': b.get('name')
            })
    
    return jsonify({
        'success': True,
        'data': dynasty_stats
    })

@stats_bp.route('/by-region', methods=['GET'])
def get_by_region():
    """按地区统计"""
    bridges = load_bridges()
    
    region_stats = {}
    for b in bridges:
        province = b.get('location', {}).get('province', '未知')
        if province not in region_stats:
            region_stats[province] = {
                'count': 0,
                'bridges': []
            }
        region_stats[province]['count'] += 1
        region_stats[province]['bridges'].append({
            'id': b.get('id'),
            'name': b.get('name')
        })
    
    return jsonify({
        'success': True,
        'data': region_stats
    })

@stats_bp.route('/tech-milestones', methods=['GET'])
def get_tech_milestones():
    """技术里程碑"""
    milestones = [
        {
            'year': '公元前6世纪',
            'title': '浮桥出现',
            'description': '中国最早的可移动桥梁形式',
            'dynasty': '春秋战国'
        },
        {
            'year': '公元595-605年',
            'title': '敞肩拱技术',
            'description': '李春主持建造赵州桥，首创敞肩拱',
            'dynasty': '隋代'
        },
        {
            'year': '公元1053-1059年',
            'title': '筏形基础技术',
            'description': '蔡襄主持建造洛阳桥，发明筏形基础和种蛎固基',
            'dynasty': '宋代'
        },
        {
            'year': '公元1170年',
            'title': '启闭式桥梁',
            'description': '广济桥首创启闭式设计，方便船只通行',
            'dynasty': '宋代'
        },
        {
            'year': '公元1705年',
            'title': '大跨度铁索桥',
            'description': '泸定桥建成，铁索锻造技术达到顶峰',
            'dynasty': '清代'
        }
    ]
    
    return jsonify({
        'success': True,
        'data': milestones
    })