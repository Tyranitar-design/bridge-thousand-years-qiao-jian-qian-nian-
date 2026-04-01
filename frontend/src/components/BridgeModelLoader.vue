<template>
  <div class="model-loader-container" ref="containerRef">
    <!-- 3D 画布 -->
    <canvas ref="canvasRef" class="model-canvas"></canvas>
    
    <!-- 控制面板 -->
    <div class="control-panel">
      <div class="control-header">
        <span class="header-seal">3D</span>
        <span class="header-title">模型展示</span>
      </div>
      
      <div class="bridge-selector" v-if="availableBridges.length > 1">
        <span class="selector-label">选择桥梁</span>
        <el-select v-model="currentBridgeId" size="small" @change="loadBridgeModel">
          <el-option 
            v-for="bridge in availableBridges" 
            :key="bridge.id"
            :label="bridge.name"
            :value="bridge.id"
          />
        </el-select>
      </div>
      
      <div class="control-section">
        <el-checkbox v-model="autoRotate" @change="toggleAutoRotate">自动旋转</el-checkbox>
      </div>
      
      <div class="control-section">
        <el-checkbox v-model="showWireframe" @change="toggleWireframe">显示线框</el-checkbox>
      </div>
      
      <div class="control-section">
        <span class="section-label">缩放</span>
        <el-slider 
          v-model="scaleValue" 
          :min="50" 
          :max="200"
          :format-tooltip="(val) => val + '%'"
          @input="updateScale"
        />
      </div>
    </div>
    
    <!-- 加载状态 -->
    <div class="loading-overlay" v-if="loading">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <span class="loading-text">加载 3D 模型中...</span>
        <span class="loading-hint">{{ currentBridge?.name || '' }}</span>
      </div>
    </div>
    
    <!-- 错误提示 -->
    <div class="error-overlay" v-if="error">
      <div class="error-content">
        <span class="error-icon">⚠️</span>
        <span class="error-text">{{ error }}</span>
        <el-button size="small" @click="retryLoad">重试</el-button>
      </div>
    </div>
    
    <!-- 模型信息 -->
    <div class="info-panel" v-if="currentBridge && !loading && !error">
      <div class="bridge-name">{{ currentBridge.name }}</div>
      <div class="bridge-desc">{{ currentBridge.description }}</div>
    </div>
    
    <!-- 操作提示 -->
    <div class="hint-panel" v-if="!loading && !error">
      <span>🖱️ 拖拽旋转 | 滚轮缩放 | 右键平移</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader'

const props = defineProps({
  bridgeId: {
    type: String,
    default: 'zhaozhou-bridge'
  }
})

// 可用的桥梁模型
const availableBridges = [
  {
    id: 'zhaozhou-bridge',
    name: '赵州桥',
    file: '/models/赵州桥.glb',
    description: '隋代敞肩石拱桥，世界上现存最早、跨度最大的单孔坦弧敞肩石拱桥'
  },
  {
    id: 'luding-bridge',
    name: '泸定桥',
    file: '/models/泸定桥.glb',
    description: '清代铁索桥，13根铁链横跨大渡河，红军长征"飞夺泸定桥"的发生地'
  },
  {
    id: 'lugou-bridge',
    name: '卢沟桥',
    file: '/models/卢沟桥.glb',
    description: '金代十一孔石拱桥，桥身有数百只石狮子，抗日战争爆发地'
  }
]

// Refs
const containerRef = ref(null)
const canvasRef = ref(null)
const loading = ref(true)
const error = ref(null)

// Three.js 对象
let scene, camera, renderer, controls
let currentModel = null
let animationId = null

// 控制状态
const currentBridgeId = ref(props.bridgeId)
const autoRotate = ref(true)
const showWireframe = ref(false)
const scaleValue = ref(100)

// 当前桥梁信息
const currentBridge = computed(() => {
  return availableBridges.find(b => b.id === currentBridgeId.value)
})

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
  camera.position.set(5, 3, 5)
  
  // 渲染器
  renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true,
    alpha: true
  })
  renderer.setSize(container.clientWidth, container.clientHeight)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.shadowMap.enabled = true
  renderer.outputColorSpace = THREE.SRGBColorSpace
  
  // 控制器
  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true
  controls.dampingFactor = 0.05
  controls.autoRotate = autoRotate.value
  controls.autoRotateSpeed = 0.5
  controls.minDistance = 1
  controls.maxDistance = 20
  
  // 灯光
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
  scene.add(ambientLight)
  
  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
  directionalLight.position.set(10, 20, 10)
  directionalLight.castShadow = true
  scene.add(directionalLight)
  
  const directionalLight2 = new THREE.DirectionalLight(0xffffff, 0.4)
  directionalLight2.position.set(-10, 10, -10)
  scene.add(directionalLight2)
  
  // 添加网格辅助
  const gridHelper = new THREE.GridHelper(10, 20, 0xC9A962, 0xE8E0D0)
  gridHelper.position.y = -2
  scene.add(gridHelper)
  
  // 加载模型
  loadBridgeModel()
  
  // 开始动画循环
  animate()
}

