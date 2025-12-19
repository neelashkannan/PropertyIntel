<template>
  <footer class="bg-white border-t border-primary-100 py-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col md:flex-row justify-between items-center gap-8">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-primary-900 rounded-lg flex items-center justify-center">
            <HomeIcon class="w-5 h-5 text-white" />
          </div>
          <span class="text-lg font-display font-black tracking-tighter text-primary-900">
            Property<span class="text-brand-600">Intel</span>
          </span>
        </div>
        
        <div class="flex items-center gap-8 text-sm font-bold text-primary-400 uppercase tracking-widest">
          <a href="#" class="hover:text-brand-600 transition-colors">Privacy</a>
          <a href="#" class="hover:text-brand-600 transition-colors">Terms</a>
          <a href="#" class="hover:text-brand-600 transition-colors">API</a>
          <a href="#" class="hover:text-brand-600 transition-colors">Support</a>
        </div>

        <p class="text-sm font-medium text-primary-400">
          &copy; {{ new Date().getFullYear() }} PropertyIntel AI. All rights reserved.
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { HomeIcon } from '@heroicons/vue/24/outline'
</script>
