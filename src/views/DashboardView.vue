<template>
  <div class="min-h-screen bg-primary-50/50 p-4 lg:p-8 animate-fade-in">
    <!-- Welcome Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-10">
      <div>
        <h1 class="text-4xl font-display font-extrabold text-primary-950 tracking-tight">
          Welcome back, <span class="text-brand-600">{{ authStore.user?.full_name?.split(' ')[0] || 'User' }}</span>
        </h1>
        <p class="text-primary-500 font-medium mt-2">
          Your agent swarm has processed <span class="text-brand-600 font-bold">124 new data points</span> since your last login.
        </p>
      </div>
      <div class="flex items-center gap-3">
        <button class="btn-secondary flex items-center gap-2">
          <ArrowDownTrayIcon class="w-5 h-5" />
          Export Intelligence
        </button>
        <RouterLink to="/properties/create" class="btn-primary flex items-center gap-2">
          <PlusIcon class="w-5 h-5" />
          Deploy New Asset
        </RouterLink>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
      <div v-for="stat in stats" :key="stat.label" class="glass-card p-6 group cursor-pointer hover:shadow-premium transition-all duration-300">
        <div class="flex items-center justify-between mb-4">
          <div :class="['p-3 rounded-2xl transition-all duration-300 group-hover:scale-110', stat.bgClass, stat.textClass]">
            <component :is="stat.icon" class="w-6 h-6" />
          </div>
          <span :class="['text-xs font-bold px-2 py-1 rounded-lg', stat.trend > 0 ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-600']">
            {{ stat.trend > 0 ? '↑' : '↓' }} {{ Math.abs(stat.trend) }}%
          </span>
        </div>
        <p class="text-xs font-bold text-primary-400 uppercase tracking-widest">{{ stat.label }}</p>
        <p class="text-3xl font-display font-bold text-primary-900 mt-1">{{ stat.value }}</p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Main Chart Area -->
      <div class="lg:col-span-2 space-y-8">
        <div class="glass-card p-8">
          <div class="flex items-center justify-between mb-8">
            <h3 class="text-xl font-bold text-primary-900">Portfolio Performance</h3>
            <select class="bg-primary-50 border-none rounded-lg text-sm font-bold text-primary-600 focus:ring-2 focus:ring-brand-500">
              <option>Last 12 Months</option>
              <option>Last 30 Days</option>
            </select>
          </div>
          
          <div class="h-80 flex items-end justify-between gap-3 px-2">
            <div v-for="i in 12" :key="i" 
              class="flex-1 bg-brand-100 rounded-t-xl hover:bg-brand-500 transition-all duration-500 relative group"
              :style="{ height: Math.random() * 70 + 20 + '%' }"
            >
              <div class="absolute -top-10 left-1/2 -translate-x-1/2 bg-primary-900 text-white text-[10px] font-bold py-1.5 px-3 rounded-lg opacity-0 group-hover:opacity-100 transition-all duration-300 whitespace-nowrap">
                £{{ (Math.random() * 100).toFixed(1) }}k
              </div>
            </div>
          </div>
          <div class="flex justify-between mt-6 px-2">
            <span v-for="m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']" :key="m" class="text-[10px] font-bold text-primary-400 uppercase tracking-widest">{{ m }}</span>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="glass-card overflow-hidden">
          <div class="p-8 border-b border-primary-100">
            <h3 class="text-xl font-bold text-primary-900">Agent Activity Logs</h3>
          </div>
          <div class="divide-y divide-primary-50">
            <div v-for="i in 4" :key="i" class="p-6 flex items-center justify-between hover:bg-primary-50/50 transition-colors group">
              <div class="flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl bg-primary-50 flex items-center justify-center text-brand-600 group-hover:bg-brand-600 group-hover:text-white transition-colors">
                  <DocumentTextIcon class="w-6 h-6" />
                </div>
                <div>
                  <p class="font-bold text-primary-900">FloodAgent Scan Complete</p>
                  <p class="text-sm text-primary-500">124 George Street, Edinburgh • <span class="text-emerald-600 font-medium">Low Risk</span></p>
                </div>
              </div>
              <span class="text-xs font-bold text-primary-400">2h ago</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar Content -->
      <div class="space-y-8">
        <!-- AI Insights Card -->
        <div class="p-8 rounded-3xl bg-gradient-to-br from-brand-600 to-violet-700 text-white shadow-premium relative overflow-hidden group">
          <div class="relative z-10">
            <div class="w-12 h-12 bg-white/20 backdrop-blur-md rounded-xl flex items-center justify-center mb-6">
              <SparklesIcon class="w-6 h-6 text-white" />
            </div>
            <h3 class="text-2xl font-display font-bold mb-4">AI Strategy Insight</h3>
            <p class="text-brand-50/80 leading-relaxed mb-8">
              "Market data suggests a 12% increase in rental demand for EH11. Consider adjusting your portfolio weight."
            </p>
            <button class="w-full py-4 bg-white text-brand-600 rounded-xl font-bold text-sm hover:bg-brand-50 transition-colors">
              View Full Analysis
            </button>
          </div>
          <!-- Decorative circles -->
          <div class="absolute -right-10 -bottom-10 w-40 h-40 bg-white/10 rounded-full blur-3xl group-hover:scale-150 transition-transform duration-700"></div>
        </div>

        <!-- Quick Actions -->
        <div class="glass-card p-8">
          <h3 class="text-lg font-bold text-primary-900 mb-6">Quick Actions</h3>
          <div class="grid grid-cols-2 gap-4">
            <button v-for="action in quickActions" :key="action.label" class="p-4 rounded-2xl bg-primary-50 hover:bg-brand-50 hover:text-brand-600 transition-all duration-200 text-center group">
              <component :is="action.icon" class="w-6 h-6 mx-auto mb-2 text-primary-400 group-hover:text-brand-600" />
              <span class="text-xs font-bold">{{ action.label }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { 
  CurrencyPoundIcon, 
  HomeIcon, 
  UserGroupIcon, 
  ChartBarIcon,
  PlusIcon,
  ArrowDownTrayIcon,
  DocumentTextIcon,
  SparklesIcon,
  ShieldCheckIcon,
  MagnifyingGlassIcon,
  BellIcon,
  Cog6ToothIcon
} from '@heroicons/vue/24/outline'

const authStore = useAuthStore()

const stats = [
  { label: 'Portfolio Value', value: '£2.4M', trend: 12.5, icon: CurrencyPoundIcon, bgClass: 'bg-brand-50', textClass: 'text-brand-600' },
  { label: 'Active Assets', value: '12', trend: 8.2, icon: HomeIcon, bgClass: 'bg-violet-50', textClass: 'text-violet-600' },
  { label: 'Total Tenants', value: '48', trend: -2.4, icon: UserGroupIcon, bgClass: 'bg-emerald-50', textClass: 'text-emerald-600' },
  { label: 'Avg. Yield', value: '6.2%', trend: 4.1, icon: ChartBarIcon, bgClass: 'bg-amber-50', textClass: 'text-amber-600' },
]

const quickActions = [
  { label: 'New Scan', icon: MagnifyingGlassIcon },
  { label: 'Security', icon: ShieldCheckIcon },
  { label: 'Alerts', icon: BellIcon },
  { label: 'Settings', icon: Cog6ToothIcon },
]
</script>
