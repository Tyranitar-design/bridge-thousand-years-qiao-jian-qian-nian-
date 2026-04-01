<template>
  <div class="dashboard-container">
    <!-- 水墨装饰背景 -->
    <div class="ink-decoration">
      <div class="ink-blob ink-blob-1"></div>
      <div class="ink-blob ink-blob-2"></div>
    </div>

    <!-- 顶部卷轴标题 -->
    <header class="dashboard-header">
      <div class="scroll-title">
        <div class="scroll-left"></div>
        <div class="scroll-content">
          <h1 class="main-title">桥 见 千 年</h1>
          <p class="sub-title">中国古代桥梁智慧可视化平台</p>
        </div>
        <div class="scroll-right"></div>
      </div>
      <div class="header-decoration">
        <span class="deco-text">连接古今 · 匠心传承</span>
      </div>
    </header>

    <!-- 核心数据卡片 -->
    <section class="stats-section">
      <div class="stats-cards">
        <div 
          class="stat-card" 
          v-for="(stat, index) in statsData" 
          :key="stat.label"
          :style="{ '--delay': index * 0.15 + 's' }"
        >
          <div class="card-corner corner-tl"></div>
          <div class="card-corner corner-tr"></div>
          <div class="card-corner corner-bl"></div>
          <div class="card-corner corner-br"></div>
          
          <div class="card-content">
            <div class="card-icon">
              <el-icon :size="24"><component :is="stat.icon" /></el-icon>
            </div>
            <div class="card-info">
              <div class="stat-value">
                <span class="number">{{ animatedNumbers[index] }}</span>
                <span class="unit">{{ stat.unit }}</span>
              </div>
              <div class="stat-label">{{ stat.label }}</div>
              <div class="stat-trend">{{ stat.trendText }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 左侧：桥梁分布可视化 -->
      <section class="map-section">
        <div class="section-card">
          <div class="card-header">
            <span class="header-seal">舆</span>
            <h3>桥梁地理分布</h3>
            <div class="header-line"></div>
          </div>
          <div class="map-container" ref="mapChart"></div>
          <div class="map-legend">
            <div class="legend-item" v-for="type in bridgeTypes" :key="type.name">
              <span class="legend-dot" :style="{ background: type.color }"></span>
              <span class="legend-label">{{ type.name }}</span>
              <span class="legend-count">{{ type.count }}座</span>
            </div>
          </div>
        </div>
      </section>

      <!-- 右侧：图表区 -->
      <section class="charts-section">
        <!-- 类型分布 -->
        <div class="chart-card">
          <div class="card-header">
            <span class="header-seal small">类</span>
            <h3>桥梁类型分布</h3>
          </div>
          <div class="chart-container" ref="typeChart"></div>
        </div>

        <!-- 朝代分布 -->
        <div class="chart-card">
          <div class="card-header">
            <span class="header-seal small">代</span>
            <h3>朝代分布统计</h3>
          </div>
          <div class="chart-container" ref="dynastyChart"></div>
        </div>

        <!-- 技术成就 -->
        <div class="achievement-card">
          <div class="card-header">
            <span class="header-seal small">匠</span>
            <h3>技术里程碑</h3>
          </div>
          <div class="achievement-list">
            <div 
              class="achievement-item" 
              v-for="(item, index) in achievements" 
              :key="index"
            >
              <div class="achievement-year">{{ item.year }}</div>
              <div class="achievement-content">
                <div class="achievement-title">{{ item.title }}</div>
                <div class="achievement-desc">{{ item.desc }}</div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- 底部：推荐桥梁 -->
    <section class="featured-section">
      <div class="section-header">
        <span class="header-seal">荐</span>
        <span class="section-title">代表性桥梁</span>
        <div class="section-line"></div>
      </div>
      <div class="featured-grid">
        <div 
          class="featured-card" 
          v-for="bridge in featuredBridges" 
          :key="bridge.id"
          @click="goToBridge(bridge.id)"
        >
          <div class="card-image" :style="getCardStyle(bridge)">
            <div class="image-overlay">
              <span class="view-btn">查看详情 →</span>
            </div>
            <div class="card-badge" v-if="bridge.heritage">遗</div>
          </div>
          <div class="card-body">
            <div class="card-type" :class="getTypeClass(bridge.type)">{{ bridge.type }}</div>
            <h4 class="card-name">{{ bridge.name }}</h4>
            <div class="card-meta">
              <span class="meta-item">{{ bridge.dynasty }}</span>
              <span class="meta-item">{{ bridge.location?.province }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import { bridgeAPI, statsAPI } from '@/api'

const router = useRouter()

// 统计数据
const statsData = ref([
  { label: '桥梁总数', value: 31, unit: '座', icon: 'LocationFilled', trendText: '覆盖16省市' },
  { label: '年代跨度', value: 2500, unit: '+年', icon: 'Clock', trendText: '北魏至清代' },
  { label: '桥梁类型', value: 4, unit: '种', icon: 'Grid', trendText: '拱梁索浮' },
  { label: '世界遗产', value: 3, unit: '处', icon: 'Trophy', trendText: '文化瑰宝' }
])

// 动画数字
const animatedNumbers = ref([0, 0, 0, 0])

// 桥梁类型
const bridgeTypes = ref([
  { name: '拱桥', color: '#8B2323', count: 21 },
  { name: '梁桥', color: '#1E3A5F', count: 8 },
  { name: '索桥', color: '#2E8B57', count: 2 }
])

// 技术成就
const achievements = ref([
  { year: '公元6世纪', title: '敞肩拱技术', desc: '赵州桥首创，世界桥梁史上的创举' },
  { year: '公元11世纪', title: '筏形基础', desc: '洛阳桥发明，世界首创生物工程' },
  { year: '公元12世纪', title: '启闭式桥梁', desc: '广济桥首创，比伦敦塔桥早400年' }
])

// 推荐桥梁
const featuredBridges = ref([])

// 图表引用
const mapChart = ref(null)
const typeChart = ref(null)
const dynastyChart = ref(null)

// 数字动画
const animateNumbers = () => {
  statsData.value.forEach((stat, index) => {
    let current = 0
    const target = stat.value
    const increment = target / 30
    const timer = setInterval(() => {
      current += increment
      if (current >= target) {
        current = target
        clearInterval(timer)
      }
      animatedNumbers.value[index] = Math.floor(current)
    }, 40)
  })
}

// 卡片样式
const getCardStyle = (bridge) => {
  const typeColors = {
    '拱桥': ['#8B2323', '#B83B3B'],
    '梁桥': ['#1E3A5F', '#2E5A8F'],
    '索桥': ['#2E8B57', '#3CB371']
  }
  const colors = typeColors[bridge.type] || typeColors['拱桥']
  return {
    background: `linear-gradient(135deg, ${colors[0]}22 0%, ${colors[1]}11 100%)`
  }
}

// 类型样式
const getTypeClass = (type) => {
  const classes = { '拱桥': 'type-arch', '梁桥': 'type-beam', '索桥': 'type-cable' }
  return classes[type] || ''
}

// 跳转详情
const goToBridge = (id) => {
  router.push(`/bridges/${id}`)
}

// 初始化桥梁分布图
const initMapChart = (bridges) => {
  const chart = echarts.init(mapChart.value)
  
  const provinceCoords = {
    '河北省': [114.5, 38.0], '北京市': [116.4, 39.9], '天津市': [117.2, 39.1],
    '山西省': [112.5, 37.9], '江苏省': [118.8, 32.1], '浙江省': [120.2, 30.3],
    '福建省': [119.3, 26.1], '广东省': [113.3, 23.1], '四川省': [104.1, 30.7],
    '云南省': [102.7, 25.0], '陕西省': [109.0, 34.3], '甘肃省': [103.8, 36.1]
  }
  
  const provinceData = {}
  bridges.forEach(bridge => {
    const province = bridge.location?.province
    if (province) {
      if (!provinceData[province]) {
        provinceData[province] = { count: 0, bridges: [] }
      }
      provinceData[province].count++
      provinceData[province].bridges.push(bridge.name)
    }
  })
  
  const scatterData = []
  Object.entries(provinceData).forEach(([province, data]) => {
    const coords = provinceCoords[province]
    if (coords) {
      scatterData.push({
        name: province,
        value: [...coords, data.count],
        count: data.count,
        bridges: data.bridges.join('、')
      })
    }
  })
  
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(42, 42, 42, 0.95)',
      borderColor: '#C9A962',
      borderWidth: 1,
      textStyle: { color: '#F5F0E6', fontFamily: 'Noto Serif SC' },
      formatter: function(params) {
        return `<div style="font-weight:bold;color:#C9A962;margin-bottom:6px">${params.name}</div>
                <div>桥梁：<strong style="color:#8B2323">${params.data.count}</strong> 座</div>
                <div style="font-size:11px;color:#7A7A7A;margin-top:4px">${params.data.bridges}</div>
                <div style="font-size:10px;color:#C9A962;margin-top:6px">点击查看详情 →</div>`
      }
    },
    geo: {
      map: 'china',
      roam: true,
      zoom: 1.2,
      center: [104, 36],
      scaleLimit: { min: 1, max: 5 },
      selectedMode: 'single',
      itemStyle: {
        areaColor: 'rgba(139, 35, 35, 0.08)',
        borderColor: 'rgba(201, 169, 98, 0.4)',
        borderWidth: 1
      },
      emphasis: {
        itemStyle: {
          areaColor: 'rgba(139, 35, 35, 0.25)',
          borderColor: '#C9A962'
        },
        label: { show: true, color: '#2A2A2A' }
      },
      select: {
        itemStyle: {
          areaColor: 'rgba(139, 35, 35, 0.3)',
          borderColor: '#8B2323'
        },
        label: { show: true, color: '#8B2323' }
      },
      label: { show: false }
    },
    series: [{
      type: 'effectScatter',
      coordinateSystem: 'geo',
      data: scatterData,
      symbolSize: function(val) {
        return Math.max(8, Math.min(20, val[2] * 4))
      },
      showEffectOn: 'render',
      rippleEffect: {
        brushType: 'stroke',
        scale: 3,
        period: 5
      },
      itemStyle: {
        color: '#8B2323',
        shadowBlur: 10,
        shadowColor: 'rgba(139, 35, 35, 0.4)'
      },
      zlevel: 1
    }]
  }
  
  chart.setOption(option)
  
  // 点击省份跳转到桥梁博览页并筛选
  chart.on('click', function(params) {
    if (params.componentType === 'series' || params.componentType === 'geo') {
      const province = params.name
      if (province && provinceData[province]) {
        // 跳转到桥梁博览页，带上省份参数
        router.push({
          path: '/bridges',
          query: { province: province }
        })
      }
    }
  })
  
  window.addEventListener('resize', () => chart.resize())
}

