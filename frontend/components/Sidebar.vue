<script setup>
import { 
  MessageSquare, 
  Files, 
  User, 
  Settings, 
  LogOut, 
  PlusCircle,
  ShieldCheck
} from 'lucide-vue-next'

defineProps(['activeTab'])
defineEmits(['setTab', 'openAuth'])

const user = ref({
  name: 'John Doe',
  email: 'john@example.com',
  avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=John'
})
</script>

<template>
  <aside class="w-72 bg-slate-50 border-r border-slate-200 flex flex-col h-screen transition-all duration-300">
    <!-- Logo -->
    <div class="p-6 flex items-center gap-3">
      <div class="bg-indigo-600 p-2 rounded-xl">
        <ShieldCheck class="w-6 h-6 text-white" />
      </div>
      <h1 class="text-xl font-bold text-slate-900 tracking-tight">HR Guard</h1>
    </div>

    <!-- Main Nav -->
    <nav class="flex-1 px-4 space-y-1">
      <button 
        @click="$emit('setTab', 'chat')"
        :class="[activeTab === 'chat' ? 'bg-white shadow-sm text-indigo-600 border-slate-200' : 'text-slate-600 hover:bg-slate-100']"
        class="w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-medium border border-transparent"
      >
        <MessageSquare class="w-5 h-6" />
        Chat Assistant
      </button>

      <button 
        @click="$emit('setTab', 'files')"
        :class="[activeTab === 'files' ? 'bg-white shadow-sm text-indigo-600 border-slate-200' : 'text-slate-600 hover:bg-slate-100']"
        class="w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-medium border border-transparent"
      >
        <Files class="w-5 h-6" />
        Policy Library
      </button>
    </nav>

    <!-- User Profile Section -->
    <div class="p-4 border-t border-slate-200">
      <button 
        @click="$emit('setTab', 'profile')"
        class="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-slate-100 transition-all group text-left"
      >
        <img :src="user.avatar" class="w-10 h-10 rounded-full border border-slate-200 shadow-sm" />
        <div class="flex-1 overflow-hidden text-ellipsis">
          <p class="text-sm font-semibold text-slate-900">{{ user.name }}</p>
          <p class="text-xs text-slate-500 truncate">{{ user.email }}</p>
        </div>
        <Settings class="w-4 h-4 text-slate-400 group-hover:text-slate-600" />
      </button>
      
      <button 
        @click="$emit('openAuth')"
        class="mt-4 w-full flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium text-slate-600 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 hover:text-indigo-600 transition-all shadow-sm"
      >
        <LogOut class="w-4 h-4" />
        Sign Out
      </button>
    </div>
  </aside>
</template>
