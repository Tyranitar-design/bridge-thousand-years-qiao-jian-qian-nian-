<template>
  <div class="quiz-container">
    <!-- 顶部标题 -->
    <header class="quiz-header">
      <div class="scroll-title">
        <div class="scroll-left"></div>
        <div class="scroll-content">
          <h1 class="main-title">古桥知识挑战</h1>
          <p class="sub-title">答对问题，赢取荣誉徽章！</p>
        </div>
        <div class="scroll-right"></div>
      </div>
    </header>

    <!-- 游戏开始界面 -->
    <div v-if="gameState === 'start'" class="game-start">
      <div class="start-content">
        <div class="start-icon">🏆</div>
        <h2>古代桥梁知识挑战赛</h2>
        <p class="description">测试你的桥梁知识，回答正确可获得成就徽章！</p>
        
        <div class="game-info">
          <div class="info-item">
            <span class="info-icon">📝</span>
            <div class="info-text">
              <strong>题目数量</strong>
              <span>{{ questions.length }}道</span>
            </div>
          </div>
          <div class="info-item">
            <span class="info-icon">⭐</span>
            <div class="info-text">
              <strong>难度等级</strong>
              <span>初级入门</span>
            </div>
          </div>
          <div class="info-item">
            <span class="info-icon">⏱️</span>
            <div class="info-text">
              <strong>时间限制</strong>
              <span>每题 30 秒</span>
            </div>
          </div>
        </div>
        
        <el-button type="primary" size="large" @click="startGame" class="start-btn">
          🚀 开始挑战
        </el-button>
      </div>
    </div>

    <!-- 答题界面 -->
    <div v-else-if="gameState === 'playing'" class="game-playing">
      <!-- 计分栏 -->
      <div class="score-bar">
        <div class="score-item">
          <span>题目 {{ currentQuestionIndex + 1 }}/{{ questions.length }}</span>
        </div>
        <div class="score-item">
          <span>得分：<strong :class="{'good-score': score >= 70}">{{ score }}分</strong></span>
        </div>
        <div class="timer-item" :class="{ 'time-warning': timer <= 10 }">
          <span>⏱️ {{ timer }}秒</span>
        </div>
      </div>

      <!-- 题目 -->
      <div class="question-card">
        <h3 class="question-text">{{ currentQuestion.question }}</h3>
        
        <!-- 选项 -->
        <div class="options-list">
          <div 
            v-for="(option, index) in currentQuestion.options" 
            :key="index"
            class="option-item"
            :class="{ selected: selectedAnswer === index, correct: checkCorrectness(index), wrong: selectedAnswer === index && !checkCorrectness(index) }"
            @click="selectAnswer(index)"
          >
            <span class="option-label">{{ String.fromCharCode(65 + index) }}.</span>
            <span class="option-text">{{ option }}</span>
          </div>
        </div>

        <!-- 反馈信息 -->
        <div class="feedback-area" v-if="selectedAnswer !== null">
          <div class="feedback-message" :class="isCorrect ? 'correct' : 'wrong'">
            <span class="feedback-icon">{{ isCorrect ? '✅' : '❌' }}</span>
            <span class="feedback-text">{{ isCorrect ? '回答正确！' : '回答错误' }}</span>
          </div>
          <p class="explanation" v-if="currentQuestion.explanation">{{ currentQuestion.explanation }}</p>
          
          <div class="next-buttons">
            <el-button type="primary" @click="nextQuestion" :disabled="!isChecking">
              {{ currentQuestionIndex < questions.length - 1 ? '下一题 →' : '查看结果' }}
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 结算界面 -->
    <div v-else-if="gameState === 'finished'" class="game-finished">
      <div class="result-content">
        <div class="result-icon">{{ getMedalIcon() }}</div>
        <h2>挑战完成！</h2>
        <p class="final-score">最终得分：<strong :class="getScoreClass(score)">{{ score }}分</strong></p>
        
        <div class="performance-desc">{{ performanceDescription }}</div>
        
        <!-- 成绩徽章 -->
        <div class="badge-section" v-if="score >= 60">
          <div class="badge" :class="badgeClass">
            <div class="badge-icon">{{ badgeEmoji }}</div>
            <h4 class="badge-name">{{ badgeName }}</h4>
            <p class="badge-desc">{{ badgeDesc }}</p>
          </div>
        </div>

        <!-- 错题回顾 -->
        <div class="wrong-answer-review" v-if="wrongAnswers.length > 0">
          <h4>📚 错题回顾</h4>
          <div class="wrong-items">
            <div class="wrong-item" v-for="(qa, idx) in wrongAnswers" :key="idx">
              <p class="wrong-q">{{ qa.question }}</p>
              <p class="wrong-a"><strong>正确答案：</strong> {{ qa.correctOption }}</p>
              <p class="wrong-exp" v-if="qa.explanation"><em>{{ qa.explanation }}</em></p>
            </div>
          </div>
        </div>

        <div class="restart-buttons">
          <el-button @click="goHome">返回首页</el-button>
          <el-button type="primary" @click="restartGame">再玩一次</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'

