<template>
  <div class="bridge-gallery-container">
    <!-- 省份筛选提示条 -->
    <div class="province-banner" v-if="selectedProvince">
      <span class="banner-text">
        📍 当前筛选：<strong>{{ selectedProvince }}</strong> 的桥梁（{{ filteredBridges.length }}座）
      </span>
      <el-button text size="small" @click="clearProvinceFilter" class="clear-btn">
        ✕ 清除筛选
      </el-button>
    </div>
    
    <!-- 顶部筛选 -->
    <div class="filter-section">
      <div class="filter-row">
        <el-input
          v-model="searchQuery"
          placeholder="搜索桥梁名称..."
          prefix-icon="Search"
          clearable
          class="search-input"
          @input="handleSearch"
        />
        
        <div class="stats-info">
          <span class="stats-label">共</span>
          <span class="stats-number">{{ filteredBridges.length }}</span>
          <span class="stats-label">座桥梁</span>
        </div>
      </div>
      
      <div class="filter-row">
        <div class="filter-group">
          <span class="filter-label">省份：</span>
          <el-select v-model="selectedProvince" placeholder="选择省份" clearable class="province-select">
            <el-option label="全部" value="" />
            <el-option 
              v-for="province in provinceList" 
              :key="province" 
              :label="province" 
              :value="province" 
            />
          </el-select>
        </div>
        
        <div class="filter-group">
          <span class="filter-label">类型：</span>
          <div class="filter-tabs">
            <span 
              class="filter-tab" 
              :class="{ active: selectedType === '' }"
              @click="selectedType = ''"
            >全部</span>
            <span 
              class="filter-tab" 
              :class="{ active: selectedType === '拱桥' }"
              @click="selectedType = '拱桥'"
            >拱桥</span>
            <span 
              class="filter-tab" 
              :class="{ active: selectedType === '梁桥' }"
              @click="selectedType = '梁桥'"
            >梁桥</span>
            <span 
              class="filter-tab" 
              :class="{ active: selectedType === '索桥' }"
              @click="selectedType = '索桥'"
            >索桥</span>
          </div>
        </div>
        
        <div class="filter-group">
          <span class="filter-label">朝代：</span>
          <el-select v-model="selectedDynasty" placeholder="选择朝代" clearable @change="handleFilter">
            <el-option label="全部" value="" />
            <el-option label="隋唐" value="隋唐" />
            <el-option label="宋代" value="宋代" />
            <el-option label="元代" value="元代" />
            <el-option label="明代" value="明代" />
            <el-option label="清代" value="清代" />
          </el-select>
        </div>
        
        <div class="filter-group">
          <el-button 
            :type="showFavoritesOnly ? 'danger' : 'default'"
            @click="showFavoritesOnly = !showFavoritesOnly"
            class="favorite-filter-btn"
          >
            <span>{{ showFavoritesOnly ? '❤️' : '🤍' }}</span>
            收藏 ({{ favoriteCount }})
          </el-button>
        </div>
      </div>
    </div>

    <!-- 桥梁列表 -->
    <div class="bridge-grid">
      <div
        class="bridge-item"
        v-for="bridge in filteredBridges"
        :key="bridge.id"
        @click="goToDetail(bridge.id)"
      >
        <!-- 装饰角 -->
        <div class="card-corner corner-tl"></div>
        <div class="card-corner corner-tr"></div>
        <div class="card-corner corner-bl"></div>
        <div class="card-corner corner-br"></div>
        
        <!-- 图片预览区 -->
        <div class="bridge-image" :style="getCardImageStyle(bridge)">
          <div class="image-overlay">
            <span class="view-btn">查看详情 →</span>
          </div>
          <div class="image-badge heritage" v-if="bridge.heritage">遗</div>
          <div class="image-badge favorite" v-if="isFavorite(bridge.id)">❤️</div>
        </div>
        
        <div class="bridge-content">
          <div class="bridge-header">
            <span class="bridge-type" :class="getTypeClass(bridge.type)">{{ bridge.type }}</span>
            <span class="bridge-dynasty">{{ bridge.dynasty }}</span>
          </div>
          
          <h3 class="bridge-name">{{ bridge.name }}</h3>
          
          <div class="bridge-alias" v-if="bridge.alias?.length">
            {{ bridge.alias.join(' · ') }}
          </div>
          
          <div class="bridge-location">
            <span>{{ bridge.location?.province }} · {{ bridge.location?.city }}</span>
          </div>
          
          <div class="bridge-dimensions" v-if="bridge.dimensions?.length">
            <span>长 {{ bridge.dimensions.length }}米</span>
            <span v-if="bridge.dimensions.width">宽 {{ bridge.dimensions.width }}米</span>
          </div>
          
          <p class="bridge-desc">{{ bridge.description?.slice(0, 55) }}...</p>
          
          <div class="bridge-features">
            <span 
              class="feature-tag"
              v-for="(feature, idx) in bridge.features?.slice(0, 2)"
              :key="idx"
            >{{ feature }}</span>
            <span class="feature-tag more" v-if="bridge.features?.length > 2">
              +{{ bridge.features.length - 2 }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div class="empty-state" v-if="filteredBridges.length === 0">
      <div class="empty-icon">🏯</div>
      <p>暂无匹配的桥梁数据</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { bridgeAPI } from '@/api'
import { isFavorite as checkFavorite, getFavorites, getFavoriteCount } from '@/utils/favorite'

const router = useRouter()
const route = useRoute()

const bridges = ref([])
const searchQuery = ref('')
const selectedType = ref('')
const selectedDynasty = ref('')
const selectedProvince = ref('')
const showFavoritesOnly = ref(false)
const favoriteCount = ref(0)

// 检查是否收藏
const isFavorite = (bridgeId) => {
  return checkFavorite(bridgeId)
}

// 获取所有省份列表
const provinceList = computed(() => {
  const provinces = new Set()
  bridges.value.forEach(b => {
    if (b.location?.province) {
      provinces.add(b.location.province)
    }
  })
  return Array.from(provinces).sort()
})

const filteredBridges = computed(() => {
  let result = bridges.value
  
  // 筛选收藏
  if (showFavoritesOnly.value) {
    const favorites = getFavorites()
    result = result.filter(b => favorites.includes(b.id))
  }
  
  // 筛选省份
  if (selectedProvince.value) {
    result = result.filter(b => b.location?.province === selectedProvince.value)
  }
  
  if (selectedType.value) {
    result = result.filter(b => b.type === selectedType.value)
  }
  
  if (selectedDynasty.value) {
    result = result.filter(b => b.dynasty?.includes(selectedDynasty.value))
  }
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(b => 
      b.name?.toLowerCase().includes(query) ||
      b.alias?.some(a => a.toLowerCase().includes(query)) ||
      b.description?.toLowerCase().includes(query)
    )
  }
  
  return result
})

