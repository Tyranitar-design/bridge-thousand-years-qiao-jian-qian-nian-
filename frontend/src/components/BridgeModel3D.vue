<template>
  <div class="bridge-3d-container" ref="containerRef">
    <!-- 3D 画布 -->
    <canvas ref="canvasRef" class="bridge-canvas"></canvas>
    
    <!-- 控制面板 -->
    <div class="control-panel">
      <div class="control-header">
        <span class="header-seal">3D</span>
        <span class="header-title">结构剖析</span>
      </div>
      
      <div class="control-buttons">
        <el-button 
          v-for="view in viewOptions" 
          :key="view.id"
          :type="currentView === view.id ? 'primary' : 'default'"
          size="small"
          @click="changeView(view.id)"
        >
          {{ view.label }}
        </el-button>
      </div>
      
      <div class="control-section">
        <span class="section-label">结构拆解</span>
        <el-slider 
          v-model="explodeAmount" 
          :min="0" 
          :max="100"
          :format-tooltip="(val) => val + '%'"
          @input="updateExplode"
        />
      </div>
      
      <div class="control-section checkboxes">
        <el-checkbox v-model="autoRotate" @change="toggleAutoRotate">自动旋转</el-checkbox>
        <el-checkbox v-model="showLabels" @change="toggleLabels">显示标注</el-checkbox>
      </div>
    </div>
    
    <!-- 信息面板 -->
    <div class="info-panel" v-if="currentPart">
      <div class="part-name">{{ currentPart.name }}</div>
      <div class="part-desc">{{ currentPart.description }}</div>
    </div>
    
    <!-- 图例 -->
    <div class="legend-panel">
      <div class="legend-item" v-for="item in legendItems" :key="item.name">
        <span class="legend-color" :style="{ background: item.color }"></span>
        <span class="legend-name">{{ item.name }}</span>
      </div>
    </div>
    
    <!-- 加载状态 -->
    <div class="loading-overlay" v-if="loading">
      <div class="loading-spinner"></div>
      <span>加载3D模型中...</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

const props = defineProps({
  bridgeId: {
    type: String,
    default: 'zhaozhou-bridge'
  }
})

// Refs
const containerRef = ref(null)
const canvasRef = ref(null)
const loading = ref(true)

// Three.js 对象
let scene, camera, renderer, controls
let bridgeGroup, archGroup, pierGroup, deckGroup
let labels = []
let animationId = null

// 控制状态
const currentView = ref('overview')
const explodeAmount = ref(0)
const autoRotate = ref(true)
const showLabels = ref(true)
const currentPart = ref(null)

// 视角选项
const viewOptions = [
  { id: 'overview', label: '全景' },
  { id: 'front', label: '正面' },
  { id: 'side', label: '侧面' },
  { id: 'top', label: '俯视' }
]

// 图例
const legendItems = [
  { name: '主拱', color: '#8B2323' },
  { name: '敞肩小拱', color: '#C9A962' },
  { name: '桥墩', color: '#4A4A4A' },
  { name: '桥面', color: '#2E8B57' }
]

// 结构部件信息
const partInfo = {
  mainArch: {
    name: '主拱',
    description: '赵州桥的主拱跨径37.02米，是世界上现存最早、跨度最大的单孔坦弧敞肩石拱桥。'
  },
  smallArch: {
    name: '敞肩小拱',
    description: '大拱两肩各设两个小拱，既减轻桥身自重约700吨，又增大泄洪面积。这是敞肩拱技术的核心创新。'
  },
  pier: {
    name: '桥墩',
    description: '桥墩采用浅基础设计，建在河床冲积层上，体现了古代工匠对地质条件的深刻理解。'
  },
  deck: {
    name: '桥面',
    description: '桥面宽9.6米，两侧设有石栏杆，既实用又美观。'
  }
}

