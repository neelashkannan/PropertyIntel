import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import "./assets/main.css";
import { useAuthStore } from "@/stores/auth";

const app = createApp(App);

app.use(createPinia());

// Initialize auth from localStorage before routing
const auth = useAuthStore();
auth.initializeAuth();

app.use(router);

app.mount("#app");
