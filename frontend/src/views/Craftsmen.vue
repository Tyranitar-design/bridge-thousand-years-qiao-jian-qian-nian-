<template>
  <div class="craftsmen-container">
    <!-- 水墨装饰背景 -->
    <div class="ink-decoration">
      <div class="ink-blob ink-blob-1"></div>
      <div class="ink-blob ink-blob-2"></div>
    </div>

    <!-- 顶部卷轴标题 -->
    <header class="page-header">
      <div class="scroll-title">
        <div class="scroll-left"></div>
        <div class="scroll-content">
          <h1 class="main-title">匠 心 人 物</h1>
          <p class="sub-title">致敬古代桥梁建造者，传承千年工匠精神</p>
        </div>
        <div class="scroll-right"></div>
      </div>
    </header>

    <!-- 统计概览 -->
    <section class="stats-section">
      <div class="stats-cards">
        <div class="stat-card">
          <div class="card-corner corner-tl"></div>
          <div class="card-corner corner-tr"></div>
          <div class="card-corner corner-bl"></div>
          <div class="card-corner corner-br"></div>
          <div class="card-icon">👨‍🔧</div>
          <div class="card-info">
            <div class="stat-value">{{ craftsmen.length }}</div>
            <div class="stat-label">知名匠人</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="card-corner corner-tl"></div>
          <div class="card-corner corner-tr"></div>
          <div class="card-corner corner-bl"></div>
          <div class="card-corner corner-br"></div>
          <div class="card-icon">🏯</div>
          <div class="card-info">
            <div class="stat-value">{{ totalWorks }}</div>
            <div class="stat-label">传世佳作</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="card-corner corner-tl"></div>
          <div class="card-corner corner-tr"></div>
          <div class="card-corner corner-bl"></div>
          <div class="card-corner corner-br"></div>
          <div class="card-icon">📜</div>
          <div class="card-info">
            <div class="stat-value">{{ dynastySpan }}</div>
            <div class="stat-label">年代跨度</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="card-corner corner-tl"></div>
          <div class="card-corner corner-tr"></div>
          <div class="card-corner corner-bl"></div>
          <div class="card-corner corner-br"></div>
          <div class="card-icon">💎</div>
          <div class="card-info">
            <div class="stat-value">{{ heritageCount }}</div>
            <div class="stat-label">世界遗产</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 匠人展示区 -->
    <main class="craftsmen-main">
      <!-- 左侧：知名匠人列表 -->
      <section class="craftsmen-list">
        <div class="section-header">
          <span class="header-seal">匠</span>
          <h3>知名匠人</h3>
          <div class="header-line"></div>
        </div>
        
        <div class="craftsmen-grid" v-if="craftsmen.length > 0">
          <div
            class="craftsman-card"
            v-for="(craftsman, index) in craftsmen"
            :key="craftsman.name"
            :class="{ active: selectedCraftsman?.name === craftsman.name }"
            @click="selectCraftsman(craftsman)"
            :style="{ '--delay': index * 0.1 + 's' }"
          >
            <div class="card-corner corner-tl"></div>
            <div class="card-corner corner-tr"></div>
            <div class="card-corner corner-bl"></div>
            <div class="card-corner corner-br"></div>
            
            <div class="avatar-wrapper">
              <div class="avatar">{{ craftsman.name.slice(0, 1) }}</div>
              <div class="avatar-ring"></div>
            </div>
            
            <div class="craftsman-info">
              <h4 class="name">{{ craftsman.name }}</h4>
              <p class="dynasty">{{ craftsman.dynasty }}</p>
              <div class="works-count">
                <span class="count">{{ craftsman.works?.length || 0 }}</span>
                <span class="label">座桥梁</span>
              </div>
            </div>
            
            <div class="card-arrow">→</div>
          </div>
        </div>

        <div class="empty-state" v-else>
          <div class="empty-icon">👷</div>
          <p>暂无匠人信息</p>
        </div>
      </section>

      <!-- 右侧：匠人详情 -->
      <section class="craftsman-detail">
        <div class="detail-card" v-if="selectedCraftsman">
          <div class="detail-header">
            <div class="detail-avatar">{{ selectedCraftsman.name.slice(0, 1) }}</div>
            <div class="detail-title">
              <h2>{{ selectedCraftsman.name }}</h2>
              <p class="detail-dynasty">{{ selectedCraftsman.dynasty }}</p>
            </div>
            <div class="detail-badge" v-if="selectedCraftsman.works?.length >= 2">
              <span class="badge-icon">🏆</span>
              <span>多产匠师</span>
            </div>
          </div>

          <div class="detail-intro">
            <div class="intro-label">
              <span class="label-seal">传</span>
              <span>生平简介</span>
            </div>
            <p class="intro-text">{{ selectedCraftsman.intro || '暂无详细生平记载，但其传世之作足以见证其精湛技艺。' }}</p>
          </div>

          <div class="detail-works">
            <div class="works-label">
              <span class="label-seal">作</span>
              <span>传世佳作</span>
            </div>
            <div class="works-list">
              <div 
                class="work-item" 
                v-for="work in selectedCraftsman.worksDetails" 
                :key="work.id"
                @click="goToBridge(work.id)"
              >
                <div class="work-icon">🏛️</div>
                <div class="work-info">
                  <h5>{{ work.name }}</h5>
                  <p>{{ work.dynasty }} · {{ work.location?.province }}</p>
                </div>
                <div class="work-type" :class="getTypeClass(work.type)">{{ work.type }}</div>
              </div>
            </div>
          </div>

          <div class="detail-tech" v-if="selectedCraftsman.worksDetails?.[0]?.technology">
            <div class="tech-label">
              <span class="label-seal">技</span>
              <span>技术贡献</span>
            </div>
            <div class="tech-card">
              <div class="tech-title">{{ selectedCraftsman.worksDetails[0].technology?.innovation }}</div>
              <div class="tech-desc">{{ selectedCraftsman.worksDetails[0].technology?.significance }}</div>
            </div>
          </div>
        </div>

        <div class="detail-placeholder" v-else>
          <div class="placeholder-content">
            <div class="placeholder-icon">👈</div>
            <p>点击左侧匠人卡片<br/>查看详细信息</p>
          </div>
          <div class="placeholder-quote">
            <p>"巧夺天工，匠心独运"</p>
            <span>—— 赞美古代工匠</span>
          </div>
        </div>
      </section>
    </main>

    <!-- 匠人精神 -->
    <section class="spirit-section">
      <div class="section-header">
        <span class="header-seal">魂</span>
        <h3>匠人精神</h3>
        <div class="header-line"></div>
      </div>
      <div class="spirit-grid">
        <div class="spirit-card">
          <div class="spirit-icon">🎯</div>
          <h4>精益求精</h4>
          <p>对每一个细节都追求完美，不放过任何瑕疵</p>
        </div>
        <div class="spirit-card">
          <div class="spirit-icon">💪</div>
          <h4>坚韧不拔</h4>
          <p>面对困难从不退缩，以毅力克服重重障碍</p>
        </div>
        <div class="spirit-card">
          <div class="spirit-icon">💡</div>
          <h4>勇于创新</h4>
          <p>敢于突破传统束缚，开创前所未有的技术</p>
        </div>
        <div class="spirit-card">
          <div class="spirit-icon">🤝</div>
          <h4>薪火相传</h4>
          <p>将技艺与精神代代相传，延续文明之脉</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { bridgeAPI } from '@/api'

