<template>
  <div class="bridge-detail-container" v-if="bridge">
    <!-- 返回按钮和操作栏 -->
    <div class="back-nav">
      <el-button text @click="goBack" class="back-btn">
        ← 返回列表
      </el-button>
      <div class="action-buttons">
        <el-button 
          :type="isFavorited ? 'danger' : 'default'"
          @click="handleFavorite"
          class="favorite-btn"
        >
          <span class="favorite-icon">{{ isFavorited ? '❤️' : '🤍' }}</span>
          {{ isFavorited ? '已收藏' : '收藏' }}
        </el-button>
      </div>
    </div>

    <!-- 头部信息 -->
    <div class="bridge-header">
      <div class="header-decoration"></div>
      <div class="header-content">
        <div class="bridge-tags">
          <span class="tag-type" :class="getTypeClass(bridge.type)">{{ bridge.type }}</span>
          <span class="tag-dynasty">{{ bridge.dynasty }}</span>
          <span class="tag-heritage" v-if="bridge.heritage">{{ bridge.heritage }}</span>
        </div>
        <h1 class="bridge-title">{{ bridge.name }}</h1>
        <p class="bridge-alias" v-if="bridge.alias?.length">
          别名：{{ bridge.alias.join('、') }}
        </p>
      </div>
      <div class="header-meta">
        <div class="meta-item">
          <span class="meta-label">所在地</span>
          <span class="meta-value">{{ bridge.location?.province }} {{ bridge.location?.city }}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">始建年份</span>
          <span class="meta-value">{{ bridge.buildYear }}</span>
        </div>
        <div class="meta-item" v-if="bridge.status">
          <span class="meta-label">保存状况</span>
          <span class="meta-value">{{ bridge.status }}</span>
        </div>
      </div>
    </div>

    <!-- 主内容 -->
    <div class="bridge-content">
      <!-- 左侧 -->
      <div class="content-left">
        <!-- 图片展示区 -->
        <div class="image-section">
          <div class="section-header">
            <span class="header-seal">影</span>
            <h3>桥梁影像</h3>
          </div>
          <div class="image-gallery">
            <!-- 主图 -->
            <div class="main-image" @click="showPreview">
              <img 
                v-if="bridgeImage?.main" 
                :src="bridgeImage.main" 
                :alt="bridge.name"
                class="real-image"
              />
              <div v-else class="image-placeholder" :style="getPlaceholderStyle(bridge)">
                <span class="bridge-icon">{{ getPlaceholderIcon(bridge) }}</span>
                <span class="bridge-name-overlay">{{ bridge.name }}</span>
                <span class="bridge-type-tag">{{ bridge.type }}</span>
              </div>
            </div>
            <!-- 缩略图 -->
            <div class="thumbnail-list" v-if="bridgeImage?.gallery?.length">
              <div 
                class="thumbnail" 
                :class="{ active: activeImage === index }"
                v-for="(img, index) in bridgeImage.gallery.slice(0, 3)" 
                :key="index"
                @click="activeImage = index"
              >
                <img :src="img" :alt="`${bridge.name} - ${index + 1}`" />
              </div>
            </div>
            <div class="thumbnail-list" v-else>
              <div class="thumbnail placeholder"><span>全景</span></div>
              <div class="thumbnail placeholder"><span>近景</span></div>
              <div class="thumbnail placeholder"><span>细节</span></div>
            </div>
          </div>
          <div class="image-note">
            📷 {{ bridgeImage?.hasImage ? bridgeImage.source + ' (' + bridgeImage.license + ')' : '图片素材收集中' }}
          </div>
        </div>

        <!-- 简介 -->
        <div class="info-card">
          <div class="section-header">
            <span class="header-seal">简</span>
            <h3>桥梁简介</h3>
          </div>
          <p>{{ bridge.description }}</p>
        </div>

        <!-- 历史沿革 -->
        <div class="info-card" v-if="bridge.history">
          <div class="section-header">
            <span class="header-seal">史</span>
            <h3>历史沿革</h3>
          </div>
          <p>{{ bridge.history }}</p>
        </div>

        <!-- 建筑成就 -->
        <div class="info-card" v-if="bridge.technology">
          <div class="section-header">
            <span class="header-seal">技</span>
            <h3>建筑成就</h3>
          </div>
          <div class="tech-section">
            <div class="tech-item">
              <span class="tech-label">技术创新：</span>
              <span class="tech-value">{{ bridge.technology.innovation }}</span>
            </div>
            <div class="tech-item">
              <span class="tech-label">技术原理：</span>
              <span class="tech-value">{{ bridge.technology.principle }}</span>
            </div>
            <div class="tech-item highlight">
              <span class="tech-label">历史意义：</span>
              <span class="tech-value">{{ bridge.technology.significance }}</span>
            </div>
          </div>
        </div>

        <!-- 核心特点 -->
        <div class="info-card" v-if="bridge.features?.length">
          <div class="section-header">
            <span class="header-seal">特</span>
            <h3>核心特点</h3>
          </div>
          <div class="feature-tags">
            <span class="feature-tag" v-for="f in bridge.features" :key="f">{{ f }}</span>
          </div>
        </div>
      </div>

      <!-- 右侧 -->
      <div class="content-right">
        <!-- 尺寸信息 -->
        <div class="info-card" v-if="bridge.dimensions">
          <div class="section-header">
            <span class="header-seal small">尺</span>
            <h3>尺寸数据</h3>
          </div>
          <div class="dimension-grid">
            <div class="dimension-item">
              <span class="dim-value">{{ bridge.dimensions.length || '-' }}</span>
              <span class="dim-label">全长（米）</span>
            </div>
            <div class="dimension-item">
              <span class="dim-value">{{ bridge.dimensions.width || '-' }}</span>
              <span class="dim-label">宽度（米）</span>
            </div>
            <div class="dimension-item">
              <span class="dim-value">{{ bridge.dimensions.span || '-' }}</span>
              <span class="dim-label">跨径</span>
            </div>
          </div>
        </div>

        <!-- 建造者 -->
        <div class="info-card" v-if="bridge.builder">
          <div class="section-header">
            <span class="header-seal small">匠</span>
            <h3>建造者</h3>
          </div>
          <div class="builder-info">
            <div class="builder-avatar">{{ bridge.builder.name?.slice(0, 1) || '?' }}</div>
            <div class="builder-name">{{ bridge.builder.name }}</div>
            <div class="builder-dynasty">{{ bridge.builder.dynasty }}</div>
            <p class="builder-intro">{{ bridge.builder.intro }}</p>
          </div>
        </div>

        <!-- 诗词歌赋 -->
        <div class="info-card" v-if="bridge.culture?.poems?.length">
          <div class="section-header">
            <span class="header-seal small">诗</span>
            <h3>诗词歌赋</h3>
          </div>
          <div class="poem-list">
            <div class="poem-item" v-for="poem in bridge.culture.poems" :key="poem.content">
              <p class="poem-content">"{{ poem.content }}"</p>
              <p class="poem-author">—— {{ poem.author }}《{{ poem.title }}》</p>
            </div>
          </div>
        </div>

        <!-- 传说故事 -->
        <div class="info-card" v-if="bridge.culture?.legends?.length">
          <div class="section-header">
            <span class="header-seal small">传</span>
            <h3>传说故事</h3>
          </div>
          <div class="legend-tags">
            <span class="legend-tag" v-for="legend in bridge.culture.legends" :key="legend">{{ legend }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 图片预览对话框 -->
    <el-dialog
      v-model="previewVisible"
      :title="bridge?.name + ' - 桥梁影像'"
      width="80%"
      top="5vh"
      class="image-preview-dialog"
    >
      <div class="preview-content" v-if="bridgeImage?.gallery?.length">
        <img :src="bridgeImage.gallery[activeImage]" class="preview-img" />
      </div>
    </el-dialog>
  </div>

  <!-- 加载状态 -->
  <div class="loading-container" v-else>
    <div class="loading-icon">🏯</div>
    <p>加载中...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { bridgeAPI } from '@/api'
import { getBridgeImage, getPlaceholderStyle, getPlaceholderIcon } from '@/utils/bridgeImages'
import { isFavorite, toggleFavorite } from '@/utils/favorite'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const bridge = ref(null)
const activeImage = ref(0)
const previewVisible = ref(false)
const isFavorited = ref(false)

// 获取桥梁图片配置
const bridgeImage = computed(() => {
  if (!bridge.value) return null
  return getBridgeImage(bridge.value.id)
})

const goBack = () => {
  router.push('/bridges')
}

const showPreview = () => {
  if (bridgeImage.value?.hasImage) {
    previewVisible.value = true
  }
}

const getTypeClass = (type) => {
  return { '拱桥': 'type-arch', '梁桥': 'type-beam', '索桥': 'type-cable' }[type] || ''
}

// 收藏功能
const handleFavorite = () => {
  if (!bridge.value) return
  
  const newState = toggleFavorite(bridge.value.id)
  isFavorited.value = newState
  
  ElMessage({
    message: newState ? '已添加到收藏 ❤️' : '已取消收藏',
    type: newState ? 'success' : 'info',
    duration: 2000
  })
}

onMounted(async () => {
  const id = route.params.id
  try {
    const res = await bridgeAPI.getDetail(id)
    if (res.success) {
      bridge.value = res.data
      // 检查收藏状态
      isFavorited.value = isFavorite(id)
    }
  } catch (error) {
    console.error('加载桥梁详情失败:', error)
  }
})
</script>

<style scoped>
.bridge-detail-container {
  height: 100%;
  overflow-y: auto;
  padding-right: 5px;
  background: linear-gradient(135deg, #F5F0E6 0%, #EDE5D5 100%);
}

.back-nav {
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.back-btn {
  color: #8B2323;
  font-size: 13px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.favorite-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 13px;
  transition: all 0.3s;
}

.favorite-btn:hover {
  transform: scale(1.05);
}

.favorite-icon {
  font-size: 16px;
}

/* 头部 */
.bridge-header {
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.12);
  border-radius: 6px;
  padding: 20px;
  margin-bottom: 16px;
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

.header-content {
  margin-bottom: 15px;
}

.bridge-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}

.tag-type {
  padding: 3px 10px;
  border-radius: 2px;
  font-size: 11px;
  font-weight: 500;
}

.tag-type.type-arch { background: rgba(139, 35, 35, 0.15); color: #8B2323; }
.tag-type.type-beam { background: rgba(30, 58, 95, 0.15); color: #1E3A5F; }
.tag-type.type-cable { background: rgba(46, 139, 87, 0.15); color: #2E8B57; }

.tag-dynasty {
  padding: 3px 10px;
  border: 1px solid rgba(139, 35, 35, 0.2);
  border-radius: 2px;
  font-size: 11px;
  color: #4A4A4A;
}

.tag-heritage {
  padding: 3px 10px;
  background: #8B2323;
  color: #F5F0E6;
  border-radius: 2px;
  font-size: 11px;
  font-weight: 500;
}

.bridge-title {
  font-size: 26px;
  color: #2A2A2A;
  margin: 0 0 6px 0;
  font-family: 'Noto Serif SC', serif;
  letter-spacing: 2px;
}

.bridge-alias {
  font-size: 13px;
  color: #7A7A7A;
  margin: 0;
}

.header-meta {
  display: flex;
  gap: 24px;
  padding-top: 12px;
  border-top: 1px dashed rgba(201, 169, 98, 0.3);
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.meta-label {
  font-size: 11px;
  color: #7A7A7A;
}

.meta-value {
  font-size: 13px;
  color: #2A2A2A;
  font-weight: 500;
}

/* 内容区 */
.bridge-content {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 16px;
}

.info-card {
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.12);
  border-radius: 6px;
  padding: 16px;
  margin-bottom: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.section-header {
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
  border-radius: 2px;
}

.header-seal.small {
  width: 20px;
  height: 20px;
  font-size: 10px;
}

.section-header h3 {
  font-size: 14px;
  color: #2A2A2A;
  margin: 0;
  font-family: 'Noto Serif SC', serif;
}

.info-card p {
  font-size: 13px;
  color: #4A4A4A;
  line-height: 1.8;
  margin: 0;
}

/* 图片展示区 */
.image-section {
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.12);
  border-radius: 6px;
  padding: 16px;
  margin-bottom: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.main-image {
  position: relative;
  width: 100%;
  height: 260px;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  margin-bottom: 10px;
}

.main-image .real-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px dashed rgba(139, 35, 35, 0.3);
  border-radius: 4px;
  position: relative;
}

.bridge-icon {
  font-size: 64px;
  margin-bottom: 12px;
  opacity: 0.8;
}

.bridge-name-overlay {
  font-size: 24px;
  color: #2A2A2A;
  font-family: 'Noto Serif SC', serif;
  letter-spacing: 4px;
}

.bridge-type-tag {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 12px;
  background: rgba(139, 35, 35, 0.9);
  color: #F5F0E6;
  font-size: 12px;
  border-radius: 3px;
}

.image-note {
  margin-top: 10px;
  padding: 8px 12px;
  background: rgba(201, 169, 98, 0.1);
  border-radius: 4px;
  font-size: 11px;
  color: #7A7A7A;
  text-align: center;
}

.thumbnail-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.thumbnail {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(232, 224, 208, 0.6);
  border: 1px solid rgba(139, 35, 35, 0.1);
  border-radius: 4px;
  font-size: 11px;
  color: #7A7A7A;
  cursor: pointer;
  transition: all 0.2s;
  overflow: hidden;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumbnail.placeholder {
  background: rgba(232, 224, 208, 0.4);
}

.thumbnail {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(232, 224, 208, 0.6);
  border: 1px solid rgba(139, 35, 35, 0.1);
  border-radius: 4px;
  font-size: 11px;
  color: #7A7A7A;
  cursor: pointer;
  transition: all 0.2s;
}

.thumbnail.active {
  border-color: #8B2323;
  background: rgba(139, 35, 35, 0.08);
}

.image-note {
  margin-top: 10px;
  padding: 8px 12px;
  background: rgba(201, 169, 98, 0.1);
  border-radius: 4px;
  font-size: 11px;
  color: #7A7A7A;
}

/* 技术部分 */
.tech-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.tech-item {
  display: flex;
  gap: 8px;
}

.tech-item.highlight {
  padding: 10px;
  background: rgba(139, 35, 35, 0.05);
  border-left: 2px solid #8B2323;
  border-radius: 0 4px 4px 0;
}

.tech-label {
  font-size: 12px;
  color: #7A7A7A;
  white-space: nowrap;
}

.tech-value {
  font-size: 12px;
  color: #4A4A4A;
  line-height: 1.6;
}

/* 特点标签 */
.feature-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.feature-tag {
  padding: 4px 12px;
  background: rgba(201, 169, 98, 0.15);
  border: 1px solid rgba(201, 169, 98, 0.3);
  border-radius: 2px;
  font-size: 12px;
  color: #8B7355;
}

/* 尺寸数据 */
.dimension-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.dimension-item {
  text-align: center;
  padding: 15px 10px;
  background: rgba(139, 35, 35, 0.04);
  border-radius: 4px;
}

.dim-value {
  display: block;
  font-size: 22px;
  font-weight: 600;
  color: #8B2323;
  font-family: 'Noto Serif SC', serif;
  margin-bottom: 4px;
}

.dim-label {
  font-size: 11px;
  color: #7A7A7A;
}

/* 建造者 */
.builder-info {
  text-align: center;
}

.builder-avatar {
  width: 50px;
  height: 50px;
  margin: 0 auto 12px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8B2323, #C9A962);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  color: #F5F0E6;
}

.builder-name {
  font-size: 16px;
  font-weight: 600;
  color: #2A2A2A;
  font-family: 'Noto Serif SC', serif;
}

.builder-dynasty {
  font-size: 12px;
  color: #8B2323;
  margin-bottom: 10px;
}

.builder-intro {
  font-size: 12px;
  color: #4A4A4A;
  line-height: 1.6;
}

/* 诗词 */
.poem-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.poem-item {
  padding: 12px;
  background: rgba(139, 35, 35, 0.04);
  border-left: 2px solid #8B2323;
  border-radius: 0 4px 4px 0;
}

.poem-content {
  font-size: 13px;
  color: #2A2A2A;
  font-style: italic;
  line-height: 1.8;
  margin: 0 0 8px 0;
}

.poem-author {
  font-size: 11px;
  color: #7A7A7A;
  margin: 0;
  text-align: right;
}

/* 传说标签 */
.legend-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.legend-tag {
  padding: 4px 10px;
  background: rgba(46, 139, 87, 0.1);
  border: 1px solid rgba(46, 139, 87, 0.2);
  border-radius: 2px;
  font-size: 11px;
  color: #2E8B57;
}

/* 加载状态 */
.loading-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #7A7A7A;
  gap: 10px;
}

.loading-icon {
  font-size: 40px;
  opacity: 0.5;
}

/* 图片预览 */
.preview-content {
  width: 100%;
}

.preview-image {
  width: 100%;
  height: 50vh;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.preview-icon {
  font-size: 80px;
  margin-bottom: 15px;
}

.preview-name {
  font-size: 24px;
  color: #2A2A2A;
  font-family: 'Noto Serif SC', serif;
}

.preview-type {
  font-size: 14px;
  color: #7A7A7A;
  margin-top: 10px;
}

/* 图片预览 */
.preview-content {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.preview-img {
  max-width: 100%;
  max-height: 70vh;
  border-radius: 4px;
}

/* 响应式 */
@media (max-width: 1000px) {
  .bridge-content {
    grid-template-columns: 1fr;
  }
  
  .bridge-header {
    padding: 16px;
  }
  
  .header-meta {
    flex-direction: column;
    gap: 8px;
  }
}
</style>