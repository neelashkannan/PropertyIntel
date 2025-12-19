<template>
  <aside class="fixed inset-y-0 left-0 w-72 bg-white border-r border-primary-100 z-50 hidden lg:flex flex-col">
    <!-- Logo -->
    <div class="p-8">
      <RouterLink to="/" class="flex items-center gap-3 group">
        <div class="w-10 h-10 bg-brand-600 rounded-xl flex items-center justify-center shadow-lg shadow-brand-200 group-hover:scale-110 transition-transform duration-300">
          <HomeIcon class="w-6 h-6 text-white" />
        </div>
        <span class="text-xl font-display font-black tracking-tighter text-primary-900">
          Property<span class="text-brand-600">Intel</span>
        </span>
      </RouterLink>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 px-4 space-y-1.5">
      <div class="px-4 mb-4">
        <span class="text-[10px] font-black text-primary-400 uppercase tracking-[0.2em]">Main Menu</span>
      </div>
      
      <RouterLink 
        v-for="item in navItems" 
        :key="item.path"
        :to="item.path"
        class="flex items-center gap-3 px-4 py-3.5 rounded-2xl text-sm font-bold transition-all duration-200 group"
        :class="isRouteActive(item.path) ? 'bg-brand-50 text-brand-700 shadow-sm shadow-brand-100/50' : 'text-primary-500 hover:bg-primary-50 hover:text-primary-900'"
      >
        <component 
          :is="item.icon" 
          class="w-5 h-5 transition-colors"
          :class="isRouteActive(item.path) ? 'text-brand-600' : 'text-primary-400 group-hover:text-primary-600'"
        />
        {{ item.name }}
      </RouterLink>
    </nav>

    <!-- User Profile -->
    <div class="p-6 border-t border-primary-50">
      <div class="flex items-center gap-4 p-4 rounded-2xl bg-primary-50/50 border border-primary-100/50">
        <div class="w-10 h-10 bg-brand-600 text-white rounded-xl flex items-center justify-center font-black shadow-lg shadow-brand-200">
          {{ userInitials }}
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-black text-primary-900 truncate">{{ authStore.user?.full_name || 'User' }}</p>
          <p class="text-[10px] font-bold text-emerald-600 uppercase tracking-widest">Pro Member</p>
        </div>
        <button @click="handleLogout" class="p-2 text-primary-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-all">
          <ArrowRightOnRectangleIcon class="w-5 h-5" />
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { 
  HomeIcon, 
  Squares2X2Icon, 
  BuildingOfficeIcon, 
  ChartBarIcon,
  ArrowRightOnRectangleIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const navItems = [
  { name: 'Dashboard', path: '/dashboard', icon: Squares2X2Icon },
  { name: 'Portfolio', path: '/properties', icon: BuildingOfficeIcon },
  { name: 'Analytics', path: '/analytics', icon: ChartBarIcon }
]

const isRouteActive = (path: string) => {
  if (path === '/dashboard') return route.path === '/dashboard'
  return route.path.startsWith(path)
}

const userInitials = computed(() => {
  const name = authStore.user?.full_name || 'U'
  return name.substring(0, 2).toUpperCase()
})

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