const handleSearch = () => {}
const handleFilter = () => {}

// 清除省份筛选
const clearProvinceFilter = () => {
  selectedProvince.value = ''
  router.replace({ path: '/bridges' })
}

const goToDetail = (id) => {
  router.push(`/bridges/${id}`)
}

const getCardImageStyle = (bridge) => {
  const typeGradients = {
    '拱桥': 'linear-gradient(135deg, rgba(139, 35, 35, 0.15) 0%, rgba(201, 169, 98, 0.08) 100%)',
    '梁桥': 'linear-gradient(135deg, rgba(30, 58, 95, 0.15) 0%, rgba(201, 169, 98, 0.08) 100%)',
    '索桥': 'linear-gradient(135deg, rgba(46, 139, 87, 0.15) 0%, rgba(201, 169, 98, 0.08) 100%)',
    '浮桥': 'linear-gradient(135deg, rgba(201, 169, 98, 0.2) 0%, rgba(139, 119, 85, 0.1) 100%)'
  }
  
  return {
    background: typeGradients[bridge.type] || typeGradients['拱桥']
  }
}

const getTypeClass = (type) => {
  const classes = {
    '拱桥': 'type-arch',
    '梁桥': 'type-beam',
    '索桥': 'type-cable',
    '浮桥': 'type-pontoon'
  }
  return classes[type] || ''
}

onMounted(async () => {
  try {
    const res = await bridgeAPI.getList()
    if (res.success) {
      bridges.value = res.data
    }
    // 获取收藏数量
    favoriteCount.value = getFavoriteCount()
    
    // 读取URL中的省份参数
    const provinceParam = route.query.province
    if (provinceParam) {
      selectedProvince.value = provinceParam
    }
  } catch (error) {
    console.error('加载桥梁数据失败:', error)
  }
})

// 监听路由参数变化
watch(() => route.query.province, (newProvince) => {
  if (newProvince) {
    selectedProvince.value = newProvince
  } else {
    selectedProvince.value = ''
  }
})
</script>

<style scoped>
.bridge-gallery-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow: hidden;
  background: linear-gradient(135deg, #F5F0E6 0%, #EDE5D5 100%);
}

/* 省份筛选提示条 */
.province-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  background: linear-gradient(90deg, rgba(139, 35, 35, 0.08), rgba(201, 169, 98, 0.08));
  border: 1px solid rgba(139, 35, 35, 0.15);
  border-radius: 6px;
  border-left: 3px solid #8B2323;
}

.banner-text {
  font-size: 13px;
  color: #4A4A4A;
}

.banner-text strong {
  color: #8B2323;
  font-size: 14px;
}

.clear-btn {
  color: #8B2323;
  font-size: 12px;
}

/* 筛选区 */
.filter-section {
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.12);
  border-radius: 6px;
  padding: 14px 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.search-input {
  width: 200px;
}

.province-select {
  width: 130px;
}

.search-input :deep(.el-input__wrapper) {
  background: rgba(232, 224, 208, 0.6);
  border: 1px solid rgba(139, 35, 35, 0.15);
  box-shadow: none;
}

.search-input :deep(.el-input__wrapper:hover) {
  border-color: #C9A962;
}

