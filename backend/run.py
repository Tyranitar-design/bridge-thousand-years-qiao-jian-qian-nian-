# -*- coding: utf-8 -*-
"""
【桥见千年】中国古代桥梁智慧可视化平台
后端API服务
"""
from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # 配置
    app.config['JSON_AS_ASCII'] = False
    app.config['SECRET_KEY'] = 'bridge-millennium-2026'
    
    # 注册路由
    from app.routes.bridges import bridge_bp
    from app.routes.ai import ai_bp
    from app.routes.statistics import stats_bp
    
    app.register_blueprint(bridge_bp, url_prefix='/api/bridges')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(stats_bp, url_prefix='/api/statistics')
    
    # 根路由
    @app.route('/')
    def index():
        return jsonify({
            'name': '【桥见千年】API',
            'version': '1.0.0',
            'message': '中国古代桥梁智慧可视化平台'
        })
    
    # 健康检查
    @app.route('/health')
    def health():
        return jsonify({'status': 'ok'})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