// 初始化 Three.js
const initThree = () => {
  if (!containerRef.value || !canvasRef.value) return
  
  const container = containerRef.value
  const canvas = canvasRef.value
  
  // 场景
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0xF5F0E6)
  
  // 相机
  camera = new THREE.PerspectiveCamera(
    45,
    container.clientWidth / container.clientHeight,
    0.1,
    1000
  )
  camera.position.set(30, 20, 30)
  
  // 渲染器
  renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true,
    alpha: true
  })
  renderer.setSize(container.clientWidth, container.clientHeight)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.shadowMap.enabled = true
  
  // 控制器
  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true
  controls.dampingFactor = 0.05
  controls.autoRotate = autoRotate.value
  controls.autoRotateSpeed = 0.5
  
  // 灯光
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
  scene.add(ambientLight)
  
  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
  directionalLight.position.set(20, 30, 20)
  directionalLight.castShadow = true
  scene.add(directionalLight)
  
  // 创建桥梁模型
  createBridge()
  
  // 添加网格辅助
  const gridHelper = new THREE.GridHelper(40, 20, 0xC9A962, 0xE8E0D0)
  gridHelper.position.y = -5
  scene.add(gridHelper)
  
  loading.value = false
  
  // 开始动画循环
  animate()
}

// 创建桥梁模型
const createBridge = () => {
  bridgeGroup = new THREE.Group()
  archGroup = new THREE.Group()
  pierGroup = new THREE.Group()
  deckGroup = new THREE.Group()
  
  // 材质
  const archMaterial = new THREE.MeshStandardMaterial({
    color: 0x8B2323,
    roughness: 0.8,
    metalness: 0.1
  })
  
  const smallArchMaterial = new THREE.MeshStandardMaterial({
    color: 0xC9A962,
    roughness: 0.7,
    metalness: 0.1
  })
  
  const pierMaterial = new THREE.MeshStandardMaterial({
    color: 0x4A4A4A,
    roughness: 0.9,
    metalness: 0
  })
  
  const deckMaterial = new THREE.MeshStandardMaterial({
    color: 0x2E8B57,
    roughness: 0.6,
    metalness: 0.1
  })
  
  // 主拱（使用 TorusGeometry 创建弧形）
  const mainArchGeometry = new THREE.TorusGeometry(10, 1.2, 16, 64, Math.PI)
  const mainArch = new THREE.Mesh(mainArchGeometry, archMaterial)
  mainArch.rotation.x = Math.PI / 2
  mainArch.rotation.z = Math.PI
  mainArch.position.y = 3
  mainArch.userData = { type: 'mainArch' }
  archGroup.add(mainArch)
  
  // 敞肩小拱（四个）
  const smallArchGeometry = new THREE.TorusGeometry(2, 0.4, 12, 32, Math.PI)
  
  // 左侧小拱
  const smallArch1 = new THREE.Mesh(smallArchGeometry, smallArchMaterial)
  smallArch1.rotation.x = Math.PI / 2
  smallArch1.rotation.z = Math.PI
  smallArch1.position.set(-5, 6, 0)
  smallArch1.userData = { type: 'smallArch' }
  archGroup.add(smallArch1)
  
  const smallArch2 = new THREE.Mesh(smallArchGeometry, smallArchMaterial)
  smallArch2.rotation.x = Math.PI / 2
  smallArch2.rotation.z = Math.PI
  smallArch2.position.set(-8, 4, 0)
  smallArch2.userData = { type: 'smallArch' }
  archGroup.add(smallArch2)
  
  // 右侧小拱
  const smallArch3 = new THREE.Mesh(smallArchGeometry, smallArchMaterial)
  smallArch3.rotation.x = Math.PI / 2
  smallArch3.rotation.z = Math.PI
  smallArch3.position.set(5, 6, 0)
  smallArch3.userData = { type: 'smallArch' }
  archGroup.add(smallArch3)
  
  const smallArch4 = new THREE.Mesh(smallArchGeometry, smallArchMaterial)
  smallArch4.rotation.x = Math.PI / 2
  smallArch4.rotation.z = Math.PI
  smallArch4.position.set(8, 4, 0)
  smallArch4.userData = { type: 'smallArch' }
  archGroup.add(smallArch4)
  
  // 桥墩
  const pierGeometry = new THREE.BoxGeometry(3, 4, 4)
  
  const leftPier = new THREE.Mesh(pierGeometry, pierMaterial)
  leftPier.position.set(-12, 0, 0)
  leftPier.userData = { type: 'pier' }
  pierGroup.add(leftPier)
  
  const rightPier = new THREE.Mesh(pierGeometry, pierMaterial)
  rightPier.position.set(12, 0, 0)
  rightPier.userData = { type: 'pier' }
  pierGroup.add(rightPier)
  
  // 桥面
  const deckGeometry = new THREE.BoxGeometry(28, 0.8, 5)
  const deck = new THREE.Mesh(deckGeometry, deckMaterial)
  deck.position.y = 13
  deck.userData = { type: 'deck' }
  deckGroup.add(deck)
  
  // 栏杆
  const railingMaterial = new THREE.MeshStandardMaterial({
    color: 0x8B2323,
    roughness: 0.7
  })
  
  // 左侧栏杆
  const leftRailing = new THREE.Mesh(
    new THREE.BoxGeometry(26, 1, 0.3),
    railingMaterial
  )
  leftRailing.position.set(0, 14, 2.5)
  deckGroup.add(leftRailing)
  
  // 右侧栏杆
  const rightRailing = new THREE.Mesh(
    new THREE.BoxGeometry(26, 1, 0.3),
    railingMaterial
  )
  rightRailing.position.set(0, 14, -2.5)
  deckGroup.add(rightRailing)
  
  // 添加到主组
  bridgeGroup.add(archGroup)
  bridgeGroup.add(pierGroup)
  bridgeGroup.add(deckGroup)
  
  // 居中显示
  bridgeGroup.position.y = -2
  
  scene.add(bridgeGroup)
  
  // 创建标注
  createLabels()
}