.stats-info {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 4px;
}

.stats-label {
  font-size: 13px;
  color: #7A7A7A;
}

.stats-number {
  font-size: 20px;
  font-weight: 600;
  color: #8B2323;
  font-family: 'Noto Serif SC', serif;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-label {
  font-size: 13px;
  color: #4A4A4A;
  font-family: 'Noto Serif SC', serif;
}

.favorite-filter-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 16px;
  font-size: 12px;
  transition: all 0.3s;
}

.favorite-filter-btn:hover {
  transform: scale(1.05);
}

.filter-tabs {
  display: flex;
  gap: 2px;
  background: rgba(232, 224, 208, 0.6);
  border-radius: 4px;
  padding: 3px;
}

.filter-tab {
  padding: 6px 14px;
  font-size: 12px;
  color: #4A4A4A;
  cursor: pointer;
  border-radius: 3px;
  transition: all 0.2s;
}

.filter-tab:hover {
  background: rgba(139, 35, 35, 0.08);
}

.filter-tab.active {
  background: #8B2323;
  color: #F5F0E6;
}

/* 桥梁网格 */
.bridge-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 18px;
  overflow-y: auto;
  padding-right: 5px;
}

.bridge-item {
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.12);
  border-radius: 6px;
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.bridge-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  border-color: #C9A962;
}

/* 装饰角 */
.card-corner {
  position: absolute;
  width: 12px;
  height: 12px;
  border-color: #C9A962;
  border-style: solid;
  opacity: 0.4;
  z-index: 1;
}
.corner-tl { top: 4px; left: 4px; border-width: 1px 0 0 1px; }
.corner-tr { top: 4px; right: 4px; border-width: 1px 1px 0 0; }
.corner-bl { bottom: 4px; left: 4px; border-width: 0 0 1px 1px; }
.corner-br { bottom: 4px; right: 4px; border-width: 0 1px 1px 0; }

/* 图片区域 */
.bridge-image {
  height: 140px;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bridge-image::before {
  content: '🏯';
  font-size: 40px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(26, 26, 26, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.bridge-item:hover .image-overlay {
  opacity: 1;
}

.view-btn {
  padding: 8px 18px;
  background: #C9A962;
  color: #1A1A1A;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
}

.image-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 24px;
  height: 24px;
  background: #8B2323;
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #F5F0E6;
  font-size: 11px;
  font-weight: bold;
}

.image-badge.heritage {
  right: 8px;
}

.image-badge.favorite {
  right: 40px;
  background: transparent;
  font-size: 14px;
  width: auto;
  height: auto;
}

/* 内容区域 */
.bridge-content {
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.bridge-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.bridge-type {
  padding: 3px 10px;
  border-radius: 2px;
  font-size: 11px;
  font-weight: 500;
}

.bridge-type.type-arch {
  background: rgba(139, 35, 35, 0.12);
  color: #8B2323;
}

.bridge-type.type-beam {
  background: rgba(30, 58, 95, 0.12);
  color: #1E3A5F;
}

.bridge-type.type-cable {
  background: rgba(46, 139, 87, 0.12);
  color: #2E8B57;
}

.bridge-type.type-pontoon {
  background: rgba(201, 169, 98, 0.2);
  color: #8B7355;
}

.bridge-dynasty {
  font-size: 11px;
  color: #7A7A7A;
}

.bridge-name {
  font-size: 17px;
  color: #2A2A2A;
  margin: 0;
  font-weight: 600;
  font-family: 'Noto Serif SC', serif;
}

.bridge-alias {
  font-size: 11px;
  color: #7A7A7A;
}

.bridge-location {
  font-size: 12px;
  color: #4A4A4A;
}

.bridge-location::before {
  content: '📍 ';
}

.bridge-dimensions {
  display: flex;
  gap: 12px;
  font-size: 11px;
  color: #7A7A7A;
}

.bridge-desc {
  font-size: 12px;
  color: #4A4A4A;
  line-height: 1.6;
  margin: 0;
  flex: 1;
}

.bridge-features {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: auto;
}

.feature-tag {
  padding: 2px 8px;
  background: rgba(201, 169, 98, 0.15);
  border: 1px solid rgba(201, 169, 98, 0.3);
  border-radius: 2px;
  font-size: 10px;
  color: #8B7355;
}

.feature-tag.more {
  background: rgba(139, 35, 35, 0.08);
  border-color: rgba(139, 35, 35, 0.2);
  color: #8B2323;
}

/* 空状态 */
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #7A7A7A;
  gap: 10px;
}

.empty-icon {
  font-size: 48px;
  opacity: 0.5;
}

/* Element Plus 样式覆盖 */
.el-select :deep(.el-input__wrapper) {
  background: rgba(232, 224, 208, 0.6);
  border: 1px solid rgba(139, 35, 35, 0.15);
  box-shadow: none;
}

/* 响应式 */
@media (max-width: 768px) {
  .filter-row {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .stats-info {
    margin-left: 0;
  }
  
  .bridge-grid {
    grid-template-columns: 1fr;
  }
}
</style>