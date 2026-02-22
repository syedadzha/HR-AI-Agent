import { defineStore } from 'pinia'
import { useAppStore } from './useAppStore'

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export const useChatStore = defineStore('chat', {
  state: () => ({
    history: [
      { role: 'assistant', content: "Hello! I'm your AI HR Assistant. I've indexed your latest company policies. How can I help you today?" }
    ] as ChatMessage[],
    isLoading: false
  }),
  
  actions: {
    addMessage(message: ChatMessage) {
      this.history.push(message)
    },
    
    async sendMessage(question: string) {
      if (!question.trim() || this.isLoading) return
      
      const appStore = useAppStore()
      const config = useRuntimeConfig()
      
      this.addMessage({ role: 'user', content: question })
      this.isLoading = true
      
      try {
        const response = await fetch(`${config.public.apiBase}/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-API-Key': appStore.apiKey
          },
          body: JSON.stringify({ 
            question, 
            history: this.history.slice(0, -1) 
          })
        })
        
        if (!response.ok) throw new Error('Chat request failed')
        
        const assistantMsg: ChatMessage = { role: 'assistant', content: '' }
        this.history.push(assistantMsg)
        const msgIndex = this.history.length - 1
        
        const reader = response.body?.getReader()
        const decoder = new TextDecoder()
        
        if (reader) {
          while (true) {
            const { done, value } = await reader.read()
            if (done) break
            const chunk = decoder.decode(value, { stream: true })
            this.history[msgIndex].content += chunk
          }
        }
      } catch (error) {
        console.error('Chat error:', error)
        this.addMessage({ role: 'assistant', content: 'Sorry, I encountered an error processing your request.' })
      } finally {
        this.isLoading = false
      }
    }
  }
})
