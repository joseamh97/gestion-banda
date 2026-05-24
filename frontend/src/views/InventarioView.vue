<script setup>
import { ref, computed, onMounted } from "vue";
import { toast } from "vue-sonner";
import Swal from "sweetalert2";

import api from "../api/axios";

const items = ref([]);
const usuarios = ref([]);
const busqueda = ref("");
const cargando = ref(true);

const modoEdicion = ref(false);
const itemEditando = ref(null);

const nuevoItem = ref({
  nombre: "",
  categoria: "Instrumento",
  estado: "disponible",
  numero_serie: "",
  observaciones: "",
  usuario_id: ""
});

const orden = ref("nombre");
const direccion = ref("asc");

const itemsFiltrados = computed(() => {
  const filtrados = items.value.filter((i) => {
    const texto = `
      ${i.nombre}
      ${i.categoria}
      ${i.estado}
      ${i.numero_serie}
      ${i.observaciones}
      ${i.usuario}
    `.toLowerCase();

    return texto.includes(busqueda.value.toLowerCase());
  });

  filtrados.sort((a, b) => {
    const valorA = (a[orden.value] || "").toString().toLowerCase();
    const valorB = (b[orden.value] || "").toString().toLowerCase();

    return direccion.value === "asc"
      ? valorA.localeCompare(valorB)
      : valorB.localeCompare(valorA);
  });

  return filtrados;
});
const cargarInventario = async () => {
  cargando.value = true;

  try {
    const response = await api.get("/inventario/");
    items.value = response.data;
  } catch (error) {
    toast.error("Error al cargar inventario");
  } finally {
    cargando.value = false;
  }
};

const cargarUsuarios = async () => {
  try {
    const response = await api.get("/usuarios/");
    usuarios.value = response.data.filter((u) => u.rol === "musico" && u.activo);
  } catch (error) {
    toast.error("Error al cargar usuarios");
  }
};

const limpiarFormulario = () => {
  nuevoItem.value = {
    nombre: "",
    categoria: "Instrumento",
    estado: "disponible",
    numero_serie: "",
    observaciones: "",
    usuario_id: ""
  };
};

const crearItem = async () => {
  if (!nuevoItem.value.nombre) {
    toast.error("El nombre es obligatorio");
    return;
  }

  if (!nuevoItem.value.categoria) {
    toast.error("La categoría es obligatoria");
    return;
  }

  try {
    await api.post("/inventario/", nuevoItem.value);

    toast.success("Elemento creado correctamente");

    limpiarFormulario();
    cargarInventario();
  } catch (error) {
    toast.error(error.response?.data?.error || "Error al crear elemento");
  }
};

const abrirEdicion = (item) => {
  modoEdicion.value = true;

  itemEditando.value = {
    id: item.id,
    nombre: item.nombre || "",
    categoria: item.categoria || "Instrumento",
    estado: item.estado || "disponible",
    numero_serie: item.numero_serie || "",
    observaciones: item.observaciones || "",
    usuario_id: item.usuario_id || ""
  };
};

const cerrarEdicion = () => {
  modoEdicion.value = false;
  itemEditando.value = null;
};

const guardarEdicion = async () => {
  if (!itemEditando.value.nombre) {
    toast.error("El nombre es obligatorio");
    return;
  }

  if (!itemEditando.value.categoria) {
    toast.error("La categoría es obligatoria");
    return;
  }

  try {
    await api.put(`/inventario/${itemEditando.value.id}`, itemEditando.value);

    toast.success("Elemento actualizado correctamente");

    cerrarEdicion();
    cargarInventario();
  } catch (error) {
    toast.error(error.response?.data?.error || "Error al actualizar elemento");
  }
};

