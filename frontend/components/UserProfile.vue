<script setup>
import { 
  User, 
  Mail, 
  Bell, 
  Lock, 
  ChevronRight,
  Camera,
  ShieldCheck
} from 'lucide-vue-next'

const user = {
  name: 'John Doe',
  email: 'john@example.com',
  role: 'HR Manager',
  company: 'Innovate Corp',
  avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=John'
}
</script>

<template>
  <div class="mx-auto max-w-4xl px-6 py-12">
    <div class="mb-12 flex items-center gap-6">
      <div class="relative">
        <img :src="user.avatar" class="size-24 rounded-3xl border-4 border-white shadow-xl" />
        <button class="absolute -bottom-2 -right-2 rounded-lg bg-indigo-600 p-2 text-white shadow-lg transition-colors hover:bg-indigo-700">
          <Camera class="size-4" />
        </button>
      </div>
      <div>
        <h2 class="text-3xl font-bold text-slate-900">{{ user.name }}</h2>
        <p class="font-medium text-slate-500">{{ user.role }} • {{ user.company }}</p>
      </div>
    </div>

    <div class="grid grid-cols-1 gap-8 md:grid-cols-2">
      <!-- Account Info -->
      <section class="rounded-3xl border border-slate-100 bg-white p-8 shadow-sm">
        <h3 class="mb-6 flex items-center gap-2 text-lg font-bold text-slate-900">
          <User class="size-5 text-indigo-500" />
          Personal Information
        </h3>
        
        <div class="space-y-6">
          <div class="group cursor-pointer">
            <p class="mb-1 text-xs font-bold uppercase tracking-widest text-slate-400">Full Name</p>
            <div class="flex items-center justify-between">
              <p class="font-semibold text-slate-900">{{ user.name }}</p>
              <ChevronRight class="size-4 text-slate-300 transition-colors group-hover:text-indigo-500" />
            </div>
          </div>

          <div class="group cursor-pointer">
            <p class="mb-1 text-xs font-bold uppercase tracking-widest text-slate-400">Email Address</p>
            <div class="flex items-center justify-between">
              <p class="font-semibold text-slate-900">{{ user.email }}</p>
              <ChevronRight class="size-4 text-slate-300 transition-colors group-hover:text-indigo-500" />
            </div>
          </div>
        </div>
      </section>

      <!-- Security & Settings -->
      <section class="rounded-3xl border border-slate-100 bg-white p-8 shadow-sm">
        <h3 class="mb-6 flex items-center gap-2 text-lg font-bold text-slate-900">
          <ShieldCheck class="size-5 text-indigo-500" />
          Security & Preferences
        </h3>

        <div class="space-y-4">
          <button class="flex w-full items-center justify-between rounded-xl border border-slate-50 p-4 text-left transition-colors hover:bg-slate-50">
            <div class="flex items-center gap-4">
              <div class="rounded-lg bg-blue-50 p-2 text-blue-600">
                <Lock class="size-5" />
              </div>
              <div>
                <p class="font-bold text-slate-900">Change Password</p>
                <p class="text-xs text-slate-500">Last changed 3 months ago</p>
              </div>
            </div>
            <ChevronRight class="size-4 text-slate-300" />
          </button>

          <button class="flex w-full items-center justify-between rounded-xl border border-slate-50 p-4 text-left transition-colors hover:bg-slate-50">
            <div class="flex items-center gap-4">
              <div class="rounded-lg bg-orange-50 p-2 text-orange-600">
                <Bell class="size-5" />
              </div>
              <div>
                <p class="font-bold text-slate-900">Notifications</p>
                <p class="text-xs text-slate-500">Configure your email alerts</p>
              </div>
            </div>
            <ChevronRight class="size-4 text-slate-300" />
          </button>
        </div>
      </section>
    </div>
  </div>
</template>
