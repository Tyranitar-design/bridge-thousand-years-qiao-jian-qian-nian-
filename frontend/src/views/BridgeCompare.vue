<template>
  <div class="compare-container">
    <header class="compare-header">
      <div class="scroll-title">
        <div class="scroll-left"></div>
        <div class="scroll-content">
          <h1 class="main-title">桥 梁 对 比</h1>
          <p class="sub-title">选择2-3座桥梁，对比各项数据特征</p>
        </div>
        <div class="scroll-right"></div>
      </div>
    </header>

    <section class="select-section">
      <div class="section-header">
        <span class="header-seal">选</span>
        <h3>选择桥梁</h3>
        <span class="select-hint">已选 {{ selectedBridges.length }}/3 座</span>
      </div>
      
      <div class="bridge-selector">
        <el-select v-model="selectedIds" multiple :multiple-limit="3" placeholder="请选择2-3座桥梁进行对比" 
          class="bridge-select" @change="handleSelectChange">
          <el-option v-for="bridge in bridges" :key="bridge.id" :label="bridge.name" :value="bridge.id">
            <span class="option-name">{{ bridge.name }}</span>
            <span class="option-info">{{ bridge.type }} · {{ bridge.dynasty }}</span>
          </el-option>
        </el-select>
        
        <el-button type="primary" @click="startCompare" :disabled="selectedIds.length < 2" class="compare-btn">
          🔍 开始对比
        </el-button>
      </div>
    </section>

    <section class="compare-result" v-if="selectedBridges.length >= 2">
      <div class="section-header">
        <span class="header-seal">比</span>
        <h3>对比结果</h3>
      </div>

      <!-- 基本信息 -->
      <div class="compare-card">
        <div class="card-header"><span class="card-seal">概</span><h4>基本信息</h4></div>
        <table class="compare-table">
          <tr class="header-row">
            <td class="label-cell">项目</td>
            <td v-for="b in selectedBridges" :key="b.id"><span>{{ b.name }}</span><span class="type-tag">{{ b.type }}</span></td>
          </tr>
          <tr><td class="label-cell">朝代</td><td v-for="b in selectedBridges">{{ b.dynasty }}</td></tr>
          <tr><td class="label-cell">始建年份</td><td v-for="b in selectedBridges">{{ b.buildYear }}</td></tr>
          <tr><td class="label-cell">所在地</td><td v-for="b in selectedBridges">{{ b.location?.province }}</td></tr>
          <tr v-if="selectedBridges.some(b => b.heritage)">
            <td class="label-cell">世界遗产</td>
            <td v-for="b in selectedBridges">{{ b.heritage || '-' }}</td>
          </tr>
        </table>
      </div>

      <!-- 尺寸对比 -->
      <div class="compare-card">
        <div class="card-header"><span class="card-seal">尺</span><h4>尺寸对比</h4></div>
        <div class="dimension-bar">
          <div class="bar-item">
            <strong>长度（米）</strong>
            <div class="bar-group" v-for="(b, i) in selectedBridges" :key="i">
              <span>{{ b.name }}:</span>
              <div class="bar-fill" :style="{ width: (b.dimensions?.length / maxLength) * 100 + '%' }"></div>
              <span>{{ b.dimensions?.length || '-' }}</span>
            </div>
          </div>
          <div class="bar-item">
            <strong>宽度（米）</strong>
            <div class="bar-group" v-for="(b, i) in selectedBridges" :key="i">
              <span>{{ b.name }}:</span>
              <div class="bar-fill" :style="{ width: (b.dimensions?.width / maxWidth) * 100 + '%' }"></div>
              <span>{{ b.dimensions?.width || '-' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 技术特色 -->
      <div class="compare-card">
        <div class="card-header"><span class="card-seal">技</span><h4>技术创新</h4></div>
        <div class="tech-grid">
          <div class="tech-item" v-for="b in selectedBridges" :key="b.id">
            <h5>{{ b.name }}</h5>
            <p v-if="b.technology"><strong>创新：</strong>{{ b.technology.innovation }}</p>
            <p v-if="b.technology"><strong>意义：</strong>{{ b.technology.significance }}</p>
          </div>
        </div>
      </div>
    </section>

    <div class="empty-state" v-else>
      <p>请选择 2-3 座桥梁进行对比</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { bridgeAPI } from '@/api'
import { ElMessage } from 'element-plus'

const bridges = ref([])
const selectedIds = ref([])
const selectedBridges = ref([])

const maxLength = computed(() => Math.max(...selectedBridges.value.map(b => b.dimensions?.length || 0)) || 1)
const maxWidth = computed(() => Math.max(...selectedBridges.value.map(b => b.dimensions?.width || 0)) || 1)

const handleSelectChange = (ids) => {
  if (ids.length > 3) {
    ElMessage.warning('最多选择 3 座桥梁')
  }
}

const startCompare = () => {
  selectedBridges.value = bridges.value.filter(b => selectedIds.value.includes(b.id))
  ElMessage.success(`正在对比 ${selectedBridges.value.length} 座桥梁`)
}

onMounted(async () => {
  const res = await bridgeAPI.getList()
  if (res.success) {
    bridges.value = res.data
  }
})
</script>

<style scoped>
.compare-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: linear-gradient(135deg, #F5F0E6 0%, #EDE5D5 100%);
  padding: 20px;
}

.compare-header { text-align: center; }
.scroll-title { display: inline-flex; align-items: stretch; }
.scroll-left, .scroll-right { width: 14px; background: linear-gradient(90deg, #8B7355, #C9A962); border-radius: 7px 0 0 7px; }
.scroll-right { border-radius: 0 7px 7px 0; }
.scroll-content { background: #F5F0E6; border-top: 2px solid #C9A962; border-bottom: 2px solid #C9A962; padding: 10px 30px; }
.main-title { font-size: 22px; color: #2A2A2A; margin: 0; letter-spacing: 8px; font-family: 'Noto Serif SC', serif; }
.sub-title { font-size: 12px; color: #7A7A7A; margin: 4px 0 0; }

.select-section { background: rgba(245, 240, 230, 0.95); padding: 16px; border-radius: 6px; }
.section-header { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
.header-seal { width: 22px; height: 22px; background: #8B2323; color: #F5F0E6; font-size: 11px; font-weight: bold; border-radius: 3px; }
.section-header h3 { font-size: 14px; color: #2A2A2A; margin: 0; }
.select-hint { margin-left: auto; font-size: 12px; color: #8B2323; }

.bridge-selector { display: flex; gap: 12px; }
.bridge-select { flex: 1; }
.compare-btn { padding: 8px 24px; }

.compare-result { display: flex; flex-direction: column; gap: 12px; }
.compare-card { background: rgba(245, 240, 230, 0.95); padding: 16px; border-radius: 6px; border: 1px solid rgba(139, 35, 35, 0.12); }
.card-header { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid rgba(201, 169, 98, 0.3); }
.card-seal { width: 20px; height: 20px; background: #8B2323; color: #F5F0E6; font-size: 10px; font-weight: bold; border-radius: 2px; display: flex; align-items: center; justify-content: center; }
.card-header h4 { font-size: 14px; color: #2A2A2A; margin: 0; }

.compare-table { width: 100%; border-collapse: collapse; }
.compare-table td { padding: 8px; border-bottom: 1px dashed rgba(201, 169, 98, 0.2); }
.label-cell { font-weight: 600; color: #4A4A4A; min-width: 80px; }
.type-tag { font-size: 10px; padding: 2px 6px; border-radius: 2px; background: rgba(139, 35, 35, 0.1); color: #8B2323; margin-left: 4px; }

.dimension-bar { display: flex; flex-direction: column; gap: 12px; }
.bar-item strong { display: block; font-size: 13px; color: #8B2323; margin-bottom: 6px; }
.bar-group { display: flex; align-items: center; gap: 8px; font-size: 12px; margin-bottom: 6px; }
.bar-fill { height: 8px; background: linear-gradient(90deg, #C9A962, #8B2323); border-radius: 4px; min-width: 20px; }

.tech-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; }
.tech-item { padding: 12px; background: rgba(139, 35, 35, 0.04); border-radius: 6px; }
.tech-item h5 { margin: 0 0 8px; color: #8B2323; font-size: 14px; }
.tech-item p { font-size: 12px; color: #4A4A4A; margin: 4px 0; line-height: 1.6; }
.tech-item strong { color: #8B2323; }

.empty-state { flex: 1; display: flex; align-items: center; justify-content: center; flex-direction: column; color: #7A7A7A; gap: 8px; }
.empty-icon { font-size: 48px; opacity: 0.5; }

@media (max-width: 768px) {
  .compare-container {
    padding: 12px;
    gap: 12px;
  }
  
  .scroll-content {
    padding: 8px 20px;
  }
  
  .main-title {
    font-size: 18px;
    letter-spacing: 4px;
  }
  
  .sub-title {
    font-size: 11px;
  }
  
  .select-section {
    padding: 12px;
  }
  
  .section-header {
    flex-wrap: wrap;
    gap: 6px;
  }
  
  .section-header h3 {
    font-size: 13px;
  }
  
  .select-hint {
    font-size: 11px;
    width: 100%;
    margin-left: 0;
    margin-top: 4px;
  }
  
  .bridge-selector {
    flex-direction: column;
    gap: 10px;
  }
  
  .compare-btn {
    width: 100%;
  }
  
  .compare-card {
    padding: 12px;
    overflow-x: auto;
  }
  
  .card-header h4 {
    font-size: 13px;
  }
  
  .compare-table {
    font-size: 12px;
    min-width: 500px;
  }
  
  .compare-table td {
    padding: 6px 4px;
  }
  
  .label-cell {
    min-width: 60px;
  }
  
  .type-tag {
    font-size: 9px;
    padding: 1px 4px;
    display: block;
    margin-left: 0;
    margin-top: 2px;
  }
  
  .dimension-bar {
    gap: 10px;
  }
  
  .bar-item strong {
    font-size: 12px;
  }
  
  .bar-group {
    font-size: 11px;
    gap: 6px;
  }
  
  .bar-fill {
    height: 6px;
  }
  
  .tech-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }
  
  .tech-item {
    padding: 10px;
  }
  
  .tech-item h5 {
    font-size: 13px;
  }
  
  .tech-item p {
    font-size: 11px;
  }
  
  .empty-state p {
    font-size: 13px;
  }
}
</style>