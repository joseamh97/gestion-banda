<script setup>
import { ref, computed, onMounted } from "vue";
import { toast } from "vue-sonner";
import api from "../api/axios";

const particellas = ref([]);
const busqueda = ref("");
const cargando = ref(true);

const cargarParticellas = async () => {
  cargando.value = true;

  try {
    const response = await api.get("/particellas/mis-particellas");
    particellas.value = response.data;
  } catch (error) {
    toast.error("Error al cargar tus particellas");
  } finally {
    cargando.value = false;
  }
};

const particellasFiltradas = computed(() => {
  return particellas.value
    .filter((p) => {
      const texto = `${p.obra} ${p.instrumento} ${p.voz}`.toLowerCase();
      return texto.includes(busqueda.value.toLowerCase());
    })
    .sort((a, b) => a.obra.localeCompare(b.obra));
});

const abrirPDF = (ruta) => {
  window.open(`http://127.0.0.1:5000/${ruta}`, "_blank");
};

const nombreArchivo = (ruta) => {
  if (!ruta) return "PDF no disponible";
  return ruta.split("/").pop();
};

onMounted(() => {
  cargarParticellas();
});
</script>

<template>
  <section class="p-6 lg:p-10">
    <div class="mb-8 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
      <div>
        <h1 class="text-4xl font-bold text-slate-900 dark:text-white">
          Mis partituras
        </h1>

        <p class="mt-2 text-slate-600 dark:text-slate-300">
          Consulta rápidamente las particellas asignadas a tu instrumento y voz.
        </p>
      </div>

      <input
        v-model="busqueda"
        placeholder="Buscar por obra..."
        class="w-full rounded-xl border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-800 md:w-80"
      />
    </div>

    <div
      v-if="cargando"
      class="rounded-2xl bg-white p-10 text-center shadow-sm dark:bg-slate-900"
    >
      <div
        class="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"
      ></div>

      <p class="text-slate-500 dark:text-slate-300">
        Cargando tus partituras...
      </p>
    </div>

    <div
      v-else-if="particellasFiltradas.length === 0"
      class="rounded-2xl bg-white p-10 text-center shadow-sm dark:bg-slate-900"
    >
      <p class="text-lg font-semibold text-slate-700 dark:text-slate-200">
        No tienes particellas asignadas.
      </p>

      <p class="mt-2 text-slate-500 dark:text-slate-300">
        Cuando el administrador suba partituras para tu instrumento y voz, aparecerán aquí.
      </p>
    </div>

    <div
      v-else
      class="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3"
    >
      <div
        v-for="p in particellasFiltradas"
        :key="p.id"
        class="rounded-2xl bg-white p-6 shadow-sm transition-all duration-200 hover:-translate-y-1 hover:shadow-lg dark:bg-slate-900"
      >
        <div class="mb-5">
          <h2 class="text-2xl font-bold text-slate-900 dark:text-white">
            {{ p.obra }}
          </h2>

          <p class="mt-2 break-all text-sm text-slate-500 dark:text-slate-300">
            {{ nombreArchivo(p.archivo_pdf) }}
          </p>
        </div>

        <div class="mb-6 flex flex-wrap gap-2">
          <span class="rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-700 dark:bg-blue-900 dark:text-blue-200">
            {{ p.instrumento }}
          </span>

          <span class="rounded-full bg-purple-100 px-3 py-1 text-xs font-semibold text-purple-700 dark:bg-purple-900 dark:text-purple-200">
            {{ p.voz }}
          </span>
        </div>

        <button
          @click="abrirPDF(p.archivo_pdf)"
          class="w-full rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-700"
        >
          Ver PDF
        </button>
      </div>
    </div>
  </section>
</template>