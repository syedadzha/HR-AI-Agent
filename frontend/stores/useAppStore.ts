import { defineStore } from 'pinia'

interface FileRecord {
  file_id: string
  filename: string
  upload_date: string
}

export const useAppStore = defineStore('app', {
  state: () => ({
    apiKey: 'default-secret-key', // In a real app, this would be set via login
    files: [] as FileRecord[],
    isLoadingFiles: false
  }),
  
  getters: {
    apiHeaders: (state) => ({
      'Content-Type': 'application/json',
      'X-API-Key': state.apiKey
    })
  },
  
  actions: {
    async fetchFiles() {
      const config = useRuntimeConfig()
      this.isLoadingFiles = true
      try {
        const data = await $fetch<FileRecord[]>(`${config.public.apiBase}/files`, {
          headers: { 'X-API-Key': this.apiKey }
        })
        this.files = data
      } catch (error) {
        console.error('Failed to fetch files:', error)
      } finally {
        this.isLoadingFiles = false
      }
    },
    
    async deleteFile(fileId: string) {
      const config = useRuntimeConfig()
      try {
        await $fetch(`${config.public.apiBase}/files/${fileId}`, {
          method: 'DELETE',
          headers: { 'X-API-Key': this.apiKey }
        })
        await this.fetchFiles()
      } catch (error) {
        console.error('Failed to delete file:', error)
      }
    }
  }
})
