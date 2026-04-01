<template>
  <div class="timeline-container">
    <!-- 顶部标题 -->
    <div class="timeline-header">
      <div class="header-decoration"></div>
      <h2>中国古桥梁发展时间轴</h2>
      <p>从春秋战国到清末，跨越2500年的桥梁建筑智慧</p>
    </div>

    <!-- 时间轴内容 -->
    <div class="timeline-content">
      <div class="timeline-track">
        <div
          class="timeline-node"
          v-for="(bridges, dynasty) in timelineData"
          :key="dynasty"
        >
          <div class="node-marker">
            <div class="node-dot"></div>
            <div class="node-line"></div>
          </div>
          <div class="node-content">
            <div class="node-header">
              <span class="dynasty-seal">{{ dynasty.slice(0, 1) }}</span>
              <span class="dynasty-name">{{ dynasty }}</span>
              <span class="bridge-count">{{ bridges.length }}座</span>
            </div>
            <div class="node-bridges">
              <span
                class="bridge-tag"
                v-for="bridge in bridges"
                :key="bridge.id"
                @click="goToBridge(bridge.id)"
              >
                {{ bridge.name }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { bridgeAPI } from '@/api'

const router = useRouter()
const timelineData = ref({})

const goToBridge = (id) => {
  router.push(`/bridges/${id}`)
}

onMounted(async () => {
  try {
    const res = await bridgeAPI.getTimeline()
    if (res.success) {
      timelineData.value = res.data
    }
  } catch (error) {
    console.error('加载时间轴数据失败:', error)
  }
})
</script>

<style scoped>
.timeline-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: linear-gradient(135deg, #F5F0E6 0%, #EDE5D5 100%);
}

.timeline-header {
  text-align: center;
  padding: 24px 20px;
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.12);
  border-radius: 6px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.header-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, #C9A962, #8B2323, #C9A962, transparent);
}

.timeline-header h2 {
  margin: 0 0 8px;
  color: #2A2A2A;
  font-size: 22px;
  font-family: 'Noto Serif SC', serif;
  letter-spacing: 4px;
}

.timeline-header p {
  margin: 0;
  color: #7A7A7A;
  font-size: 13px;
  letter-spacing: 1px;
}

.timeline-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.timeline-track {
  position: relative;
  padding-left: 50px;
}

.timeline-track::before {
  content: '';
  position: absolute;
  left: 20px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(180deg, #C9A962, #8B2323, #C9A962);
}

.timeline-node {
  position: relative;
  margin-bottom: 24px;
  display: flex;
  gap: 16px;
}

.node-marker {
  position: absolute;
  left: -50px;
  top: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.node-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #8B2323;
  border: 2px solid #F5F0E6;
  box-shadow: 0 0 0 3px rgba(139, 35, 35, 0.2);
  z-index: 1;
}

.node-line {
  width: 2px;
  flex: 1;
  background: rgba(201, 169, 98, 0.3);
}

.timeline-node:last-child .node-line {
  display: none;
}

.node-content {
  flex: 1;
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.12);
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.node-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: linear-gradient(90deg, rgba(139, 35, 35, 0.06), transparent);
  border-bottom: 1px solid rgba(201, 169, 98, 0.2);
}

.dynasty-seal {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: #8B2323;
  color: #F5F0E6;
  font-size: 13px;
  font-weight: bold;
  border-radius: 3px;
}

.dynasty-name {
  font-size: 15px;
  font-weight: 600;
  color: #2A2A2A;
  font-family: 'Noto Serif SC', serif;
}

.bridge-count {
  margin-left: auto;
  font-size: 12px;
  color: #8B2323;
  background: rgba(139, 35, 35, 0.08);
  padding: 2px 8px;
  border-radius: 10px;
}

.node-bridges {
  padding: 12px 16px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.bridge-tag {
  padding: 6px 14px;
  background: rgba(232, 224, 208, 0.8);
  border: 1px solid rgba(139, 35, 35, 0.15);
  border-radius: 2px;
  font-size: 12px;
  color: #4A4A4A;
  cursor: pointer;
  transition: all 0.2s;
}

.bridge-tag:hover {
  background: rgba(139, 35, 35, 0.08);
  border-color: #8B2323;
  color: #8B2323;
  transform: translateX(2px);
}

/* 响应式 */
@media (max-width: 768px) {
  .timeline-header {
    padding: 16px 12px;
  }
  
  .timeline-header h2 {
    font-size: 18px;
    letter-spacing: 2px;
  }
  
  .timeline-header p {
    font-size: 11px;
  }
  
  .timeline-content {
    padding: 12px;
  }
  
  .timeline-track {
    padding-left: 36px;
  }
  
  .timeline-track::before {
    left: 14px;
  }
  
  .node-marker {
    left: -36px;
  }
  
  .node-dot {
    width: 10px;
    height: 10px;
  }
  
  .node-content {
    border-radius: 4px;
  }
  
  .node-header {
    padding: 10px 12px;
    gap: 8px;
  }
  
  .dynasty-seal {
    width: 24px;
    height: 24px;
    font-size: 12px;
  }
  
  .dynasty-name {
    font-size: 14px;
  }
  
  .bridge-count {
    font-size: 11px;
    padding: 2px 6px;
  }
  
  .node-bridges {
    padding: 10px 12px;
    gap: 6px;
  }
  
  .bridge-tag {
    padding: 5px 10px;
    font-size: 11px;
  }
}
</style>