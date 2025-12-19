<template>
  <div id="app" class="min-h-screen bg-primary-50/30 flex font-sans selection:bg-brand-100 selection:text-brand-900">
    <!-- Sidebar for authenticated users -->
    <TheSidebar v-if="authStore.isAuthenticated" />

    <div class="flex-1 flex flex-col min-w-0">
      <!-- Header -->
      <TheHeader />
      
      <main :class="[
        'flex-1',
        authStore.isAuthenticated ? 'lg:ml-72' : ''
      ]">
        <div :class="{ 'max-w-7xl mx-auto w-full': authStore.isAuthenticated }">
          <RouterView v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </RouterView>
        </div>
      </main>

      <TheFooter v-if="!authStore.isAuthenticated" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import TheHeader from "@/components/layout/TheHeader.vue";
import TheSidebar from "@/components/layout/TheSidebar.vue";
import TheFooter from "@/components/layout/TheFooter.vue";

const authStore = useAuthStore();
</script>

<style>
/* Global Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #e4e4e7;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #d4d4d8;
}
</style>
