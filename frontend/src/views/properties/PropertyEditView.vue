<template>
  <div class="min-h-screen bg-primary-50/50 p-4 lg:p-8 animate-fade-in">
    <div v-if="loading" class="flex flex-col justify-center items-center py-24">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-600 mb-6"></div>
      <p class="text-primary-500 font-bold tracking-tight">Retrieving asset data...</p>
    </div>

    <div v-else-if="property" class="max-w-5xl mx-auto">
      <!-- Header -->
      <div class="mb-10 flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div>
          <div class="flex items-center gap-2 text-primary-400 text-xs font-bold uppercase tracking-widest mb-3">
            <RouterLink to="/properties" class="hover:text-brand-600 transition-colors">Portfolio</RouterLink>
            <ChevronRightIcon class="w-4 h-4 text-primary-300" />
            <RouterLink :to="`/properties/${propertyId}`" class="hover:text-brand-600 transition-colors">Asset Details</RouterLink>
            <ChevronRightIcon class="w-4 h-4 text-primary-300" />
            <span class="text-primary-900">Edit</span>
          </div>
          <h1 class="text-4xl font-display font-extrabold text-primary-900 tracking-tight">
            Edit Property Asset
          </h1>
          <p class="mt-2 text-primary-500 font-medium">
            Update specifications for <span class="font-bold text-primary-900">{{ property.house_number }} {{ property.street_name }}</span>.
          </p>
        </div>
        <div class="flex items-center gap-4">
          <RouterLink :to="`/properties/${propertyId}`" class="btn-secondary px-6">
            Cancel
          </RouterLink>
          <button @click="handleSubmit" :disabled="saving" class="btn-primary px-8 py-3 flex items-center gap-2">
            <CheckIcon v-if="!saving" class="w-5 h-5" />
            <div v-else class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            {{ saving ? "Saving Changes..." : "Save Changes" }}
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
        <!-- Main Form -->
        <div class="lg:col-span-2 space-y-8">
          <!-- Address Section -->
          <div class="glass-card overflow-hidden">
            <div class="px-8 py-5 border-b border-primary-50 bg-primary-50/30">
              <h2 class="text-xs font-black text-primary-400 uppercase tracking-widest">Location Details</h2>
            </div>
            <div class="p-8 space-y-8">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <label class="block text-xs font-bold text-primary-400 uppercase tracking-widest mb-3">House Number</label>
                  <input v-model="form.house_number" type="text" required class="input-field" />
                </div>
                <div>
                  <label class="block text-xs font-bold text-primary-400 uppercase tracking-widest mb-3">Street Name</label>
                  <input v-model="form.street_name" type="text" required class="input-field" />
                </div>
                <div class="md:col-span-2">
                  <label class="block text-xs font-bold text-primary-400 uppercase tracking-widest mb-3">Postcode</label>
                  <input v-model="form.postcode" type="text" required class="input-field" />
                </div>
              </div>
            </div>
          </div>

          <!-- Property Specs -->
          <div class="glass-card overflow-hidden">
            <div class="px-8 py-5 border-b border-primary-50 bg-primary-50/30">
              <h2 class="text-xs font-black text-primary-400 uppercase tracking-widest">Property Specifications</h2>
            </div>
            <div class="p-8 space-y-8">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <label class="block text-xs font-bold text-primary-400 uppercase tracking-widest mb-3">Property Type</label>
                  <select v-model="form.property_type" required class="input-field">
                    <option value="house">House</option>
                    <option value="flat">Flat</option>
                    <option value="detached">Detached</option>
                    <option value="semi-detached">Semi-detached</option>
                    <option value="bungalow">Bungalow</option>
                  </select>
                </div>
                <div>
                  <label class="block text-xs font-bold text-primary-400 uppercase tracking-widest mb-3">Size (sq ft)</label>
                  <div class="relative">
                    <input v-model.number="form.size_sqft" type="number" class="input-field pr-16" />
                    <span class="absolute inset-y-0 right-0 pr-6 flex items-center text-primary-400 text-sm font-bold">sqft</span>
                  </div>
                </div>
                <div>
                  <label class="block text-xs font-bold text-primary-400 uppercase tracking-widest mb-3">Bedrooms</label>
                  <div class="grid grid-cols-4 gap-3">
                    <button 
                      v-for="n in 4" :key="n"
                      type="button"
                      @click="form.bedrooms = n"
                      class="py-3 text-sm font-black rounded-2xl border transition-all transform active:scale-95"
                      :class="form.bedrooms === n ? 'bg-brand-600 border-brand-600 text-white shadow-lg shadow-brand-200' : 'bg-white border-primary-100 text-primary-600 hover:border-brand-300'"
                    >
                      {{ n }}
                    </button>
                  </div>
                </div>
                <div>
                  <label class="block text-xs font-bold text-primary-400 uppercase tracking-widest mb-3">EPC Rating</label>
                  <select v-model="form.epc_rating" class="input-field">
                    <option v-for="r in ['A', 'B', 'C', 'D', 'E', 'F', 'G']" :key="r" :value="r">{{ r }}</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar Info -->
        <div class="space-y-8">
          <div class="glass-card p-8">
            <h3 class="text-lg font-bold text-primary-900 mb-6">Asset Health</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between text-sm">
                <span class="text-primary-500">Data Integrity</span>
                <span class="text-emerald-600 font-bold">100%</span>
              </div>
              <div class="h-2 bg-primary-100 rounded-full overflow-hidden">
                <div class="h-full bg-emerald-500 rounded-full" style="width: 100%"></div>
              </div>
              <p class="text-xs text-primary-400 mt-4">
                Updating these specifications will trigger a re-scan by the agent swarm to ensure valuation accuracy.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { propertyService } from '@/services/api'
import type { Property } from '@/types'
import { 
  ChevronRightIcon, 
  CheckIcon 
} from '@heroicons/vue/24/outline'

const route = useRoute()
const router = useRouter()
const propertyId = Number(route.params.id)

const property = ref<Property | null>(null)
const loading = ref(true)
const saving = ref(false)

const form = reactive({
  house_number: '',
  street_name: '',
  postcode: '',
  property_type: '',
  size_sqft: 0,
  bedrooms: 1,
  epc_rating: ''
})

const fetchProperty = async () => {
  try {
    const data = await propertyService.getById(propertyId)
    property.value = data
    Object.assign(form, {
      house_number: data.house_number,
      street_name: data.street_name,
      postcode: data.postcode,
      property_type: data.property_type,
      size_sqft: data.size_sqft,
      bedrooms: data.bedrooms,
      epc_rating: data.epc_rating
    })
  } catch (error) {
    console.error('Failed to fetch property:', error)
    router.push('/properties')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  saving.value = true
  try {
    await propertyService.update(propertyId, form)
    router.push(`/properties/${propertyId}`)
  } catch (error) {
    console.error('Failed to update property:', error)
  } finally {
    saving.value = false
  }
}

onMounted(fetchProperty)
</script>