// 创建标注
const createLabels = () => {
  const labelPositions = [
    { pos: [0, 5, 0], text: '主拱', type: 'mainArch' },
    { pos: [-5, 8, 0], text: '敞肩小拱', type: 'smallArch' },
    { pos: [-12, 2, 0], text: '桥墩', type: 'pier' },
    { pos: [0, 14, 0], text: '桥面', type: 'deck' }
  ]
  
  labelPositions.forEach(item => {
    const sprite = createTextSprite(item.text)
    sprite.position.set(...item.pos)
    sprite.userData = { type: item.type, isLabel: true }
    scene.add(sprite)
    labels.push(sprite)
  })
}

// 创建文字精灵
const createTextSprite = (text) => {
  const canvas = document.createElement('canvas')
  const context = canvas.getContext('2d')
  canvas.width = 256
  canvas.height = 64
  
  context.fillStyle = 'rgba(139, 35, 35, 0.9)'
  context.fillRect(0, 0, canvas.width, canvas.height)
  
  context.font = 'bold 28px serif'
  context.fillStyle = '#F5F0E6'
  context.textAlign = 'center'
  context.textBaseline = 'middle'
  context.fillText(text, canvas.width / 2, canvas.height / 2)
  
  const texture = new THREE.CanvasTexture(canvas)
  const spriteMaterial = new THREE.SpriteMaterial({ map: texture })
  const sprite = new THREE.Sprite(spriteMaterial)
  sprite.scale.set(6, 1.5, 1)
  
  return sprite
}

// 更新拆解动画
const updateExplode = (value) => {
  if (!bridgeGroup) return
  
  const explode = value / 100
  
  // 拱向上
  archGroup.position.y = explode * 8
  
  // 桥面向上
  deckGroup.position.y = explode * 12
  
  // 桥墩向下
  pierGroup.position.y = -explode * 4
}

// 切换视角
const changeView = (viewId) => {
  currentView.value = viewId
  
  const positions = {
    overview: { x: 30, y: 20, z: 30 },
    front: { x: 0, y: 10, z: 35 },
    side: { x: 35, y: 10, z: 0 },
    top: { x: 0, y: 40, z: 0.1 }
  }
  
  const pos = positions[viewId]
  if (pos) {
    animateCamera(pos)
  }
}