const router = useRouter()

const bridges = ref([])
const selectedCraftsman = ref(null)

// 提取匠人列表（排除佚名）
const craftsmen = computed(() => {
  const builders = new Map()
  
  bridges.value.forEach(bridge => {
    if (bridge.builder?.name && bridge.builder.name !== '佚名') {
      if (!builders.has(bridge.builder.name)) {
        builders.set(bridge.builder.name, {
          name: bridge.builder.name,
          dynasty: bridge.builder.dynasty,
          intro: bridge.builder.intro,
          works: [bridge.name],
          worksDetails: [bridge]
        })
      } else {
        builders.get(bridge.builder.name).works.push(bridge.name)
        builders.get(bridge.builder.name).worksDetails.push(bridge)
      }
    }
  })
  
  return Array.from(builders.values())
})

// 统计数据
const totalWorks = computed(() => {
  return craftsmen.value.reduce((sum, c) => sum + (c.works?.length || 0), 0)
})

const dynastySpan = computed(() => {
  if (craftsmen.value.length === 0) return '0年'
  // 简化计算，返回朝代数量
  const dynasties = new Set(craftsmen.value.map(c => c.dynasty))
  return `${dynasties.size}个朝代`
})

const heritageCount = computed(() => {
  let count = 0
  craftsmen.value.forEach(c => {
    c.worksDetails?.forEach(w => {
      if (w.heritage) count++
    })
  })
  return count
})

