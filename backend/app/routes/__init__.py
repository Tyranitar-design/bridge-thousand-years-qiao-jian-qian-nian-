# -*- coding: utf-8 -*-
"""Routes module"""
from .bridges import bridge_bp
from .ai import ai_bp
from .statistics import stats_bp

__all__ = ['bridge_bp', 'ai_bp', 'stats_bp']