<template>
  <div class="min-h-screen bg-primary-50/50 p-4 lg:p-8 animate-fade-in">
    <div class="max-w-5xl mx-auto">
      <!-- Header -->
      <div class="mb-10 flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div>
          <div class="flex items-center gap-2 text-primary-400 text-xs font-bold uppercase tracking-widest mb-3">
            <RouterLink to="/properties" class="hover:text-brand-600 transition-colors">Portfolio</RouterLink>
            <ChevronRightIcon class="w-4 h-4 text-primary-300" />
            <span class="text-primary-900">Add Asset</span>
          </div>
          <h1 class="text-4xl font-display font-extrabold text-primary-900 tracking-tight">
            New Property Asset
          </h1>
          <p class="mt-2 text-primary-500 font-medium">
            Register a new property to your investment portfolio for institutional analysis.
          </p>
        </div>
        <div class="flex items-center gap-4">
          <RouterLink to="/properties" class="btn-secondary px-6">
            Discard
          </RouterLink>
          <button @click="handleSubmit" :disabled="loading" class="btn-primary px-8 py-3 flex items-center gap-2">
            <PlusIcon v-if="!loading" class="w-5 h-5" />
            <div v-else class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            {{ loading ? "Saving..." : "Save Property" }}
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
                <div class="md:col-span-1">
                  <label class="block text-xs font-bold text-primary-400 uppercase tracking-widest mb-3">House/Flat Number</label>
                  <input v-model="form.house_number" type="text" required class="input-field" placeholder="e.g. 12A" />
                </div>
                <div class="md:col-span-1">
                  <label class="block text-xs font-bold text-primary-400 uppercase tracking-widest mb-3">Street Name</label>
                  <input v-model="form.street_name" type="text" required class="input-field" placeholder="e.g. High Street" />
                </div>
                <div class="md:col-span-2">
                  <label class="block text-xs font-bold text-primary-400 uppercase tracking-widest mb-3">Postcode</label>
                  <input v-model="form.postcode" type="text" required class="input-field" placeholder="e.g. EH1 1AA" />
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
                    <option value="">Select Type</option>
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
                    <input v-model.number="form.size_sqft" type="number" class="input-field pr-16" placeholder="0" />
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
                    <option value="">Select Rating</option>
                    <option v-for="r in ['A', 'B', 'C', 'D', 'E', 'F', 'G']" :key="r" :value="r">{{ r }}</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar Info -->
        <div class="space-y-8">
          <div class="p-8 rounded-3xl bg-gradient-to-br from-brand-600 to-violet-700 text-white shadow-premium relative overflow-hidden group">
            <div class="relative z-10">
              <div class="w-12 h-12 bg-white/20 backdrop-blur-md rounded-xl flex items-center justify-center mb-6">
                <SparklesIcon class="w-6 h-6 text-white" />
              </div>
              <h3 class="text-xl font-display font-bold mb-4">AI Pre-Scan</h3>
              <p class="text-brand-50/80 text-sm leading-relaxed">
                Once saved, our agent swarm will automatically begin scanning for flood risks, school catchments, and market trends.
              </p>
            </div>
            <div class="absolute -right-10 -bottom-10 w-40 h-40 bg-white/10 rounded-full blur-3xl group-hover:scale-150 transition-transform duration-700"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { propertyService } from '@/services/api'
import { 
  ChevronRightIcon, 
  PlusIcon, 
  SparklesIcon 
} from '@heroicons/vue/24/outline'

const router = useRouter()
const loading = ref(false)

const form = reactive({
  house_number: '',
  street_name: '',
  postcode: '',
  property_type: '',
  size_sqft: null as number | null,
  bedrooms: 1,
  epc_rating: ''
})

const handleSubmit = async () => {
  loading.value = true
  try {
    await propertyService.create({
      house_number: form.house_number,
      street_name: form.street_name,
      postcode: form.postcode,
      property_type: form.property_type,
      size_sqft: form.size_sqft || 0,
      bedrooms: form.bedrooms,
      epc_rating: form.epc_rating
    })
    router.push('/properties')
  } catch (error) {
    console.error('Failed to create property:', error)
  } finally {
    loading.value = false
  }
}
</script>