const eliminarItem = async (item) => {
  const result = await Swal.fire({
    title: "¿Eliminar elemento?",
    text: `Se eliminará "${item.nombre}" del inventario.`,
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
    await api.delete(`/inventario/${item.id}`);

    toast.success("Elemento eliminado correctamente");

    cargarInventario();
  } catch (error) {
    toast.error("Error al eliminar elemento");
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

onMounted(() => {
  cargarInventario();
  cargarUsuarios();
});
</script>

<template>
  <section class="p-6 lg:p-10">
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-slate-900 dark:text-white">
        Inventario
      </h1>

      <p class="mt-2 text-slate-600 dark:text-slate-300">
        Gestión de instrumentos, uniformes, accesorios y material de la banda.
      </p>
    </div>

    <div class="mb-8 rounded-2xl bg-white p-6 shadow-sm dark:bg-slate-900">
      <h2 class="mb-5 text-xl font-semibold text-slate-800 dark:text-white">
        Añadir elemento
      </h2>

      <div class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
        <input
          v-model="nuevoItem.nombre"
          placeholder="Nombre del material"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        />

        <select
          v-model="nuevoItem.categoria"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        >
          <option value="Instrumento">Instrumento</option>
          <option value="Uniforme">Uniforme</option>
          <option value="Accesorio">Accesorio</option>
          <option value="Material">Material</option>
        </select>

        <select
          v-model="nuevoItem.estado"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        >
          <option value="disponible">Disponible</option>
          <option value="prestado">Prestado</option>
          <option value="reparacion">Reparación</option>
          <option value="baja">Baja</option>
        </select>

        <input
          v-model="nuevoItem.numero_serie"
          placeholder="Número de serie / Código"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        />

        <select
          v-model="nuevoItem.usuario_id"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        >
          <option value="">Sin asignar</option>

          <option
            v-for="usuario in usuarios"
            :key="usuario.id"
            :value="usuario.id"
          >
            {{ usuario.nombre }} {{ usuario.apellidos }}
          </option>
        </select>

        <input
          v-model="nuevoItem.observaciones"
          placeholder="Observaciones"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        />
      </div>

      <button
        @click="crearItem"
        class="mt-5 rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-700"
      >
        Añadir al inventario
      </button>
    </div>

    <div class="overflow-hidden rounded-2xl bg-white shadow-sm dark:bg-slate-900">
      <div class="flex flex-col gap-4 border-b border-slate-200 px-6 py-4 dark:border-slate-700 md:flex-row md:items-center md:justify-between">
        <h2 class="text-xl font-semibold text-slate-800 dark:text-white">
          Listado de inventario
        </h2>

        <input
          v-model="busqueda"
          placeholder="Buscar material..."
          class="w-full rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800 md:w-80"
        />
      </div>

      <div v-if="cargando" class="p-10 text-center">
        <div
          class="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"
        ></div>

        <p class="text-slate-500 dark:text-slate-300">
          Cargando inventario...
        </p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead class="bg-slate-50 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
            <tr>
              <th @click="ordenarPor('nombre')" class="cursor-pointer px-6 py-4 hover:text-blue-600">Nombre</th>
              <th @click="ordenarPor('categoria')" class="cursor-pointer px-6 py-4 hover:text-blue-600">Categoría</th>
              <th @click="ordenarPor('estado')" class="cursor-pointer px-6 py-4 hover:text-blue-600">Estado</th>
              <th @click="ordenarPor('numero_serie')" class="cursor-pointer px-6 py-4 hover:text-blue-600">Código</th>
              <th @click="ordenarPor('usuario')" class="cursor-pointer px-6 py-4 hover:text-blue-600">Asignado a</th>
              <th class="px-6 py-4 text-right">Acciones</th>
            </tr>
          </thead>

          <tbody class="divide-y divide-slate-200 dark:divide-slate-700">
            <tr
              v-for="item in itemsFiltrados"
              :key="item.id"
              class="transition-colors duration-200 hover:bg-slate-50 dark:hover:bg-slate-800"
            >
              <td class="px-6 py-4 font-medium text-slate-900 dark:text-white">
                {{ item.nombre }}
              </td>

              <td class="px-6 py-4 text-slate-600 dark:text-slate-300">
                {{ item.categoria }}
              </td>

              <td class="px-6 py-4">
                <span
                  class="rounded-full px-3 py-1 text-xs font-semibold"
                  :class="{
                    'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-200': item.estado === 'disponible',
                    'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-200': item.estado === 'prestado',
                    'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-200': item.estado === 'reparacion',
                    'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-200': item.estado === 'baja'
                  }"
                >
                  {{ item.estado }}
                </span>
              </td>

              <td class="px-6 py-4 text-slate-600 dark:text-slate-300">
                {{ item.numero_serie || "-" }}
              </td>

              <td class="px-6 py-4 text-slate-600 dark:text-slate-300">
                {{ item.usuario || "Sin asignar" }}
              </td>

              <td class="px-6 py-4">
                <div class="flex justify-end gap-3">
                  <button
                    @click="abrirEdicion(item)"
                    class="rounded-lg bg-yellow-500 px-4 py-2 text-sm font-semibold text-white hover:bg-yellow-600"
                  >
                    Editar
                  </button>

                  <button
                    @click="eliminarItem(item)"
                    class="rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-700"
                  >
                    Eliminar
                  </button>
                </div>
              </td>
            </tr>

            <tr v-if="itemsFiltrados.length === 0">
              <td colspan="6" class="px-6 py-8 text-center text-slate-500 dark:text-slate-300">
                No se encontraron elementos.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div
      v-if="modoEdicion"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-6"
    >
      <div class="w-full max-w-3xl rounded-2xl bg-white p-6 dark:bg-slate-900">
        <h2 class="mb-5 text-2xl font-bold text-slate-900 dark:text-white">
          Editar elemento
        </h2>

        <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
          <input
            v-model="itemEditando.nombre"
            placeholder="Nombre del material"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          />

          <select
            v-model="itemEditando.categoria"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          >
            <option value="Instrumento">Instrumento</option>
            <option value="Uniforme">Uniforme</option>
            <option value="Accesorio">Accesorio</option>
            <option value="Material">Material</option>
          </select>

          <select
            v-model="itemEditando.estado"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          >
            <option value="disponible">Disponible</option>
            <option value="prestado">Prestado</option>
            <option value="reparacion">Reparación</option>
            <option value="baja">Baja</option>
          </select>

          <input
            v-model="itemEditando.numero_serie"
            placeholder="Número de serie / Código"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          />

          <select
            v-model="itemEditando.usuario_id"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          >
            <option value="">Sin asignar</option>

            <option
              v-for="usuario in usuarios"
              :key="usuario.id"
              :value="usuario.id"
            >
              {{ usuario.nombre }} {{ usuario.apellidos }}
            </option>
          </select>

          <input
            v-model="itemEditando.observaciones"
            placeholder="Observaciones"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          />
        </div>

        <div class="mt-6 flex justify-end gap-3">
          <button
            @click="cerrarEdicion"
            class="rounded-xl border px-5 py-3 dark:border-slate-700"
          >
            Cancelar
          </button>

          <button
            @click="guardarEdicion"
            class="rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-700"
          >
            Guardar cambios
          </button>
        </div>
      </div>
    </div>
  </section>
</template>