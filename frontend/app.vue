<script setup>
const isAppLaunched = ref(false)
const activeTab = ref('chat')
const showAuth = ref(false)

const setTab = (tab) => {
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
  <div class="font-sans text-slate-900 overflow-x-hidden">
    <!-- Landing Page View -->
    <div v-if="!isAppLaunched" class="animate-in fade-in duration-700">
      <LandingPage @getStarted="launchApp" />
    </div>

    <!-- Main Application View -->
    <div v-else class="flex h-screen bg-white overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-500">
      <!-- Main Sidebar -->
      <Sidebar 
        :activeTab="activeTab" 
        @setTab="setTab" 
        @openAuth="toggleAuth"
      />

      <!-- Main Content Area -->
      <main class="flex-1 flex flex-col h-full bg-white relative">
        <!-- Transition wrapper for views -->
        <div class="flex-1 overflow-hidden">
          <div v-if="activeTab === 'chat'" class="h-full">
            <ChatInterface />
          </div>
          
          <div v-if="activeTab === 'files'" class="h-full overflow-y-auto">
            <div class="p-8 max-w-6xl mx-auto w-full">
              <header class="mb-10">
                <h2 class="text-3xl font-bold tracking-tight">Policy Library</h2>
                <p class="text-slate-500 mt-2">Manage and upload your HR documentation for analysis.</p>
              </header>
              
              <div class="space-y-12 pb-20">
                <section>
                  <h3 class="text-sm font-bold text-slate-400 uppercase tracking-widest mb-6">Quick Upload</h3>
                  <FileUpload />
                </section>
                
                <section>
                  <h3 class="text-sm font-bold text-slate-400 uppercase tracking-widest mb-6">Indexed Documents</h3>
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
