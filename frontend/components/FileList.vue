<template>
  <div class="space-y-3">
    <div v-if="loading" class="text-sm text-gray-500">Loading files...</div>
    <div v-else-if="files.length === 0" class="text-sm text-gray-500 italic">No files uploaded yet.</div>
    <ul v-else class="space-y-2">
      <li v-for="file in files" :key="file.file_id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-100 hover:bg-gray-100 transition">
        <div class="overflow-hidden">
          <p class="text-sm font-medium text-gray-700 truncate" :title="file.filename">{{ file.filename }}</p>
          <p class="text-xs text-gray-400">{{ formatDate(file.upload_date) }}</p>
        </div>
        <button @click="deleteFile(file.file_id)" class="text-red-400 hover:text-red-600 ml-2" title="Delete">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-trash-2"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/></svg>
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const files = ref([])
const loading = ref(true)
const config = useRuntimeConfig()

const fetchFiles = async () => {
  loading.value = true
  try {
    const res = await fetch(`${config.public.apiBase}/files`)
    if (res.ok) {
      files.value = await res.json()
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const deleteFile = async (fileId) => {
  if (!confirm('Are you sure you want to delete this file?')) return

  try {
    const res = await fetch(`${config.public.apiBase}/files/${fileId}`, {
      method: 'DELETE'
    })
    if (res.ok) {
      files.value = files.value.filter(f => f.file_id !== fileId)
    } else {
        alert("Failed to delete")
    }
  } catch (e) {
    console.error(e)
    alert("Error deleting file")
  }
}

const formatDate = (dateStr) => {
    if (!dateStr) return ''
    return new Date(dateStr).toLocaleDateString()
}

onMounted(() => {
  fetchFiles()
})
</script>
