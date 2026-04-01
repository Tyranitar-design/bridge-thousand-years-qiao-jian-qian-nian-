<template>
  <div class="statistics-container">
    <!-- 顶部数据概览 -->
    <div class="overview-section">
      <div class="overview-card" v-for="(item, index) in overviewData" :key="index">
        <div class="card-icon">{{ item.icon }}</div>
        <div class="card-info">
          <div class="card-value">{{ item.value }}</div>
          <div class="card-label">{{ item.label }}</div>
        </div>
      </div>
    </div>

    <!-- 主要图表区域 -->
    <div class="stats-grid">
      <!-- 桥梁类型分布 -->
      <div class="chart-card">
        <div class="card-header">
          <span class="header-seal">型</span>
          <h3>桥梁类型分布</h3>
        </div>
        <div ref="typeChart" class="chart"></div>
        <div class="chart-legend">
          <div class="legend-item" v-for="item in typeLegend" :key="item.name">
            <span class="legend-dot" :style="{ background: item.color }"></span>
            <span class="legend-name">{{ item.name }}</span>
            <span class="legend-value">{{ item.count }}座</span>
          </div>
        </div>
      </div>
      
      <!-- 朝代分布统计 -->
      <div class="chart-card">
        <div class="card-header">
          <span class="header-seal">代</span>
          <h3>朝代分布统计</h3>
        </div>
        <div ref="dynastyChart" class="chart"></div>
      </div>
      
      <!-- 地区分布 -->
      <div class="chart-card wide">
        <div class="card-header">
          <span class="header-seal">域</span>
          <h3>地区分布 TOP10</h3>
        </div>
        <div ref="regionChart" class="chart region-chart"></div>
      </div>

      <!-- 桥梁规模分布 -->
      <div class="chart-card">
        <div class="card-header">
          <span class="header-seal">尺</span>
          <h3>桥梁长度分布</h3>
        </div>
        <div ref="sizeChart" class="chart"></div>
      </div>

      <!-- 技术创新统计 -->
      <div class="chart-card">
        <div class="card-header">
          <span class="header-seal">技</span>
          <h3>核心技术统计</h3>
        </div>
        <div ref="techChart" class="chart"></div>
      </div>
      
      <!-- 技术里程碑 -->
      <div class="chart-card">
        <div class="card-header">
          <span class="header-seal">碑</span>
          <h3>技术里程碑</h3>
        </div>
        <div class="milestones">
          <div class="milestone" v-for="m in milestones" :key="m.year">
            <div class="year">{{ m.year }}</div>
            <div class="content">
              <strong>{{ m.title }}</strong>
              <p>{{ m.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 数据洞察 -->
    <div class="insight-section">
      <div class="section-header">
        <span class="header-seal">察</span>
        <h3>数据洞察</h3>
      </div>
      <div class="insight-grid">
        <div class="insight-card" v-for="(insight, index) in insights" :key="index">
          <span class="insight-icon">{{ insight.icon }}</span>
          <div class="insight-content">
            <strong>{{ insight.title }}</strong>
            <p>{{ insight.content }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, computed } from 'vue'
import * as echarts from 'echarts'
import { statsAPI, bridgeAPI } from '@/api'

const typeChart = ref(null)
const dynastyChart = ref(null)
const regionChart = ref(null)
const sizeChart = ref(null)
const techChart = ref(null)
const milestones = ref([])
const bridges = ref([])

// 概览数据
const overviewData = computed(() => [
  { icon: '🏯', value: bridges.value.length, label: '古桥总数' },
  { icon: '🏛️', value: new Set(bridges.value.map(b => b.dynasty)).size, label: '跨越朝代' },
  { icon: '📍', value: new Set(bridges.value.map(b => b.location?.province)).size, label: '分布省份' },
  { icon: '👨‍🔧', value: bridges.value.filter(b => b.builder?.name && b.builder.name !== '佚名').length, label: '知名匠人' }
])

// 类型图例
const typeLegend = computed(() => {
  const typeColors = { '拱桥': '#8B2323', '梁桥': '#1E3A5F', '索桥': '#2E8B57', '浮桥': '#C9A962' }
  const counts = {}
  bridges.value.forEach(b => {
    counts[b.type] = (counts[b.type] || 0) + 1
  })
  return Object.entries(counts).map(([name, count]) => ({
    name, count,
    color: typeColors[name] || '#7A7A7A'
  }))
})

// 数据洞察
const insights = computed(() => {
  const total = bridges.value.length
  if (total === 0) return []
  
  const archBridges = bridges.value.filter(b => b.type === '拱桥').length
  const songBridges = bridges.value.filter(b => b.dynasty?.includes('宋')).length
  const heritageBridges = bridges.value.filter(b => b.heritage).length
  
  return [
    {
      icon: '🌉',
      title: '拱桥技术领先',
      content: `拱桥共${archBridges}座，占比${Math.round(archBridges/total*100)}%，是中国古代桥梁的主流形式`
    },
    {
      icon: '📜',
      title: '宋代建桥高峰',
      content: `宋代共建桥${songBridges}座，是古代桥梁建设的黄金时期`
    },
    {
      icon: '🏆',
      title: '世界遗产潜力',
      content: `${heritageBridges}座桥梁列入世界文化遗产预备名单，展现中国古桥的世界价值`
    },
    {
      icon: '💡',
      title: '技术创新典范',
      content: '敞肩拱、筏形基础、铁索悬吊等技术领先世界数百年，彰显古代工匠智慧'
    }
  ]
})

onMounted(async () => {
  try {
    // 获取所有桥梁数据
    const bridgesRes = await bridgeAPI.getList()
    if (bridgesRes.success) {
      bridges.value = bridgesRes.data
    }

    const [typeRes, dynastyRes, regionRes, mileRes] = await Promise.all([
      statsAPI.getByType(),
      statsAPI.getByDynasty(),
      statsAPI.getByRegion(),
      statsAPI.getMilestones()
    ])
    
    await nextTick()
    
    // 类型分布饼图
    if (typeRes.success && typeChart.value) {
      const chart = echarts.init(typeChart.value)
      chart.setOption({
        backgroundColor: 'transparent',
        tooltip: { 
          trigger: 'item',
          backgroundColor: 'rgba(42, 42, 42, 0.95)',
          borderColor: '#C9A962',
          textStyle: { color: '#F5F0E6', fontFamily: 'Noto Serif SC' },
          formatter: '{b}: {c}座 ({d}%)'
        },
        series: [{
          type: 'pie',
          radius: ['45%', '75%'],
          center: ['50%', '50%'],
          avoidLabelOverlap: true,
          itemStyle: {
            borderRadius: 4,
            borderColor: '#F5F0E6',
            borderWidth: 2
          },
          label: {
            show: true,
            position: 'outside',
            color: '#4A4A4A',
            fontFamily: 'Noto Serif SC',
            formatter: '{b}\n{c}座'
          },
          labelLine: {
            lineStyle: { color: '#C9A962' }
          },
          data: Object.entries(typeRes.data).map(([name, data], index) => ({
            name,
            value: data.count,
            itemStyle: { 
              color: ['#8B2323', '#1E3A5F', '#2E8B57', '#C9A962'][index % 4]
            }
          }))
        }]
      })
    }
    
    // 朝代分布柱状图
    if (dynastyRes.success && dynastyChart.value) {
      const chart = echarts.init(dynastyChart.value)
      const data = Object.entries(dynastyRes.data).map(([d, data]) => ({
        name: d,
        value: data.count
      }))
      chart.setOption({
        backgroundColor: 'transparent',
        tooltip: { 
          trigger: 'axis',
          backgroundColor: 'rgba(42, 42, 42, 0.95)',
          borderColor: '#C9A962',
          textStyle: { color: '#F5F0E6' }
        },
        grid: { left: '12%', right: '8%', bottom: '18%', top: '12%' },
        xAxis: {
          type: 'category',
          data: data.map(d => d.name),
          axisLabel: { color: '#4A4A4A', fontFamily: 'Noto Serif SC', fontSize: 11, rotate: 30 },
          axisLine: { lineStyle: { color: 'rgba(139, 35, 35, 0.3)' } }
        },
        yAxis: {
          type: 'value',
          axisLabel: { color: '#7A7A7A' },
          splitLine: { lineStyle: { color: 'rgba(139, 35, 35, 0.1)', type: 'dashed' } }
        },
        series: [{
          type: 'bar',
          data: data.map(d => ({ value: d.value, itemStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: '#8B2323' }, { offset: 1, color: '#C9A96288' }]), borderRadius: [4, 4, 0, 0] } })),
          barWidth: '50%', label: { show: true, position: 'top', color: '#8B2323' }
        }]
      })
    }
    
    // 地区分布横向柱状图
    if (regionRes.success && regionChart.value) {
      const chart = echarts.init(regionChart.value)
      const data = Object.entries(regionRes.data).sort((a, b) => b[1].count - a[1].count).slice(0, 10)
      chart.setOption({
        backgroundColor: 'transparent',
        tooltip: { trigger: 'axis', backgroundColor: 'rgba(42, 42, 42, 0.95)', borderColor: '#C9A962', textStyle: { color: '#F5F0E6' } },
        grid: { left: '22%', right: '12%', bottom: '5%', top: '5%' },
        xAxis: { type: 'value', axisLabel: { color: '#7A7A7A' }, splitLine: { lineStyle: { color: 'rgba(30, 58, 95, 0.1)', type: 'dashed' } } },
        yAxis: { type: 'category', data: data.map(d => d[0]).reverse(), axisLabel: { color: '#4A4A4A', fontFamily: 'Noto Serif SC' } },
        series: [{ type: 'bar', data: data.map(d => d[1].count).reverse(), itemStyle: { color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [{ offset: 0, color: '#1E3A5F' }, { offset: 1, color: '#C9A962' }]), borderRadius: [0, 4, 4, 0] }, label: { show: true, position: 'right', color: '#1E3A5F' } }]
      })
    }

    // 桥梁长度分布
    if (bridges.value.length > 0 && sizeChart.value) {
      const chart = echarts.init(sizeChart.value)
      const lengths = bridges.value.filter(b => b.dimensions?.length).map(b => b.dimensions.length)
      const ranges = [{ name: '<100米', min: 0, max: 100 }, { name: '100-300米', min: 100, max: 300 }, { name: '300-500米', min: 300, max: 500 }, { name: '>500米', min: 500, max: 999999 }]
      const distribution = ranges.map(r => ({ name: r.name, value: lengths.filter(l => l >= r.min && l < r.max).length }))
      chart.setOption({
        backgroundColor: 'transparent',
        tooltip: { trigger: 'item', backgroundColor: 'rgba(42, 42, 42, 0.95)', borderColor: '#C9A962', textStyle: { color: '#F5F0E6' } },
        series: [{ type: 'pie', radius: ['35%', '65%'], data: distribution.map((d, i) => ({ name: d.name, value: d.value, itemStyle: { color: ['#C9A962', '#8B2323', '#1E3A5F', '#2E8B57'][i] } })), label: { color: '#4A4A4A', fontFamily: 'Noto Serif SC', fontSize: 11 } }]
      })
    }

    // 核心技术统计
    if (bridges.value.length > 0 && techChart.value) {
      const chart = echarts.init(techChart.value)
      const techs = ['敞肩拱', '筏形基础', '铁索悬吊', '榫卯结构', '浮桥启闭']
      const techCounts = techs.map(t => ({ name: t, value: bridges.value.filter(b => b.technology?.innovation?.includes(t) || b.features?.some(f => f.includes(t))).length }))
      chart.setOption({
        backgroundColor: 'transparent',
        tooltip: { trigger: 'axis', backgroundColor: 'rgba(42, 42, 42, 0.95)', borderColor: '#C9A962', textStyle: { color: '#F5F0E6' } },
        radar: { indicator: techCounts.map(t => ({ name: t.name, max: 10 })), axisName: { color: '#4A4A4A', fontFamily: 'Noto Serif SC', fontSize: 10 }, splitLine: { lineStyle: { color: 'rgba(139, 35, 35, 0.2)' } }, splitArea: { areaStyle: { color: ['rgba(245, 240, 230, 0.3)', 'rgba(245, 240, 230, 0.5)'] } } },
        series: [{ type: 'radar', data: [{ value: techCounts.map(t => t.value), name: '技术统计', areaStyle: { color: 'rgba(139, 35, 35, 0.3)' }, lineStyle: { color: '#8B2323' }, itemStyle: { color: '#8B2323' } }] }]
      })
    }

    if (mileRes.success) milestones.value = mileRes.data
  } catch (error) { console.error('加载统计数据失败:', error) }
})
</script>

