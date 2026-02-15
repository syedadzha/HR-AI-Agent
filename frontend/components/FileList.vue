<script setup>
import { 
  FileText, 
  Trash2, 
  Clock, 
  Search,
  CheckCircle2,
  AlertCircle
} from 'lucide-vue-next'

const files = ref([])
const searchQuery = ref('')

const fetchFiles = async () => {
  const res = await fetch('http://localhost:8000/files')
  files.value = await res.json()
}

const deleteFile = async (id) => {
  if (!confirm('Are you sure you want to delete this document?')) return
  await fetch('http://localhost:8000/files/' + id, { method: 'DELETE' })
  fetchFiles()
}

onMounted(fetchFiles)

const filteredFiles = computed(() => {
  return files.value.filter(f => f.filename.toLowerCase().includes(searchQuery.value.toLowerCase()))
})

const formatDate = (dateStr) => {
  if (!dateStr) return 'Unknown'
  return new Date(dateStr).toLocaleDateString('en-MY', { 
    day: 'numeric', 
    month: 'short', 
    year: 'numeric' 
  })
}
</script>

<template>
  <div class="space-y-6">
    <!-- Search Bar -->
    <div class="relative max-w-md">
      <Search class="absolute left-4 top-3.5 w-5 h-5 text-slate-400" />
      <input 
        v-model="searchQuery"
        placeholder="Search documents..." 
        class="w-full pl-12 pr-4 py-3 bg-white border border-slate-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-indigo-500/10 focus:border-indigo-500 transition-all shadow-sm"
      />
    </div>

    <!-- Empty State -->
    <div v-if="filteredFiles.length === 0" class="text-center py-20 bg-slate-50/50 rounded-[2rem] border-2 border-dashed border-slate-100">
      <div class="bg-white w-16 h-16 rounded-2xl shadow-sm border border-slate-100 flex items-center justify-center mx-auto mb-4">
        <FileText class="w-8 h-8 text-slate-300" />
      </div>
      <p class="text-slate-500 font-medium">No documents found matching your search.</p>
    </div>

    <!-- Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div 
        v-for="file in filteredFiles" 
        :key="file.file_id"
        class="group bg-white p-5 rounded-3xl border border-slate-100 shadow-sm hover:shadow-md hover:border-indigo-100 transition-all relative overflow-hidden"
      >
        <div class="flex items-start gap-4">
          <div class="p-3 bg-indigo-50 text-indigo-600 rounded-2xl">
            <FileText class="w-6 h-6" />
          </div>
          <div class="flex-1 min-w-0">
            <h4 class="font-bold text-slate-900 truncate mb-1">{{ file.filename }}</h4>
            <div class="flex items-center gap-1.5 text-xs text-slate-400 font-medium">
              <Clock class="w-3.5 h-3.5" />
              {{ formatDate(file.upload_date) }}
            </div>
          </div>
        </div>

        <!-- Status Tag -->
        <div class="mt-4 flex items-center justify-between">
          <span class="inline-flex items-center gap-1.5 px-3 py-1 bg-green-50 text-green-600 rounded-full text-[10px] font-bold uppercase tracking-wider border border-green-100">
            <CheckCircle2 class="w-3 h-3" />
            Indexed
          </span>
          <button 
            @click="deleteFile(file.file_id)"
            class="p-2 text-slate-300 hover:text-rose-500 hover:bg-rose-50 rounded-xl transition-all opacity-0 group-hover:opacity-100"
          >
            <Trash2 class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>