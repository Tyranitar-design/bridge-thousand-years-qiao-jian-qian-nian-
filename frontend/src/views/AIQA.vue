<template>
  <div class="ai-qa-container">
    <!-- 左侧：对话区 -->
    <div class="chat-section">
      <div class="chat-header">
        <div class="ai-avatar">🌉</div>
        <div class="ai-info">
          <h3>古桥智能助手</h3>
          <p>我可以回答关于中国古代桥梁的各种问题</p>
        </div>
      </div>

      <!-- 消息列表 -->
      <div class="message-list" ref="messageList">
        <div class="welcome-message">
          <div class="message bot">
            <div class="message-avatar">🌉</div>
            <div class="message-content">
              <p>您好！我是【桥见千年】古桥智能助手，专注于中国古代桥梁知识。</p>
              <p>您可以问我：</p>
              <ul>
                <li @click="askQuestion('赵州桥为什么能屹立1400年不倒？')">赵州桥为什么能屹立1400年不倒？</li>
                <li @click="askQuestion('中国古代桥梁有哪些主要类型？')">中国古代桥梁有哪些主要类型？</li>
                <li @click="askQuestion('敞肩拱技术是什么？')">敞肩拱技术是什么？</li>
              </ul>
            </div>
          </div>
        </div>

        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['message', msg.role]"
        >
          <div class="message-avatar">{{ msg.role === 'user' ? '👤' : '🌉' }}</div>
          <div class="message-content">
            <p v-html="formatMessage(msg.content)"></p>
          </div>
        </div>

        <!-- 加载动画 -->
        <div class="message bot" v-if="isLoading">
          <div class="message-avatar">🌉</div>
          <div class="message-content loading">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </div>
        </div>
      </div>

      <!-- 输入区 -->
      <div class="input-area">
        <el-input
          v-model="inputText"
          type="textarea"
          :rows="2"
          placeholder="请输入你的问题..."
          @keydown.enter.ctrl="sendMessage"
          class="chat-input"
        />
        <el-button type="primary" @click="sendMessage" :loading="isLoading" class="send-btn">
          发送
        </el-button>
      </div>
    </div>

    <!-- 右侧：推荐问题 -->
    <div class="suggestions-section">
      <div class="suggestion-card">
        <div class="card-header">
          <span class="header-seal">问</span>
          <h3>推荐问题</h3>
        </div>
        <div class="suggestion-list">
          <div
            class="suggestion-item"
            v-for="q in suggestions"
            :key="q"
            @click="askQuestion(q)"
          >
            <span class="suggestion-icon">◆</span>
            <span>{{ q }}</span>
          </div>
        </div>
      </div>

      <div class="suggestion-card">
        <div class="card-header">
          <span class="header-seal">知</span>
          <h3>知识范围</h3>
        </div>
        <div class="knowledge-scope">
          <span class="knowledge-tag" v-for="tag in knowledgeTags" :key="tag">{{ tag }}</span>
        </div>
      </div>

      <div class="suggestion-card tips">
        <div class="card-header">
          <span class="header-seal">示</span>
          <h3>使用提示</h3>
        </div>
        <ul class="tips-list">
          <li>可以直接输入自然语言问题</li>
          <li>支持追问和多轮对话</li>
          <li>按 Ctrl+Enter 快速发送</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { aiAPI } from '@/api'

const inputText = ref('')
const messages = ref([])
const suggestions = ref([])
const isLoading = ref(false)
const messageList = ref(null)

const knowledgeTags = [
  '桥梁历史', '建筑技术', '建造工艺',
  '历史人物', '诗词典故', '文化传说'
]

onMounted(async () => {
  try {
    const res = await aiAPI.getSuggestions()
    if (res.success) {
      suggestions.value = res.data
    }
  } catch (error) {
    console.error('加载推荐问题失败:', error)
  }
})

const sendMessage = async () => {
  if (!inputText.value.trim() || isLoading.value) return

  const question = inputText.value.trim()
  inputText.value = ''

  messages.value.push({ role: 'user', content: question })
  
  await nextTick()
  scrollToBottom()

  isLoading.value = true
  try {
    const history = messages.value.slice(-10).map(m => ({
      role: m.role === 'user' ? 'user' : 'assistant',
      content: m.content
    }))

    const res = await aiAPI.chat(question, history)
    
    if (res.success) {
      messages.value.push({ role: 'bot', content: res.data.answer })
    } else {
      messages.value.push({ role: 'bot', content: '抱歉，我暂时无法回答这个问题，请稍后再试。' })
    }
  } catch (error) {
    messages.value.push({ role: 'bot', content: '抱歉，服务暂时不可用，请稍后再试。' })
  } finally {
    isLoading.value = false
    await nextTick()
    scrollToBottom()
  }
}

const askQuestion = (question) => {
  inputText.value = question
  sendMessage()
}

const formatMessage = (text) => {
  if (!text) return ''
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>')
}

const scrollToBottom = () => {
  if (messageList.value) {
    messageList.value.scrollTop = messageList.value.scrollHeight
  }
}
</script>

