<script setup>
import { 
  User, 
  Mail, 
  Bell, 
  Lock, 
  ChevronRight,
  Camera
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
  <div class="max-w-4xl mx-auto py-12 px-6">
    <div class="flex items-center gap-6 mb-12">
      <div class="relative">
        <img :src="user.avatar" class="w-24 h-24 rounded-3xl border-4 border-white shadow-xl" />
        <button class="absolute -bottom-2 -right-2 p-2 bg-indigo-600 text-white rounded-lg shadow-lg hover:bg-indigo-700 transition-colors">
          <Camera class="w-4 h-4" />
        </button>
      </div>
      <div>
        <h2 class="text-3xl font-bold text-slate-900">{{ user.name }}</h2>
        <p class="text-slate-500 font-medium">{{ user.role }} • {{ user.company }}</p>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <!-- Account Info -->
      <section class="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm">
        <h3 class="text-lg font-bold text-slate-900 mb-6 flex items-center gap-2">
          <User class="w-5 h-5 text-indigo-500" />
          Personal Information
        </h3>
        
        <div class="space-y-6">
          <div class="group cursor-pointer">
            <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Full Name</p>
            <div class="flex items-center justify-between">
              <p class="text-slate-900 font-semibold">{{ user.name }}</p>
              <ChevronRight class="w-4 h-4 text-slate-300 group-hover:text-indigo-500 transition-colors" />
            </div>
          </div>

          <div class="group cursor-pointer">
            <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Email Address</p>
            <div class="flex items-center justify-between">
              <p class="text-slate-900 font-semibold">{{ user.email }}</p>
              <ChevronRight class="w-4 h-4 text-slate-300 group-hover:text-indigo-500 transition-colors" />
            </div>
          </div>
        </div>
      </section>

      <!-- Security & Settings -->
      <section class="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm">
        <h3 class="text-lg font-bold text-slate-900 mb-6 flex items-center gap-2">
          <ShieldCheck class="w-5 h-5 text-indigo-500" />
          Security & Preferences
        </h3>

        <div class="space-y-4">
          <button class="w-full flex items-center justify-between p-4 rounded-xl border border-slate-50 hover:bg-slate-50 transition-colors text-left">
            <div class="flex items-center gap-4">
              <div class="p-2 bg-blue-50 text-blue-600 rounded-lg">
                <Lock class="w-5 h-5" />
              </div>
              <div>
                <p class="font-bold text-slate-900">Change Password</p>
                <p class="text-xs text-slate-500">Last changed 3 months ago</p>
              </div>
            </div>
            <ChevronRight class="w-4 h-4 text-slate-300" />
          </button>

          <button class="w-full flex items-center justify-between p-4 rounded-xl border border-slate-50 hover:bg-slate-50 transition-colors text-left">
            <div class="flex items-center gap-4">
              <div class="p-2 bg-orange-50 text-orange-600 rounded-lg">
                <Bell class="w-5 h-5" />
              </div>
              <div>
                <p class="font-bold text-slate-900">Notifications</p>
                <p class="text-xs text-slate-500">Configure your email alerts</p>
              </div>
            </div>
            <ChevronRight class="w-4 h-4 text-slate-300" />
          </button>
        </div>
      </section>
    </div>
  </div>
</template>
