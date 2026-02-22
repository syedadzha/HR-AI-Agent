<script setup lang="ts">
import { Upload, FileCheck, Loader2 } from 'lucide-vue-next'
import { useAppStore } from '~/stores/useAppStore'

const appStore = useAppStore()
const config = useRuntimeConfig()

const fileInput = ref<HTMLInputElement | null>(null)
const isUploading = ref(false)
const dragOver = ref(false)

const triggerUpload = () => fileInput.value?.click()

const handleFileUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  isUploading.value = true
  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await fetch(`${config.public.apiBase}/upload`, {
      method: 'POST',
      headers: {
        'X-API-Key': appStore.apiKey
      },
      body: formData
    })
    if (res.ok) {
      await appStore.fetchFiles()
    }
  } catch (error) {
    console.error('Upload failed:', error)
  } finally {
    isUploading.value = false
  }
}

const onDrop = (e: DragEvent) => {
  dragOver.value = false
  const file = e.dataTransfer?.files[0]
  if (file) {
    const inputEvent = { target: { files: [file] } } as unknown as Event
    handleFileUpload(inputEvent)
  }
}
</script>

<template>
  <div 
    :class="[
      dragOver ? 'border-indigo-500 bg-indigo-50/50' : 'border-slate-200 bg-slate-50/50 hover:border-indigo-300 hover:bg-slate-50',
      isUploading ? 'pointer-events-none opacity-70' : ''
    ]"
    class="group relative cursor-pointer rounded-[2.5rem] border-2 border-dashed p-12 text-center transition-all"
    @dragover.prevent="dragOver = true"
    @dragleave.prevent="dragOver = false"
    @drop.prevent="onDrop"
    @click="triggerUpload"
  >
    <input 
      ref="fileInput" 
      type="file" 
      class="hidden" 
      accept=".pdf,.docx,.txt"
      @change="handleFileUpload"
    />

    <div v-if="!isUploading" class="space-y-4">
      <div class="inline-flex size-20 items-center justify-center rounded-3xl border border-slate-100 bg-white shadow-lg transition-transform duration-300 group-hover:-translate-y-1">
        <Upload class="size-10 text-indigo-600" />
      </div>
      <div>
        <h4 class="text-xl font-bold text-slate-900">Upload Policy Documents</h4>
        <p class="mt-2 font-medium text-slate-500">Drag & drop your PDF or DOCX files here</p>
      </div>
      <div class="flex items-center justify-center gap-6 pt-4">
        <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-slate-400">
          <FileCheck class="size-4 text-green-500" />
          PDF Support
        </div>
        <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-slate-400">
          <FileCheck class="size-4 text-blue-500" />
          Word Support
        </div>
      </div>
    </div>

    <div v-else class="space-y-6 py-6">
      <div class="flex flex-col items-center justify-center">
        <Loader2 class="mb-4 size-12 animate-spin text-indigo-600" />
        <h4 class="text-xl font-bold text-slate-900">Processing Document</h4>
        <p class="mt-2 font-medium italic text-slate-500">Converting to Markdown & Extracting Propositions...</p>
      </div>
      
      <div class="mx-auto h-2 w-full max-w-xs overflow-hidden rounded-full bg-slate-200">
        <div class="animate-progress-bar h-full bg-indigo-600"></div>
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