<style scoped>
.ai-qa-container {
  height: 100%;
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 16px;
  background: linear-gradient(135deg, #F5F0E6 0%, #EDE5D5 100%);
}

/* 对话区 */
.chat-section {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.12);
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.chat-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-bottom: 1px solid rgba(201, 169, 98, 0.3);
  background: linear-gradient(90deg, rgba(139, 35, 35, 0.04), transparent);
}

.ai-avatar {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #8B2323, #C9A962);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
}

.ai-info h3 {
  margin: 0;
  font-size: 15px;
  color: #2A2A2A;
  font-family: 'Noto Serif SC', serif;
}

.ai-info p {
  margin: 4px 0 0;
  font-size: 11px;
  color: #7A7A7A;
}

/* 消息列表 */
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.message {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(139, 35, 35, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.message.user .message-avatar {
  background: rgba(30, 58, 95, 0.1);
}

.message-content {
  max-width: 70%;
  padding: 10px 14px;
  border-radius: 4px;
  background: rgba(232, 224, 208, 0.8);
  border: 1px solid rgba(139, 35, 35, 0.1);
}

.message.user .message-content {
  background: rgba(30, 58, 95, 0.08);
  border-color: rgba(30, 58, 95, 0.15);
}

.message-content p {
  margin: 0 0 8px;
  font-size: 13px;
  color: #2A2A2A;
  line-height: 1.7;
}

.message-content p:last-child {
  margin-bottom: 0;
}

.message-content ul {
  margin: 10px 0;
  padding-left: 18px;
  color: #4A4A4A;
}

.message-content li {
  margin-bottom: 6px;
  cursor: pointer;
  transition: color 0.2s;
}

.message-content li:hover {
  color: #8B2323;
}

/* 加载动画 */
.message-content.loading {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
}

.dot {
  width: 6px;
  height: 6px;
  background: #8B2323;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out;
}

.dot:nth-child(1) { animation-delay: 0s; }
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

/* 输入区 */
.input-area {
  display: flex;
  gap: 10px;
  padding: 14px;
  border-top: 1px solid rgba(201, 169, 98, 0.3);
  background: rgba(245, 240, 230, 0.5);
}

.chat-input :deep(.el-textarea__inner) {
  background: rgba(232, 224, 208, 0.6);
  border: 1px solid rgba(139, 35, 35, 0.15);
  border-radius: 4px;
  color: #2A2A2A;
}

.send-btn {
  background: #8B2323;
  border-color: #8B2323;
}

.send-btn:hover {
  background: #6B1A1A;
  border-color: #6B1A1A;
}

/* 右侧区 */
.suggestions-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.suggestion-card {
  background: rgba(245, 240, 230, 0.95);
  border: 1px solid rgba(139, 35, 35, 0.12);
  border-radius: 6px;
  padding: 14px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
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
  width: 20px;
  height: 20px;
  background: #8B2323;
  color: #F5F0E6;
  font-size: 10px;
  font-weight: bold;
  border-radius: 2px;
}

.card-header h3 {
  font-size: 13px;
  color: #2A2A2A;
  margin: 0;
  font-family: 'Noto Serif SC', serif;
}

.suggestion-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.suggestion-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 8px 10px;
  background: rgba(232, 224, 208, 0.5);
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  color: #4A4A4A;
  transition: all 0.2s;
}

.suggestion-item:hover {
  background: rgba(139, 35, 35, 0.06);
  color: #8B2323;
}

.suggestion-icon {
  font-size: 8px;
  color: #C9A962;
  margin-top: 3px;
}

.knowledge-scope {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.knowledge-tag {
  padding: 3px 10px;
  background: rgba(201, 169, 98, 0.15);
  border: 1px solid rgba(201, 169, 98, 0.3);
  border-radius: 2px;
  font-size: 11px;
  color: #8B7355;
}

.tips-list {
  margin: 0;
  padding-left: 16px;
  font-size: 11px;
  color: #7A7A7A;
  line-height: 2;
}

/* 响应式 */
@media (max-width: 1000px) {
  .ai-qa-container {
    grid-template-columns: 1fr;
  }
  
  .suggestions-section {
    display: none;
  }
}

@media (max-width: 768px) {
  .ai-qa-container {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .chat-header {
    padding: 12px;
    gap: 10px;
  }
  
  .ai-avatar {
    width: 36px;
    height: 36px;
    font-size: 18px;
  }
  
  .ai-info h3 {
    font-size: 14px;
  }
  
  .ai-info p {
    font-size: 10px;
  }
  
  .message-list {
    padding: 12px;
  }
  
  .message {
    gap: 8px;
    margin-bottom: 12px;
  }
  
  .message-avatar {
    width: 28px;
    height: 28px;
    font-size: 14px;
  }
  
  .message-content {
    max-width: 85%;
    padding: 8px 12px;
  }
  
  .message-content p {
    font-size: 12px;
    line-height: 1.6;
  }
  
  .message-content ul {
    margin: 8px 0;
    padding-left: 14px;
  }
  
  .message-content li {
    font-size: 12px;
    margin-bottom: 4px;
  }
  
  .input-area {
    padding: 10px;
    gap: 8px;
    flex-direction: column;
  }
  
  .chat-input :deep(.el-textarea__inner) {
    font-size: 13px;
  }
  
  .send-btn {
    width: 100%;
  }
}
</style>