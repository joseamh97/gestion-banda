<script setup>
</script>

<template>
  <section class="flex min-h-screen items-center justify-center bg-slate-100 px-6 dark:bg-slate-950">
    <div class="max-w-xl rounded-3xl bg-white p-10 text-center shadow-xl dark:bg-slate-900">
      <h1 class="text-7xl font-bold text-blue-600">
        404
      </h1>

      <h2 class="mt-4 text-3xl font-bold text-slate-900 dark:text-white">
        Página no encontrada
      </h2>

      <p class="mt-3 text-slate-600 dark:text-slate-300">
        La ruta que intentas visitar no existe o no está disponible.
      </p>

      <router-link
        to="/dashboard"
        class="mt-8 inline-block rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-700"
      >
        Volver al dashboard
      </router-link>
    </div>
  </section>
</template>