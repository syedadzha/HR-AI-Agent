<script setup>
import { X, Mail, Lock, ShieldCheck } from 'lucide-vue-next'

const emit = defineEmits(['close'])
const isLogin = ref(true)

const toggleMode = () => isLogin.value = !isLogin.value
</script>

<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 p-4 backdrop-blur-sm">
    <div class="animate-in fade-in zoom-in w-full max-w-md overflow-hidden rounded-3xl border border-slate-100 bg-white shadow-2xl duration-300">
      <div class="relative p-8">
        <button class="absolute right-6 top-6 text-slate-400 transition-colors hover:text-slate-600" @click="$emit('close')">
          <X class="size-6" />
        </button>

        <div class="mb-10 text-center">
          <div class="mb-4 inline-flex size-16 items-center justify-center rounded-2xl bg-indigo-50">
            <ShieldCheck class="size-8 text-indigo-600" />
          </div>
          <h2 class="text-2xl font-bold text-slate-900">{{ isLogin ? 'Welcome back' : 'Create an account' }}</h2>
          <p class="mt-2 text-slate-500">{{ isLogin ? 'Secure access to your policy data' : 'Start managing your HR policies effortlessly' }}</p>
        </div>

        <form class="space-y-4" @submit.prevent>
          <div>
            <label class="mb-1.5 ml-1 block text-sm font-semibold text-slate-700">Work Email</label>
            <div class="relative">
              <Mail class="absolute left-4 top-3.5 size-5 text-slate-400" />
              <input 
                type="email" 
                placeholder="name@company.com" 
                class="w-full rounded-xl border border-slate-200 bg-slate-50 py-3.5 pl-12 pr-4 transition-all placeholder:text-slate-400 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
              />
            </div>
          </div>

          <div>
            <label class="mb-1.5 ml-1 block text-sm font-semibold text-slate-700">Password</label>
            <div class="relative">
              <Lock class="absolute left-4 top-3.5 size-5 text-slate-400" />
              <input 
                type="password" 
                placeholder="••••••••" 
                class="w-full rounded-xl border border-slate-200 bg-slate-50 py-3.5 pl-12 pr-4 transition-all placeholder:text-slate-400 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
              />
            </div>
          </div>

          <button class="w-full rounded-xl bg-indigo-600 py-4 font-bold text-white shadow-lg shadow-indigo-200 transition-all hover:-translate-y-0.5 hover:bg-indigo-700 active:translate-y-0">
            {{ isLogin ? 'Sign In' : 'Create Account' }}
          </button>
        </form>

        <div class="mt-8 border-t border-slate-100 pt-6 text-center">
          <p class="text-sm text-slate-600">
            {{ isLogin ? "Don't have an account?" : "Already have an account?" }}
            <button class="font-bold text-indigo-600 hover:underline" @click="toggleMode">
              {{ isLogin ? 'Sign up' : 'Sign in' }}
            </button>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