// 初始化类型图表
const initTypeChart = (typeData) => {
  const chart = echarts.init(typeChart.value)
  
  const colors = ['#8B2323', '#1E3A5F', '#2E8B57', '#C9A962']
  
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(42, 42, 42, 0.9)',
      borderColor: '#C9A962',
      textStyle: { color: '#F5F0E6' }
    },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: false,
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
        show: true,
        lineStyle: { color: 'rgba(139, 35, 35, 0.3)' }
      },
      data: Object.entries(typeData).map(([name, value], index) => ({
        name,
        value,
        itemStyle: { color: colors[index % colors.length] }
      }))
    }]
  })
  
  window.addEventListener('resize', () => chart.resize())
}

// 初始化朝代图表
const initDynastyChart = (dynastyData) => {
  const chart = echarts.init(dynastyChart.value)
  
  const dynasties = ['北魏', '隋代', '唐代', '宋代', '金代', '元代', '明代', '清代']
  const data = dynasties.map(d => dynastyData[d]?.count || 0)
  
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(42, 42, 42, 0.9)',
      borderColor: '#C9A962',
      textStyle: { color: '#F5F0E6' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: dynasties,
      axisLine: { lineStyle: { color: 'rgba(139, 35, 35, 0.3)' } },
      axisLabel: { 
        color: '#4A4A4A', 
        fontSize: 11, 
        interval: 0,
        fontFamily: 'Noto Serif SC'
      },
      axisTick: { show: false }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: { color: '#7A7A7A' },
      splitLine: { lineStyle: { color: 'rgba(139, 35, 35, 0.1)' } }
    },
    series: [{
      type: 'bar',
      data,
      barWidth: '50%',
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#8B2323' },
          { offset: 1, color: '#8B232355' }
        ]),
        borderRadius: [3, 3, 0, 0]
      }
    }]
  })
  
  window.addEventListener('resize', () => chart.resize())
}

