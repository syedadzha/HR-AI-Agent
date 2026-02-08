<template>
  <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-indigo-500 transition-colors cursor-pointer"
       @dragover.prevent
       @drop.prevent="handleDrop"
       @click="triggerFileInput">
    <input type="file" ref="fileInput" class="hidden" @change="handleFileSelect" accept=".pdf,.docx,.txt" />
    <div v-if="uploading" class="text-indigo-600">
      Uploading...
    </div>
    <div v-else>
      <p class="text-gray-600">Drag & drop files here, or click to select</p>
      <p class="text-xs text-gray-400 mt-2">PDF, DOCX supported</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['uploaded'])
const fileInput = ref(null)
const uploading = ref(false)
const config = useRuntimeConfig()

const triggerFileInput = () => {
  fileInput.value.click()
}

const uploadFile = async (file) => {
  if (!file) return
  
  uploading.value = true
  const formData = new FormData()
  formData.append('file', file)
  
  try {
    const res = await fetch(`${config.public.apiBase}/upload`, {
      method: 'POST',
      body: formData
    })
    
    if (!res.ok) throw new Error('Upload failed')
    
    emit('uploaded')
  } catch (e) {
    console.error(e)
    alert('Failed to upload file')
  } finally {
    uploading.value = false
  }
}

const handleFileSelect = (e) => {
  const file = e.target.files[0]
  uploadFile(file)
}

const handleDrop = (e) => {
  const file = e.dataTransfer.files[0]
  uploadFile(file)
}
</script>