<style scoped>
.statistics-container { height: 100%; overflow-y: auto; background: linear-gradient(135deg, #F5F0E6 0%, #EDE5D5 100%); padding: 16px; }
.overview-section { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px; }
.overview-card { display: flex; align-items: center; gap: 12px; padding: 14px 16px; background: rgba(245, 240, 230, 0.95); border: 1px solid rgba(139, 35, 35, 0.12); border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.overview-card .card-icon { font-size: 28px; }
.overview-card .card-value { font-size: 22px; font-weight: 700; color: #8B2323; font-family: 'Noto Serif SC', serif; }
.overview-card .card-label { font-size: 12px; color: #7A7A7A; }
.stats-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }
.chart-card { padding: 16px; background: rgba(245, 240, 230, 0.95); border: 1px solid rgba(139, 35, 35, 0.12); border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.chart-card.wide { grid-column: span 2; }
.card-header, .section-header { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px solid rgba(201, 169, 98, 0.3); }
.header-seal { display: inline-flex; align-items: center; justify-content: center; width: 22px; height: 22px; background: #8B2323; color: #F5F0E6; font-size: 11px; font-weight: bold; border-radius: 2px; }
.card-header h3, .section-header h3 { margin: 0; font-size: 14px; color: #2A2A2A; font-family: 'Noto Serif SC', serif; }
.chart { height: 220px; }
.region-chart { height: 280px; }
.chart-legend { display: flex; justify-content: center; gap: 16px; margin-top: 8px; }
.legend-item { display: flex; align-items: center; gap: 4px; font-size: 11px; }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; }
.legend-name { color: #4A4A4A; }
.legend-value { color: #8B2323; font-weight: 600; }
.milestones { display: flex; flex-direction: column; gap: 10px; max-height: 280px; overflow-y: auto; }
.milestone { display: flex; gap: 12px; padding: 10px; background: rgba(139, 35, 35, 0.04); border-radius: 4px; border-left: 3px solid #8B2323; }
.milestone .year { flex-shrink: 0; width: 80px; font-size: 11px; color: #C9A962; font-weight: 600; }
.milestone .content strong { font-size: 12px; color: #2A2A2A; display: block; margin-bottom: 4px; }
.milestone .content p { margin: 0; font-size: 11px; color: #7A7A7A; line-height: 1.5; }
.insight-section { margin-top: 16px; padding: 16px; background: rgba(245, 240, 230, 0.95); border: 1px solid rgba(139, 35, 35, 0.12); border-radius: 6px; }
.insight-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-top: 12px; }
.insight-card { display: flex; gap: 12px; padding: 12px; background: linear-gradient(135deg, rgba(139, 35, 35, 0.05) 0%, rgba(201, 169, 98, 0.05) 100%); border-radius: 6px; border: 1px solid rgba(201, 169, 98, 0.2); }
.insight-icon { font-size: 24px; }
.insight-content strong { font-size: 13px; color: #2A2A2A; display: block; margin-bottom: 4px; font-family: 'Noto Serif SC', serif; }
.insight-content p { margin: 0; font-size: 11px; color: #7A7A7A; line-height: 1.6; }
@media (max-width: 900px) {
  .overview-section { grid-template-columns: repeat(2, 1fr); }
  .stats-grid { grid-template-columns: 1fr; }
  .chart-card.wide { grid-column: span 1; }
  .insight-grid { grid-template-columns: 1fr; }
}
</style>