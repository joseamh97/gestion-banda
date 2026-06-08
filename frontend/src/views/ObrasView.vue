<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../api/axios";
import { toast } from "vue-sonner";
import Swal from "sweetalert2";

const obras = ref([]);
const editando = ref(false);
const obraEditandoId = ref(null);
const busqueda = ref("");
const orden = ref("titulo");
const direccion = ref("asc");

const nuevaObra = ref({
  titulo: "",
  compositor: "",
  genero: "",
  descripcion: ""
});

const cargarObras = async () => {
  const response = await api.get("/obras/");
  obras.value = response.data;
};

const limpiarFormulario = () => {
  editando.value = false;
  obraEditandoId.value = null;

  nuevaObra.value = {
    titulo: "",
    compositor: "",
    genero: "",
    descripcion: ""
  };
};

const guardarObra = async () => {
  try {
    if (editando.value) {
      await api.put(`/obras/${obraEditandoId.value}`, nuevaObra.value);
      toast.success("Obra creada correctamente");
    } else {
      await api.post("/obras/", nuevaObra.value);
      toast.success("Obra creada correctamente");
    }

    limpiarFormulario();
    cargarObras();
  } catch (error) {
    toast.error("Error al guardar obra");
  }
};

const editarObra = (obra) => {
  editando.value = true;
  obraEditandoId.value = obra.id;

  nuevaObra.value = {
    titulo: obra.titulo,
    compositor: obra.compositor || "",
    genero: obra.genero || "",
    descripcion: obra.descripcion || ""
  };
};

const eliminarObra = async (id) => {
  const result = await Swal.fire({
    title: "¿Eliminar obra?",
    text: "Esta acción no se puede deshacer",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#dc2626",
    cancelButtonColor: "#64748b",
    confirmButtonText: "Sí, eliminar",
    cancelButtonText: "Cancelar"
  });
  if (!result.isConfirmed) {
    return;
  }
  try {
    await api.delete(`/obras/${id}`);
    toast.success(
      "Obra eliminada correctamente"
    );
    cargarObras();
  } catch (error) {
    toast.error(
      "Error al eliminar obra"
    );
  }
};

const ordenarPor = (campo) => {
  if (orden.value === campo) {
    direccion.value = direccion.value === "asc" ? "desc" : "asc";
  } else {
    orden.value = campo;
    direccion.value = "asc";
  }
};

const obrasFiltradas = computed(() => {
  const filtradas = obras.value.filter((o) => {
    const texto = `
      ${o.titulo}
      ${o.compositor}
      ${o.genero}
      ${o.descripcion}
    `.toLowerCase();

    return texto.includes(busqueda.value.toLowerCase());
  });

  filtradas.sort((a, b) => {
    const valorA = (a[orden.value] || "").toString().toLowerCase();
    const valorB = (b[orden.value] || "").toString().toLowerCase();

    return direccion.value === "asc"
      ? valorA.localeCompare(valorB)
      : valorB.localeCompare(valorA);
  });

  return filtradas;
});

onMounted(() => {
  cargarObras();
});
</script>

