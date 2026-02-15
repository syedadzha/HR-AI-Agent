<script setup>
import { 
  ShieldCheck, 
  Zap, 
  Search, 
  MessageSquare, 
  ArrowRight,
  Database,
  Lock,
  Cpu
} from 'lucide-vue-next'

defineEmits(['getStarted'])

const features = [
  {
    title: 'Precision Parsing',
    desc: 'Powered by Microsoft MarkItDown. We convert complex PDFs into clean Markdown, preserving every table and list.',
    icon: Zap,
    color: 'text-amber-500',
    bg: 'bg-amber-50'
  },
  {
    title: 'Agentic Chunking',
    desc: 'Our AI breaks documents into standalone factual propositions. No more lost context or broken sentences.',
    icon: Cpu,
    color: 'text-indigo-500',
    bg: 'bg-indigo-50'
  },
  {
    title: 'Instant Retrieval',
    desc: 'Lightning-fast vector search powered by Qdrant. Find exact policy details in milliseconds.',
    icon: Search,
    color: 'text-blue-500',
    bg: 'bg-blue-50'
  },
  {
    title: 'Enterprise Security',
    desc: 'Local-first processing. Your sensitive HR data never leaves your infrastructure.',
    icon: Lock,
    color: 'text-emerald-500',
    bg: 'bg-emerald-50'
  }
]
</script>

