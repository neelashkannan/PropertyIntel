import { createRouter, createWebHashHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/auth/LoginView.vue";
import RegisterView from "@/views/auth/RegisterView.vue";
import DashboardView from "@/views/DashboardView.vue";
import PropertiesView from "@/views/properties/PropertiesView.vue";
import PropertyCreateView from "@/views/properties/PropertyCreateView.vue";
import PropertyEditView from "@/views/properties/PropertyEditView.vue";
import PropertyDetailView from "@/views/properties/PropertyDetailView.vue";
import AnalyticsView from "@/views/AnalyticsView.vue";

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
      meta: { requiresGuest: true },
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView,
      meta: { requiresGuest: true },
    },
    {
      path: "/dashboard",
      name: "dashboard",
      component: DashboardView,
      meta: { requiresAuth: true },
    },
    {
      path: "/properties",
      name: "properties",
      component: PropertiesView,
      meta: { requiresAuth: true },
    },
    {
      path: "/properties/create",
      name: "property-create",
      component: PropertyCreateView,
      meta: { requiresAuth: true },
    },
    {
      path: "/properties/:id",
      name: "property-detail",
      component: PropertyDetailView,
      meta: { requiresAuth: true },
      props: true,
    },
    {
      path: "/properties/:id/edit",
      name: "property-edit",
      component: PropertyEditView,
      meta: { requiresAuth: true },
      props: true,
    },
    {
      path: "/analytics",
      name: "analytics",
      component: AnalyticsView,
      meta: { requiresAuth: true },
    },
  ],
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: "login" });
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next({ name: "dashboard" });
  } else {
    next();
  }
});

export default router;
