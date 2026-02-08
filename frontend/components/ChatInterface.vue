<template>
  <div class="flex flex-col h-full">
    <div class="flex-1 overflow-y-auto space-y-4 mb-4 pr-2" ref="chatContainer">
      <div v-for="(msg, index) in history" :key="index" :class="['flex', msg.role === 'user' ? 'justify-end' : 'justify-start']">
        <div :class="[
            'max-w-[85%] rounded-lg px-4 py-2 text-sm shadow-sm', 
            msg.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-800'
        ]">
          <div v-if="msg.role === 'assistant'" class="prose prose-sm max-w-none prose-slate" v-html="renderMarkdown(msg.content)"></div>
          <div v-else class="whitespace-pre-wrap">{{ msg.content }}</div>
        </div>
      </div>
      <div v-if="loading" class="flex justify-start">
         <div class="bg-gray-100 text-gray-800 rounded-lg px-4 py-2 text-sm shadow-sm animate-pulse">
            Thinking...
         </div>
      </div>
    </div>

    <form @submit.prevent="sendMessage" class="flex gap-2">
      <input 
        v-model="input" 
        type="text" 
        placeholder="Ask a question about your documents..." 
        class="flex-1 rounded-lg border border-gray-300 px-4 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none shadow-sm"
        :disabled="loading"
      />
      <button 
        type="submit" 
        class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium transition-colors shadow-sm"
        :disabled="loading || !input.trim()"
      >
        Send
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import MarkdownIt from 'markdown-it'

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true
})

const renderMarkdown = (content) => {
  return md.render(content)
}

const input = ref('')
const history = ref([])
const loading = ref(false)
const chatContainer = ref(null)
const config = useRuntimeConfig()

const scrollToBottom = async () => {
    await nextTick()
    if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
}

const sendMessage = async () => {
  if (!input.value.trim() || loading.value) return
  
  const question = input.value.trim()
  input.value = ''
  
  // Create a copy of history for the request before adding the user message
  const historyForRequest = [...history.value]
  
  history.value.push({ role: 'user', content: question })
  scrollToBottom()
  
  loading.value = true
  
  // Add an empty assistant message to populate as we stream
  const assistantMessageIndex = history.value.length
  history.value.push({ role: 'assistant', content: '' })
  
  try {
    const res = await fetch(`${config.public.apiBase}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        question,
        history: historyForRequest
      })
    })
    
    if (!res.ok) throw new Error('Chat failed')
    
    const reader = res.body.getReader()
    const decoder = new TextDecoder()
    
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      
      const chunk = decoder.decode(value, { stream: true })
      history.value[assistantMessageIndex].content += chunk
      scrollToBottom()
    }
    
  } catch (e) {
    console.error(e)
    history.value[assistantMessageIndex].content = "Sorry, I encountered an error."
  } finally {
    loading.value = false
    scrollToBottom()
  }
}
</script>
