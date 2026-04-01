<template>
  <div class="structure-container">
    <!-- 左侧：3D 展示区 -->
    <div class="model-section">
      <div class="section-header">
        <span class="header-seal">构</span>
        <h3>赵州桥 3D 结构模型</h3>
        <p class="header-desc">敞肩拱技术的完美呈现</p>
      </div>
      
      <div class="model-wrapper">
        <BridgeModelLoader :bridge-id="currentBridgeId" />
      </div>
    </div>
    
    <!-- 右侧：技术说明 -->
    <div class="tech-section">
      <!-- 技术卡片 -->
      <div class="tech-card">
        <div class="card-header">
          <span class="header-seal small">技</span>
          <h4>敞肩拱技术</h4>
        </div>
        <div class="tech-content">
          <p class="tech-desc">
            敞肩拱是世界桥梁史上的重大创新，由隋代工匠李春在赵州桥首次应用。
            在大拱两肩各砌两个小拱，形成"敞肩"结构。
          </p>
          <div class="tech-advantages">
            <div class="advantage-item">
              <span class="advantage-icon">⚖️</span>
              <div class="advantage-content">
                <span class="advantage-title">减轻自重</span>
                <span class="advantage-value">约700吨</span>
              </div>
            </div>
            <div class="advantage-item">
              <span class="advantage-icon">🌊</span>
              <div class="advantage-content">
                <span class="advantage-title">增大泄洪</span>
                <span class="advantage-value">减少冲击力</span>
              </div>
            </div>
            <div class="advantage-item">
              <span class="advantage-icon">💎</span>
              <div class="advantage-content">
                <span class="advantage-title">节省材料</span>
                <span class="advantage-value">经济高效</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 数据卡片 -->
      <div class="data-card">
        <div class="card-header">
          <span class="header-seal small">尺</span>
          <h4>桥梁尺寸</h4>
        </div>
        <div class="data-grid">
          <div class="data-item">
            <span class="data-value">64.4</span>
            <span class="data-label">全长（米）</span>
          </div>
          <div class="data-item">
            <span class="data-value">9.6</span>
            <span class="data-label">宽度（米）</span>
          </div>
          <div class="data-item">
            <span class="data-value">37.02</span>
            <span class="data-label">跨径（米）</span>
          </div>
          <div class="data-item highlight">
            <span class="data-value">1400+</span>
            <span class="data-label">屹立年数</span>
          </div>
        </div>
      </div>
      
      <!-- 历史意义 -->
      <div class="history-card">
        <div class="card-header">
          <span class="header-seal small">史</span>
          <h4>历史意义</h4>
        </div>
        <div class="history-content">
          <div class="history-item">
            <span class="history-year">公元595-605年</span>
            <span class="history-event">隋代始建，李春主持</span>
          </div>
          <div class="history-item">
            <span class="history-year">领先1200年</span>
            <span class="history-event">比欧洲同类桥梁早</span>
          </div>
          <div class="history-item">
            <span class="history-year">8次地震</span>
            <span class="history-event">历经多次地震仍屹立不倒</span>
          </div>
        </div>
      </div>
      
      <!-- 其他桥梁 -->
      <div class="other-bridges">
        <div class="card-header">
          <span class="header-seal small">览</span>
          <h4>其他桥梁结构</h4>
        </div>
        <div class="bridge-list">
          <div 
            class="bridge-item" 
            v-for="bridge in otherBridges" 
            :key="bridge.id"
            @click="currentBridgeId = bridge.id"
            :class="{ active: currentBridgeId === bridge.id }"
          >
            <span class="bridge-type" :class="bridge.typeClass">{{ bridge.type }}</span>
            <span class="bridge-name">{{ bridge.name }}</span>
            <span class="bridge-tech">{{ bridge.tech }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BridgeModelLoader from '@/components/BridgeModelLoader.vue'

const currentBridgeId = ref('zhaozhou-bridge')

const otherBridges = ref([
  { id: 'zhaozhou-bridge', name: '赵州桥', type: '拱桥', typeClass: 'type-arch', tech: '敞肩拱结构' },
  { id: 'luding-bridge', name: '泸定桥', type: '索桥', typeClass: 'type-cable', tech: '铁索悬吊' },
  { id: 'lugou-bridge', name: '卢沟桥', type: '拱桥', typeClass: 'type-arch', tech: '联拱结构' }
])
</script>

<style scoped>
.structure-container {
  height: 100%;
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 16px;
  background: linear-gradient(135deg, #F5F0E6 0%, #EDE5D5 100%);
  padding: 16px;
}

/* 左侧模型区 */
.model-section {
  display: flex;
  flex-direction: column;
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.12);
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.section-header {
  padding: 16px;
  border-bottom: 1px solid rgba(201, 169, 98, 0.3);
  background: linear-gradient(90deg, rgba(139, 35, 35, 0.04), transparent);
}

.section-header h3 {
  margin: 0;
  font-size: 18px;
  color: #2A2A2A;
  font-family: 'Noto Serif SC', serif;
  letter-spacing: 2px;
}

.header-desc {
  margin: 6px 0 0;
  font-size: 12px;
  color: #7A7A7A;
}

.model-wrapper {
  flex: 1;
  min-height: 400px;
}

/* 右侧技术区 */
.tech-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow-y: auto;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(201, 169, 98, 0.3);
}

.header-seal {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: #8B2323;
  color: #F5F0E6;
  font-size: 11px;
  font-weight: bold;
  border-radius: 3px;
}

.header-seal.small {
  width: 20px;
  height: 20px;
  font-size: 10px;
}

.card-header h4 {
  margin: 0;
  font-size: 14px;
  color: #2A2A2A;
  font-family: 'Noto Serif SC', serif;
}

/* 技术卡片 */
.tech-card, .data-card, .history-card, .other-bridges {
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.12);
  border-radius: 6px;
  padding: 14px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.tech-desc {
  font-size: 13px;
  color: #4A4A4A;
  line-height: 1.8;
  margin: 0 0 14px;
}

.tech-advantages {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.advantage-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  background: rgba(232, 224, 208, 0.5);
  border-radius: 4px;
  border-left: 2px solid #8B2323;
}

.advantage-icon {
  font-size: 20px;
}

.advantage-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.advantage-title {
  font-size: 12px;
  color: #7A7A7A;
}

.advantage-value {
  font-size: 14px;
  font-weight: 600;
  color: #8B2323;
}

/* 数据卡片 */
.data-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.data-item {
  text-align: center;
  padding: 14px 10px;
  background: rgba(232, 224, 208, 0.5);
  border-radius: 4px;
}

.data-item.highlight {
  background: rgba(139, 35, 35, 0.08);
  border: 1px solid rgba(139, 35, 35, 0.15);
}

.data-value {
  display: block;
  font-size: 22px;
  font-weight: 600;
  color: #8B2323;
  font-family: 'Noto Serif SC', serif;
  margin-bottom: 4px;
}

.data-label {
  font-size: 11px;
  color: #7A7A7A;
}

/* 历史卡片 */
.history-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background: rgba(232, 224, 208, 0.5);
  border-radius: 4px;
}

