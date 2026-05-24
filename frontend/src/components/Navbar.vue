<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import {
  LayoutDashboard,
  Users,
  Music,
  FileMusic,
  CalendarDays,
  ClipboardCheck,
  Boxes,
  UserCircle,
  LogOut,
  CalendarSync,
  LucideCalendarDays,
  Calendar1,
  CalendarDaysIcon,
  UserCircle2,
  TicketCheck
} from "lucide-vue-next";

const router = useRouter();

const usuario = JSON.parse(
  localStorage.getItem("usuario")
);

const isDark = ref(
  localStorage.getItem("darkMode") === "true"
);

const menuMovilAbierto = ref(false);

if (isDark.value) {

  document.documentElement.classList.add("dark");

} else {

  document.documentElement.classList.remove("dark");
}

const toggleDarkMode = () => {

  isDark.value = !isDark.value;

  if (isDark.value) {

    document.documentElement.classList.add("dark");

    localStorage.setItem(
      "darkMode",
      "true"
    );

  } else {

    document.documentElement.classList.remove("dark");

    localStorage.setItem(
      "darkMode",
      "false"
    );
  }
};

const logout = () => {

  localStorage.removeItem("token");
  localStorage.removeItem("usuario");

  router.push("/");
};
</script>

<template>
  <div>
    <div
      v-if="menuMovilAbierto"
      @click="menuMovilAbierto = false"
      class="fixed inset-0 z-40 bg-black/50 lg:hidden"
    ></div>

    <aside
      :class="
        menuMovilAbierto
          ? 'translate-x-0'
          : '-translate-x-full lg:translate-x-0'
      "
      class="fixed left-0 top-0 z-50 flex h-screen w-64 flex-col justify-between border-r border-slate-800 bg-slate-950 text-white transition-transform duration-300 ease-in-out"
    >
      <div class="min-h-0 flex-1 overflow-y-auto">
        <div class="border-b border-slate-800 p-6">
          <h1 class="text-3xl font-bold">
            Gestión Banda
          </h1>

          <p class="mt-2 text-slate-400">
            Panel de control
          </p>
        </div>

        <nav class="mt-6 flex flex-col gap-2 px-4 pb-6">
          <router-link
            v-if="usuario?.rol === 'admin'"
            to="/dashboard"
            @click="menuMovilAbierto = false"
            class="flex items-center gap-3 rounded-xl px-4 py-3 hover:bg-blue-600"
            active-class="bg-blue-600"
          >
            <LayoutDashboard class="h-5 w-5" />
            Dashboard
          </router-link>

          <router-link
            v-if="usuario?.rol === 'admin'"
            to="/usuarios"
            @click="menuMovilAbierto = false"
            class="flex items-center gap-3 rounded-xl px-4 py-3 hover:bg-blue-600"
            active-class="bg-blue-600"
          >
            <Users class="h-5 w-5" />
            Usuarios
          </router-link>

          <router-link
            to="/eventos"
            @click="menuMovilAbierto = false"
            class="flex items-center gap-3 rounded-xl px-4 py-3 hover:bg-blue-600"
            active-class="bg-blue-600"
          >
            <TicketCheck class="h-5 w-5" />
            Eventos
          </router-link>

          <router-link
            v-if="usuario?.rol === 'admin'"
            to="/obras"
            @click="menuMovilAbierto = false"
            class="flex items-center gap-3 rounded-xl px-4 py-3 hover:bg-blue-600"
            active-class="bg-blue-600"
          >
            <Music class="h-5 w-5" />
            Obras
          </router-link>

          <router-link
            v-if="usuario?.rol === 'musico'"
            to="/mis-particellas"
            @click="menuMovilAbierto = false"
            class="flex items-center gap-3 rounded-xl px-4 py-3 hover:bg-blue-600"
            active-class="bg-blue-600"
          >
            <FileMusic class="h-5 w-5" />
            Mis partituras
          </router-link>

          <router-link
            v-if="usuario?.rol === 'admin'"
            to="/particellas"
            @click="menuMovilAbierto = false"
            class="flex items-center gap-3 rounded-xl px-4 py-3 hover:bg-blue-600"
            active-class="bg-blue-600"
          >
            <FileMusic class="h-5 w-5" />
            Particellas
          </router-link>

          <router-link
            to="/calendario"
            @click="menuMovilAbierto = false"
            class="flex items-center gap-3 rounded-xl px-4 py-3 hover:bg-blue-600"
            active-class="bg-blue-600"
          >
            <CalendarDaysIcon class="h-5 w-5" />
            Calendario
          </router-link>

          <router-link
            v-if="usuario?.rol === 'admin'"
            to="/inventario"
            @click="menuMovilAbierto = false"
            class="flex items-center gap-3 rounded-xl px-4 py-3 hover:bg-blue-600"
            active-class="bg-blue-600"
          >
            <Boxes class="h-5 w-5" />
            Inventario
          </router-link>

          <router-link
            to="/perfil"
            @click="menuMovilAbierto = false"
            class="flex items-center gap-3 rounded-xl px-4 py-3 hover:bg-blue-600"
            active-class="bg-blue-600"
          >
            <UserCircle2 class="h-5 w-5" />
            Mi perfil
          </router-link>
        </nav>
      </div>

      <div class="border-t border-slate-800 p-4">
        <div class="mb-4">
          <p class="font-semibold">
            {{ usuario.nombre }}
          </p>

          <p class="text-slate-400">
            {{ usuario.rol }}
          </p>
        </div>

        <button
          @click="logout"
          class="flex w-full items-center justify-center gap-2 rounded-xl bg-red-600 px-4 py-3 font-semibold text-white hover:bg-red-700"
        >
          <LogOut class="h-5 w-5" />
          Cerrar sesión
        </button>
      </div>
    </aside>

    <header
      class="sticky top-0 z-30 flex items-center justify-between border-b bg-white px-6 py-4 dark:bg-slate-900 lg:ml-64"
    >
      <div class="flex items-center gap-3">
        <button
          @click="menuMovilAbierto = true"
          class="rounded-xl border px-4 py-2 text-slate-800 dark:border-slate-700 dark:text-white lg:hidden"
        >
          ☰
        </button>

        <h2 class="text-xl font-bold text-slate-800 dark:text-white">
          Gestión Banda
        </h2>
      </div>

      <div class="flex items-center gap-4">
        <span class="hidden text-slate-600 dark:text-slate-300 md:block">
          {{ usuario.nombre }} · {{ usuario.rol }}
        </span>

        <button
          @click="toggleDarkMode"
          class="rounded-xl border px-4 py-2 dark:border-slate-700"
        >
          {{ isDark ? "☀️" : "🌙" }}
        </button>
      </div>
    </header>
  </div>
</template>