// 题库数据
const questions = ref([
  {
    id: 1,
    question: '赵州桥的建造者是谁？',
    options: ['鲁班', '李春', '蔡襄', '苏轼'],
    correct: 1,
    explanation: '赵州桥由隋代工匠李春设计建造，是世界上现存最早的敞肩石拱桥。'
  },
  {
    id: 2,
    question: '赵州桥的主拱跨径是多少米？',
    options: ['37.02 米', '45.8 米', '52.3 米', '30.5 米'],
    correct: 0,
    explanation: '赵州桥主拱跨径 37.02 米，在当时的世界是跨度最大的单孔石拱桥。'
  },
  {
    id: 3,
    question: '洛阳桥的筏形基础是什么技术？',
    options: ['铁索悬吊', '石墩石梁', '铺石成基', '木桩支撑'],
    correct: 2,
    explanation: '洛阳桥采用筏形基础，即在桥墩下铺垫石块形成基础，是世界首创的工程技术。'
  },
  {
    id: 4,
    question: '卢沟桥有多少只石狮？',
    options: ['285 只', '485 只', '501 只', '360 只'],
    correct: 2,
    explanation: '卢沟桥桥栏望柱雕刻石狮共 501 只（一说 485 只），形态各异，无一雷同。'
  },
  {
    id: 5,
    question: '泸定桥的铁索总共有多少根？',
    options: ['10 根', '13 根', '15 根', '18 根'],
    correct: 1,
    explanation: '泸定桥由 13 根铁链组成（9 根底链，4 根扶手链），每根重约 1.5 吨。'
  },
  {
    id: 6,
    question: '广济桥的特色是什么？',
    options: ['敞肩拱', '启闭式', '联拱结构', '铁索桥'],
    correct: 1,
    explanation: '广济桥是世界上最早的启闭式桥梁，中间设浮桥段可开合通航。'
  },
  {
    id: 7,
    question: '程阳风雨桥是哪个民族的建筑？',
    options: ['苗族', '侗族', '瑶族', '壮族'],
    correct: 1,
    explanation: '程阳风雨桥是侗族建筑的杰出代表，全桥不用一钉一铆。'
  },
  {
    id: 8,
    question: '安平桥又称为什么？',
    options: ['五里桥', '三里桥', '七里桥', '十里桥'],
    correct: 0,
    explanation: '安平桥因长约 5 华里，俗称"五里桥"，是中古时代世界最长的梁式石桥。'
  },
  {
    id: 9,
    question: '宝带桥有多少个桥孔？',
    options: ['30 孔', '40 孔', '50 孔', '53 孔'],
    correct: 3,
    explanation: '宝带桥呈弧形，共有 53 孔，是中国现存最长、保存最完整的多孔石拱桥。'
  },
  {
    id: 10,
    question: '《清明上河图》中描绘的是哪座桥？',
    options: ['赵州桥', '虹桥', '卢沟桥', '广济桥'],
    correct: 1,
    explanation: '《清明上河图》描绘的是北宋汴京的虹桥，是一座木拱桥。'
  }
])

const gameState = ref('start')
const currentQuestionIndex = ref(0)
const score = ref(0)
const timer = ref(30)
const selectedAnswer = ref(null)
const isChecking = ref(true)
const wrongAnswers = ref([])

