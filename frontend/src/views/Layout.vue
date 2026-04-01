<template>
  <div class="layout-container">
    <!-- 水墨背景装饰 -->
    <div class="ink-decoration">
      <div class="ink-blob ink-blob-1"></div>
      <div class="ink-blob ink-blob-2"></div>
      <div class="ink-blob ink-blob-3"></div>
    </div>

    <!-- 顶部导航 -->
    <header class="layout-header">
      <div class="header-left">
        <div class="logo">
          <span class="logo-icon">🏛️</span>
          <span class="logo-text">桥见千年</span>
        </div>
        <div class="subtitle">中国古代桥梁智慧可视化平台</div>
      </div>
      
      <nav class="header-nav">
        <el-menu
          mode="horizontal"
          :default-active="activeMenu"
          :ellipsis="false"
          router
        >
          <el-menu-item index="/dashboard">
            <el-icon><HomeFilled /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="/bridges">
            <el-icon><PictureFilled /></el-icon>
            <span>桥梁博览</span>
          </el-menu-item>
          <el-menu-item index="/timeline">
            <el-icon><Clock /></el-icon>
            <span>时间轴</span>
          </el-menu-item>
          <el-menu-item index="/ai-qa">
            <el-icon><ChatDotRound /></el-icon>
            <span>AI问答</span>
          </el-menu-item>
          <el-menu-item index="/structure">
            <el-icon><DataAnalysis /></el-icon>
            <span>结构剖析</span>
          </el-menu-item>
          <el-menu-item index="/craftsmen">
            <el-icon><User /></el-icon>
            <span>匠心人物</span>
          </el-menu-item>
          <el-menu-item index="/builder">
            <el-icon><Box /></el-icon>
            <span>建造坊</span>
          </el-menu-item>
          <el-menu-item index="/compare">
            <el-icon><DocumentChecked /></el-icon>
            <span>桥梁对比</span>
          </el-menu-item>
          <el-menu-item index="/quiz">
            <el-icon><Trophy /></el-icon>
            <span>知识挑战</span>
          </el-menu-item>
          <el-menu-item index="/statistics">
            <el-icon><TrendCharts /></el-icon>
            <span>数据统计</span>
          </el-menu-item>
          <el-menu-item index="/about">
            <el-icon><InfoFilled /></el-icon>
            <span>关于</span>
          </el-menu-item>
        </el-menu>
      </nav>
      
      <div class="header-right">
        <div class="seal-outline">传承千年智慧</div>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="layout-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- 底部信息 -->
    <footer class="layout-footer">
      <div class="footer-decoration"></div>
      <span class="footer-text">© 2026 【桥见千年】团队 | AI创意主题大赛参赛作品</span>
      <div class="footer-decoration"></div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style scoped>
.layout-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
  background: linear-gradient(135deg, #F5F0E6 0%, #EDE5D5 50%, #E8E0D0 100%);
}

/* 水墨装饰 */
.ink-decoration {
  position: fixed;
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
  filter: blur(60px);
  opacity: 0.04;
}

.ink-blob-1 {
  width: 400px;
  height: 400px;
  background: #1A1A1A;
  top: -100px;
  right: 10%;
}

.ink-blob-2 {
  width: 300px;
  height: 300px;
  background: #8B2323;
  bottom: 20%;
  left: 5%;
}

.ink-blob-3 {
  width: 250px;
  height: 250px;
  background: #C9A962;
  top: 40%;
  right: 5%;
}

/* 顶部导航 */
.layout-header {
  height: 70px;
  background: rgba(245, 240, 230, 0.95);
  border-bottom: 1px solid rgba(139, 35, 35, 0.2);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
  position: relative;
  z-index: 100;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

/* 顶部装饰边 */
.layout-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    #C9A962 20%, 
    #8B2323 50%, 
    #C9A962 80%, 
    transparent 100%
  );
}

.header-left {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  font-size: 28px;
}

.logo-text {
  font-size: 24px;
  font-weight: 600;
  letter-spacing: 4px;
  color: #2A2A2A;
  font-family: 'Noto Serif SC', 'Source Han Serif SC', serif;
}

.subtitle {
  font-size: 11px;
  color: #7A7A7A;
  letter-spacing: 2px;
  margin-top: 2px;
}

.header-nav {
  flex: 1;
  display: flex;
  justify-content: center;
}

.header-nav .el-menu {
  background: transparent !important;
  border: none;
  height: 70px;
}

.header-nav .el-menu-item {
  height: 70px;
  line-height: 70px;
  font-size: 14px;
  padding: 0 18px;
  color: #4A4A4A !important;
  font-family: 'Noto Serif SC', serif;
  letter-spacing: 1px;
}

.header-nav .el-menu-item:hover {
  color: #8B2323 !important;
  background: rgba(139, 35, 35, 0.06) !important;
}

.header-nav .el-menu-item.is-active {
  color: #8B2323 !important;
  background: rgba(139, 35, 35, 0.1) !important;
  border-bottom: 3px solid #8B2323;
}

.header-right {
  display: flex;
  align-items: center;
}

.header-right .seal-outline {
  font-size: 11px;
  padding: 4px 10px;
  border-color: #8B2323;
  color: #8B2323;
}

/* 主内容区 */
.layout-main {
  flex: 1;
  overflow: hidden;
  padding: 20px;
  position: relative;
  z-index: 1;
}

/* 底部 */
.layout-footer {
  height: 36px;
  background: rgba(245, 240, 230, 0.9);
  border-top: 1px solid rgba(139, 35, 35, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  position: relative;
  z-index: 100;
}

.footer-decoration {
  width: 60px;
  height: 1px;
  background: linear-gradient(90deg, transparent, #C9A962, transparent);
}

.footer-text {
  font-size: 12px;
  color: #7A7A7A;
  letter-spacing: 1px;
}

/* 页面过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式 */
@media (max-width: 1400px) {
  .header-nav .el-menu-item {
    padding: 0 12px;
    font-size: 13px;
  }
  
  .header-nav .el-menu-item span {
    display: none;
  }
}

@media (max-width: 768px) {
  .layout-header {
    padding: 0 15px;
  }
  
  .header-left .subtitle {
    display: none;
  }
  
  .logo-text {
    font-size: 20px;
    letter-spacing: 2px;
  }
  
  .header-right {
    display: none;
  }
}
</style>