.history-year {
  font-size: 12px;
  font-weight: 600;
  color: #8B2323;
}

.history-event {
  font-size: 12px;
  color: #4A4A4A;
}

/* 其他桥梁 */
.bridge-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.bridge-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: rgba(232, 224, 208, 0.5);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.bridge-item:hover {
  background: rgba(139, 35, 35, 0.06);
  transform: translateX(2px);
}

.bridge-item.active {
  background: rgba(139, 35, 35, 0.1);
  border-left: 2px solid #8B2323;
}

.bridge-type {
  padding: 2px 8px;
  border-radius: 2px;
  font-size: 10px;
}

.bridge-type.type-arch {
  background: rgba(139, 35, 35, 0.15);
  color: #8B2323;
}

.bridge-type.type-beam {
  background: rgba(30, 58, 95, 0.15);
  color: #1E3A5F;
}

.bridge-type.type-cable {
  background: rgba(46, 139, 87, 0.15);
  color: #2E8B57;
}

.bridge-name {
  flex: 1;
  font-size: 13px;
  color: #2A2A2A;
}

.bridge-tech {
  font-size: 11px;
  color: #7A7A7A;
}

/* 响应式 */
@media (max-width: 1200px) {
  .structure-container {
    grid-template-columns: 1fr;
  }
  
  .model-section {
    min-height: 450px;
  }
  
  .tech-section {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .structure-container {
    grid-template-columns: 1fr;
    padding: 12px;
    gap: 12px;
  }
  
  .section-header {
    padding: 12px;
  }
  
  .section-header h3 {
    font-size: 16px;
    letter-spacing: 1px;
  }
  
  .header-desc {
    font-size: 11px;
  }
  
  .model-wrapper {
    min-height: 280px;
  }
  
  .tech-section {
    display: flex;
    flex-direction: column;
  }
  
  .tech-card, .data-card, .history-card, .other-bridges {
    padding: 12px;
  }
  
  .card-header h4 {
    font-size: 13px;
  }
  
  .tech-desc {
    font-size: 12px;
    line-height: 1.7;
  }
  
  .advantage-item {
    padding: 8px 10px;
    gap: 10px;
  }
  
  .advantage-icon {
    font-size: 18px;
  }
  
  .advantage-title {
    font-size: 11px;
  }
  
  .advantage-value {
    font-size: 13px;
  }
  
  .data-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }
  
  .data-item {
    padding: 10px 8px;
  }
  
  .data-value {
    font-size: 18px;
    margin-bottom: 2px;
  }
  
  .data-label {
    font-size: 10px;
  }
  
  .history-item {
    padding: 8px 10px;
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
  
  .history-year {
    font-size: 11px;
  }
  
  .history-event {
    font-size: 11px;
  }
  
  .bridge-item {
    padding: 8px 10px;
  }
  
  .bridge-name {
    font-size: 12px;
  }
  
  .bridge-tech {
    font-size: 10px;
  }
}
</style>