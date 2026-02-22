<script setup>
import { 
  ShieldCheck, 
  Zap, 
  Search, 
  MessageSquare, 
  ArrowRight,
  Database,
  Lock,
  Cpu,
  Sparkles
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
    <nav class="fixed top-0 z-40 w-full border-b border-slate-100 bg-white/80 backdrop-blur-md">
      <div class="mx-auto flex h-20 max-w-7xl items-center justify-between px-6">
        <div class="flex items-center gap-3">
          <div class="rounded-xl bg-indigo-600 p-2">
            <ShieldCheck class="size-6 text-white" />
          </div>
          <span class="text-xl font-bold tracking-tight">HR Guard</span>
        </div>
        
        <div class="hidden items-center gap-10 md:flex">
          <a href="#features" class="text-sm font-semibold text-slate-600 transition-colors hover:text-indigo-600">Features</a>
          <a href="#how-it-works" class="text-sm font-semibold text-slate-600 transition-colors hover:text-indigo-600">Technology</a>
          <button class="rounded-xl bg-slate-900 px-6 py-2.5 text-sm font-bold text-white shadow-lg shadow-slate-200 transition-all hover:bg-slate-800 active:scale-95" @click="$emit('getStarted')">
            Sign In
          </button>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <header class="overflow-hidden px-6 pb-20 pt-40">
      <div class="relative mx-auto max-w-7xl text-center">
        <!-- Abstract Background Blobs -->
        <div class="absolute -left-20 -top-24 size-72 animate-pulse rounded-full bg-indigo-100 opacity-30 mix-blend-multiply blur-3xl"></div>
        <div class="absolute -right-20 -top-24 size-72 animate-pulse rounded-full bg-purple-100 opacity-30 mix-blend-multiply blur-3xl delay-700"></div>

        <div class="animate-in fade-in slide-in-from-top-4 mb-8 inline-flex items-center gap-2 rounded-full border border-indigo-100 bg-indigo-50 px-4 py-2 text-xs font-bold uppercase tracking-widest text-indigo-600 duration-1000">
          <Sparkles class="size-4" />
          Next-Gen HR Policy Intelligence
        </div>
        
        <h1 class="animate-in fade-in slide-in-from-bottom-4 mb-8 text-6xl font-extrabold leading-[1.1] tracking-tight text-slate-900 duration-1000 md:text-7xl">
          Your company policies, <br />
          <span class="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">now fully conversational.</span>
        </h1>
        
        <p class="animate-in fade-in slide-in-from-bottom-4 mx-auto mb-12 max-w-2xl text-xl leading-relaxed text-slate-500 delay-200 duration-1000">
          Empower your employees with instant, accurate answers to policy questions. HR Guard uses advanced RAG technology to turn static handbooks into interactive assets.
        </p>

        <div class="animate-in fade-in slide-in-from-bottom-4 flex flex-col items-center justify-center gap-4 delay-300 duration-1000 sm:flex-row">
          <button 
            class="group flex items-center gap-2 rounded-2xl bg-indigo-600 px-10 py-5 text-lg font-bold text-white shadow-xl shadow-indigo-200 transition-all hover:-translate-y-1 hover:bg-indigo-700"
            @click="$emit('getStarted')"
          >
            Launch Assistant
            <ArrowRight class="size-5 transition-transform group-hover:translate-x-1" />
          </button>
          <button class="rounded-2xl border border-slate-200 bg-white px-10 py-5 text-lg font-bold text-slate-900 transition-all hover:bg-slate-50">
            Book a Demo
          </button>
        </div>

        <!-- Dashboard Preview -->
        <div class="animate-in fade-in slide-in-from-bottom-8 relative mx-auto mt-24 max-w-5xl delay-500 duration-1000">
          <div class="absolute -inset-1 rounded-[3rem] bg-gradient-to-r from-indigo-500 to-purple-600 opacity-20 blur-2xl"></div>
          <div class="relative overflow-hidden rounded-[2.5rem] border border-white/10 bg-slate-900 p-4 shadow-2xl">
            <div class="mb-4 flex gap-2 px-2">
              <div class="size-3 rounded-full bg-rose-500/50"></div>
              <div class="size-3 rounded-full bg-amber-500/50"></div>
              <div class="size-3 rounded-full bg-emerald-500/50"></div>
            </div>
            <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=2070" class="rounded-2xl opacity-80" />
          </div>
        </div>
      </div>
    </header>

    <!-- Features Grid -->
    <section id="features" class="bg-slate-50 py-32">
      <div class="mx-auto max-w-7xl px-6">
        <div class="mb-20 text-center">
          <h2 class="text-4xl font-bold tracking-tight text-slate-900">Built for Enterprise Accuracy</h2>
          <p class="mt-4 text-lg text-slate-500">We didn't just build another chatbot. We built a precision retrieval engine.</p>
        </div>

        <div class="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-4">
          <div 
            v-for="feature in features" 
            :key="feature.title"
            class="rounded-[2rem] border border-slate-100 bg-white p-8 transition-all duration-300 hover:-translate-y-2 hover:shadow-xl"
          >
            <div :class="[feature.bg, feature.color]" class="mb-6 flex size-14 items-center justify-center rounded-2xl">
              <component :is="feature.icon" class="size-7" />
            </div>
            <h3 class="mb-3 text-xl font-bold text-slate-900">{{ feature.title }}</h3>
            <p class="text-sm font-medium leading-relaxed text-slate-500">{{ feature.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats -->
    <section class="bg-indigo-600 py-24">
      <div class="mx-auto grid max-w-7xl grid-cols-1 gap-12 px-6 text-center md:grid-cols-3">
        <div>
          <p class="mb-2 text-5xl font-extrabold text-white">99.8%</p>
          <p class="text-xs font-bold uppercase tracking-widest text-indigo-100">Retrieval Accuracy</p>
        </div>
        <div>
          <p class="mb-2 text-5xl font-extrabold text-white">&lt;2s</p>
          <p class="text-xs font-bold uppercase tracking-widest text-indigo-100">Response Time</p>
        </div>
        <div>
          <p class="mb-2 text-5xl font-extrabold text-white">100%</p>
          <p class="text-xs font-bold uppercase tracking-widest text-indigo-100">Local Data Sovereignty</p>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="border-t border-slate-100 bg-white py-20">
      <div class="mx-auto flex max-w-7xl flex-col items-center justify-between gap-10 px-6 md:flex-row">
        <div class="flex items-center gap-3">
          <div class="rounded-xl bg-indigo-600 p-2">
            <ShieldCheck class="size-5 text-white" />
          </div>
          <span class="text-lg font-bold tracking-tight">HR Guard</span>
        </div>
        
        <p class="text-center text-sm font-medium text-slate-400">
          © 2026 HR Guard AI. All rights reserved. Built with advanced Agentic Chunking technology.
        </p>

        <div class="flex gap-8">
          <a href="#" class="text-slate-400 transition-colors hover:text-indigo-600">Twitter</a>
          <a href="#" class="text-slate-400 transition-colors hover:text-indigo-600">LinkedIn</a>
          <a href="#" class="text-slate-400 transition-colors hover:text-indigo-600">Privacy</a>
        </div>
      </div>
    </footer>
  </div>
</template>
