<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import * as XLSX from "xlsx";

import api from "../api/axios";

const route = useRoute();

const asistencias = ref([]);
const busqueda = ref("");

const cargarAsistencias = async () => {
  try {
    const response = await api.get(
      `/asistencias/evento/${route.params.id}`
    );

    asistencias.value = response.data;
  } catch (error) {
    alert("Error al cargar asistencias");
  }
};

const totalAsistencias = computed(() => {
  return asistencias.value.length;
});

const totalAsistiran = computed(() => {
  return asistencias.value.filter(
    (a) => a.estado === "asistira"
  ).length;
});

const totalNoAsistiran = computed(() => {
  return asistencias.value.filter(
    (a) => a.estado === "no_asistira"
  ).length;
});

const asistenciasFiltradas = computed(() => {
  return asistencias.value.filter((a) => {
    const texto = `
      ${a.usuario}
      ${a.estado}
      ${a.comentario}
    `.toLowerCase();

    return texto.includes(
      busqueda.value.toLowerCase()
    );
  });
});

const exportarExcel = () => {
  const datos = asistenciasFiltradas.value.map((a) => ({
    Musico: a.usuario,
    Estado: a.estado === "asistira" ? "Asistirá" : "No asistirá",
    Comentario: a.comentario || ""
  }));

  const worksheet = XLSX.utils.json_to_sheet(datos);
  const workbook = XLSX.utils.book_new();

  XLSX.utils.book_append_sheet(
    workbook,
    worksheet,
    "Asistencias"
  );

  XLSX.writeFile(
    workbook,
    "asistencias.xlsx"
  );
};

onMounted(() => {
  cargarAsistencias();
});
</script>

<template>
  <section class="p-6 lg:p-10">
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-slate-900 dark:text-white">
        Asistencias del evento
      </h1>

      <p class="mt-2 text-slate-600 dark:text-slate-300">
        Consulta las respuestas de los músicos.
      </p>
    </div>

    <div class="mb-8 grid grid-cols-1 gap-6 md:grid-cols-3">
      <div class="rounded-2xl bg-white p-6 shadow-sm dark:bg-slate-900">
        <p class="text-sm text-slate-500 dark:text-slate-300">
          Respuestas
        </p>

        <p class="mt-3 text-4xl font-bold text-blue-600">
          {{ totalAsistencias }}
        </p>
      </div>

      <div class="rounded-2xl bg-white p-6 shadow-sm dark:bg-slate-900">
        <p class="text-sm text-slate-500 dark:text-slate-300">
          Asistirán
        </p>

        <p class="mt-3 text-4xl font-bold text-green-600">
          {{ totalAsistiran }}
        </p>
      </div>

      <div class="rounded-2xl bg-white p-6 shadow-sm dark:bg-slate-900">
        <p class="text-sm text-slate-500 dark:text-slate-300">
          No asistirán
        </p>

        <p class="mt-3 text-4xl font-bold text-red-600">
          {{ totalNoAsistiran }}
        </p>
      </div>
    </div>

    <div class="overflow-hidden rounded-2xl bg-white shadow-sm dark:bg-slate-900">
      <div class="border-b border-slate-200 px-6 py-4 dark:border-slate-700">
        <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <h2 class="text-xl font-semibold text-slate-800 dark:text-white">
            Listado de respuestas
          </h2>

          <div class="flex flex-col gap-3 md:flex-row">
            <input
              v-model="busqueda"
              placeholder="Buscar músico, estado o comentario"
              class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
            />

            <button
              @click="exportarExcel"
              class="rounded-xl bg-green-600 px-4 py-3 font-semibold text-white hover:bg-green-700"
            >
              Exportar Excel
            </button>
          </div>
        </div>
      </div>

      <div v-if="asistencias.length === 0" class="p-10 text-center">
        <p class="text-slate-500 dark:text-slate-300">
          Todavía no hay respuestas.
        </p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead class="bg-slate-50 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
            <tr>
              <th class="px-6 py-4">Músico</th>
              <th class="px-6 py-4">Estado</th>
              <th class="px-6 py-4">Comentario</th>
            </tr>
          </thead>

          <tbody class="divide-y divide-slate-200 dark:divide-slate-700">
            <tr
              v-for="a in asistenciasFiltradas"
              :key="a.id"
              class="hover:bg-slate-50 dark:hover:bg-slate-800"
            >
              <td class="px-6 py-4 font-medium text-slate-900 dark:text-white">
                {{ a.usuario }}
              </td>

              <td class="px-6 py-4">
                <span
                  class="rounded-full px-3 py-1 text-xs font-semibold"
                  :class="
                    a.estado === 'asistira'
                      ? 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-200'
                      : 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-200'
                  "
                >
                  {{
                    a.estado === "asistira"
                      ? "Asistirá"
                      : "No asistirá"
                  }}
                </span>
              </td>

              <td class="px-6 py-4 text-slate-600 dark:text-slate-300">
                {{ a.comentario || "-" }}
              </td>
            </tr>

            <tr v-if="asistenciasFiltradas.length === 0">
              <td colspan="3" class="px-6 py-8 text-center text-slate-500 dark:text-slate-300">
                No se encontraron resultados.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <router-link
      to="/eventos"
      class="mt-6 inline-block rounded-xl border px-5 py-3 font-semibold text-slate-700 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
    >
      Volver a eventos
    </router-link>
  </section>
</template>