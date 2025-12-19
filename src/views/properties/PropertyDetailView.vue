<template>
  <div class="min-h-screen bg-primary-50/50 p-4 lg:p-8 animate-fade-in">
    <div v-if="loading" class="flex flex-col justify-center items-center py-32 space-y-6">
      <div class="relative">
        <div class="w-16 h-16 rounded-full border-4 border-primary-200 border-t-brand-600 animate-spin"></div>
        <div class="absolute inset-0 flex items-center justify-center">
          <div class="w-2 h-2 bg-brand-500 rounded-full animate-pulse"></div>
        </div>
      </div>
      <p class="text-primary-500 font-bold uppercase tracking-widest animate-pulse">Synchronizing Asset Data...</p>
    </div>

    <div v-else-if="property" class="max-w-7xl mx-auto space-y-8">
      <!-- Breadcrumbs & Actions -->
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <nav class="flex" aria-label="Breadcrumb">
          <ol class="flex items-center space-x-3 text-xs font-bold uppercase tracking-widest">
            <li>
              <RouterLink to="/properties" class="text-primary-400 hover:text-brand-600 transition-colors">Portfolio</RouterLink>
            </li>
            <li class="flex items-center space-x-3">
              <ChevronRightIcon class="h-4 w-4 text-primary-300" />
              <span class="text-primary-900">{{ property.house_number }} {{ property.street_name }}</span>
            </li>
          </ol>
        </nav>
        <div class="flex items-center gap-3">
          <RouterLink :to="`/properties/${property.id}/edit`" class="btn-secondary flex items-center gap-2">
            <PencilSquareIcon class="w-4 h-4" />
            Modify Asset
          </RouterLink>
          <button @click="deleteProperty" class="btn-secondary text-rose-600 hover:bg-rose-50 border-rose-100 flex items-center gap-2">
            <TrashIcon class="w-4 h-4" />
            Decommission
          </button>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 space-y-8">
          <!-- Hero Card -->
          <div class="glass-card overflow-hidden">
            <div class="aspect-video bg-primary-100 relative flex items-center justify-center overflow-hidden">
              <img src="https://images.unsplash.com/photo-1568605114967-8130f3a36994?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80" class="w-full h-full object-cover opacity-90" />
              <div class="absolute inset-0 bg-gradient-to-t from-primary-900/60 via-transparent to-transparent"></div>
              
              <div class="absolute top-6 right-6">
                <span :class="['badge text-sm px-6 py-2 shadow-lg', getEPCBadgeClass(property.epc_rating)]">
                  EPC Rating {{ property.epc_rating || '?' }}
                </span>
              </div>
              
              <div class="absolute bottom-6 left-6 flex items-center gap-3 bg-white/20 backdrop-blur-md px-4 py-2 rounded-xl border border-white/30">
                <div class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
                <span class="text-[10px] font-bold text-white uppercase tracking-widest">Live Intelligence Feed</span>
              </div>
            </div>

            <div class="p-8 lg:p-12">
              <div class="flex flex-col md:flex-row md:items-end md:justify-between gap-8 mb-12">
                <div>
                  <h1 class="text-4xl lg:text-5xl font-display font-extrabold text-primary-900 tracking-tight leading-tight">
                    {{ property.house_number }} {{ property.street_name }}
                  </h1>
                  <p class="text-xl text-primary-500 mt-3 font-medium">{{ property.postcode }}</p>
                </div>
                <div class="text-right">
                  <p class="text-xs font-bold text-primary-400 uppercase tracking-widest mb-2">Asset Valuation</p>
                  <p class="text-4xl lg:text-5xl font-display font-bold text-brand-600">
                    £{{ (property.size_sqft ? property.size_sqft * 200 : 150000).toLocaleString() }}
                  </p>
                </div>
              </div>

              <div class="grid grid-cols-2 md:grid-cols-4 gap-8 py-10 border-y border-primary-100">
                <div class="space-y-2">
                  <p class="text-xs font-bold text-primary-400 uppercase tracking-widest">Size</p>
                  <div class="flex items-baseline gap-1">
                    <span class="text-2xl font-bold text-primary-900">{{ property.size_sqft || '?' }}</span>
                    <span class="text-xs font-bold text-primary-400 uppercase">sqft</span>
                  </div>
                </div>
                <div class="space-y-2 border-l border-primary-100 pl-8">
                  <p class="text-xs font-bold text-primary-400 uppercase tracking-widest">Type</p>
                  <p class="text-2xl font-bold text-primary-900 capitalize">{{ property.property_type }}</p>
                </div>
                <div class="space-y-2 border-l border-primary-100 pl-8">
                  <p class="text-xs font-bold text-primary-400 uppercase tracking-widest">Bedrooms</p>
                  <p class="text-2xl font-bold text-primary-900">{{ property.bedrooms || '?' }}</p>
                </div>
                <div class="space-y-2 border-l border-primary-100 pl-8">
                  <p class="text-xs font-bold text-primary-400 uppercase tracking-widest">Status</p>
                  <span class="inline-flex items-center px-3 py-1 rounded-full bg-emerald-50 text-emerald-600 text-[10px] font-bold uppercase tracking-widest border border-emerald-100">Optimized</span>
                </div>
              </div>

              <!-- Detailed Specs -->
              <div class="mt-12 grid grid-cols-1 md:grid-cols-2 gap-12">
                <div>
                  <h3 class="text-lg font-bold text-primary-900 mb-6">Internal Specifications</h3>
                  <div class="space-y-4">
                    <div v-for="spec in internalSpecs" :key="spec.label" class="flex items-center justify-between py-3 border-b border-primary-50">
                      <span class="text-primary-500 font-medium">{{ spec.label }}</span>
                      <span class="text-primary-900 font-bold">{{ spec.value }}</span>
                    </div>
                  </div>
                </div>
                <div>
                  <h3 class="text-lg font-bold text-primary-900 mb-6">External Features</h3>
                  <div class="space-y-4">
                    <div v-for="feature in externalFeatures" :key="feature.label" class="flex items-center justify-between py-3 border-b border-primary-50">
                      <span class="text-primary-500 font-medium">{{ feature.label }}</span>
                      <span :class="['badge font-bold', feature.value === 'Yes' ? 'bg-emerald-50 text-emerald-600' : 'bg-primary-50 text-primary-400']">
                        {{ feature.value }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-8">
          <!-- AI Agent Swarm Card -->
          <div class="p-8 rounded-3xl bg-gradient-to-br from-brand-600 to-violet-700 text-white shadow-premium relative overflow-hidden group">
            <div class="relative z-10">
              <div class="flex items-center gap-3 mb-8">
                <div class="p-2 bg-white/20 backdrop-blur-md rounded-lg">
                  <CpuChipIcon class="w-6 h-6 text-white" />
                </div>
                <h3 class="text-xl font-display font-bold">Agent Swarm</h3>
              </div>
              
              <div class="space-y-4">
                <div v-for="agent in agents" :key="agent.name" class="flex items-center justify-between bg-white/10 backdrop-blur-sm p-4 rounded-2xl border border-white/10">
                  <div class="flex items-center gap-3">
                    <component :is="agent.icon" class="w-5 h-5 text-brand-200" />
                    <span class="text-sm font-bold">{{ agent.name }}</span>
                  </div>
                  <span class="text-[10px] font-black bg-white text-brand-600 px-2 py-0.5 rounded uppercase tracking-widest">Active</span>
                </div>
              </div>

              <button class="w-full mt-8 py-4 bg-white text-brand-600 rounded-xl font-bold text-sm hover:bg-brand-50 transition-all transform hover:scale-[1.02] active:scale-[0.98]">
                Run Deep Audit
              </button>
            </div>
            <div class="absolute -right-10 -bottom-10 w-40 h-40 bg-white/10 rounded-full blur-3xl group-hover:scale-150 transition-transform duration-700"></div>
          </div>

          <!-- Market Context -->
          <div class="glass-card p-8">
            <h3 class="text-lg font-bold text-primary-900 mb-6">Market Context</h3>
            <div class="space-y-6">
              <div>
                <div class="flex justify-between text-sm mb-2">
                  <span class="text-primary-500 font-medium">Regional Demand</span>
                  <span class="text-emerald-600 font-bold">High</span>
                </div>
                <div class="h-2 bg-primary-100 rounded-full overflow-hidden">
                  <div class="h-full bg-emerald-500 rounded-full" style="width: 85%"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-sm mb-2">
                  <span class="text-primary-500 font-medium">Price Growth (12m)</span>
                  <span class="text-brand-600 font-bold">+4.2%</span>
                </div>
                <div class="h-2 bg-primary-100 rounded-full overflow-hidden">
                  <div class="h-full bg-brand-500 rounded-full" style="width: 65%"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { propertyService } from '@/services/api'
import type { Property } from '@/types'
import { 
  ChevronRightIcon,
  PencilSquareIcon,
  TrashIcon,
  CpuChipIcon,
  ShieldCheckIcon,
  AcademicCapIcon,
  TruckIcon,
  ChartBarIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()
const router = useRouter()
const property = ref<Property | null>(null)
const loading = ref(true)

const internalSpecs = computed(() => [
  { label: 'Heating System', value: 'Gas Central' },
  { label: 'Glazing', value: 'Double Glazed' },
  { label: 'Kitchen Grade', value: 'Premium' },
  { label: 'Flooring', value: 'Hardwood' }
])

const externalFeatures = computed(() => [
  { label: 'Private Garden', value: 'Yes' },
  { label: 'Parking Space', value: 'Yes' },
  { label: 'Solar Panels', value: 'No' },
  { label: 'EV Charging', value: 'Yes' }
])

const agents = [
  { name: 'Valuation Bot', icon: ChartBarIcon },
  { name: 'Risk Analyzer', icon: ShieldCheckIcon },
  { name: 'EPC Optimizer', icon: AcademicCapIcon },
  { name: 'Logistics Agent', icon: TruckIcon }
]

const fetchProperty = async () => {
  try {
    const id = parseInt(route.params.id as string)
    property.value = await propertyService.getById(id)
  } catch (error) {
    console.error('Failed to fetch property:', error)
    router.push('/properties')
  } finally {
    loading.value = false
  }
}

const deleteProperty = async () => {
  if (!property.value || !confirm('Are you sure you want to decommission this asset?')) return
  
  try {
    await propertyService.delete(property.value.id)
    router.push('/properties')
  } catch (error) {
    console.error('Failed to delete property:', error)
  }
}

const getEPCBadgeClass = (rating?: string) => {
  const classes: Record<string, string> = {
    'A': 'bg-emerald-500 text-white',
    'B': 'bg-emerald-400 text-white',
    'C': 'bg-lime-500 text-white',
    'D': 'bg-yellow-500 text-white',
    'E': 'bg-orange-500 text-white',
    'F': 'bg-rose-500 text-white',
    'G': 'bg-rose-600 text-white'
  }
  return classes[rating || ''] || 'bg-primary-500 text-white'
}

onMounted(fetchProperty)
</script>
