<script setup>
import { ref, onMounted } from "vue";
import api from "../api/axios";

const usuario = JSON.parse(localStorage.getItem("usuario"));
const stats = ref(null);

const cargarStats = async () => {
  try {
    const response = await api.get("/dashboard/stats");
    stats.value = response.data;
  } catch (error) {
    console.log(error);
  }
};

onMounted(() => {
  if (usuario.rol === "admin") {
    cargarStats();
  }
});
</script>

<template>
  <section class="p-6 lg:p-10">
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-slate-900 dark:text-white">
        Dashboard
      </h1>

      <p class="mt-2 text-slate-600 dark:text-slate-300">
        Panel general de administración de la banda.
      </p>
    </div>

    <div v-if="usuario.rol === 'admin' && stats">

      <div class="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-5">

        <router-link
          to="/usuarios"
          class="rounded-2xl bg-white p-6 shadow-sm hover:shadow-lg dark:bg-slate-900"
        >
          <p class="text-sm text-slate-500 dark:text-slate-300">
            Usuarios
          </p>

          <p class="mt-3 text-4xl font-bold text-blue-600">
            {{ stats.usuarios }}
          </p>

          <p class="mt-2 text-sm text-slate-500 dark:text-slate-300">
            {{ stats.usuarios_activos }} activos ·
            {{ stats.usuarios_inactivos }} inactivos
          </p>
        </router-link>

        <router-link
          to="/obras"
          class="rounded-2xl bg-white p-6 shadow-sm hover:shadow-lg dark:bg-slate-900"
        >
          <p class="text-sm text-slate-500 dark:text-slate-300">
            Obras
          </p>

          <p class="mt-3 text-4xl font-bold text-green-600">
            {{ stats.obras }}
          </p>

          <p class="mt-2 text-sm text-slate-500 dark:text-slate-300">
            Catálogo musical
          </p>
        </router-link>

        <router-link
          to="/particellas"
          class="rounded-2xl bg-white p-6 shadow-sm hover:shadow-lg dark:bg-slate-900"
        >
          <p class="text-sm text-slate-500 dark:text-slate-300">
            Particellas
          </p>

          <p class="mt-3 text-4xl font-bold text-purple-600">
            {{ stats.particellas }}
          </p>

          <p class="mt-2 text-sm text-slate-500 dark:text-slate-300">
            PDFs individuales
          </p>
        </router-link>

        <router-link
          to="/eventos"
          class="rounded-2xl bg-white p-6 shadow-sm hover:shadow-lg dark:bg-slate-900"
        >
          <p class="text-sm text-slate-500 dark:text-slate-300">
            Eventos
          </p>

          <p class="mt-3 text-4xl font-bold text-orange-500">
            {{ stats.eventos }}
          </p>

          <p class="mt-2 text-sm text-slate-500 dark:text-slate-300">
            Ensayos, conciertos y procesiones
          </p>
        </router-link>

        <router-link
          to="/inventario"
          class="rounded-2xl bg-white p-6 shadow-sm hover:shadow-lg dark:bg-slate-900"
        >
          <p class="text-sm text-slate-500 dark:text-slate-300">
            Inventario
          </p>

          <p class="mt-3 text-4xl font-bold text-cyan-600">
            {{ stats.inventario }}
          </p>

          <p class="mt-2 text-sm text-slate-500 dark:text-slate-300">
            Instrumentos y material
          </p>
        </router-link>

      </div>

      <div class="mt-8 grid grid-cols-1 gap-6 xl:grid-cols-3">

        <div class="rounded-2xl bg-white p-6 shadow-sm dark:bg-slate-900">
          <h2 class="mb-6 text-xl font-semibold text-slate-800 dark:text-white">
            Tipos de eventos
          </h2>

          <div class="space-y-5 text-slate-700 dark:text-slate-200">

            <div>
              <div class="mb-1 flex justify-between text-sm">
                <span>Ensayos</span>
                <span>{{ stats.ensayos }}</span>
              </div>

              <div class="h-3 rounded-full bg-slate-200 dark:bg-slate-700">
                <div
                  class="h-3 rounded-full bg-blue-600"
                  :style="{ width: Math.min(stats.ensayos * 10, 100) + '%' }"
                ></div>
              </div>
            </div>

            <div>
              <div class="mb-1 flex justify-between text-sm">
                <span>Conciertos</span>
                <span>{{ stats.conciertos }}</span>
              </div>

              <div class="h-3 rounded-full bg-slate-200 dark:bg-slate-700">
                <div
                  class="h-3 rounded-full bg-green-600"
                  :style="{ width: Math.min(stats.conciertos * 10, 100) + '%' }"
                ></div>
              </div>
            </div>

            <div>
              <div class="mb-1 flex justify-between text-sm">
                <span>Procesiones</span>
                <span>{{ stats.procesiones }}</span>
              </div>

              <div class="h-3 rounded-full bg-slate-200 dark:bg-slate-700">
                <div
                  class="h-3 rounded-full bg-purple-600"
                  :style="{ width: Math.min(stats.procesiones * 10, 100) + '%' }"
                ></div>
              </div>
            </div>

          </div>
        </div>

        <div class="rounded-2xl bg-white p-6 shadow-sm dark:bg-slate-900">
          <h2 class="mb-6 text-xl font-semibold text-slate-800 dark:text-white">
            Asistencia general
          </h2>

          <div class="mb-6">
            <p class="text-sm text-slate-500 dark:text-slate-300">
              Porcentaje de asistencia
            </p>

            <p class="mt-2 text-5xl font-bold text-green-600">
              {{ stats.porcentaje_asistencia }}%
            </p>
          </div>

          <div class="h-4 rounded-full bg-slate-200 dark:bg-slate-700">
            <div
              class="h-4 rounded-full bg-green-600"
              :style="{ width: stats.porcentaje_asistencia + '%' }"
            ></div>
          </div>

          <div class="mt-6 grid grid-cols-2 gap-4">

            <div class="rounded-xl bg-green-50 p-4 dark:bg-green-900/30">
              <p class="text-sm text-green-700 dark:text-green-200">
                Asistirán
              </p>

              <p class="mt-2 text-3xl font-bold text-green-600">
                {{ stats.asistiran }}
              </p>
            </div>

            <div class="rounded-xl bg-red-50 p-4 dark:bg-red-900/30">
              <p class="text-sm text-red-700 dark:text-red-200">
                No asistirán
              </p>

              <p class="mt-2 text-3xl font-bold text-red-600">
                {{ stats.no_asistiran }}
              </p>
            </div>

          </div>
        </div>

        <div class="rounded-2xl bg-white p-6 shadow-sm dark:bg-slate-900">
          <h2 class="mb-6 text-xl font-semibold text-slate-800 dark:text-white">
            Estado del inventario
          </h2>

          <div class="space-y-5">

            <div>
              <div class="mb-1 flex justify-between text-sm">
                <span class="text-slate-700 dark:text-slate-200">
                  Disponible
                </span>

                <span class="text-slate-700 dark:text-slate-200">
                  {{ stats.inventario_disponible }}
                </span>
              </div>

              <div class="h-3 rounded-full bg-slate-200 dark:bg-slate-700">
                <div
                  class="h-3 rounded-full bg-green-600"
                  :style="{
                    width:
                      Math.min(
                        (stats.inventario_disponible / Math.max(stats.inventario, 1)) * 100,
                        100
                      ) + '%'
                  }"
                ></div>
              </div>
            </div>

            <div>
              <div class="mb-1 flex justify-between text-sm">
                <span class="text-slate-700 dark:text-slate-200">
                  Prestado
                </span>

                <span class="text-slate-700 dark:text-slate-200">
                  {{ stats.inventario_prestado }}
                </span>
              </div>

              <div class="h-3 rounded-full bg-slate-200 dark:bg-slate-700">
                <div
                  class="h-3 rounded-full bg-blue-600"
                  :style="{
                    width:
                      Math.min(
                        (stats.inventario_prestado / Math.max(stats.inventario, 1)) * 100,
                        100
                      ) + '%'
                  }"
                ></div>
              </div>
            </div>

            <div>
              <div class="mb-1 flex justify-between text-sm">
                <span class="text-slate-700 dark:text-slate-200">
                  Reparación
                </span>

                <span class="text-slate-700 dark:text-slate-200">
                  {{ stats.inventario_reparacion }}
                </span>
              </div>

              <div class="h-3 rounded-full bg-slate-200 dark:bg-slate-700">
                <div
                  class="h-3 rounded-full bg-yellow-500"
                  :style="{
                    width:
                      Math.min(
                        (stats.inventario_reparacion / Math.max(stats.inventario, 1)) * 100,
                        100
                      ) + '%'
                  }"
                ></div>
              </div>
            </div>

            <div>
              <div class="mb-1 flex justify-between text-sm">
                <span class="text-slate-700 dark:text-slate-200">
                  Baja
                </span>

                <span class="text-slate-700 dark:text-slate-200">
                  {{ stats.inventario_baja }}
                </span>
              </div>

              <div class="h-3 rounded-full bg-slate-200 dark:bg-slate-700">
                <div
                  class="h-3 rounded-full bg-red-600"
                  :style="{
                    width:
                      Math.min(
                        (stats.inventario_baja / Math.max(stats.inventario, 1)) * 100,
                        100
                      ) + '%'
                  }"
                ></div>
              </div>
            </div>

          </div>
        </div>

      </div>

      <div class="mt-8 rounded-2xl bg-white p-6 shadow-sm dark:bg-slate-900">
        <h2 class="mb-6 text-xl font-semibold text-slate-800 dark:text-white">
          Resumen general
        </h2>

        <div class="grid grid-cols-1 gap-4 md:grid-cols-3">

          <div class="rounded-xl border p-4 dark:border-slate-700">
            <p class="text-sm text-slate-500 dark:text-slate-300">
              Total asistencias
            </p>

            <p class="mt-2 text-3xl font-bold text-slate-900 dark:text-white">
              {{ stats.asistencias }}
            </p>
          </div>

          <div class="rounded-xl border p-4 dark:border-slate-700">
            <p class="text-sm text-slate-500 dark:text-slate-300">
              Usuarios activos
            </p>

            <p class="mt-2 text-3xl font-bold text-blue-600">
              {{ stats.usuarios_activos }}
            </p>
          </div>

          <div class="rounded-xl border p-4 dark:border-slate-700">
            <p class="text-sm text-slate-500 dark:text-slate-300">
              Usuarios inactivos
            </p>

            <p class="mt-2 text-3xl font-bold text-red-600">
              {{ stats.usuarios_inactivos }}
            </p>
          </div>

        </div>
      </div>

    </div>
  </section>
</template>