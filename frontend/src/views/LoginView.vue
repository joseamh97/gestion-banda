<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { toast } from "vue-sonner";
import api from "../api/axios";

const router = useRouter();

const email = ref("");
const password = ref("");

const login = async () => {
  if (!email.value || !password.value) {
    toast.error("Debes introducir email y contraseña", {
      duration: 6000
    });
    return;
  }

  try {
    const response = await api.post("/auth/login", {
      email: email.value,
      password: password.value
    });

    localStorage.setItem("token", response.data.access_token);
    localStorage.setItem("usuario", JSON.stringify(response.data.usuario));

    toast.success("Inicio de sesión correcto");

    if (response.data.usuario.rol === "admin") {
      router.push("/dashboard");
    } else {
      router.push("/eventos");
    }
  } catch (error) {
    toast.error("Correo electrónico o contraseña incorrectos", {
      duration: 6000
    });
  }
};
</script>

<template>
  <section class="flex min-h-screen items-center justify-center bg-slate-100 px-6 dark:bg-slate-950">
    <div class="grid w-full max-w-5xl overflow-hidden rounded-3xl bg-white shadow-xl dark:bg-slate-900 md:grid-cols-2">
      <div class="hidden bg-slate-950 p-10 text-white md:flex md:flex-col md:justify-between">
        <div>
          <h1 class="text-4xl font-bold">
            Gestión Banda
          </h1>

          <p class="mt-4 text-slate-300">
            Aplicación web para la gestión de bandas de música.
          </p>
        </div>

        <div class="rounded-2xl bg-white/10 p-6">
          <p class="text-sm text-slate-300">
            Accede a tus particellas, confirma asistencia a eventos y consulta la actividad de la banda.
          </p>
        </div>
      </div>

      <div class="p-8 md:p-12">
        <h2 class="text-3xl font-bold text-slate-900 dark:text-white">
          Iniciar sesión
        </h2>

        <p class="mt-2 text-slate-500 dark:text-slate-300">
          Introduce tus credenciales para acceder.
        </p>

        <div class="mt-8 space-y-5">
          <div>
            <label class="mb-2 block text-sm font-semibold text-slate-700 dark:text-slate-300">
              Email
            </label>

            <input
              v-model="email"
              type="email"
              placeholder="admin@banda.com"
              class="w-full rounded-xl border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
            />
          </div>

          <div>
            <label class="mb-2 block text-sm font-semibold text-slate-700 dark:text-slate-300">
              Contraseña
            </label>

            <input
              v-model="password"
              type="password"
              placeholder="••••••••"
              class="w-full rounded-xl border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
              @keyup.enter="login"
            />
          </div>

          <button
            type="button"
            @click="login"
            class="w-full rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-700"
          >
            Entrar
          </button>
        </div>
      </div>
    </div>
  </section>
</template>