// 选择匠人
const selectCraftsman = (craftsman) => {
  selectedCraftsman.value = craftsman
}

// 跳转到桥梁详情
const goToBridge = (id) => {
  router.push(`/bridges/${id}`)
}

// 类型样式
const getTypeClass = (type) => {
  const classes = { '拱桥': 'type-arch', '梁桥': 'type-beam', '索桥': 'type-cable' }
  return classes[type] || ''
}

onMounted(async () => {
  try {
    const res = await bridgeAPI.getList()
    if (res.success) {
      bridges.value = res.data
      // 默认选中第一个匠人
      if (craftsmen.value.length > 0) {
        selectedCraftsman.value = craftsmen.value[0]
      }
    }
  } catch (error) {
    console.error('加载数据失败:', error)
  }
})
</script>

<style scoped>
/* 主容器 */
.craftsmen-container {
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
  width: 400px;
  height: 400px;
  background: #1A1A1A;
  top: -100px;
  right: 5%;
}

.ink-blob-2 {
  width: 300px;
  height: 300px;
  background: #8B2323;
  bottom: 10%;
  left: -50px;
}

/* 顶部标题 */
.page-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px 20px;
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
  width: 16px;
  background: linear-gradient(90deg, #8B7355, #C9A962);
  border-radius: 8px 0 0 8px;
}

.scroll-right {
  border-radius: 0 8px 8px 0;
}

.scroll-content {
  background: linear-gradient(180deg, #F5F0E6 0%, #EDE5D5 100%);
  border-top: 3px solid #C9A962;
  border-bottom: 3px solid #C9A962;
  padding: 12px 36px;
  text-align: center;
}

.main-title {
  font-size: 26px;
  font-weight: 600;
  color: #2A2A2A;
  margin: 0;
  letter-spacing: 10px;
  font-family: 'Noto Serif SC', 'Source Han Serif SC', serif;
}

.sub-title {
  font-size: 12px;
  color: #7A7A7A;
  margin: 6px 0 0;
  letter-spacing: 2px;
}

/* 统计卡片区 */
.stats-section {
  position: relative;
  z-index: 10;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}

.stat-card {
  position: relative;
  padding: 16px 18px;
  background: rgba(245, 240, 230, 0.9);
  border: 1px solid rgba(139, 35, 35, 0.15);
  border-left: 3px solid #8B2323;
  display: flex;
  align-items: center;
  gap: 14px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
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

.card-icon {
  font-size: 28px;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(139, 35, 35, 0.08), rgba(201, 169, 98, 0.08));
  border-radius: 8px;
}

.card-info {
  flex: 1;
}

.stat-value {
  font-size: 26px;
  font-weight: 600;
  color: #8B2323;
  font-family: 'Noto Serif SC', serif;
}

.stat-label {
  font-size: 12px;
  color: #7A7A7A;
  margin-top: 2px;
}

/* 主内容区 */
.craftsmen-main {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 16px;
  min-height: 0;
  position: relative;
  z-index: 10;
}

/* 左侧匠人列表 */
.craftsmen-list {
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.12);
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.section-header {
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
}

.section-header h3 {
  font-size: 14px;
  color: #2A2A2A;
  margin: 0;
  font-family: 'Noto Serif SC', serif;
  letter-spacing: 1px;
}

.header-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, rgba(201, 169, 98, 0.4), transparent);
}

