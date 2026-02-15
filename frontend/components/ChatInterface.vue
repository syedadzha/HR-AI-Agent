<script setup>
import { 
  Send, 
  Bot, 
  User, 
  Sparkles,
  RefreshCcw,
  Info
} from 'lucide-vue-next'

const question = ref('')
const history = ref([
  { role: 'assistant', content: "Hello! I'm your AI HR Assistant. I've indexed your latest company policies. How can I help you today?" }
])
const isLoading = ref(false)

const askQuestion = async () => {
  if (!question.value.trim() || isLoading.value) return

  const userMsg = { role: 'user', content: question.value }
  history.value.push(userMsg)
  const currentQuestion = question.value
  question.value = ''
  isLoading.value = true

  try {
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: currentQuestion, history: history.value.slice(0, -1) })
    })

    const assistantMsg = { role: 'assistant', content: '' }
    history.value.push(assistantMsg)

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      assistantMsg.content += decoder.decode(value)
    }
  } catch (error) {
    console.error('Chat error:', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="flex flex-col h-full max-w-5xl mx-auto w-full px-4 lg:px-8">
    <!-- Chat Header -->
    <header class="py-6 border-b border-slate-100 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="p-2 bg-indigo-50 text-indigo-600 rounded-xl">
          <Sparkles class="w-5 h-5" />
        </div>
        <div>
          <h2 class="font-bold text-slate-900 leading-none">Policy Assistant</h2>
          <span class="text-[10px] text-green-500 font-bold uppercase tracking-widest flex items-center gap-1 mt-1">
            <span class="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></span>
            System Ready
          </span>
        </div>
      </div>
      <button class="p-2 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-xl transition-all">
        <RefreshCcw class="w-5 h-5" />
      </button>
    </header>

    <!-- Messages -->
    <div class="flex-1 overflow-y-auto py-8 space-y-8 no-scrollbar">
      <div 
        v-for="(msg, i) in history" 
        :key="i"
        class="flex gap-4 animate-in fade-in slide-in-from-bottom-2 duration-300"
        :class="[msg.role === 'user' ? 'flex-row-reverse' : '']"
      >
        <div 
          class="w-10 h-10 rounded-2xl flex items-center justify-center shrink-0 shadow-sm"
          :class="[msg.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-600 border border-slate-200']"
        >
          <User v-if="msg.role === 'user'" class="w-5 h-5" />
          <Bot v-else class="w-5 h-5" />
        </div>

        <div 
          class="max-w-[80%] rounded-3xl px-6 py-4 shadow-sm leading-relaxed text-sm whitespace-pre-wrap"
          :class="[
            msg.role === 'user' 
              ? 'bg-indigo-600 text-white rounded-tr-none font-medium' 
              : 'bg-white text-slate-700 border border-slate-100 rounded-tl-none'
          ]"
        >
          {{ msg.content }}
        </div>
      </div>
      
      <div v-if="isLoading && !history[history.length-1].content" class="flex gap-4 animate-pulse">
        <div class="w-10 h-10 bg-slate-100 rounded-2xl border border-slate-200"></div>
        <div class="h-12 bg-slate-50 w-24 rounded-3xl rounded-tl-none border border-slate-100"></div>
      </div>
    </div>

    <!-- Input Section -->
    <div class="pb-10 pt-4">
      <div class="relative group">
        <div class="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-[2rem] blur opacity-10 group-focus-within:opacity-25 transition duration-1000 group-hover:duration-200"></div>
        <div class="relative bg-white border border-slate-200 rounded-3xl shadow-xl p-2 transition-all group-focus-within:border-indigo-300 group-focus-within:ring-4 group-focus-within:ring-indigo-50">
          <form @submit.prevent="askQuestion" class="flex items-center gap-2">
            <input 
              v-model="question"
              placeholder="Ask anything about company policies..." 
              class="flex-1 bg-transparent border-none focus:ring-0 py-4 px-6 text-slate-700 font-medium placeholder:text-slate-400"
            />
            <button 
              type="submit"
              :disabled="!question.trim() || isLoading"
              class="p-4 bg-indigo-600 text-white rounded-2xl shadow-lg shadow-indigo-200 hover:bg-indigo-700 disabled:bg-slate-100 disabled:text-slate-400 disabled:shadow-none transition-all"
            >
              <Send class="w-5 h-5" />
            </button>
          </form>
        </div>
        <p class="text-center text-[11px] text-slate-400 mt-4 flex items-center justify-center gap-1">
          <Info class="w-3 h-3" />
          AI can make mistakes. Verify important policy details with HR.
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>