<template>
  <section class="p-6 lg:p-10">
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-slate-900 dark:text-white">
        Obras
      </h1>

      <p class="mt-2 text-slate-600 dark:text-slate-300">
        Gestiona el catálogo musical de la banda.
      </p>
    </div>

    <div class="mb-8 rounded-2xl bg-white p-6 shadow-sm dark:bg-slate-900">
      <h2 class="mb-5 text-xl font-semibold text-slate-800 dark:text-white">
        {{ editando ? "Editar obra" : "Crear nueva obra" }}
      </h2>

      <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
        <input
          v-model="nuevaObra.titulo"
          class="rounded-xl border px-4 py-3 text-slate-900 placeholder:text-slate-400 outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:placeholder:text-slate-500"
          placeholder="Título"
        />

        <input
          v-model="nuevaObra.compositor"
          class="rounded-xl border px-4 py-3 text-slate-900 placeholder:text-slate-400 outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:placeholder:text-slate-500"
          placeholder="Compositor"
        />

        <input
          v-model="nuevaObra.genero"
          class="rounded-xl border px-4 py-3 text-slate-900 placeholder:text-slate-400 outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:placeholder:text-slate-500"
          placeholder="Género"
        />

        <input
          v-model="nuevaObra.descripcion"
          class="rounded-xl border px-4 py-3 text-slate-900 placeholder:text-slate-400 outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:placeholder:text-slate-500"
          placeholder="Descripción"
        />
      </div>

      <div class="mt-5 flex flex-wrap gap-3">
        <button
          @click="guardarObra"
          class="rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-700"
        >
          {{ editando ? "Guardar cambios" : "Crear obra" }}
        </button>

        <button
          v-if="editando"
          @click="limpiarFormulario"
          class="rounded-xl border px-5 py-3 font-semibold text-slate-700 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
        >
          Cancelar
        </button>
      </div>
    </div>

    <div class="overflow-hidden rounded-2xl bg-white shadow-sm dark:bg-slate-900">
      <div class="border-b border-slate-200 px-6 py-4 dark:border-slate-700">
        <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <h2 class="text-xl font-semibold text-slate-800 dark:text-white">
            Listado de obras
          </h2>
          <input
            v-model="busqueda"
            placeholder="Buscar obra, compositor o género"
            class="rounded-xl border px-4 py-3 text-slate-900 placeholder:text-slate-400 outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:placeholder:text-slate-500"
          />
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead class="bg-slate-50 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
            <tr>
              <th
                @click="ordenarPor('titulo')"
                class="cursor-pointer px-6 py-4 hover:text-blue-600"
              >
                Título
              </th>

              <th
                @click="ordenarPor('compositor')"
                class="cursor-pointer px-6 py-4 hover:text-blue-600"
              >
                Compositor
              </th>

              <th
                @click="ordenarPor('genero')"
                class="cursor-pointer px-6 py-4 hover:text-blue-600"
              >
                Género
              </th>

              <th
                @click="ordenarPor('descripcion')"
                class="cursor-pointer px-6 py-4 hover:text-blue-600"
              >
                Descripción
              </th>

              <th class="px-6 py-4 text-right">
                Acciones
              </th>
            </tr>
          </thead>

          <tbody class="divide-y divide-slate-200 dark:divide-slate-700">
            <tr
              v-for="obra in obrasFiltradas"
              :key="obra.id"
              class="transition-colors duration-200 hover:bg-slate-50 dark:hover:bg-slate-800"
            >
              <td class="px-6 py-4 font-medium text-slate-900 dark:text-white">
                {{ obra.titulo }}
              </td>

              <td class="px-6 py-4 text-slate-600 dark:text-slate-300">
                {{ obra.compositor || "-" }}
              </td>

              <td class="px-6 py-4">
                <span class="rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700 dark:bg-green-900 dark:text-green-200">
                  {{ obra.genero || "Sin género" }}
                </span>
              </td>

              <td class="px-6 py-4 text-slate-600 dark:text-slate-300">
                {{ obra.descripcion || "-" }}
              </td>

              <td class="px-6 py-4 text-right">
                <button
                  @click="editarObra(obra)"
                  class="rounded-lg bg-yellow-500 px-3 py-2 text-sm font-semibold text-white hover:bg-yellow-600"
                >
                  Editar
                </button>

                <button
                  @click="eliminarObra(obra.id)"
                  class="ml-2 rounded-lg bg-red-600 px-3 py-2 text-sm font-semibold text-white hover:bg-red-700"
                >
                  Eliminar
                </button>
              </td>
            </tr>

            <tr v-if="obrasFiltradas.length === 0">
              <td
                colspan="5"
                class="px-6 py-8 text-center text-slate-500 dark:text-slate-300"
              >
                No hay obras registradas.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    </section>
</template>