// 加载桥梁模型
const loadBridgeModel = async () => {
  if (!scene) return
  
  loading.value = true
  error.value = null
  
  // 清除之前的模型
  if (currentModel) {
    scene.remove(currentModel)
    // 释放资源
    currentModel.traverse((child) => {
      if (child.geometry) {
        child.geometry.dispose()
      }
      if (child.material) {
        if (Array.isArray(child.material)) {
          child.material.forEach(mat => mat.dispose())
        } else {
          child.material.dispose()
        }
      }
    })
    currentModel = null
  }
  
  const bridge = currentBridge.value
  if (!bridge) {
    error.value = '未找到桥梁模型'
    loading.value = false
    return
  }
  
  // 创建加载器
  const loader = new GLTFLoader()
  
  // 可选：使用 Draco 压缩解码器（如果模型使用了 Draco 压缩）
  // const dracoLoader = new DRACOLoader()
  // dracoLoader.setDecoderPath('/draco/')
  // loader.setDRACOLoader(dracoLoader)
  
  try {
    const gltf = await new Promise((resolve, reject) => {
      loader.load(
        bridge.file,
        (gltf) => resolve(gltf),
        (progress) => {
          // 加载进度
          if (progress.total > 0) {
            const percent = Math.round((progress.loaded / progress.total) * 100)
            console.log(`加载进度: ${percent}%`)
          }
        },
        (error) => {
          console.error('模型加载错误:', error)
          reject(error)
        }
      )
    })
    
    currentModel = gltf.scene
    
    // 计算模型边界盒并调整大小
    const box = new THREE.Box3().setFromObject(currentModel)
    const size = box.getSize(new THREE.Vector3())
    const center = box.getCenter(new THREE.Vector3())
    
    // 计算缩放比例，让模型适应场景
    const maxDim = Math.max(size.x, size.y, size.z)
    const scale = 3 / maxDim
    currentModel.scale.setScalar(scale)
    
    // 居中模型
    currentModel.position.sub(center.multiplyScalar(scale))
    currentModel.position.y = -box.min.y * scale - 2
    
    // 启用阴影
    currentModel.traverse((child) => {
      if (child.isMesh) {
        child.castShadow = true
        child.receiveShadow = true
      }
    })
    
    scene.add(currentModel)
    
    // 重置相机位置
    camera.position.set(5, 3, 5)
    controls.target.set(0, 0, 0)
    controls.update()
    
    loading.value = false
    
  } catch (err) {
    console.error('加载模型失败:', err)
    error.value = `加载模型失败: ${bridge.name}`
    loading.value = false
  }
}

// 切换自动旋转
const toggleAutoRotate = (value) => {
  if (controls) {
    controls.autoRotate = value
  }
}

// 切换线框模式
const toggleWireframe = (value) => {
  if (!currentModel) return
  
  currentModel.traverse((child) => {
    if (child.isMesh && child.material) {
      if (Array.isArray(child.material)) {
        child.material.forEach(mat => {
          mat.wireframe = value
        })
      } else {
        child.material.wireframe = value
      }
    }
  })
}

// 更新缩放
const updateScale = (value) => {
  if (!currentModel) return
  
  const scale = value / 100
  currentModel.scale.setScalar(scale * 0.03) // 基础缩放
}

// 重试加载
const retryLoad = () => {
  loadBridgeModel()
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

// 监听 bridgeId 变化
watch(() => props.bridgeId, (newId) => {
  currentBridgeId.value = newId
})

watch(currentBridgeId, () => {
  if (scene) {
    loadBridgeModel()
  }
})

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
  
  // 清理资源
  if (currentModel) {
    currentModel.traverse((child) => {
      if (child.geometry) {
        child.geometry.dispose()
      }
      if (child.material) {
        if (Array.isArray(child.material)) {
          child.material.forEach(mat => mat.dispose())
        } else {
          child.material.dispose()
        }
      }
    })
  }
  
  if (renderer) {
    renderer.dispose()
  }
})
</script>

<style scoped>
.model-loader-container {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 400px;
  background: linear-gradient(135deg, #F5F0E6 0%, #EDE5D5 100%);
  border-radius: 6px;
  overflow: hidden;
}

.model-canvas {
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

.bridge-selector {
  margin-bottom: 12px;
}

.selector-label {
  display: block;
  font-size: 12px;
  color: #7A7A7A;
  margin-bottom: 6px;
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

.bridge-name {
  font-size: 16px;
  font-weight: 600;
  color: #8B2323;
  margin-bottom: 4px;
}

.bridge-desc {
  font-size: 13px;
  color: #4A4A4A;
  line-height: 1.6;
}

/* 操作提示 */
.hint-panel {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(245, 240, 230, 0.9);
  border: 1px solid rgba(139, 35, 35, 0.15);
  border-radius: 4px;
  padding: 8px 12px;
  font-size: 12px;
  color: #7A7A7A;
}

/* 加载状态 */
.loading-overlay {
  position: absolute;
  inset: 0;
  background: rgba(245, 240, 230, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(139, 35, 35, 0.2);
  border-top-color: #8B2323;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  font-size: 14px;
  color: #4A4A4A;
}

.loading-hint {
  font-size: 12px;
  color: #8B2323;
}

/* 错误提示 */
.error-overlay {
  position: absolute;
  inset: 0;
  background: rgba(245, 240, 230, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.error-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.error-icon {
  font-size: 48px;
}

.error-text {
  font-size: 14px;
  color: #8B2323;
}

/* 响应式 */
@media (max-width: 768px) {
  .control-panel {
    top: 8px;
    left: 8px;
    padding: 10px;
    min-width: 150px;
  }
  
  .info-panel {
    bottom: 8px;
    left: 8px;
    right: 8px;
    padding: 10px;
  }
  
  .hint-panel {
    display: none;
  }
}
</style>