const currentQuestion = computed(() => questions.value[currentQuestionIndex.value])
const isCorrect = computed(() => selectedAnswer.value === currentQuestion.value.correct)

const startGame = () => {
  gameState.value = 'playing'
  currentQuestionIndex.value = 0
  score.value = 0
  wrongAnswers.value = []
  startTimer()
}

const startTimer = () => {
  clearInterval(timerInterval)
  timer.value = 30
  
  timerInterval = setInterval(() => {
    if (timer.value > 0) {
      timer.value--
    } else {
      handleTimeout()
    }
  }, 1000)
}

let timerInterval = null

const selectAnswer = (index) => {
  if (selectedAnswer.value !== null) return
  selectedAnswer.value = index
  isChecking.value = false
  
  if (index === currentQuestion.value.correct) {
    score.value += 10
    ElMessage.success('回答正确！+10 分')
  } else {
    wrongAnswers.value.push({
      question: currentQuestion.value.question,
      correctOption: currentQuestion.value.options[currentQuestion.value.correct],
      explanation: currentQuestion.value.explanation
    })
    ElMessage.error('回答错误')
  }
  
  clearInterval(timerInterval)
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++
    selectedAnswer.value = null
    isChecking.value = true
    timer.value = 30
    startTimer()
  } else {
    endGame()
  }
}

const handleTimeout = () => {
  clearInterval(timerInterval)
  selectedAnswer.value = null
  wrongAnswers.value.push({
    question: currentQuestion.value.question,
    correctOption: currentQuestion.value.options[currentQuestion.value.correct],
    explanation: currentQuestion.value.explanation
  })
  ElMessage.warning('时间到！')
}

const endGame = () => {
  gameState.value = 'finished'
  clearInterval(timerInterval)
  ElMessage.success(`挑战完成！最终得分：${score.value}分`)
}

const restartGame = () => {
  startGame()
}

const goHome = () => {
  window.location.href = '/'
}

const getMedalIcon = () => {
  if (score.value >= 90) return '🥇'
  if (score.value >= 70) return '🥈'
  if (score.value >= 50) return '🥉'
  return '⭐'
}

const getScoreClass = (s) => {
  if (s >= 80) return 'excellent'
  if (s >= 60) return 'good'
  return 'normal'
}

const performanceDescription = computed(() => {
  if (score.value >= 90) return '太棒了！你是真正的古桥专家！'
  if (score.value >= 70) return '不错！你对古桥知识有一定了解！'
  if (score.value >= 50) return '还可以，但还有提升空间！'
  return '继续加油，多学习古桥知识吧！'
})

const badgeClass = computed(() => {
  if (score.value >= 90) return 'gold-badge'
  if (score.value >= 70) return 'silver-badge'
  if (score.value >= 50) return 'bronze-badge'
  return 'participation-badge'
})

const badgeEmoji = computed(() => {
  if (score.value >= 90) return '👑'
  if (score.value >= 70) return '🏅'
  if (score.value >= 50) return '🎖️'
  return '📚'
})

const badgeName = computed(() => {
  if (score.value >= 90) return '古桥大师'
  if (score.value >= 70) return '桥梁爱好者'
  if (score.value >= 50) return '初识古桥'
  return '学习新手'
})

const badgeDesc = computed(() => {
  if (score.value >= 90) return '你掌握了丰富的古桥知识'
  if (score.value >= 70) return '你已经熟悉了主要古桥特点'
  if (score.value >= 50) return '你已经了解了基本古桥知识'
  return '继续学习，你会成为专家的！'
})

const checkCorrectness = (index) => index === currentQuestion.value.correct

watch(() => currentQuestionIndex.value, () => {
  selectedAnswer.value = null
  isChecking.value = true
  timer.value = 30
  startTimer()
})
</script>

<style scoped>
.quiz-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  background: linear-gradient(135deg, #F5F0E6 0%, #EDE5D5 100%);
  padding: 20px;
  overflow-y: auto;
}

