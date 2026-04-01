import axios from 'axios'

// API 基础地址
const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

// 创建 axios 实例
const request = axios.create({
  baseURL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 可以在这里添加 token 等
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default request

// 桥梁相关 API
export const bridgeAPI = {
  // 获取桥梁列表
  getList: (params) => request.get('/api/bridges', { params }),
  
  // 获取桥梁详情
  getDetail: (id) => request.get(`/api/bridges/${id}`),
  
  // 搜索桥梁
  search: (query) => request.get('/api/bridges/search', { params: { q: query } }),
  
  // 获取地图数据
  getMapData: () => request.get('/api/bridges/map'),
  
  // 获取时间轴数据
  getTimeline: () => request.get('/api/bridges/timeline')
}

// AI 问答相关 API
export const aiAPI = {
  // 发送问题
  chat: (question, history = []) => request.post('/api/ai/chat', { question, history }),
  
  // 获取推荐问题
  getSuggestions: () => request.get('/api/ai/suggestions')
}

// 统计相关 API
export const statsAPI = {
  // 获取总览数据
  getOverview: () => request.get('/api/statistics/overview'),
  
  // 按类型统计
  getByType: () => request.get('/api/statistics/by-type'),
  
  // 按朝代统计
  getByDynasty: () => request.get('/api/statistics/by-dynasty'),
  
  // 按地区统计
  getByRegion: () => request.get('/api/statistics/by-region'),
  
  // 技术里程碑
  getMilestones: () => request.get('/api/statistics/tech-milestones')
}