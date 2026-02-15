<script setup>
import { X, Mail, Lock, ShieldCheck } from 'lucide-vue-next'

const emit = defineEmits(['close'])
const isLogin = ref(true)

const toggleMode = () => isLogin.value = !isLogin.value
</script>

<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-sm p-4">
    <div class="bg-white w-full max-w-md rounded-3xl shadow-2xl overflow-hidden border border-slate-100 animate-in fade-in zoom-in duration-300">
      <div class="p-8 relative">
        <button @click="$emit('close')" class="absolute top-6 right-6 text-slate-400 hover:text-slate-600 transition-colors">
          <X class="w-6 h-6" />
        </button>

        <div class="text-center mb-10">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-indigo-50 rounded-2xl mb-4">
            <ShieldCheck class="w-8 h-8 text-indigo-600" />
          </div>
          <h2 class="text-2xl font-bold text-slate-900">{{ isLogin ? 'Welcome back' : 'Create an account' }}</h2>
          <p class="text-slate-500 mt-2">{{ isLogin ? 'Secure access to your policy data' : 'Start managing your HR policies effortlessly' }}</p>
        </div>

        <form @submit.prevent class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-1.5 ml-1">Work Email</label>
            <div class="relative">
              <Mail class="absolute left-4 top-3.5 w-5 h-5 text-slate-400" />
              <input 
                type="email" 
                placeholder="name@company.com" 
                class="w-full pl-12 pr-4 py-3.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all placeholder:text-slate-400"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-1.5 ml-1">Password</label>
            <div class="relative">
              <Lock class="absolute left-4 top-3.5 w-5 h-5 text-slate-400" />
              <input 
                type="password" 
                placeholder="••••••••" 
                class="w-full pl-12 pr-4 py-3.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all placeholder:text-slate-400"
              />
            </div>
          </div>

          <button class="w-full py-4 bg-indigo-600 text-white font-bold rounded-xl shadow-lg shadow-indigo-200 hover:bg-indigo-700 hover:-translate-y-0.5 active:translate-y-0 transition-all">
            {{ isLogin ? 'Sign In' : 'Create Account' }}
          </button>
        </form>

        <div class="mt-8 pt-6 border-t border-slate-100 text-center">
          <p class="text-sm text-slate-600">
            {{ isLogin ? "Don't have an account?" : "Already have an account?" }}
            <button @click="toggleMode" class="text-indigo-600 font-bold hover:underline">
              {{ isLogin ? 'Sign up' : 'Sign in' }}
            </button>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
