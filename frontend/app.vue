<script setup lang="ts">
const isAppLaunched = ref(false)
const activeTab = ref('chat')
const showAuth = ref(false)

const setTab = (tab: string) => {
  activeTab.value = tab
}

const toggleAuth = () => {
  showAuth.value = !showAuth.value
}

const launchApp = () => {
  isAppLaunched.value = true
}
</script>

<template>
  <div class="overflow-x-hidden font-sans text-slate-900">
    <!-- Landing Page View -->
    <div v-if="!isAppLaunched" class="animate-in fade-in duration-700">
      <LandingPage @get-started="launchApp" />
    </div>

    <!-- Main Application View -->
    <div v-else class="animate-in fade-in slide-in-from-bottom-4 flex h-screen overflow-hidden bg-white duration-500">
      <!-- Main Sidebar -->
      <Sidebar 
        :active-tab="activeTab" 
        @set-tab="setTab" 
        @open-auth="toggleAuth"
      />

      <!-- Main Content Area -->
      <main class="relative flex h-full flex-1 flex-col bg-white">
        <!-- Transition wrapper for views -->
        <div class="flex-1 overflow-hidden">
          <div v-if="activeTab === 'chat'" class="h-full">
            <ChatInterface />
          </div>
          
          <div v-if="activeTab === 'files'" class="h-full overflow-y-auto">
            <div class="mx-auto w-full max-w-6xl p-8">
              <header class="mb-10">
                <h2 class="text-3xl font-bold tracking-tight">Policy Library</h2>
                <p class="mt-2 text-slate-500">Manage and upload your HR documentation for analysis.</p>
              </header>
              
              <div class="space-y-12 pb-20">
                <section>
                  <h3 class="mb-6 text-sm font-bold uppercase tracking-widest text-slate-400">Quick Upload</h3>
                  <FileUpload />
                </section>
                
                <section>
                  <h3 class="mb-6 text-sm font-bold uppercase tracking-widest text-slate-400">Indexed Documents</h3>
                  <FileList />
                </section>
              </div>
            </div>
          </div>

          <div v-if="activeTab === 'profile'" class="h-full overflow-y-auto">
            <UserProfile />
          </div>
        </div>
      </main>
    </div>

    <!-- Global Auth Modal -->
    <AuthModal v-if="showAuth" @close="toggleAuth" />
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

body {
  font-family: 'Plus Jakarta Sans', sans-serif;
  -webkit-font-smoothing: antialiased;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #e2e8f0;
  border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
  background: #cbd5e1;
}

/* Animations */
.animate-in {
  animation-fill-mode: forwards;
}
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes zoom-in {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
@keyframes slide-in-from-bottom-4 {
  from { transform: translateY(1rem); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
@keyframes slide-in-from-top-4 {
  from { transform: translateY(-1rem); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>
