<template>
  <header class="sticky top-0 z-50 w-full border-b border-primary-100 bg-white/80 backdrop-blur-xl">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-20">
        <div class="flex items-center gap-10">
          <RouterLink to="/" class="flex items-center gap-3 group">
            <div class="w-10 h-10 bg-brand-600 rounded-xl flex items-center justify-center shadow-lg shadow-brand-200 group-hover:scale-110 transition-transform duration-300">
              <HomeIcon class="w-6 h-6 text-white" />
            </div>
            <span class="text-xl font-display font-black tracking-tighter text-primary-900">
              Property<span class="text-brand-600">Intel</span>
            </span>
          </RouterLink>

          <nav v-if="authStore.isAuthenticated" class="hidden md:flex items-center gap-1">
            <RouterLink 
              v-for="item in navItems" 
              :key="item.path"
              :to="item.path"
              class="px-4 py-2 text-sm font-bold rounded-xl transition-all duration-200"
              :class="route.path.startsWith(item.path) ? 'bg-brand-50 text-brand-700' : 'text-primary-500 hover:text-primary-900 hover:bg-primary-50'"
            >
              {{ item.name }}
            </RouterLink>
          </nav>
        </div>

        <div class="flex items-center gap-4">
          <template v-if="authStore.isAuthenticated">
            <div class="hidden sm:flex flex-col items-end mr-2">
              <span class="text-xs font-black text-primary-900 uppercase tracking-widest">{{ authStore.user?.full_name || 'User' }}</span>
              <span class="text-[10px] font-bold text-emerald-600 uppercase tracking-widest">Pro Account</span>
            </div>
            <button 
              @click="handleLogout"
              class="p-2.5 text-primary-400 hover:text-rose-600 hover:bg-rose-50 rounded-xl transition-all duration-200"
              title="Sign Out"
            >
              <ArrowRightOnRectangleIcon class="w-6 h-6" />
            </button>
          </template>
          <template v-else>
            <RouterLink to="/login" class="text-sm font-bold text-primary-600 hover:text-primary-900 px-4">
              Sign In
            </RouterLink>
            <RouterLink to="/register" class="btn-primary px-6 py-2.5 text-sm">
              Get Started
            </RouterLink>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { 
  HomeIcon, 
  ArrowRightOnRectangleIcon 
} from '@heroicons/vue/24/outline'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const navItems = [
  { name: 'Dashboard', path: '/dashboard' },
  { name: 'Portfolio', path: '/properties' },
  { name: 'Analytics', path: '/analytics' }
]

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