// 注册中国地图
const registerChinaMap = async () => {
  try {
    const response = await fetch('/100000_full.json')
    if (!response.ok) throw new Error('本地文件加载失败')
    const geoJson = await response.json()
    echarts.registerMap('china', geoJson)
    return true
  } catch (error) {
    console.warn('加载地图 GeoJSON 失败:', error)
    return false
  }
}

// 加载数据
onMounted(async () => {
  animateNumbers()
  
  try {
    const [overviewRes, dynastyRes, bridgesRes] = await Promise.all([
      statsAPI.getOverview(),
      statsAPI.getByDynasty(),
      bridgeAPI.getList()
    ])
    
    if (overviewRes.success) {
      statsData.value[0].value = overviewRes.data.totalBridges
      statsData.value[3].value = overviewRes.data.heritageCount
      
      const typeDist = overviewRes.data.typeDistribution
      bridgeTypes.value = [
        { name: '拱桥', color: '#8B2323', count: typeDist['拱桥'] || 0 },
        { name: '梁桥', color: '#1E3A5F', count: typeDist['梁桥'] || 0 },
        { name: '索桥', color: '#2E8B57', count: typeDist['索桥'] || 0 }
      ]
    }
    
    if (bridgesRes.success) {
      featuredBridges.value = bridgesRes.data.slice(0, 4)
    }
    
    await nextTick()
    
    const mapLoaded = await registerChinaMap()
    
    if (bridgesRes.success && mapLoaded) {
      initMapChart(bridgesRes.data)
    }
    
    if (overviewRes.success) {
      initTypeChart(overviewRes.data.typeDistribution)
    }
    
    if (dynastyRes.success) {
      initDynastyChart(dynastyRes.data)
    }
    
  } catch (error) {
    console.error('加载数据失败:', error)
  }
})
</script>

