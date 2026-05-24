<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../api/axios";

const eventos = ref([]);

const cargarEventos = async () => {
  const response = await api.get("/eventos/");
  eventos.value = response.data;
};

const eventosPorFecha = computed(() => {
  const agrupados = {};

  eventos.value.forEach((evento) => {
    if (!agrupados[evento.fecha]) {
      agrupados[evento.fecha] = [];
    }

    agrupados[evento.fecha].push(evento);
  });

  return agrupados;
});

const fechasOrdenadas = computed(() => {
  return Object.keys(eventosPorFecha.value).sort();
});

onMounted(() => {
  cargarEventos();
});
</script>

<template>
  <section class="p-6 lg:p-10">
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-slate-900 dark:text-white">
        Calendario
      </h1>

      <p class="mt-2 text-slate-600 dark:text-slate-300">
        Consulta los próximos ensayos, conciertos y procesiones.
      </p>
    </div>

    <div
      v-if="fechasOrdenadas.length === 0"
      class="rounded-2xl bg-white p-10 text-center shadow-sm dark:bg-slate-900"
    >
      <p class="text-slate-500 dark:text-slate-300">
        No hay eventos programados.
      </p>
    </div>

    <div class="space-y-6">
      <div
        v-for="fecha in fechasOrdenadas"
        :key="fecha"
        class="rounded-2xl bg-white p-6 shadow-sm dark:bg-slate-900"
      >
        <h2 class="mb-4 text-xl font-semibold text-slate-800 dark:text-white">
          {{ fecha }}
        </h2>

        <div class="space-y-4">
          <div
            v-for="evento in eventosPorFecha[fecha]"
            :key="evento.id"
            class="rounded-xl border border-slate-200 p-4 dark:border-slate-700"
          >
            <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <div>
                <h3 class="text-lg font-bold text-slate-900 dark:text-white">
                  {{ evento.titulo }}
                </h3>

                <p class="text-sm text-slate-500 dark:text-slate-300">
                  {{ evento.descripcion }}
                </p>
              </div>

              <span class="rounded-full bg-blue-100 px-3 py-1 text-sm font-semibold text-blue-700 dark:bg-blue-900 dark:text-blue-200">
                {{ evento.tipo }}
              </span>
            </div>

            <div class="mt-4 grid grid-cols-1 gap-3 text-sm text-slate-600 dark:text-slate-300 md:grid-cols-2">
              <p>🕒 {{ evento.hora }}</p>
              <p>📍 {{ evento.ubicacion }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>