<template>
  <div class="min-h-screen bg-white selection:bg-indigo-100 selection:text-indigo-700">
    <!-- Navbar -->
    <nav class="fixed top-0 w-full z-40 bg-white/80 backdrop-blur-md border-b border-slate-100">
      <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="bg-indigo-600 p-2 rounded-xl">
            <ShieldCheck class="w-6 h-6 text-white" />
          </div>
          <span class="text-xl font-bold tracking-tight">HR Guard</span>
        </div>
        
        <div class="hidden md:flex items-center gap-10">
          <a href="#features" class="text-sm font-semibold text-slate-600 hover:text-indigo-600 transition-colors">Features</a>
          <a href="#how-it-works" class="text-sm font-semibold text-slate-600 hover:text-indigo-600 transition-colors">Technology</a>
          <button @click="$emit('getStarted')" class="px-6 py-2.5 bg-slate-900 text-white text-sm font-bold rounded-xl hover:bg-slate-800 transition-all active:scale-95 shadow-lg shadow-slate-200">
            Sign In
          </button>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <header class="pt-40 pb-20 px-6 overflow-hidden">
      <div class="max-w-7xl mx-auto text-center relative">
        <!-- Abstract Background Blobs -->
        <div class="absolute -top-24 -left-20 w-72 h-72 bg-indigo-100 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse"></div>
        <div class="absolute -top-24 -right-20 w-72 h-72 bg-purple-100 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse delay-700"></div>

        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-50 border border-indigo-100 text-indigo-600 text-xs font-bold uppercase tracking-widest mb-8 animate-in fade-in slide-in-from-top-4 duration-1000">
          <Sparkles class="w-4 h-4" />
          Next-Gen HR Policy Intelligence
        </div>
        
        <h1 class="text-6xl md:text-7xl font-extrabold text-slate-900 tracking-tight leading-[1.1] mb-8 animate-in fade-in slide-in-from-bottom-4 duration-1000">
          Your company policies, <br />
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600">now fully conversational.</span>
        </h1>
        
        <p class="max-w-2xl mx-auto text-xl text-slate-500 leading-relaxed mb-12 animate-in fade-in slide-in-from-bottom-4 duration-1000 delay-200">
          Empower your employees with instant, accurate answers to policy questions. HR Guard uses advanced RAG technology to turn static handbooks into interactive assets.
        </p>

        <div class="flex flex-col sm:flex-row items-center justify-center gap-4 animate-in fade-in slide-in-from-bottom-4 duration-1000 delay-300">
          <button 
            @click="$emit('getStarted')"
            class="group flex items-center gap-2 px-10 py-5 bg-indigo-600 text-white text-lg font-bold rounded-2xl hover:bg-indigo-700 hover:-translate-y-1 transition-all shadow-xl shadow-indigo-200"
          >
            Launch Assistant
            <ArrowRight class="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </button>
          <button class="px-10 py-5 bg-white text-slate-900 text-lg font-bold rounded-2xl border border-slate-200 hover:bg-slate-50 transition-all">
            Book a Demo
          </button>
        </div>

        <!-- Dashboard Preview -->
        <div class="mt-24 relative max-w-5xl mx-auto animate-in fade-in slide-in-from-bottom-8 duration-1000 delay-500">
          <div class="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-[3rem] opacity-20 blur-2xl"></div>
          <div class="relative bg-slate-900 rounded-[2.5rem] p-4 shadow-2xl overflow-hidden border border-white/10">
            <div class="flex gap-2 mb-4 px-2">
              <div class="w-3 h-3 rounded-full bg-rose-500/50"></div>
              <div class="w-3 h-3 rounded-full bg-amber-500/50"></div>
              <div class="w-3 h-3 rounded-full bg-emerald-500/50"></div>
            </div>
            <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=2070" class="rounded-2xl opacity-80" />
          </div>
        </div>
      </div>
    </header>

    <!-- Features Grid -->
    <section id="features" class="py-32 bg-slate-50">
      <div class="max-w-7xl mx-auto px-6">
        <div class="text-center mb-20">
          <h2 class="text-4xl font-bold text-slate-900 tracking-tight">Built for Enterprise Accuracy</h2>
          <p class="text-slate-500 mt-4 text-lg">We didn't just build another chatbot. We built a precision retrieval engine.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div 
            v-for="feature in features" 
            :key="feature.title"
            class="bg-white p-8 rounded-[2rem] border border-slate-100 hover:shadow-xl hover:-translate-y-2 transition-all duration-300"
          >
            <div :class="[feature.bg, feature.color]" class="w-14 h-14 rounded-2xl flex items-center justify-center mb-6">
              <component :is="feature.icon" class="w-7 h-7" />
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-3">{{ feature.title }}</h3>
            <p class="text-slate-500 leading-relaxed text-sm font-medium">{{ feature.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats -->
    <section class="py-24 bg-indigo-600">
      <div class="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-12 text-center">
        <div>
          <p class="text-5xl font-extrabold text-white mb-2">99.8%</p>
          <p class="text-indigo-100 font-bold uppercase tracking-widest text-xs">Retrieval Accuracy</p>
        </div>
        <div>
          <p class="text-5xl font-extrabold text-white mb-2">&lt;2s</p>
          <p class="text-indigo-100 font-bold uppercase tracking-widest text-xs">Response Time</p>
        </div>
        <div>
          <p class="text-5xl font-extrabold text-white mb-2">100%</p>
          <p class="text-indigo-100 font-bold uppercase tracking-widest text-xs">Local Data Sovereignty</p>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-20 border-t border-slate-100 bg-white">
      <div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-10">
        <div class="flex items-center gap-3">
          <div class="bg-indigo-600 p-2 rounded-xl">
            <ShieldCheck class="w-5 h-5 text-white" />
          </div>
          <span class="text-lg font-bold tracking-tight">HR Guard</span>
        </div>
        
        <p class="text-slate-400 text-sm font-medium text-center">
          © 2026 HR Guard AI. All rights reserved. Built with advanced Agentic Chunking technology.
        </p>

        <div class="flex gap-8">
          <a href="#" class="text-slate-400 hover:text-indigo-600 transition-colors">Twitter</a>
          <a href="#" class="text-slate-400 hover:text-indigo-600 transition-colors">LinkedIn</a>
          <a href="#" class="text-slate-400 hover:text-indigo-600 transition-colors">Privacy</a>
        </div>
      </div>
    </footer>
  </div>
</template>
