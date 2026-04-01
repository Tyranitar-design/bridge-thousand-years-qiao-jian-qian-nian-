<template>
  <div class="about-container">
    <div class="about-card">
      <!-- 卷轴顶部装饰 -->
      <div class="scroll-top"></div>
      
      <div class="logo-section">
        <span class="logo">🏛️</span>
        <h1>桥 见 千 年</h1>
        <p class="subtitle">中国古代桥梁智慧可视化平台</p>
      </div>

      <div class="info-section">
        <div class="section-header">
          <span class="header-seal">源</span>
          <h3>项目背景</h3>
        </div>
        <p>
          中国是桥梁的故乡，自古以来就有"桥的国度"之称。本项目以1911年前中国古代桥梁成就为主题，
          从建筑成就与科学家精神双角度切入，运用AI技术与现代可视化手段，打造一个集知识传播、
          互动体验、智能问答于一体的数字化平台，让千年桥梁智慧在数字时代焕发新生。
        </p>
      </div>

      <div class="info-section">
        <div class="section-header">
          <span class="header-seal">功</span>
          <h3>核心功能</h3>
        </div>
        <div class="feature-grid">
          <div class="feature-item">
            <span class="feature-icon">🗺️</span>
            <span>古桥梁分布地图</span>
          </div>
          <div class="feature-item">
            <span class="feature-icon">📚</span>
            <span>桥梁博览知识库</span>
          </div>
          <div class="feature-item">
            <span class="feature-icon">⏳</span>
            <span>历史时间轴演进</span>
          </div>
          <div class="feature-item">
            <span class="feature-icon">🤖</span>
            <span>AI智能问答系统</span>
          </div>
          <div class="feature-item">
            <span class="feature-icon">🔧</span>
            <span>桥梁结构剖析</span>
          </div>
          <div class="feature-item">
            <span class="feature-icon">👤</span>
            <span>匠心人物传记</span>
          </div>
        </div>
      </div>

      <div class="info-section">
        <div class="section-header">
          <span class="header-seal">技</span>
          <h3>技术栈</h3>
        </div>
        <div class="tech-tags">
          <span class="tech-tag" v-for="tech in ['Vue 3', 'Element Plus', 'ECharts', 'Flask', 'GLM-4']" :key="tech">{{ tech }}</span>
        </div>
      </div>

      <div class="info-section">
        <div class="section-header">
          <span class="header-seal">智</span>
          <h3>AI工具声明</h3>
        </div>
        <p>本作品使用了以下AI工具：</p>
        <ul>
          <li><strong>GLM-4（智谱AI）</strong>：用于构建AI智能问答功能</li>
          <li><strong>GitHub Copilot</strong>：辅助代码编写</li>
        </ul>
      </div>

      <div class="info-section">
        <div class="section-header">
          <span class="header-seal">赛</span>
          <h3>参赛信息</h3>
        </div>
        <div class="competition-info">
          <div class="info-row">
            <span class="info-label">比赛名称</span>
            <span class="info-value">信息管理学院"AI领航·创见无限"AI创意主题大赛</span>
          </div>
          <div class="info-row">
            <span class="info-label">参赛赛道</span>
            <span class="info-value">AI+信息可视化设计 / 大数据应用</span>
          </div>
          <div class="info-row">
            <span class="info-label">主题限定</span>
            <span class="info-value">1911年前中国古代建筑成就</span>
          </div>
        </div>
      </div>

      <div class="footer-section">
        <div class="footer-line"></div>
        <p>© 2026 【桥见千年】团队</p>
        <p class="slogan">桥见千年，连接古今 🌉</p>
      </div>
      
      <!-- 卷轴底部装饰 -->
      <div class="scroll-bottom"></div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.about-container {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow-y: auto;
  background: linear-gradient(135deg, #F5F0E6 0%, #EDE5D5 100%);
  padding: 20px;
}

.about-card {
  max-width: 750px;
  padding: 40px 50px;
  background: rgba(245, 240, 230, 0.98);
  border: 1px solid rgba(139, 35, 35, 0.12);
  border-radius: 6px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  position: relative;
}

.scroll-top,
.scroll-bottom {
  position: absolute;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, #8B7355, #C9A962, #8B7355);
}

.scroll-top {
  top: 0;
  border-radius: 6px 6px 0 0;
}

.scroll-bottom {
  bottom: 0;
  border-radius: 0 0 6px 6px;
}

.logo-section {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 25px;
  border-bottom: 1px solid rgba(201, 169, 98, 0.3);
}

.logo {
  font-size: 56px;
  display: block;
  margin-bottom: 12px;
}

.logo-section h1 {
  font-size: 32px;
  margin: 0 0 10px;
  color: #2A2A2A;
  font-family: 'Noto Serif SC', serif;
  letter-spacing: 8px;
}

.subtitle {
  font-size: 14px;
  color: #7A7A7A;
  margin: 0;
  letter-spacing: 2px;
}

.info-section {
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.header-seal {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: #8B2323;
  color: #F5F0E6;
  font-size: 12px;
  font-weight: bold;
  border-radius: 3px;
}

.section-header h3 {
  font-size: 15px;
  color: #2A2A2A;
  margin: 0;
  font-family: 'Noto Serif SC', serif;
}

.info-section p {
  font-size: 13px;
  color: #4A4A4A;
  line-height: 1.8;
  margin: 0;
}

.info-section ul {
  margin: 10px 0 0;
  padding-left: 20px;
  color: #4A4A4A;
  line-height: 1.8;
  font-size: 13px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  background: rgba(139, 35, 35, 0.04);
  border: 1px solid rgba(139, 35, 35, 0.08);
  border-radius: 4px;
  font-size: 12px;
  color: #4A4A4A;
}

.feature-icon {
  font-size: 16px;
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tech-tag {
  padding: 4px 12px;
  background: rgba(30, 58, 95, 0.08);
  border: 1px solid rgba(30, 58, 95, 0.2);
  border-radius: 2px;
  font-size: 12px;
  color: #1E3A5F;
}

.competition-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-row {
  display: flex;
  gap: 12px;
  padding: 8px 12px;
  background: rgba(139, 35, 35, 0.03);
  border-radius: 4px;
}

.info-label {
  font-size: 12px;
  color: #7A7A7A;
  min-width: 70px;
}

.info-value {
  font-size: 12px;
  color: #2A2A2A;
}

.footer-section {
  text-align: center;
  padding-top: 24px;
  margin-top: 24px;
  position: relative;
}

.footer-line {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 1px;
  background: linear-gradient(90deg, transparent, #C9A962, transparent);
}

.footer-section p {
  font-size: 12px;
  color: #7A7A7A;
  margin: 0;
}

.slogan {
  margin-top: 8px !important;
  font-size: 13px !important;
  color: #8B2323 !important;
  letter-spacing: 1px;
}

@media (max-width: 768px) {
  .about-card {
    padding: 30px 24px;
  }
  
  .feature-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .logo-section h1 {
    font-size: 26px;
    letter-spacing: 4px;
  }
}
</style>