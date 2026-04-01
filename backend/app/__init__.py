# -*- coding: utf-8 -*-
"""App module"""
from .routes.bridges import bridge_bp
from .routes.ai import ai_bp
from .routes.statistics import stats_bp

__all__ = ['bridge_bp', 'ai_bp', 'stats_bp']