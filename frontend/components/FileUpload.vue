<script setup>
import { Upload, X, FileCheck, Loader2 } from 'lucide-vue-next'

const fileInput = ref(null)
const isUploading = ref(false)
const dragOver = ref(false)

const triggerUpload = () => fileInput.value.click()

const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  isUploading.value = true
  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData
    })
    if (res.ok) {
      window.location.reload() // Refresh to update list
    }
  } catch (error) {
    console.error('Upload failed:', error)
  } finally {
    isUploading.value = false
  }
}

const onDrop = (e) => {
  dragOver.value = false
  const file = e.dataTransfer.files[0]
  if (file) {
    const inputEvent = { target: { files: [file] } }
    handleFileUpload(inputEvent)
  }
}
</script>

<template>
  <div 
    @dragover.prevent="dragOver = true"
    @dragleave.prevent="dragOver = false"
    @drop.prevent="onDrop"
    :class="[
      dragOver ? 'border-indigo-500 bg-indigo-50/50' : 'border-slate-200 bg-slate-50/50 hover:bg-slate-50 hover:border-indigo-300',
      isUploading ? 'opacity-70 pointer-events-none' : ''
    ]"
    class="relative border-2 border-dashed rounded-[2.5rem] p-12 transition-all group cursor-pointer text-center"
    @click="triggerUpload"
  >
    <input 
      type="file" 
      ref="fileInput" 
      class="hidden" 
      @change="handleFileUpload"
      accept=".pdf,.docx,.txt"
    />

    <div v-if="!isUploading" class="space-y-4">
      <div class="inline-flex items-center justify-center w-20 h-20 bg-white rounded-3xl shadow-lg border border-slate-100 group-hover:-translate-y-1 transition-transform duration-300">
        <Upload class="w-10 h-10 text-indigo-600" />
      </div>
      <div>
        <h4 class="text-xl font-bold text-slate-900">Upload Policy Documents</h4>
        <p class="text-slate-500 mt-2 font-medium">Drag & drop your PDF or DOCX files here</p>
      </div>
      <div class="flex items-center justify-center gap-6 pt-4">
        <div class="flex items-center gap-2 text-xs font-bold text-slate-400 uppercase tracking-widest">
          <FileCheck class="w-4 h-4 text-green-500" />
          PDF Support
        </div>
        <div class="flex items-center gap-2 text-xs font-bold text-slate-400 uppercase tracking-widest">
          <FileCheck class="w-4 h-4 text-blue-500" />
          Word Support
        </div>
      </div>
    </div>

    <div v-else class="py-6 space-y-6">
      <div class="flex flex-col items-center justify-center">
        <Loader2 class="w-12 h-12 text-indigo-600 animate-spin mb-4" />
        <h4 class="text-xl font-bold text-slate-900">Processing Document</h4>
        <p class="text-slate-500 mt-2 font-medium italic">Converting to Markdown & Extracting Propositions...</p>
      </div>
      
      <div class="max-w-xs mx-auto w-full bg-slate-200 h-2 rounded-full overflow-hidden">
        <div class="bg-indigo-600 h-full animate-progress-bar"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes progress-bar {
  0% { width: 0%; }
  100% { width: 100%; }
}
.animate-progress-bar {
  animation: progress-bar 10s ease-in-out infinite;
}
</style>