.craftsmen-grid {
  flex: 1;
  padding: 12px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.craftsman-card {
  position: relative;
  padding: 14px 16px;
  background: rgba(245, 240, 230, 0.8);
  border: 1px solid rgba(139, 35, 35, 0.1);
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
  transition: all 0.3s;
  animation: fadeInUp 0.5s ease forwards;
  animation-delay: var(--delay);
  opacity: 0;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.craftsman-card:hover {
  background: rgba(139, 35, 35, 0.05);
  border-color: rgba(139, 35, 35, 0.25);
  transform: translateX(4px);
}

.craftsman-card.active {
  background: rgba(139, 35, 35, 0.08);
  border-color: #8B2323;
  box-shadow: 0 2px 8px rgba(139, 35, 35, 0.15);
}

.avatar-wrapper {
  position: relative;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8B2323, #C9A962);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: bold;
  color: #F5F0E6;
  position: relative;
  z-index: 1;
}

.avatar-ring {
  position: absolute;
  top: -3px;
  left: -3px;
  right: -3px;
  bottom: -3px;
  border: 2px solid rgba(201, 169, 98, 0.4);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.4; }
  50% { transform: scale(1.05); opacity: 0.6; }
}

.craftsman-info {
  flex: 1;
}

.craftsman-info .name {
  margin: 0 0 3px;
  font-size: 15px;
  color: #2A2A2A;
  font-family: 'Noto Serif SC', serif;
}

.craftsman-info .dynasty {
  margin: 0 0 6px;
  font-size: 12px;
  color: #8B2323;
}

.works-count {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.works-count .count {
  font-size: 18px;
  font-weight: 600;
  color: #C9A962;
}

.works-count .label {
  font-size: 11px;
  color: #7A7A7A;
}

.card-arrow {
  color: #C9A962;
  font-size: 18px;
  opacity: 0;
  transition: all 0.3s;
}

.craftsman-card:hover .card-arrow,
.craftsman-card.active .card-arrow {
  opacity: 1;
  transform: translateX(4px);
}

/* 右侧详情 */
.craftsman-detail {
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.12);
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.detail-card {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(201, 169, 98, 0.3);
}

.detail-avatar {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8B2323, #C9A962);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  font-weight: bold;
  color: #F5F0E6;
  box-shadow: 0 4px 15px rgba(139, 35, 35, 0.2);
}

.detail-title h2 {
  margin: 0;
  font-size: 22px;
  color: #2A2A2A;
  font-family: 'Noto Serif SC', serif;
}

.detail-dynasty {
  margin: 4px 0 0;
  font-size: 13px;
  color: #8B2323;
}

.detail-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 12px;
  background: linear-gradient(135deg, #C9A962, #8B7355);
  border-radius: 12px;
  color: #F5F0E6;
  font-size: 11px;
  margin-left: auto;
}

.badge-icon {
  font-size: 12px;
}

.detail-intro,
.detail-works,
.detail-tech {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.intro-label,
.works-label,
.tech-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.label-seal {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  background: #8B2323;
  color: #F5F0E6;
  font-size: 11px;
  font-weight: bold;
  border-radius: 3px;
}

.intro-label span:last-child,
.works-label span:last-child,
.tech-label span:last-child {
  font-size: 13px;
  color: #4A4A4A;
  font-family: 'Noto Serif SC', serif;
}

.intro-text {
  margin: 0;
  font-size: 13px;
  color: #4A4A4A;
  line-height: 1.8;
  padding: 12px 14px;
  background: rgba(139, 35, 35, 0.04);
  border-left: 3px solid #8B2323;
  border-radius: 0 6px 6px 0;
}

.works-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.work-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  background: rgba(245, 240, 230, 0.8);
  border: 1px solid rgba(139, 35, 35, 0.1);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.work-item:hover {
  background: rgba(139, 35, 35, 0.06);
  border-color: #C9A962;
  transform: translateX(4px);
}

.work-icon {
  font-size: 24px;
}

.work-info {
  flex: 1;
}

.work-info h5 {
  margin: 0 0 3px;
  font-size: 14px;
  color: #2A2A2A;
  font-family: 'Noto Serif SC', serif;
}

.work-info p {
  margin: 0;
  font-size: 11px;
  color: #7A7A7A;
}

.work-type {
  padding: 3px 10px;
  border-radius: 2px;
  font-size: 11px;
}

.work-type.type-arch {
  background: rgba(139, 35, 35, 0.15);
  color: #8B2323;
}

.work-type.type-beam {
  background: rgba(30, 58, 95, 0.15);
  color: #1E3A5F;
}

.work-type.type-cable {
  background: rgba(46, 139, 87, 0.15);
  color: #2E8B57;
}

.tech-card {
  padding: 14px 16px;
  background: linear-gradient(135deg, rgba(201, 169, 98, 0.1), rgba(139, 35, 35, 0.05));
  border: 1px solid rgba(201, 169, 98, 0.3);
  border-radius: 6px;
}

.tech-title {
  font-size: 14px;
  color: #2A2A2A;
  font-weight: 500;
  margin-bottom: 6px;
  font-family: 'Noto Serif SC', serif;
}

.tech-desc {
  font-size: 12px;
  color: #7A7A7A;
  line-height: 1.6;
}

/* 详情占位 */
.detail-placeholder {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  gap: 30px;
}

.placeholder-content {
  text-align: center;
}

.placeholder-icon {
  font-size: 48px;
  margin-bottom: 16px;
  animation: hintLeft 1.5s ease-in-out infinite;
}

@keyframes hintLeft {
  0%, 100% { transform: translateX(0); }
  50% { transform: translateX(-10px); }
}

.placeholder-content p {
  margin: 0;
  font-size: 14px;
  color: #7A7A7A;
  line-height: 1.8;
}

.placeholder-quote {
  text-align: center;
  padding: 16px 24px;
  background: rgba(139, 35, 35, 0.04);
  border-radius: 6px;
}

.placeholder-quote p {
  margin: 0 0 6px;
  font-size: 16px;
  color: #8B2323;
  font-family: 'Noto Serif SC', serif;
  letter-spacing: 2px;
}

.placeholder-quote span {
  font-size: 11px;
  color: #7A7A7A;
}

/* 匠人精神区 */
.spirit-section {
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.12);
  border-radius: 6px;
  padding: 16px;
  position: relative;
  z-index: 10;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.spirit-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}

.spirit-card {
  text-align: center;
  padding: 16px 12px;
  background: rgba(245, 240, 230, 0.6);
  border: 1px solid rgba(139, 35, 35, 0.08);
  border-radius: 6px;
  transition: all 0.3s;
}

.spirit-card:hover {
  background: rgba(139, 35, 35, 0.05);
  border-color: rgba(139, 35, 35, 0.2);
  transform: translateY(-3px);
}

.spirit-icon {
  font-size: 28px;
  margin-bottom: 8px;
}

.spirit-card h4 {
  margin: 0 0 6px;
  font-size: 14px;
  color: #2A2A2A;
  font-family: 'Noto Serif SC', serif;
}

.spirit-card p {
  margin: 0;
  font-size: 11px;
  color: #7A7A7A;
  line-height: 1.5;
}

/* 空状态 */
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  gap: 12px;
}

.empty-icon {
  font-size: 48px;
  opacity: 0.5;
}

.empty-state p {
  margin: 0;
  font-size: 14px;
  color: #7A7A7A;
}

/* 响应式 */
@media (max-width: 1400px) {
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .spirit-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .craftsmen-main {
    grid-template-columns: 1fr;
  }
  
  .craftsmen-list {
    max-height: 300px;
  }
}

@media (max-width: 768px) {
  .main-title {
    font-size: 20px;
    letter-spacing: 6px;
  }
  
  .stats-cards {
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }
  
  .stat-card {
    padding: 12px 14px;
  }
  
  .card-icon {
    width: 40px;
    height: 40px;
    font-size: 22px;
  }
  
  .stat-value {
    font-size: 20px;
  }
  
  .spirit-grid {
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }
  
  .spirit-card {
    padding: 12px 10px;
  }
}
</style>