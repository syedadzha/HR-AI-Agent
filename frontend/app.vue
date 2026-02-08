<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 font-sans flex flex-col">
    <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <h1 class="text-xl font-semibold text-indigo-600 flex items-center gap-2">
          <span>HR Policy Assistant</span>
        </h1>
        
        <nav class="flex gap-4">
          <button 
            @click="currentView = 'chat'"
            :class="['px-4 py-2 rounded-lg font-medium transition-colors', currentView === 'chat' ? 'bg-indigo-50 text-indigo-600' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100']"
          >
            Chat
          </button>
          <button 
            @click="currentView = 'settings'"
            :class="['px-4 py-2 rounded-lg font-medium transition-colors', currentView === 'settings' ? 'bg-indigo-50 text-indigo-600' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100']"
          >
            Settings
          </button>
        </nav>
      </div>
    </header>

    <main class="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full overflow-hidden flex flex-col">
      <!-- Chat View -->
      <section v-if="currentView === 'chat'" class="flex-1 bg-white p-6 rounded-xl shadow-sm border border-gray-200 flex flex-col overflow-hidden">
        <h2 class="text-lg font-medium mb-4 border-b pb-2">Conversation</h2>
        <ChatInterface class="flex-1 overflow-hidden" />
      </section>

      <!-- Settings View -->
      <section v-else-if="currentView === 'settings'" class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="md:col-span-1 space-y-6">
          <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
            <h2 class="text-lg font-medium mb-4">Upload New Document</h2>
            <FileUpload @uploaded="refreshFiles" />
          </div>
        </div>
        
        <div class="md:col-span-2">
          <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
            <h2 class="text-lg font-medium mb-4">Manage Documents</h2>
            <FileList :key="refreshKey" />
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const currentView = ref('chat')
const refreshKey = ref(0)

const refreshFiles = () => {
  refreshKey.value++
}
</script>

<style>
/* Ensure the body doesn't scroll so the app can be full-height if needed */
body {
  height: 100vh;
  margin: 0;
}
</style>
