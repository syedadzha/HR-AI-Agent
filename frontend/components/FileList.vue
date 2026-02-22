<script setup lang="ts">
import { 
  FileText, 
  Trash2, 
  Clock, 
  Search,
  CheckCircle2
} from 'lucide-vue-next'
import { useAppStore } from '~/stores/useAppStore'

const appStore = useAppStore()
const searchQuery = ref('')

onMounted(() => {
  appStore.fetchFiles()
})

const filteredFiles = computed(() => {
  return appStore.files.filter(f => f.filename.toLowerCase().includes(searchQuery.value.toLowerCase()))
})

const deleteFile = async (id: string) => {
  if (!confirm('Are you sure you want to delete this document?')) return
  await appStore.deleteFile(id)
}

const formatDate = (dateStr: string) => {
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
      <Search class="absolute left-4 top-3.5 size-5 text-slate-400" />
      <input 
        v-model="searchQuery"
        placeholder="Search documents..." 
        class="w-full rounded-2xl border border-slate-200 bg-white py-3 pl-12 pr-4 shadow-sm transition-all focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/10"
      />
    </div>

    <!-- Empty State -->
    <div v-if="filteredFiles.length === 0" class="rounded-[2rem] border-2 border-dashed border-slate-100 bg-slate-50/50 py-20 text-center">
      <div class="mx-auto mb-4 flex size-16 items-center justify-center rounded-2xl border border-slate-100 bg-white shadow-sm">
        <FileText class="size-8 text-slate-300" />
      </div>
      <p class="font-medium text-slate-500">No documents found matching your search.</p>
    </div>

    <!-- Grid -->
    <div v-else class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
      <div 
        v-for="file in filteredFiles" 
        :key="file.file_id"
        class="group relative overflow-hidden rounded-3xl border border-slate-100 bg-white p-5 shadow-sm transition-all hover:border-indigo-100 hover:shadow-md"
      >
        <div class="flex items-start gap-4">
          <div class="rounded-2xl bg-indigo-50 p-3 text-indigo-600">
            <FileText class="size-6" />
          </div>
          <div class="min-w-0 flex-1">
            <h4 class="mb-1 truncate font-bold text-slate-900">{{ file.filename }}</h4>
            <div class="flex items-center gap-1.5 text-xs font-medium text-slate-400">
              <Clock class="size-3.5" />
              {{ formatDate(file.upload_date) }}
            </div>
          </div>
        </div>

        <!-- Status Tag -->
        <div class="mt-4 flex items-center justify-between">
          <span class="inline-flex items-center gap-1.5 rounded-full border border-green-100 bg-green-50 px-3 py-1 text-[10px] font-bold uppercase tracking-wider text-green-600">
            <CheckCircle2 class="size-3" />
            Indexed
          </span>
          <button 
            class="rounded-xl p-2 text-slate-300 opacity-0 transition-all hover:bg-rose-50 hover:text-rose-500 group-hover:opacity-100"
            @click="deleteFile(file.file_id)"
          >
            <Trash2 class="size-4" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
