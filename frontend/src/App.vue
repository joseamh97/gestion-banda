<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import Navbar from "./components/Navbar.vue";
import { Toaster } from "vue-sonner";

const route = useRoute();

const mostrarLayout = computed(() => {
  return route.path !== "/";
});
</script>

<template>
  <div
    v-if="mostrarLayout"
    class="min-h-screen bg-slate-100 text-slate-900 dark:bg-slate-950 dark:text-white"
  >
    <Navbar />

    <main class="lg:ml-64">
      <router-view />
    </main>
    <Toaster richColors />
  </div>

  <router-view v-else />
</template>