<style scoped>
/* 主容器 */
.dashboard-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow: hidden;
  position: relative;
  background: linear-gradient(135deg, #F5F0E6 0%, #EDE5D5 50%, #E8E0D0 100%);
}

/* 水墨装饰 */
.ink-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.ink-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.03;
}

.ink-blob-1 {
  width: 500px;
  height: 500px;
  background: #1A1A1A;
  top: -150px;
  right: 5%;
}

.ink-blob-2 {
  width: 400px;
  height: 400px;
  background: #8B2323;
  bottom: 10%;
  left: -100px;
}

/* 顶部标题 */
.dashboard-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  position: relative;
  z-index: 10;
}

.scroll-title {
  display: flex;
  align-items: stretch;
  justify-content: center;
}

.scroll-left,
.scroll-right {
  width: 20px;
  background: linear-gradient(90deg, #8B7355, #C9A962);
  border-radius: 10px 0 0 10px;
}

.scroll-right {
  border-radius: 0 10px 10px 0;
}

.scroll-content {
  background: linear-gradient(180deg, #F5F0E6 0%, #EDE5D5 100%);
  border-top: 3px solid #C9A962;
  border-bottom: 3px solid #C9A962;
  padding: 15px 40px;
  text-align: center;
}

.main-title {
  font-size: 32px;
  font-weight: 600;
  color: #2A2A2A;
  margin: 0;
  letter-spacing: 12px;
  font-family: 'Noto Serif SC', 'Source Han Serif SC', serif;
}

.sub-title {
  font-size: 13px;
  color: #7A7A7A;
  margin: 6px 0 0;
  letter-spacing: 3px;
}

.header-decoration {
  margin-top: 12px;
}

.deco-text {
  font-size: 12px;
  color: #8B7355;
  letter-spacing: 8px;
  position: relative;
}

.deco-text::before,
.deco-text::after {
  content: '◆';
  color: #C9A962;
  margin: 0 15px;
  font-size: 8px;
}

/* 统计卡片区 */
.stats-section { position: relative; z-index: 10; }
.stats-cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }

.stat-card {
  position: relative;
  padding: 18px 20px;
  background: rgba(245, 240, 230, 0.9);
  border: 1px solid rgba(139, 35, 35, 0.15);
  border-left: 3px solid #8B2323;
  animation: fadeInUp 0.6s ease forwards;
  animation-delay: var(--delay);
  opacity: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}

.card-corner {
  position: absolute;
  width: 10px;
  height: 10px;
  border-color: #C9A962;
  border-style: solid;
  opacity: 0.5;
}
.corner-tl { top: 4px; left: 4px; border-width: 1px 0 0 1px; }
.corner-tr { top: 4px; right: 4px; border-width: 1px 1px 0 0; }
.corner-bl { bottom: 4px; left: 4px; border-width: 0 0 1px 1px; }
.corner-br { bottom: 4px; right: 4px; border-width: 0 1px 1px 0; }

.card-content { display: flex; align-items: center; gap: 14px; }

.card-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, rgba(139, 35, 35, 0.1), rgba(201, 169, 98, 0.1));
  border: 1px solid rgba(139, 35, 35, 0.2);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8B2323;
}

