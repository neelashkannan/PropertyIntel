<template>
  <div class="min-h-screen bg-primary-50/50 p-4 lg:p-8 animate-fade-in">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-10">
      <div>
        <h1 class="text-4xl font-display font-extrabold text-primary-950 tracking-tight">Intelligence Portfolio</h1>
        <p class="text-primary-500 font-medium mt-2">Real-time monitoring of your deployed real estate assets.</p>
      </div>
      <RouterLink to="/properties/create" class="btn-primary flex items-center gap-2">
        <PlusIcon class="w-5 h-5" />
        Deploy New Asset
      </RouterLink>
    </div>

    <!-- Filters -->
    <div class="glass-card p-6 mb-10">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="relative">
          <span class="absolute inset-y-0 left-0 pl-4 flex items-center text-primary-400">
            <MagnifyingGlassIcon class="w-5 h-5" />
          </span>
          <input v-model="searchTerm" type="text" placeholder="Search address..." class="input-field pl-12" />
        </div>
        <select v-model="filterType" class="input-field">
          <option value="">All Asset Types</option>
          <option value="house">House</option>
          <option value="flat">Flat</option>
        </select>
        <select v-model="filterEPC" class="input-field">
          <option value="">All EPC Ratings</option>
          <option v-for="r in ['A', 'B', 'C', 'D', 'E', 'F', 'G']" :key="r" :value="r">Rating {{ r }}</option>
        </select>
        <button @click="clearFilters" class="btn-secondary">Reset Filters</button>
      </div>
    </div>

    <!-- Property Grid -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div v-for="i in 6" :key="i" class="glass-card h-96 animate-pulse bg-primary-100/50"></div>
    </div>

    <div v-else-if="filteredProperties.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div v-for="property in filteredProperties" :key="property.id" 
        class="glass-card group cursor-pointer hover:shadow-premium transition-all duration-500"
        @click="router.push(`/properties/${property.id}`)"
      >
        <div class="aspect-video bg-primary-100 relative overflow-hidden rounded-t-2xl">
          <img src="https://images.unsplash.com/photo-1568605114967-8130f3a36994?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" />
          <div class="absolute inset-0 bg-gradient-to-t from-primary-900/40 to-transparent"></div>
          <div class="absolute top-4 right-4">
            <span v-if="property.epc_rating" :class="['badge shadow-lg', getEPCBadgeClass(property.epc_rating)]">
              EPC {{ property.epc_rating }}
            </span>
          </div>
          <div class="absolute bottom-4 left-4">
            <span class="text-[10px] font-bold text-white uppercase tracking-widest bg-brand-600/80 backdrop-blur-md px-2 py-1 rounded">Active Monitoring</span>
          </div>
        </div>
        <div class="p-6">
          <div class="flex justify-between items-start mb-6">
            <div>
              <h3 class="text-xl font-bold text-primary-900 group-hover:text-brand-600 transition-colors leading-tight">
                {{ property.house_number }} {{ property.street_name }}
              </h3>
              <p class="text-sm text-primary-500 font-medium mt-1">{{ property.postcode }}</p>
            </div>
            <p class="text-2xl font-display font-bold text-brand-600">£{{ (property.size_sqft ? property.size_sqft * 200 : 150000).toLocaleString() }}</p>
          </div>
          
          <div class="grid grid-cols-3 gap-4 py-5 border-t border-primary-100">
            <div class="text-center">
              <p class="text-[10px] font-bold text-primary-400 uppercase tracking-widest mb-1">Size</p>
              <p class="text-sm font-bold text-primary-700">{{ property.size_sqft || '?' }} <span class="text-[10px] text-primary-400">sqft</span></p>
            </div>
            <div class="text-center border-x border-primary-100">
              <p class="text-[10px] font-bold text-primary-400 uppercase tracking-widest mb-1">Beds</p>
              <p class="text-sm font-bold text-primary-700">{{ property.bedrooms || '?' }}</p>
            </div>
            <div class="text-center">
              <p class="text-[10px] font-bold text-primary-400 uppercase tracking-widest mb-1">Type</p>
              <p class="text-sm font-bold text-primary-700 capitalize">{{ property.property_type }}</p>
            </div>
          </div>
          
          <div class="mt-4 pt-4 border-t border-primary-100 flex items-center justify-between">
            <div class="flex -space-x-2">
              <div v-for="i in 3" :key="i" class="w-6 h-6 rounded-full border-2 border-white bg-primary-100 flex items-center justify-center">
                <div class="w-2 h-2 rounded-full bg-brand-500 animate-pulse"></div>
              </div>
            </div>
            <span class="text-[10px] font-bold text-primary-400 uppercase tracking-widest">3 Agents Active</span>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="glass-card p-20 text-center border-dashed border-primary-200 bg-primary-50/50">
      <div class="w-24 h-24 bg-white rounded-3xl flex items-center justify-center mx-auto mb-8 border border-primary-100 shadow-sm">
        <HomeIcon class="w-12 h-12 text-primary-300" />
      </div>
      <h3 class="text-2xl font-bold text-primary-900 mb-2">No assets found</h3>
      <p class="text-primary-500 mb-8 max-w-md mx-auto">Your intelligence portfolio is currently empty. Deploy your first asset to start monitoring.</p>
      <RouterLink to="/properties/create" class="btn-primary inline-flex items-center gap-2">
        <PlusIcon class="w-5 h-5" />
        Deploy First Asset
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { propertyService } from '@/services/api'
import type { Property } from '@/types'
import { 
  PlusIcon, 
  MagnifyingGlassIcon, 
  HomeIcon 
} from '@heroicons/vue/24/outline'

const router = useRouter()
const properties = ref<Property[]>([])
const loading = ref(true)
const searchTerm = ref('')
const filterType = ref('')
const filterEPC = ref('')

const fetchProperties = async () => {
  try {
    properties.value = await propertyService.getAll()
  } catch (error) {
    console.error('Failed to fetch properties:', error)
  } finally {
    loading.value = false
  }
}

const filteredProperties = computed(() => {
  return properties.value.filter(p => {
    const address = `${p.house_number} ${p.street_name}`.toLowerCase()
    const matchesSearch = address.includes(searchTerm.value.toLowerCase()) ||
                         p.postcode.toLowerCase().includes(searchTerm.value.toLowerCase())
    const matchesType = !filterType.value || p.property_type === filterType.value
    const matchesEPC = !filterEPC.value || p.epc_rating === filterEPC.value
    return matchesSearch && matchesType && matchesEPC
  })
})

const clearFilters = () => {
  searchTerm.value = ''
  filterType.value = ''
  filterEPC.value = ''
}

const getEPCBadgeClass = (rating: string) => {
  const classes: Record<string, string> = {
    'A': 'bg-emerald-500 text-white',
    'B': 'bg-emerald-400 text-white',
    'C': 'bg-lime-500 text-white',
    'D': 'bg-yellow-500 text-white',
    'E': 'bg-orange-500 text-white',
    'F': 'bg-rose-500 text-white',
    'G': 'bg-rose-600 text-white'
  }
  return classes[rating] || 'bg-primary-500 text-white'
}

onMounted(fetchProperties)
</script>