// 相机动画
const animateCamera = (targetPos) => {
  const startPos = { x: camera.position.x, y: camera.position.y, z: camera.position.z }
  const duration = 1000
  const startTime = Date.now()
  
  const animateFrame = () => {
    const elapsed = Date.now() - startTime
    const progress = Math.min(elapsed / duration, 1)
    
    // 缓动函数
    const easeProgress = 1 - Math.pow(1 - progress, 3)
    
    camera.position.x = startPos.x + (targetPos.x - startPos.x) * easeProgress
    camera.position.y = startPos.y + (targetPos.y - startPos.y) * easeProgress
    camera.position.z = startPos.z + (targetPos.z - startPos.z) * easeProgress
    
    if (progress < 1) {
      requestAnimationFrame(animateFrame)
    }
  }
  
  animateFrame()
}

// 切换自动旋转
const toggleAutoRotate = (value) => {
  if (controls) {
    controls.autoRotate = value
  }
}

// 切换标注显示
const toggleLabels = (value) => {
  labels.forEach(label => {
    label.visible = value
  })
}

// 动画循环
const animate = () => {
  animationId = requestAnimationFrame(animate)
  
  if (controls) {
    controls.update()
  }
  
  if (renderer && scene && camera) {
    renderer.render(scene, camera)
  }
}

// 窗口大小变化
const handleResize = () => {
  if (!containerRef.value || !camera || !renderer) return
  
  const container = containerRef.value
  camera.aspect = container.clientWidth / container.clientHeight
  camera.updateProjectionMatrix()
  renderer.setSize(container.clientWidth, container.clientHeight)
}

// 生命周期
onMounted(() => {
  initThree()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  window.removeEventListener('resize', handleResize)
  if (renderer) {
    renderer.dispose()
  }
})
</script>

<style scoped>
.bridge-3d-container {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 400px;
  background: linear-gradient(135deg, #F5F0E6 0%, #EDE5D5 100%);
  border-radius: 6px;
  overflow: hidden;
}

.bridge-canvas {
  display: block;
  width: 100%;
  height: 100%;
}

/* 控制面板 */
.control-panel {
  position: absolute;
  top: 16px;
  left: 16px;
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.15);
  border-radius: 6px;
  padding: 14px;
  min-width: 180px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.control-header {
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

.header-title {
  font-size: 14px;
  font-weight: 600;
  color: #2A2A2A;
  font-family: 'Noto Serif SC', serif;
}

.control-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 12px;
}

.control-buttons :deep(.el-button) {
  background: rgba(232, 224, 208, 0.8);
  border-color: rgba(139, 35, 35, 0.15);
  color: #4A4A4A;
}

.control-buttons :deep(.el-button--primary) {
  background: #8B2323;
  border-color: #8B2323;
  color: #F5F0E6;
}

.control-section {
  margin-bottom: 12px;
}

.section-label {
  display: block;
  font-size: 12px;
  color: #7A7A7A;
  margin-bottom: 6px;
}

.checkboxes {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* 信息面板 */
.info-panel {
  position: absolute;
  bottom: 16px;
  left: 16px;
  right: 16px;
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.15);
  border-radius: 6px;
  padding: 12px 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.part-name {
  font-size: 14px;
  font-weight: 600;
  color: #8B2323;
  margin-bottom: 4px;
}

.part-desc {
  font-size: 12px;
  color: #4A4A4A;
  line-height: 1.6;
}

/* 图例 */
.legend-panel {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.15);
  border-radius: 6px;
  padding: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.legend-item:last-child {
  margin-bottom: 0;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 3px;
}

.legend-name {
  font-size: 12px;
  color: #4A4A4A;
}

/* 加载状态 */
.loading-overlay {
  position: absolute;
  inset: 0;
  background: rgba(245, 240, 230, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  z-index: 100;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(139, 35, 35, 0.2);
  border-top-color: #8B2323;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-overlay span {
  font-size: 13px;
  color: #7A7A7A;
}

/* 响应式 */
@media (max-width: 768px) {
  .control-panel {
    top: 8px;
    left: 8px;
    padding: 10px;
    min-width: 150px;
  }
  
  .legend-panel {
    top: 8px;
    right: 8px;
    padding: 8px;
  }
  
  .info-panel {
    bottom: 8px;
    left: 8px;
    right: 8px;
    padding: 10px;
  }
}
</style>