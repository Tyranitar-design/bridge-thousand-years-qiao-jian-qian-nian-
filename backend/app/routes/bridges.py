# -*- coding: utf-8 -*-
"""
桥梁数据API路由
"""
from flask import Blueprint, jsonify, request
import json
import os

bridge_bp = Blueprint('bridges', __name__)

# 数据文件路径
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
BRIDGES_FILE = os.path.join(DATA_DIR, 'bridges.json')

def load_bridges():
    """加载桥梁数据"""
    if os.path.exists(BRIDGES_FILE):
        with open(BRIDGES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_bridges(bridges):
    """保存桥梁数据"""
    with open(BRIDGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(bridges, f, ensure_ascii=False, indent=2)

@bridge_bp.route('', methods=['GET'])
def get_bridges():
    """获取桥梁列表"""
    bridges = load_bridges()
    
    # 支持筛选
    bridge_type = request.args.get('type')
    dynasty = request.args.get('dynasty')
    province = request.args.get('province')
    
    if bridge_type:
        bridges = [b for b in bridges if b.get('type') == bridge_type]
    if dynasty:
        bridges = [b for b in bridges if dynasty in b.get('dynasty', '')]
    if province:
        bridges = [b for b in bridges if province in b.get('location', {}).get('province', '')]
    
    return jsonify({
        'success': True,
        'data': bridges,
        'total': len(bridges)
    })

@bridge_bp.route('/<bridge_id>', methods=['GET'])
def get_bridge(bridge_id):
    """获取桥梁详情"""
    bridges = load_bridges()
    bridge = next((b for b in bridges if b.get('id') == bridge_id), None)
    
    if bridge:
        return jsonify({
            'success': True,
            'data': bridge
        })
    return jsonify({
        'success': False,
        'message': '桥梁不存在'
    }), 404

@bridge_bp.route('/search', methods=['GET'])
def search_bridges():
    """搜索桥梁"""
    query = request.args.get('q', '').lower()
    bridges = load_bridges()
    
    if query:
        results = []
        for b in bridges:
            if (query in b.get('name', '').lower() or
                query in b.get('alias', []) and any(query in a.lower() for a in b.get('alias', [])) or
                query in b.get('description', '').lower()):
                results.append(b)
    else:
        results = bridges
    
    return jsonify({
        'success': True,
        'data': results,
        'total': len(results)
    })

@bridge_bp.route('/map', methods=['GET'])
def get_map_data():
    """获取地图数据（含坐标）"""
    bridges = load_bridges()
    
    map_data = []
    for b in bridges:
        location = b.get('location', {})
        coords = location.get('coordinates', [])
        if coords and len(coords) == 2:
            map_data.append({
                'id': b.get('id'),
                'name': b.get('name'),
                'type': b.get('type'),
                'dynasty': b.get('dynasty'),
                'province': location.get('province'),
                'coordinates': coords,
                'value': 1  # 用于热力图
            })
    
    return jsonify({
        'success': True,
        'data': map_data
    })

@bridge_bp.route('/timeline', methods=['GET'])
def get_timeline_data():
    """获取时间轴数据"""
    bridges = load_bridges()
    
    # 按朝代分组
    dynasty_order = ['春秋战国', '秦汉', '魏晋南北朝', '隋唐', '宋代', '元代', '明代', '清代']
    timeline = {d: [] for d in dynasty_order}
    
    for b in bridges:
        dynasty = b.get('dynasty', '未知')
        # 简单匹配
        for d in dynasty_order:
            if d in dynasty:
                timeline[d].append({
                    'id': b.get('id'),
                    'name': b.get('name'),
                    'year': b.get('buildYear'),
                    'type': b.get('type')
                })
                break
    
    return jsonify({
        'success': True,
        'data': timeline
    })

@bridge_bp.route('', methods=['POST'])
def add_bridge():
    """添加桥梁（管理功能）"""
    data = request.get_json()
    bridges = load_bridges()
    
    # 生成ID
    data['id'] = data.get('id') or data.get('name', '').lower().replace(' ', '-')
    
    bridges.append(data)
    save_bridges(bridges)
    
    return jsonify({
        'success': True,
        'message': '添加成功',
        'data': data
    })
