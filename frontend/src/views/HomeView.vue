<template>
  <div class="min-h-screen bg-white overflow-hidden">
    <!-- Hero Section -->
    <section class="relative pt-32 pb-20 lg:pt-48 lg:pb-32">
      <!-- Decorative Background -->
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full z-0 pointer-events-none">
        <div class="absolute top-[-10%] left-[-10%] w-[60%] h-[60%] bg-brand-50 rounded-full blur-[120px] opacity-60"></div>
        <div class="absolute bottom-[10%] right-[-10%] w-[50%] h-[50%] bg-violet-50 rounded-full blur-[120px] opacity-60"></div>
      </div>

      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="text-center max-w-4xl mx-auto">
          <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-brand-50 border border-brand-100 text-brand-700 text-sm font-bold mb-8 animate-fade-in">
            <span class="flex h-2 w-2 rounded-full bg-brand-500 animate-ping"></span>
            Next-Gen Property Intelligence
          </div>
          
          <h1 class="text-6xl lg:text-8xl font-display font-extrabold text-primary-950 mb-8 tracking-tight leading-[1.1]">
            Decisions Powered by <br />
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-600 via-brand-500 to-violet-600">Specialist Agents</span>
          </h1>
          
          <p class="text-xl text-primary-600 mb-12 max-w-2xl mx-auto leading-relaxed font-medium">
            PropertyIntel deploys a swarm of specialized AI agents to analyze flood risks, school quality, transit links, and market sentiment in real-time.
          </p>
          
          <div class="flex flex-col sm:flex-row gap-6 justify-center items-center">
            <RouterLink to="/register" class="btn-primary text-lg px-12 py-4 w-full sm:w-auto group">
              Get Started Free
              <ArrowRightIcon class="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
            </RouterLink>
            <RouterLink to="/login" class="btn-secondary text-lg px-12 py-4 w-full sm:w-auto">
              View Demo
            </RouterLink>
          </div>
        </div>

        <!-- Agent Swarm Visualization -->
        <div class="mt-32 grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-6 animate-fade-in">
          <div v-for="(agent, index) in agents" :key="index" class="glass-card p-6 group hover:border-brand-200 transition-all duration-500">
            <div class="w-12 h-12 rounded-xl bg-primary-50 flex items-center justify-center mb-4 group-hover:bg-brand-600 group-hover:text-white transition-colors">
              <component :is="agent.icon" class="w-6 h-6" />
            </div>
            <h4 class="text-sm font-bold text-primary-900 mb-1">{{ agent.name }}</h4>
            <p class="text-xs text-primary-500">{{ agent.status }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-32 relative bg-primary-50/50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-24 items-center">
          <div class="relative">
            <div class="aspect-square rounded-3xl overflow-hidden border border-white shadow-premium relative group">
              <img src="https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80" alt="Property" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" />
              <div class="absolute inset-0 bg-gradient-to-t from-primary-950/40 to-transparent"></div>
              
              <!-- Floating Agent Data -->
              <div class="absolute top-8 right-8 glass-card p-4 border-brand-200 animate-float">
                <div class="flex items-center gap-3">
                  <div class="w-2 h-2 rounded-full bg-brand-500 animate-pulse"></div>
                  <span class="text-xs font-bold text-brand-600 uppercase tracking-widest">FloodAgent Active</span>
                </div>
                <p class="text-lg font-bold text-primary-900 mt-1">Risk Score: 1.2/5</p>
              </div>
            </div>
          </div>
          
          <div>
            <h2 class="text-brand-600 font-bold text-sm uppercase tracking-[0.3em] mb-4">The Intelligence Engine</h2>
            <h3 class="text-4xl lg:text-5xl font-display font-extrabold text-primary-900 mb-8 leading-tight">
              Holistic scoring through <br />
              <span class="text-brand-600">Agent Aggregation.</span>
            </h3>
            <p class="text-lg text-primary-600 mb-10 leading-relaxed">
              Our Portfolio Manager Agent (PMA) synthesizes data from 10+ specialist agents to provide a single, weighted investment score for every asset.
            </p>
            <div class="space-y-6">
              <div v-for="feature in features" :key="feature.title" class="flex gap-6 p-6 rounded-2xl bg-white border border-primary-100 hover:border-brand-200 transition-colors">
                <div class="flex-shrink-0 w-12 h-12 bg-brand-50 rounded-xl flex items-center justify-center text-brand-600">
                  <component :is="feature.icon" class="w-6 h-6" />
                </div>
                <div>
                  <h4 class="text-xl font-bold text-primary-900 mb-2">{{ feature.title }}</h4>
                  <p class="text-primary-500 leading-relaxed">{{ feature.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { 
  ArrowRightIcon, 
  ShieldCheckIcon, 
  AcademicCapIcon, 
  TruckIcon, 
  ChartBarIcon, 
  SparklesIcon,
  MagnifyingGlassIcon,
  GlobeAltIcon,
  CpuChipIcon
} from '@heroicons/vue/24/outline'

const agents = [
  { name: 'FloodAgent', status: 'Scanning EH11...', icon: ShieldCheckIcon },
  { name: 'SchoolAgent', status: 'Rating Catchments', icon: AcademicCapIcon },
  { name: 'TransitAgent', status: 'Mapping Links', icon: TruckIcon },
  { name: 'MarketAgent', status: 'Analyzing Trends', icon: ChartBarIcon },
  { name: 'SentimentAgent', status: 'Parsing Reviews', icon: SparklesIcon },
]

const features = [
  {
    title: 'Real-time Risk Assessment',
    description: 'Continuous monitoring of environmental and regulatory risks across your entire portfolio.',
    icon: MagnifyingGlassIcon
  },
  {
    title: 'Global Market Context',
    description: 'Compare local property performance against national and international benchmarks.',
    icon: GlobeAltIcon
  },
  {
    title: 'Automated Due Diligence',
    description: 'Reduce weeks of research to seconds with our automated agent-driven reporting.',
    icon: CpuChipIcon
  }
]
</script>