.card-info { flex: 1; }
.stat-value { display: flex; align-items: baseline; gap: 4px; }
.stat-value .number { 
  font-size: 28px; 
  font-weight: 600; 
  color: #8B2323; 
  font-family: 'Noto Serif SC', serif;
}
.stat-value .unit { font-size: 14px; color: #4A4A4A; }
.stat-label { font-size: 13px; color: #4A4A4A; margin-top: 2px; letter-spacing: 1px; }
.stat-trend { font-size: 11px; color: #7A7A7A; margin-top: 4px; }

/* 主内容区 */
.main-content {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 16px;
  min-height: 0;
  position: relative;
  z-index: 10;
}

.section-card {
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.12);
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-bottom: 1px solid rgba(201, 169, 98, 0.3);
  background: linear-gradient(90deg, rgba(139, 35, 35, 0.04), transparent);
}

.header-seal {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  background: #8B2323;
  color: #F5F0E6;
  font-size: 12px;
  font-weight: bold;
  border-radius: 3px;
  letter-spacing: 0;
}

.header-seal.small {
  width: 22px;
  height: 22px;
  font-size: 11px;
}

.card-header h3 { 
  font-size: 14px; 
  color: #2A2A2A; 
  margin: 0;
  font-family: 'Noto Serif SC', serif;
  letter-spacing: 1px;
}
.header-line { flex: 1; height: 1px; background: linear-gradient(90deg, rgba(201, 169, 98, 0.4), transparent); }

/* 地图区域 */
.map-section { display: flex; flex-direction: column; }
.map-container { flex: 1; min-height: 280px; }

.map-legend {
  display: flex;
  gap: 20px;
  padding: 10px 16px;
  background: rgba(139, 35, 35, 0.03);
  border-top: 1px solid rgba(201, 169, 98, 0.2);
}

.legend-item { display: flex; align-items: center; gap: 6px; }
.legend-dot { width: 8px; height: 8px; border-radius: 50%; }
.legend-label { font-size: 12px; color: #4A4A4A; }
.legend-count { font-size: 12px; color: #8B2323; font-weight: 500; }

/* 图表区 */
.charts-section { display: flex; flex-direction: column; gap: 16px; }

.chart-card {
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.12);
  border-radius: 6px;
  flex: 1;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.chart-container { flex: 1; min-height: 130px; }

/* 成就卡片 */
.achievement-card {
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.12);
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.achievement-list {
  flex: 1;
  padding: 8px 12px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.achievement-item {
  display: flex;
  gap: 10px;
  padding: 10px 12px;
  background: linear-gradient(90deg, rgba(139, 35, 35, 0.04), transparent);
  border-radius: 4px;
  border-left: 2px solid #8B2323;
}

.achievement-year { 
  font-size: 10px; 
  color: #C9A962; 
  font-weight: 600;
  white-space: nowrap;
  padding-top: 2px;
}
.achievement-title { font-size: 12px; color: #2A2A2A; font-weight: 500; }
.achievement-desc { font-size: 10px; color: #7A7A7A; margin-top: 3px; line-height: 1.5; }

/* 推荐桥梁区 */
.featured-section {
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.12);
  border-radius: 6px;
  padding: 14px 16px;
  position: relative;
  z-index: 10;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.section-header { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.section-title { 
  font-size: 14px; 
  color: #2A2A2A; 
  font-family: 'Noto Serif SC', serif;
  letter-spacing: 1px;
}
.section-line { flex: 1; height: 1px; background: linear-gradient(90deg, rgba(201, 169, 98, 0.4), transparent); }

.featured-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }

.featured-card {
  background: rgba(232, 224, 208, 0.6);
  border: 1px solid rgba(139, 35, 35, 0.1);
  border-radius: 6px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.featured-card:hover {
  transform: translateY(-3px);
  border-color: #C9A962;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.card-image { 
  height: 90px; 
  position: relative; 
  display: flex; 
  align-items: center; 
  justify-content: center;
  font-size: 32px;
}

.card-image::before { content: '🏯'; }

.image-overlay {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(26, 26, 26, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.featured-card:hover .image-overlay { opacity: 1; }

.view-btn {
  padding: 6px 14px;
  background: #C9A962;
  color: #1A1A1A;
  border-radius: 14px;
  font-size: 11px;
  font-weight: 500;
}

.card-badge {
  position: absolute;
  top: 6px; right: 6px;
  width: 22px; height: 22px;
  background: #8B2323;
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #F5F0E6;
  font-size: 11px;
  font-weight: bold;
}

.card-body { padding: 10px; }
.card-type { 
  display: inline-block; 
  padding: 2px 8px; 
  border-radius: 2px; 
  font-size: 10px;
  margin-bottom: 6px;
}
.card-type.type-arch { background: rgba(139, 35, 35, 0.15); color: #8B2323; }
.card-type.type-beam { background: rgba(30, 58, 95, 0.15); color: #1E3A5F; }
.card-type.type-cable { background: rgba(46, 139, 87, 0.15); color: #2E8B57; }
.card-name { font-size: 14px; color: #2A2A2A; margin: 0 0 5px; font-family: 'Noto Serif SC', serif; }
.card-meta { display: flex; gap: 10px; font-size: 11px; color: #7A7A7A; }
.meta-item::before { content: '·'; margin-right: 4px; }

/* 响应式 */
@media (max-width: 1400px) {
  .stats-cards { grid-template-columns: repeat(2, 1fr); }
  .featured-grid { grid-template-columns: repeat(2, 1fr); }
  .main-content { grid-template-columns: 1fr; }
  .charts-section { flex-direction: row; }
  .chart-card, .achievement-card { flex: 1; }
}
</style>
