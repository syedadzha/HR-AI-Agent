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
  <aside class="flex h-screen w-72 flex-col border-r border-slate-200 bg-slate-50 transition-all duration-300">
    <!-- Logo -->
    <div class="flex items-center gap-3 p-6">
      <div class="rounded-xl bg-indigo-600 p-2">
        <ShieldCheck class="size-6 text-white" />
      </div>
      <h1 class="text-xl font-bold tracking-tight text-slate-900">HR Guard</h1>
    </div>

    <!-- Main Nav -->
    <nav class="flex-1 space-y-1 px-4">
      <button 
        :class="[activeTab === 'chat' ? 'border-slate-200 bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:bg-slate-100']"
        class="flex w-full items-center gap-3 rounded-xl border border-transparent px-4 py-3 font-medium transition-all"
        @click="$emit('setTab', 'chat')"
      >
        <MessageSquare class="h-6 w-5" />
        Chat Assistant
      </button>

      <button 
        :class="[activeTab === 'files' ? 'border-slate-200 bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:bg-slate-100']"
        class="flex w-full items-center gap-3 rounded-xl border border-transparent px-4 py-3 font-medium transition-all"
        @click="$emit('setTab', 'files')"
      >
        <Files class="h-6 w-5" />
        Policy Library
      </button>
    </nav>

    <!-- User Profile Section -->
    <div class="border-t border-slate-200 p-4">
      <button 
        class="group flex w-full items-center gap-3 rounded-xl p-3 text-left transition-all hover:bg-slate-100"
        @click="$emit('setTab', 'profile')"
      >
        <img :src="user.avatar" class="size-10 rounded-full border border-slate-200 shadow-sm" />
        <div class="flex-1 overflow-hidden text-ellipsis">
          <p class="text-sm font-semibold text-slate-900">{{ user.name }}</p>
          <p class="truncate text-xs text-slate-500">{{ user.email }}</p>
        </div>
        <Settings class="size-4 text-slate-400 group-hover:text-slate-600" />
      </button>
      
      <button 
        class="mt-4 flex w-full items-center justify-center gap-2 rounded-lg border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-600 shadow-sm transition-all hover:bg-slate-50 hover:text-indigo-600"
        @click="$emit('openAuth')"
      >
        <LogOut class="size-4" />
        Sign Out
      </button>
    </div>
  </aside>
</template>