.quiz-header { text-align: center; }
.scroll-title { display: inline-flex; align-items: stretch; }
.scroll-left, .scroll-right { width: 14px; background: linear-gradient(90deg, #8B7355, #C9A962); border-radius: 7px 0 0 7px; }
.scroll-right { border-radius: 0 7px 7px 0; }
.scroll-content { background: #F5F0E6; border-top: 2px solid #C9A962; border-bottom: 2px solid #C9A962; padding: 10px 30px; }
.main-title { font-size: 22px; color: #2A2A2A; margin: 0; letter-spacing: 8px; font-family: 'Noto Serif SC', serif; }
.sub-title { font-size: 12px; color: #7A7A7A; margin: 4px 0 0; }

/* 开始界面 */
.game-start { flex: 1; display: flex; align-items: center; justify-content: center; }
.start-content { text-align: center; max-width: 600px; }
.start-icon { font-size: 72px; margin-bottom: 16px; }
.start-content h2 { font-size: 28px; color: #2A2A2A; margin: 0 0 12px; font-family: 'Noto Serif SC', serif; }
.description { font-size: 14px; color: #7A7A7A; margin-bottom: 24px; }

.game-info { display: flex; justify-content: space-around; margin-bottom: 32px; }
.info-item { display: flex; align-items: center; gap: 12px; background: rgba(245, 240, 230, 0.8); padding: 12px 20px; border-radius: 8px; }
.info-icon { font-size: 24px; }
.info-text strong { display: block; font-size: 12px; color: #8B2323; }
.info-text span { font-size: 14px; color: #4A4A4A; }

.start-btn { padding: 14px 48px; font-size: 16px; }

/* 答题界面 */
.game-playing { display: flex; flex-direction: column; gap: 16px; flex: 1; }

.score-bar { display: flex; justify-content: space-between; padding: 12px 20px; background: rgba(245, 240, 230, 0.95); border-radius: 6px; font-size: 13px; }
.timer-item { color: #8B2323; font-weight: 600; }
.timer-item.time-warning { animation: pulse 0.5s infinite; color: #c0392b; }

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.question-card { flex: 1; display: flex; flex-direction: column; background: rgba(245, 240, 230, 0.95); padding: 24px; border-radius: 8px; border: 1px solid rgba(139, 35, 35, 0.12); }
.question-text { font-size: 18px; color: #2A2A2A; margin: 0 0 20px; line-height: 1.6; }

.options-list { display: flex; flex-direction: column; gap: 10px; flex: 1; }
.option-item { padding: 14px 18px; background: rgba(232, 224, 208, 0.6); border: 2px solid rgba(139, 35, 35, 0.1); border-radius: 8px; cursor: pointer; transition: all 0.3s; display: flex; gap: 12px; }
.option-item:hover { background: rgba(139, 35, 35, 0.08); border-color: #C9A962; }
.option-item.selected { border-color: #8B2323; background: rgba(139, 35, 35, 0.12); }
.option-item.correct { border-color: #27ae60; background: rgba(39, 174, 96, 0.1); }
.option-item.wrong { border-color: #e74c3c; background: rgba(231, 76, 60, 0.1); }
.option-label { font-weight: bold; color: #8B2323; font-size: 16px; }
.option-text { flex: 1; font-size: 14px; color: #4A4A4A; }

.feedback-area { margin-top: 20px; padding: 16px; background: rgba(232, 224, 208, 0.5); border-radius: 8px; }
.feedback-message { display: flex; align-items: center; gap: 8px; font-size: 16px; font-weight: 600; margin-bottom: 8px; }
.feedback-message.correct { color: #27ae60; }
.feedback-message.wrong { color: #c0392b; }
.explanation { font-size: 13px; color: #4A4A4A; line-height: 1.6; margin: 12px 0; padding: 12px; background: rgba(139, 35, 35, 0.04); border-radius: 6px; }
.next-buttons { text-align: right; }

/* 结算界面 */
.game-finished { flex: 1; display: flex; align-items: center; justify-content: center; }
.result-content { text-align: center; max-width: 600px; }
.result-icon { font-size: 72px; margin-bottom: 16px; }
.result-content h2 { font-size: 28px; color: #2A2A2A; margin: 0 0 12px; }
.final-score { font-size: 24px; margin: 16px 0; }
.final-score.good-score { color: #27ae60; }
.final-score.excellent { color: #f39c12; }

.performance-desc { font-size: 14px; color: #7A7A7A; margin: 20px 0; }

.badge-section { margin: 24px 0; }
.badge { padding: 24px; background: rgba(245, 240, 230, 0.95); border-radius: 12px; border: 2px solid #C9A962; }
.gold-badge { border-color: #f39c12; background: linear-gradient(135deg, #fff9e6, #fffbeb); }
.silver-badge { border-color: #95a5a6; background: linear-gradient(135deg, #ecf0f1, #f5f6f7); }
.bronze-badge { border-color: #d35400; background: linear-gradient(135deg, #fdf2e9, #fef5eb); }
.participation-badge { border-color: #7A7A7A; background: linear-gradient(135deg, #fafafa, #f5f5f5); }

.badge-icon { font-size: 48px; margin-bottom: 12px; }
.badge-name { font-size: 18px; color: #2A2A2A; margin: 0 0 6px; font-family: 'Noto Serif SC', serif; }
.badge-desc { font-size: 13px; color: #7A7A7A; margin: 0; }

.wrong-answer-review { margin-top: 32px; text-align: left; padding: 20px; background: rgba(232, 224, 208, 0.5); border-radius: 8px; }
.wrong-answer-review h4 { font-size: 16px; color: #2A2A2A; margin: 0 0 16px; }
.wrong-items { display: flex; flex-direction: column; gap: 12px; }
.wrong-item { padding: 12px; background: rgba(245, 240, 230, 0.8); border-radius: 6px; }
.wrong-q { font-size: 13px; color: #2A2A2A; margin: 0 0 6px; }
.wrong-a, .wrong-exp { font-size: 12px; color: #7A7A7A; margin: 4px 0; }

.restart-buttons { display: flex; gap: 12px; justify-content: center; margin-top: 24px; }

@media (max-width: 768px) {
  .quiz-container {
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
  
  /* 开始界面 */
  .start-content h2 {
    font-size: 22px;
  }
  
  .description {
    font-size: 13px;
    padding: 0 12px;
  }
  
  .game-info {
    flex-direction: column;
    gap: 10px;
  }
  
  .info-item {
    padding: 10px 16px;
  }
  
  .info-icon {
    font-size: 20px;
  }
  
  .info-text strong {
    font-size: 11px;
  }
  
  .info-text span {
    font-size: 13px;
  }
  
  .start-btn {
    padding: 12px 36px;
    font-size: 15px;
  }
  
  /* 答题界面 */
  .score-bar {
    padding: 10px 14px;
    font-size: 12px;
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .question-card {
    padding: 16px;
  }
  
  .question-text {
    font-size: 15px;
    margin-bottom: 16px;
  }
  
  .options-list {
    gap: 8px;
  }
  
  .option-item {
    padding: 10px 14px;
    gap: 10px;
  }
  
  .option-label {
    font-size: 14px;
  }
  
  .option-text {
    font-size: 13px;
  }
  
  .feedback-area {
    padding: 12px;
    margin-top: 16px;
  }
  
  .feedback-message {
    font-size: 14px;
  }
  
  .explanation {
    font-size: 12px;
    padding: 10px;
  }
  
  .next-buttons {
    text-align: center;
  }
  
  .next-buttons .el-button {
    width: 100%;
  }
  
  /* 结算界面 */
  .result-content h2 {
    font-size: 22px;
  }
  
  .final-score {
    font-size: 20px;
  }
  
  .performance-desc {
    font-size: 13px;
    padding: 0 12px;
  }
  
  .badge {
    padding: 16px;
    margin: 0 12px;
  }
  
  .badge-icon {
    font-size: 36px;
  }
  
  .badge-name {
    font-size: 16px;
  }
  
  .badge-desc {
    font-size: 12px;
  }
  
  .wrong-answer-review {
    padding: 14px;
    margin: 0 12px;
  }
  
  .wrong-answer-review h4 {
    font-size: 14px;
  }
  
  .wrong-item {
    padding: 10px;
  }
  
  .wrong-q {
    font-size: 12px;
  }
  
  .wrong-a, .wrong-exp {
    font-size: 11px;
  }
  
  .restart-buttons {
    flex-direction: column;
    gap: 10px;
    padding: 0 12px;
  }
  
  .restart-buttons .el-button {
    width: 100%;
  }
}
</style>