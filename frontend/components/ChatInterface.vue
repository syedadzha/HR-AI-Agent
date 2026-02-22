<script setup lang="ts">
import { 
  Send, 
  Bot, 
  User, 
  Sparkles,
  RefreshCcw,
  Info
} from 'lucide-vue-next'
import MarkdownIt from 'markdown-it'
import { useChatStore } from '~/stores/useChatStore'

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true
})

const chatStore = useChatStore()
const question = ref('')

const askQuestion = async () => {
  if (!question.value.trim() || chatStore.isLoading) return
  const currentQuestion = question.value
  question.value = ''
  await chatStore.sendMessage(currentQuestion)
}

const clearHistory = () => {
  chatStore.$reset()
}
</script>

<template>
  <div class="mx-auto flex size-full max-w-5xl flex-col px-4 lg:px-8">
    <!-- Chat Header -->
    <header class="flex items-center justify-between border-b border-slate-100 py-6">
      <div class="flex items-center gap-3">
        <div class="rounded-xl bg-indigo-50 p-2 text-indigo-600">
          <Sparkles class="size-5" />
        </div>
        <div>
          <h2 class="font-bold leading-none text-slate-900">Policy Assistant</h2>
          <span class="mt-1 flex items-center gap-1 text-[10px] font-bold uppercase tracking-widest text-green-500">
            <span class="size-1.5 animate-pulse rounded-full bg-green-500"></span>
            System Ready
          </span>
        </div>
      </div>
      <button 
        class="rounded-xl p-2 text-slate-400 transition-all hover:bg-indigo-50 hover:text-indigo-600"
        title="Clear chat history"
        @click="clearHistory"
      >
        <RefreshCcw class="size-5" />
      </button>
    </header>

    <!-- Messages -->
    <div class="no-scrollbar flex-1 space-y-8 overflow-y-auto py-8">
      <div 
        v-for="(msg, i) in chatStore.history" 
        :key="i"
        class="animate-in fade-in slide-in-from-bottom-2 flex gap-4 duration-300"
        :class="[msg.role === 'user' ? 'flex-row-reverse' : '']"
      >
        <div 
          class="flex size-10 shrink-0 items-center justify-center rounded-2xl shadow-sm"
          :class="[msg.role === 'user' ? 'bg-indigo-600 text-white' : 'border border-slate-200 bg-slate-100 text-slate-600']"
        >
          <User v-if="msg.role === 'user'" class="size-5" />
          <Bot v-else class="size-5" />
        </div>

        <div 
          class="max-w-[80%] rounded-3xl px-6 py-4 text-sm leading-relaxed shadow-sm"
          :class="[
            msg.role === 'user' 
              ? 'whitespace-pre-wrap rounded-tr-none bg-indigo-600 font-medium text-white' 
              : 'prose prose-sm prose-slate max-w-none rounded-tl-none border border-slate-100 bg-white text-slate-700'
          ]"
        >
          <template v-if="msg.role === 'user'">
            {{ msg.content }}
          </template>
          <div v-else v-html="md.render(msg.content)"></div>
        </div>
      </div>
      
      <div v-if="chatStore.isLoading && !chatStore.history[chatStore.history.length-1].content" class="flex animate-pulse gap-4">
        <div class="size-10 rounded-2xl border border-slate-200 bg-slate-100"></div>
        <div class="h-12 w-24 rounded-3xl rounded-tl-none border border-slate-100 bg-slate-50"></div>
      </div>
    </div>

    <!-- Input Section -->
    <div class="pb-10 pt-4">
      <div class="group relative">
        <div class="absolute -inset-1 rounded-[2rem] bg-gradient-to-r from-indigo-500 to-purple-500 opacity-10 blur transition duration-1000 group-focus-within:opacity-25 group-hover:duration-200"></div>
        <div class="relative rounded-3xl border border-slate-200 bg-white p-2 shadow-xl transition-all group-focus-within:border-indigo-300 group-focus-within:ring-4 group-focus-within:ring-indigo-50">
          <form class="flex items-center gap-2" @submit.prevent="askQuestion">
            <input 
              v-model="question"
              placeholder="Ask anything about company policies..." 
              class="flex-1 border-none bg-transparent px-6 py-4 font-medium text-slate-700 placeholder:text-slate-400 focus:outline-none focus:ring-0"
            />
            <button 
              type="submit"
              :disabled="!question.trim() || chatStore.isLoading"
              class="rounded-2xl bg-indigo-600 p-4 text-white shadow-lg shadow-indigo-200 transition-all hover:bg-indigo-700 disabled:bg-slate-100 disabled:text-slate-400 disabled:shadow-none"
            >
              <Send class="size-5" />
            </button>
          </form>
        </div>
        <p class="mt-4 flex items-center justify-center gap-1 text-center text-[11px] text-slate-400">
          <Info class="size-3" />
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
