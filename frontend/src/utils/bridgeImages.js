/**
 * 桥梁图片资源配置
 * 使用本地图片资源
 * 更新时间：2026-04-01
 */

// 图片基础路径
const IMAGE_BASE = '/images/bridges/'

// 桥梁图片配置 - 使用本地图片
export const BRIDGE_IMAGES = {
  // 赵州桥
  'zhaozhou-bridge': {
    main: IMAGE_BASE + 'zhaozhou-bridge-main.jpg',
    thumb: IMAGE_BASE + 'zhaozhou-bridge-thumb.jpg',
    gallery: [
      IMAGE_BASE + 'zhaozhou-bridge-main.jpg',
      IMAGE_BASE + 'zhaozhou-bridge-detail.jpg'
    ],
    hasImage: true,
    source: '网络收集',
    license: '仅用于学习展示'
  },
  
  // 卢沟桥
  'lugou-bridge': {
    main: IMAGE_BASE + 'lugou-bridge-main.jpg',
    thumb: IMAGE_BASE + 'lugou-bridge-thumb.jpg',
    gallery: [
      IMAGE_BASE + 'lugou-bridge-main.jpg',
      IMAGE_BASE + 'lugou-bridge-detail.jpg'
    ],
    hasImage: true,
    source: '网络收集',
    license: '仅用于学习展示'
  },
  
  // 泸定桥
  'luding-bridge': {
    main: IMAGE_BASE + 'luding-bridge-main.jpg',
    thumb: IMAGE_BASE + 'luding-bridge-thumb.jpg',
    gallery: [
      IMAGE_BASE + 'luding-bridge-main.jpg'
    ],
    hasImage: true,
    source: '网络收集',
    license: '仅用于学习展示'
  },
  
  // 洛阳桥
  'luoyang-bridge': {
    main: IMAGE_BASE + 'luoyang-bridge-main.jpg',
    thumb: IMAGE_BASE + 'luoyang-bridge-thumb.jpg',
    gallery: [
      IMAGE_BASE + 'luoyang-bridge-main.jpg'
    ],
    hasImage: true,
    source: '网络收集',
    license: '仅用于学习展示'
  },
  
  // 广济桥
  'guangji-bridge': {
    main: IMAGE_BASE + 'guangji-bridge-main.jpg',
    thumb: IMAGE_BASE + 'guangji-bridge-thumb.jpg',
    gallery: [
      IMAGE_BASE + 'guangji-bridge-main.jpg'
    ],
    hasImage: true,
    source: '网络收集',
    license: '仅用于学习展示'
  },
  
  // 十七孔桥
  'shiqiqiao-bridge': {
    main: IMAGE_BASE + 'shiqiqiao-bridge-main.jpg',
    thumb: IMAGE_BASE + 'shiqiqiao-bridge-thumb.jpg',
    gallery: [
      IMAGE_BASE + 'shiqiqiao-bridge-main.jpg'
    ],
    hasImage: true,
    source: '网络收集',
    license: '仅用于学习展示'
  },
  
  // 程阳风雨桥
  'chengyang-bridge': {
    main: IMAGE_BASE + 'chengyang-bridge-main.jpg',
    thumb: IMAGE_BASE + 'chengyang-bridge-thumb.jpg',
    gallery: [
      IMAGE_BASE + 'chengyang-bridge-main.jpg'
    ],
    hasImage: true,
    source: '网络收集',
    license: '仅用于学习展示'
  },
  
  // 安平桥
  'anping-bridge': {
    main: IMAGE_BASE + 'anping-bridge-main.jpg',
    thumb: IMAGE_BASE + 'anping-bridge-thumb.jpg',
    gallery: [
      IMAGE_BASE + 'anping-bridge-main.jpg'
    ],
    hasImage: true,
    source: '网络收集',
    license: '仅用于学习展示'
  },
  
  // 断桥
  'duanqiao-bridge': {
    main: IMAGE_BASE + 'duanqiao-bridge-main.jpg',
    thumb: IMAGE_BASE + 'duanqiao-bridge-thumb.jpg',
    gallery: [
      IMAGE_BASE + 'duanqiao-bridge-main.jpg'
    ],
    hasImage: true,
    source: '网络收集',
    license: '仅用于学习展示'
  }
}

/**
 * 获取桥梁图片
 */
export function getBridgeImage(bridgeId) {
  const config = BRIDGE_IMAGES[bridgeId]
  if (config && config.hasImage) {
    return config
  }
  return { main: null, gallery: [], hasImage: false }
}

/**
 * 获取占位图样式
 */
export function getPlaceholderStyle(bridge) {
  const typeColors = {
    '拱桥': ['rgba(139, 35, 35, 0.15)', 'rgba(201, 169, 98, 0.08)'],
    '梁桥': ['rgba(30, 58, 95, 0.15)', 'rgba(201, 169, 98, 0.08)'],
    '索桥': ['rgba(46, 139, 87, 0.15)', 'rgba(201, 169, 98, 0.08)']
  }
  const colors = typeColors[bridge?.type] || typeColors['拱桥']
  return { background: `linear-gradient(135deg, ${colors[0]} 0%, ${colors[1]} 100%)` }
}

/**
 * 获取占位图图标
 */
export function getPlaceholderIcon(bridge) {
  const icons = { '拱桥': '🌉', '梁桥': '🏛️', '索桥': '⛓️' }
  return icons[bridge?.type] || '🏯'
}

export default { 
  BRIDGE_IMAGES, 
  getBridgeImage, 
  getPlaceholderStyle, 
  getPlaceholderIcon 
}
