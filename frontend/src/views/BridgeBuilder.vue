<template>
  <div class="builder-container">
    <!-- 顶部标题 -->
    <header class="builder-header">
      <div class="scroll-title">
        <div class="scroll-left"></div>
        <div class="scroll-content">
          <h1 class="main-title">古 桥 建 造 坊</h1>
          <p class="sub-title">体验古代工匠智慧，亲手建造千年古桥</p>
        </div>
        <div class="scroll-right"></div>
      </div>
    </header>

    <main class="builder-main">
      <!-- 左侧：组件库 -->
      <section class="components-panel">
        <div class="panel-header">
          <span class="header-seal">材</span>
          <h3>建筑材料</h3>
        </div>
        
        <div class="component-category">
          <h4>🏛️ 拱桥组件</h4>
          <div class="component-grid">
            <div class="component-item" v-for="comp in archComponents" :key="comp.id"
              draggable="true" @dragstart="onDragStart($event, comp)">
              <span class="component-icon">{{ comp.icon }}</span>
              <span class="component-name">{{ comp.name }}</span>
            </div>
          </div>
        </div>
        
        <div class="component-category">
          <h4>🌉 梁桥组件</h4>
          <div class="component-grid">
            <div class="component-item" v-for="comp in beamComponents" :key="comp.id"
              draggable="true" @dragstart="onDragStart($event, comp)">
              <span class="component-icon">{{ comp.icon }}</span>
              <span class="component-name">{{ comp.name }}</span>
            </div>
          </div>
        </div>
        
        <div class="component-category">
          <h4>⛓️ 索桥组件</h4>
          <div class="component-grid">
            <div class="component-item" v-for="comp in cableComponents" :key="comp.id"
              draggable="true" @dragstart="onDragStart($event, comp)">
              <span class="component-icon">{{ comp.icon }}</span>
              <span class="component-name">{{ comp.name }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- 中间：建造区域 -->
      <section class="build-area">
        <div class="area-header">
          <span class="header-seal">建</span>
          <h3>建造区域</h3>
          <div class="bridge-type-selector">
            <span class="type-btn" :class="{ active: selectedBridgeType === 'arch' }" 
              @click="selectBridgeType('arch')">拱桥</span>
            <span class="type-btn" :class="{ active: selectedBridgeType === 'beam' }" 
              @click="selectBridgeType('beam')">梁桥</span>
            <span class="type-btn" :class="{ active: selectedBridgeType === 'cable' }" 
              @click="selectBridgeType('cable')">索桥</span>
          </div>
        </div>
        
        <div class="build-canvas" @dragover.prevent @drop="onDrop" ref="buildCanvas">
          <div class="bridge-base">
            <div class="pier"><div class="pier-body"></div><span>左桥墩</span></div>
            <div class="water-flow">〜 河水流向 → 〜</div>
            <div class="pier"><div class="pier-body"></div><span>右桥墩</span></div>
          </div>
          
          <div class="placed-component" v-for="(comp, index) in placedComponents" :key="index"
            :style="{ left: comp.x + 'px', top: comp.y + 'px' }">
            <span class="comp-icon">{{ comp.icon }}</span>
            <span class="comp-name">{{ comp.name }}</span>
            <button class="remove-btn" @click="removeComponent(index)">×</button>
          </div>
          
          <div class="build-guide" v-if="placedComponents.length === 0">
            <p>👆 从左侧拖拽组件到此处开始建造</p>
          </div>
        </div>
        
        <div class="action-buttons">
          <el-button @click="clearBuild">🗑️ 清空</el-button>
          <el-button type="primary" @click="checkBuild">✅ 检查</el-button>
          <el-button type="success" @click="showCompleteDialog = true">🏛️ 真桥</el-button>
        </div>
      </section>

      <!-- 右侧：信息面板 -->
      <section class="info-panel">
        <div class="info-card">
          <div class="panel-header">
            <span class="header-seal">绩</span>
            <h3>建造成绩</h3>
          </div>
          <div class="score-item"><span>组件数量</span><strong>{{ placedComponents.length }}</strong></div>
          <div class="score-item"><span>结构评分</span><strong :class="scoreClass">{{ structureScore }}分</strong></div>
          <div class="score-item total"><span>总评</span><strong>{{ totalScore }}</strong></div>
        </div>
        
        <div class="info-card">
          <div class="panel-header">
            <span class="header-seal">示</span>
            <h3>建造提示</h3>
          </div>
          <p class="tip-text">{{ currentTip }}</p>
        </div>
        
        <div class="info-card">
          <div class="panel-header">
            <span class="header-seal">知</span>
            <h3>古桥知识</h3>
          </div>
          <h4 class="knowledge-title">{{ currentKnowledge.title }}</h4>
          <p class="knowledge-text">{{ currentKnowledge.content }}</p>
        </div>
      </section>
    </main>

    <!-- 完成弹窗 -->
    <el-dialog v-model="showCompleteDialog" title="🎉 建造完成！" width="400px" center>
      <div class="complete-content">
        <div class="complete-icon">{{ structureScore >= 80 ? '🏆' : '👏' }}</div>
        <h3>你的{{ bridgeTypeNames[selectedBridgeType] }}建造完成！</h3>
        <p>结构评分：<strong :class="scoreClass">{{ structureScore }}</strong> 分</p>
        <p>{{ completeComment }}</p>
        <div class="real-bridge-info">
          <h4>📌 对比真桥：{{ realBridgeInfo.name }}</h4>
          <p>{{ realBridgeInfo.dynasty }} · {{ realBridgeInfo.technology }}</p>
        </div>
      </div>
      <template #footer>
        <el-button @click="showCompleteDialog = false">继续建造</el-button>
        <el-button type="primary" @click="goToRealBridge">查看真桥详情</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const buildCanvas = ref(null)

const selectedBridgeType = ref('arch')
const bridgeTypeNames = { arch: '拱桥', beam: '梁桥', cable: '索桥' }
const placedComponents = ref([])
const showCompleteDialog = ref(false)

const archComponents = [
  { id: 'main-arch', name: '主拱', icon: '🌉', type: 'arch' },
  { id: 'side-arch', name: '敞肩小拱', icon: '🌀', type: 'arch' },
  { id: 'arch-stone', name: '拱石', icon: '🧱', type: 'arch' },
  { id: 'pier', name: '桥墩', icon: '🏛️', type: 'arch' },
  { id: 'railing', name: '栏杆', icon: '🚧', type: 'arch' },
  { id: 'deck', name: '桥面', icon: '🛤️', type: 'arch' }
]

const beamComponents = [
  { id: 'beam', name: '梁木', icon: '🪵', type: 'beam' },
  { id: 'pier', name: '桥墩', icon: '🏛️', type: 'beam' },
  { id: 'deck', name: '桥面', icon: '🛤️', type: 'beam' },
  { id: 'railing', name: '栏杆', icon: '🚧', type: 'beam' },
  { id: 'column', name: '立柱', icon: '🧱', type: 'beam' }
]

const cableComponents = [
  { id: 'cable', name: '铁索', icon: '⛓️', type: 'cable' },
  { id: 'anchor', name: '锚固', icon: '⚓', type: 'cable' },
  { id: 'deck', name: '桥面', icon: '🛤️', type: 'cable' },
  { id: 'railing', name: '护栏', icon: '🚧', type: 'cable' },
  { id: 'tower', name: '桥塔', icon: '🗼', type: 'cable' }
]

const onDragStart = (event, component) => {
  event.dataTransfer.setData('component', JSON.stringify(component))
}

const onDrop = (event) => {
  const data = event.dataTransfer.getData('component')
  if (!data) return
  const component = JSON.parse(data)
  const rect = buildCanvas.value.getBoundingClientRect()
  placedComponents.value.push({ 
    ...component, 
    x: event.clientX - rect.left - 40, 
    y: event.clientY - rect.top - 30 
  })
  ElMessage.success(`已放置：${component.name}`)
}

const removeComponent = (index) => placedComponents.value.splice(index, 1)

const selectBridgeType = (type) => {
  selectedBridgeType.value = type
  placedComponents.value = []
  ElMessage.info(`已选择建造${bridgeTypeNames[type]}`)
}

const clearBuild = () => {
  placedComponents.value = []
  ElMessage.info('已清空')
}

const structureScore = computed(() => {
  if (placedComponents.value.length === 0) return 0
  let score = 0
  const placedIds = placedComponents.value.map(c => c.id)
  const required = { arch: ['main-arch', 'pier'], beam: ['beam', 'pier'], cable: ['cable', 'anchor'] }
  required[selectedBridgeType.value]?.forEach(id => { if (placedIds.includes(id)) score += 30 })
  score += Math.min(20, placedComponents.value.length * 4)
  const matchCount = placedComponents.value.filter(c => c.type === selectedBridgeType.value).length
  score += Math.min(20, matchCount * 5)
  return Math.min(100, score)
})

const totalScore = computed(() => {
  if (structureScore.value >= 80) return '优秀 ⭐⭐⭐'
  if (structureScore.value >= 60) return '良好 ⭐⭐'
  if (structureScore.value >= 40) return '合格 ⭐'
  return '需要改进'
})

const scoreClass = computed(() => structureScore.value >= 80 ? 'excellent' : structureScore.value >= 60 ? 'good' : structureScore.value >= 40 ? 'pass' : 'poor')

const currentTip = computed(() => ({
  arch: '拱桥关键：先放置主拱，再添加桥墩支撑。敞肩小拱是赵州桥的特色创新！',
  beam: '梁桥关键：梁木横跨桥墩，桥面铺设其上。洛阳桥首创筏形基础！',
  cable: '索桥关键：铁索锚固于两岸，桥面悬挂索上。泸定桥用13根铁链！'
}[selectedBridgeType.value]))

const currentKnowledge = computed(() => ({
  arch: { title: '赵州桥的敞肩拱', content: '李春首创敞肩拱技术，大拱两肩各设两个小拱，减轻自重约700吨。比欧洲早1200多年！' },
  beam: { title: '洛阳桥的筏形基础', content: '蔡襄首创筏形基础和种蛎固基法，解决了跨海建桥难题。' },
  cable: { title: '泸定桥的铁索', content: '泸定桥用13根铁链组成，每根重约1.5吨，体现清代冶金技术高超。' }
}[selectedBridgeType.value]))

const completeComment = computed(() => {
  if (structureScore.value >= 80) return '太棒了！你已经掌握了古桥建造的精髓！'
  if (structureScore.value >= 60) return '不错！继续努力！'
  if (structureScore.value >= 40) return '还可以，但结构还有改进空间。'
  return '继续尝试，添加更多必要组件吧！'
})

const realBridgeInfo = computed(() => ({
  arch: { id: 'zhaozhou-bridge', name: '赵州桥', dynasty: '隋代', technology: '敞肩拱技术' },
  beam: { id: 'luoyang-bridge', name: '洛阳桥', dynasty: '宋代', technology: '筏形基础' },
  cable: { id: 'luding-bridge', name: '泸定桥', dynasty: '清代', technology: '铁索悬吊' }
}[selectedBridgeType.value]))

const checkBuild = () => {
  if (placedComponents.value.length === 0) {
    ElMessage.warning('请先放置一些建筑组件！')
    return
  }
  showCompleteDialog.value = true
}

const goToRealBridge = () => {
  router.push(`/bridges/${realBridgeInfo.value.id}`)
}
</script>

<style scoped>
.builder-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: linear-gradient(135deg, #F5F0E6 0%, #EDE5D5 100%);
}

.builder-header { display: flex; justify-content: center; padding: 10px; }
.scroll-title { display: flex; align-items: stretch; }
.scroll-left, .scroll-right { width: 14px; background: linear-gradient(90deg, #8B7355, #C9A962); border-radius: 7px 0 0 7px; }
.scroll-right { border-radius: 0 7px 7px 0; }
.scroll-content { background: #F5F0E6; border-top: 2px solid #C9A962; border-bottom: 2px solid #C9A962; padding: 8px 28px; text-align: center; }
.main-title { font-size: 22px; font-weight: 600; color: #2A2A2A; margin: 0; letter-spacing: 8px; font-family: 'Noto Serif SC', serif; }
.sub-title { font-size: 11px; color: #7A7A7A; margin: 4px 0 0; }

.builder-main { flex: 1; display: grid; grid-template-columns: 200px 1fr 240px; gap: 12px; min-height: 0; }

.panel-header { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; padding-bottom: 8px; border-bottom: 1px solid rgba(201, 169, 98, 0.3); }
.header-seal { width: 22px; height: 22px; background: #8B2323; color: #F5F0E6; font-size: 11px; font-weight: bold; border-radius: 3px; display: flex; align-items: center; justify-content: center; }
.panel-header h3 { font-size: 13px; color: #2A2A2A; margin: 0; font-family: 'Noto Serif SC', serif; }

/* 左侧组件库 */
.components-panel { background: rgba(245, 240, 230, 0.95); border: 1px solid rgba(139, 35, 35, 0.12); border-radius: 6px; padding: 12px; overflow-y: auto; }
.component-category { margin-bottom: 12px; }
.component-category h4 { font-size: 12px; color: #8B2323; margin: 0 0 8px; padding-bottom: 6px; border-bottom: 1px dashed rgba(139, 35, 35, 0.2); }
.component-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; }
.component-item { padding: 8px 6px; background: rgba(232, 224, 208, 0.6); border: 1px solid rgba(139, 35, 35, 0.1); border-radius: 6px; text-align: center; cursor: grab; transition: all 0.2s; }
.component-item:hover { background: rgba(139, 35, 35, 0.08); border-color: #C9A962; transform: scale(1.05); }
.component-icon { font-size: 22px; display: block; }
.component-name { font-size: 10px; color: #4A4A4A; }

/* 中间建造区域 */
.build-area { display: flex; flex-direction: column; background: rgba(245, 240, 230, 0.95); border: 1px solid rgba(139, 35, 35, 0.12); border-radius: 6px; overflow: hidden; }
.area-header { display: flex; align-items: center; gap: 10px; padding: 10px 14px; border-bottom: 1px solid rgba(201, 169, 98, 0.3); background: linear-gradient(90deg, rgba(139, 35, 35, 0.04), transparent); }
.bridge-type-selector { display: flex; gap: 4px; margin-left: auto; }
.type-btn { padding: 4px 12px; font-size: 11px; border-radius: 12px; cursor: pointer; background: rgba(232, 224, 208, 0.6); color: #4A4A4A; transition: all 0.2s; }
.type-btn.active { background: #8B2323; color: #F5F0E6; }

.build-canvas { flex: 1; position: relative; background: linear-gradient(180deg, rgba(201, 169, 98, 0.05) 0%, rgba(139, 35, 35, 0.02) 100%); min-height: 280px; }

.bridge-base { position: absolute; bottom: 20px; left: 10%; right: 10%; display: flex; justify-content: space-between; align-items: flex-end; }
.pier { text-align: center; }
.pier-body { width: 36px; height: 50px; background: linear-gradient(180deg, #8B7355, #6B5344); border-radius: 4px 4px 0 0; border: 2px solid #4A3728; }
.pier span { font-size: 10px; color: #7A7A7A; display: block; margin-top: 4px; }
.water-flow { flex: 1; text-align: center; padding-bottom: 20px; color: #1E6490; font-size: 12px; opacity: 0.6; }

.placed-component { position: absolute; padding: 8px 12px; background: rgba(139, 35, 35, 0.1); border: 2px solid #8B2323; border-radius: 8px; cursor: move; display: flex; align-items: center; gap: 6px; }
.comp-icon { font-size: 20px; }
.comp-name { font-size: 11px; color: #2A2A2A; }
.remove-btn { width: 18px; height: 18px; border-radius: 50%; background: #c0392b; color: white; border: none; cursor: pointer; font-size: 12px; line-height: 1; }

.build-guide { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; color: #7A7A7A; }
.build-guide p { margin: 8px 0; font-size: 14px; }

.action-buttons { display: flex; gap: 8px; padding: 10px; border-top: 1px solid rgba(201, 169, 98, 0.3); justify-content: center; }

/* 右侧信息面板 */
.info-panel { display: flex; flex-direction: column; gap: 10px; }
.info-card { background: rgba(245, 240, 230, 0.95); border: 1px solid rgba(139, 35, 35, 0.12); border-radius: 6px; padding: 12px; }
.score-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px dashed rgba(201, 169, 98, 0.2); }
.score-item.total { border-bottom: none; background: rgba(139, 35, 35, 0.05); margin-top: 4px; padding: 10px; border-radius: 4px; }
.score-item strong { font-size: 18px; color: #8B2323; }
.score-item strong.excellent { color: #27ae60; }
.score-item strong.good { color: #2980b9; }
.score-item strong.pass { color: #f39c12; }
.score-item strong.poor { color: #7A7A7A; }

.tip-text { font-size: 12px; color: #4A4A4A; line-height: 1.6; margin: 0; }
.knowledge-title { font-size: 13px; color: #8B2323; margin: 0 0 6px; }
.knowledge-text { font-size: 11px; color: #4A4A4A; line-height: 1.6; margin: 0; }

/* 弹窗 */
.complete-content { text-align: center; }
.complete-icon { font-size: 48px; margin-bottom: 12px; }
.complete-content h3 { font-size: 18px; color: #2A2A2A; margin: 0 0 12px; }
.complete-score { font-size: 14px; color: #4A4A4A; }
.complete-comment { font-size: 13px; color: #7A7A7A; margin: 12px 0; }
.real-bridge-info { background: rgba(139, 35, 35, 0.05); padding: 12px; border-radius: 6px; margin-top: 12px; }
.real-bridge-info h4 { font-size: 13px; color: #8B2323; margin: 0 0 6px; }
.real-bridge-info p { font-size: 12px; color: #4A4A4A; margin: 0; }

@media (max-width: 1000px) {
  .builder-main { grid-template-columns: 1fr; }
  .components-panel, .info-panel { display: none; }
}

@media (max-width: 768px) {
  .builder-container {
    gap: 10px;
  }
  
  .builder-header {
    padding: 8px;
  }
  
  .scroll-content {
    padding: 6px 20px;
  }
  
  .main-title {
    font-size: 18px;
    letter-spacing: 4px;
  }
  
  .sub-title {
    font-size: 10px;
  }
  
  .builder-main {
    gap: 10px;
  }
  
  /* 隐藏侧边栏，移动端只显示建造区域 */
  .components-panel, .info-panel {
    display: none;
  }
  
  .build-area {
    min-height: 400px;
  }
  
  .area-header {
    padding: 8px 12px;
    gap: 8px;
    flex-wrap: wrap;
  }
  
  .area-header h3 {
    font-size: 13px;
  }
  
  .bridge-type-selector {
    width: 100%;
    justify-content: center;
    margin-left: 0;
    margin-top: 6px;
  }
  
  .type-btn {
    padding: 5px 14px;
    font-size: 12px;
  }
  
  .build-canvas {
    min-height: 260px;
  }
  
  .bridge-base {
    left: 5%;
    right: 5%;
  }
  
  .pier-body {
    width: 30px;
    height: 40px;
  }
  
  .pier span {
    font-size: 9px;
  }
  
  .water-flow {
    font-size: 11px;
    padding-bottom: 16px;
  }
  
  .placed-component {
    padding: 6px 10px;
    }
  
  .comp-icon {
    font-size: 18px;
  }
  
  .comp-name {
    font-size: 10px;
  }
  
  .remove-btn {
    width: 16px;
    height: 16px;
    font-size: 11px;
  }
  
  .build-guide p {
    font-size: 12px;
    padding: 0 20px;
  }
  
  .action-buttons {
    padding: 8px;
    gap: 6px;
    flex-wrap: wrap;
  }
  
  .action-buttons .el-button {
    flex: 1;
    min-width: 80px;
    font-size: 12px;
    padding: 8px 12px;
  }
  
  /* 弹窗适配 */
  :deep(.el-dialog) {
    width: 90% !important;
    max-width: 360px;
  }
  
  .complete-icon {
    font-size: 40px;
  }
  
  .complete-content h3 {
    font-size: 16px;
  }
  
  .complete-content p {
    font-size: 13px;
  }
  
  .real-bridge-info {
    padding: 10px;
  }
  
  .real-bridge-info h4 {
    font-size: 12px;
  }
  
  .real-bridge-info p {
    font-size: 11px;
  }
}
</style>