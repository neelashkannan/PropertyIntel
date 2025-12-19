<template>
  <div class="min-h-[calc(100vh-80px)] flex items-center justify-center p-4 bg-primary-50/50">
    <div class="w-full max-w-md">
      <div class="glass-card p-10">
        <div class="text-center mb-10">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-brand-600 rounded-2xl shadow-xl shadow-brand-200 mb-6">
            <LockClosedIcon class="w-8 h-8 text-white" />
          </div>
          <h1 class="text-3xl font-display font-black text-primary-900 tracking-tight mb-2">Welcome Back</h1>
          <p class="text-primary-500 font-medium">Access your property intelligence dashboard</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-6">
          <div v-if="error" class="p-4 bg-rose-50 border border-rose-100 rounded-2xl text-rose-600 text-sm font-bold flex items-center gap-3">
            <ExclamationCircleIcon class="w-5 h-5" />
            {{ error }}
          </div>

          <div>
            <label class="block text-xs font-black text-primary-400 uppercase tracking-widest mb-3">Email Address</label>
            <div class="relative">
              <EnvelopeIcon class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-primary-300" />
              <input 
                v-model="email" 
                type="email" 
                required 
                class="input-field pl-12" 
                placeholder="admin@local.com"
              />
            </div>
          </div>

          <div>
            <label class="block text-xs font-black text-primary-400 uppercase tracking-widest mb-3">Password</label>
            <div class="relative">
              <KeyIcon class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-primary-300" />
              <input 
                v-model="password" 
                type="password" 
                required 
                class="input-field pl-12" 
                placeholder="••••••••"
              />
            </div>
          </div>

          <button 
            type="submit" 
            :disabled="loading"
            class="btn-primary w-full py-4 text-base flex items-center justify-center gap-3"
          >
            <div v-if="loading" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            {{ loading ? 'Authenticating...' : 'Sign In' }}
          </button>
        </form>

        <div class="mt-10 text-center">
          <p class="text-primary-500 font-medium">
            Don't have an account? 
            <RouterLink to="/register" class="text-brand-600 font-black hover:underline">Create one now</RouterLink>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { 
  LockClosedIcon, 
  EnvelopeIcon, 
  KeyIcon,
  ExclamationCircleIcon 
} from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  try {
    await authStore.login({ email: email.value, password: password.value })
    router.push('/dashboard')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Invalid credentials. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
