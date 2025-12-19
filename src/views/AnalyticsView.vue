<template>
  <div class="min-h-screen bg-primary-50/50 p-4 lg:p-8">
    <!-- Header Section -->
    <div class="mb-8 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div>
        <h1 class="text-3xl font-display font-extrabold text-primary-900 tracking-tight">
          Portfolio <span class="text-brand-600">Intelligence</span>
        </h1>
        <p class="text-primary-500 mt-1">AI-powered market analysis and portfolio optimization</p>
      </div>
      <div class="flex items-center gap-3">
        <button class="btn-secondary flex items-center gap-2">
          <ArrowDownTrayIcon class="w-5 h-5" />
          Export Report
        </button>
        <button class="btn-primary flex items-center gap-2">
          <SparklesIcon class="w-5 h-5" />
          Run AI Audit
        </button>
      </div>
    </div>

    <!-- Key Metrics Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div v-for="metric in metrics" :key="metric.label" class="glass-card p-6 hover:shadow-premium transition-all duration-300 group">
        <div class="flex items-center justify-between mb-4">
          <div :class="[metric.bg, 'p-3 rounded-xl group-hover:scale-110 transition-transform duration-300']">
            <component :is="metric.icon" :class="[metric.color, 'w-6 h-6']" />
          </div>
          <span :class="[metric.trend > 0 ? 'text-emerald-600 bg-emerald-50' : 'text-rose-600 bg-rose-50', 'text-xs font-bold px-2 py-1 rounded-lg']">
            {{ metric.trend > 0 ? '+' : '' }}{{ metric.trend }}%
          </span>
        </div>
        <h3 class="text-primary-500 text-sm font-medium">{{ metric.label }}</h3>
        <p class="text-2xl font-display font-bold text-primary-900 mt-1">{{ metric.value }}</p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Market Trends Chart (Placeholder) -->
      <div class="lg:col-span-2 glass-card p-8">
        <div class="flex items-center justify-between mb-8">
          <div>
            <h2 class="text-xl font-bold text-primary-900">Market Performance</h2>
            <p class="text-sm text-primary-500">Price trends vs. Regional average</p>
          </div>
          <select class="bg-primary-50 border-none rounded-lg text-sm font-medium text-primary-700 focus:ring-2 focus:ring-brand-500">
            <option>Last 12 Months</option>
            <option>Last 3 Years</option>
          </select>
        </div>
        
        <div class="h-[350px] flex items-end justify-between gap-2 px-4">
          <div v-for="(bar, i) in chartData" :key="i" class="flex-1 flex flex-col items-center gap-2 group">
            <div class="w-full bg-primary-100 rounded-t-lg relative overflow-hidden" :style="{ height: bar.value + '%' }">
              <div class="absolute inset-0 bg-gradient-to-t from-brand-600 to-brand-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>
            <span class="text-[10px] font-medium text-primary-400 uppercase tracking-wider">{{ bar.label }}</span>
          </div>
        </div>
      </div>

      <!-- AI Insights Panel -->
      <div class="glass-card p-8 bg-gradient-to-br from-white to-brand-50/30">
        <div class="flex items-center gap-2 mb-6">
          <div class="p-2 bg-brand-100 rounded-lg">
            <CpuChipIcon class="w-5 h-5 text-brand-600" />
          </div>
          <h2 class="text-xl font-bold text-primary-900">AI Insights</h2>
        </div>

        <div class="space-y-6">
          <div v-for="(insight, i) in insights" :key="i" class="relative pl-6 border-l-2 border-brand-100">
            <div class="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-white border-2 border-brand-500"></div>
            <h4 class="text-sm font-bold text-primary-900 mb-1">{{ insight.title }}</h4>
            <p class="text-sm text-primary-600 leading-relaxed">{{ insight.description }}</p>
            <div class="mt-2 flex items-center gap-2">
              <span class="text-[10px] font-bold uppercase tracking-widest text-brand-500">{{ insight.tag }}</span>
              <span class="text-[10px] text-primary-400">• {{ insight.time }}</span>
            </div>
          </div>
        </div>

        <button class="w-full mt-8 py-4 bg-primary-900 text-white rounded-xl font-bold text-sm hover:bg-black transition-colors flex items-center justify-center gap-2">
          View Full Strategy
          <ArrowRightIcon class="w-4 h-4" />
        </button>
      </div>
    </div>

    <!-- Risk Assessment Section -->
    <div class="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="glass-card p-8">
        <h2 class="text-xl font-bold text-primary-900 mb-6">Risk Distribution</h2>
        <div class="space-y-6">
          <div v-for="risk in risks" :key="risk.label">
            <div class="flex justify-between text-sm mb-2">
              <span class="font-medium text-primary-700">{{ risk.label }}</span>
              <span class="font-bold text-primary-900">{{ risk.value }}%</span>
            </div>
            <div class="h-2 bg-primary-100 rounded-full overflow-hidden">
              <div :class="[risk.color, 'h-full rounded-full']" :style="{ width: risk.value + '%' }"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="glass-card p-8">
        <h2 class="text-xl font-bold text-primary-900 mb-6">Optimization Queue</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div v-for="opt in optimizations" :key="opt.title" class="p-4 rounded-2xl border border-primary-100 hover:border-brand-200 hover:bg-brand-50/30 transition-all cursor-pointer group">
            <div :class="[opt.bg, 'w-10 h-10 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform']">
              <component :is="opt.icon" :class="[opt.color, 'w-5 h-5']" />
            </div>
            <h4 class="text-sm font-bold text-primary-900 mb-1">{{ opt.title }}</h4>
            <p class="text-xs text-primary-500 leading-relaxed">{{ opt.desc }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { 
  ArrowDownTrayIcon, 
  SparklesIcon, 
  CpuChipIcon, 
  ArrowRightIcon,
  CurrencyPoundIcon,
  ChartBarIcon,
  HomeIcon,
  UserGroupIcon,
  FireIcon,
  BanknotesIcon,
  ScaleIcon,
  ShieldCheckIcon
} from '@heroicons/vue/24/outline'

const metrics = [
  { 
    label: 'Portfolio Value', 
    value: '£4.2M', 
    trend: 12.5, 
    icon: CurrencyPoundIcon, 
    color: 'text-brand-600', 
    bg: 'bg-brand-50' 
  },
  { 
    label: 'Avg. Yield', 
    value: '5.8%', 
    trend: 0.4, 
    icon: ChartBarIcon, 
    color: 'text-emerald-600', 
    bg: 'bg-emerald-50' 
  },
  { 
    label: 'Total Assets', 
    value: '12', 
    trend: 2, 
    icon: HomeIcon, 
    color: 'text-violet-600', 
    bg: 'bg-violet-50' 
  },
  { 
    label: 'Active Tenants', 
    value: '28', 
    trend: -1.2, 
    icon: UserGroupIcon, 
    color: 'text-blue-600', 
    bg: 'bg-blue-50' 
  },
]

const chartData = [
  { label: 'Jan', value: 35 },
  { label: 'Feb', value: 42 },
  { label: 'Mar', value: 48 },
  { label: 'Apr', value: 61 },
  { label: 'May', value: 55 },
  { label: 'Jun', value: 67 },
  { label: 'Jul', value: 72 },
  { label: 'Aug', value: 65 },
  { label: 'Sep', value: 78 },
  { label: 'Oct', value: 85 },
  { label: 'Nov', value: 82 },
  { label: 'Dec', value: 90 },
]

const insights = [
  { 
    title: 'Yield Optimization', 
    description: 'Properties in EH11 are showing 15% higher rental demand than current portfolio average.', 
    tag: 'Opportunity',
    time: '2h ago'
  },
  { 
    title: 'Risk Alert', 
    description: 'Upcoming regulatory changes in short-term lets may impact 3 of your city-center assets.', 
    tag: 'Compliance',
    time: '5h ago'
  },
  { 
    title: 'Portfolio Rebalance', 
    description: 'Consider divesting from low-yield commercial units to capitalize on residential growth.', 
    tag: 'Strategy',
    time: '1d ago'
  }
]

const risks = [
  { label: 'Market Volatility', value: 25, color: 'bg-emerald-500' },
  { label: 'Regulatory Risk', value: 45, color: 'bg-amber-500' },
  { label: 'Tenant Default', value: 15, color: 'bg-emerald-400' },
  { label: 'Maintenance Liability', value: 65, color: 'bg-rose-500' },
]

const optimizations = [
  { 
    title: 'Energy Retrofit', 
    desc: 'Improve EPC ratings to boost value by 8%', 
    icon: FireIcon, 
    color: 'text-orange-600', 
    bg: 'bg-orange-50' 
  },
  { 
    title: 'Refinancing', 
    desc: 'Current rates allow for 1.2% interest saving', 
    icon: BanknotesIcon, 
    color: 'text-emerald-600', 
    bg: 'bg-emerald-50' 
  },
  { 
    title: 'Legal Audit', 
    desc: 'Update lease agreements for new standards', 
    icon: ScaleIcon, 
    color: 'text-blue-600', 
    bg: 'bg-blue-50' 
  },
  { 
    title: 'Security Upgrade', 
    desc: 'Smart monitoring reduces insurance by 5%', 
    icon: ShieldCheckIcon, 
    color: 'text-violet-600', 
    bg: 'bg-violet-50' 
  },
]
</script>

<style scoped>
.glass-card {
  @apply bg-white/80 backdrop-blur-md border border-white/20 shadow-glass rounded-2xl;
}
</style>
