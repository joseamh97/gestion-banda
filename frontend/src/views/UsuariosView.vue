<script setup>
import { ref, computed, onMounted } from "vue";
import { toast } from "vue-sonner";
import api from "../api/axios";
import Swal from "sweetalert2";
import * as XLSX from "xlsx";

const usuarios = ref([]);
const busqueda = ref("");
const cargando = ref(true);

const modoEdicion = ref(false);
const usuarioEditando = ref(null);

const nuevoUsuario = ref({
  nombre: "",
  apellidos: "",
  email: "",
  password: "",
  rol: "musico",
  instrumento: "",
  voz: "",
  telefono: ""
});

const orden = ref("nombre");
const direccion = ref("asc");

const cargarUsuarios = async () => {
  cargando.value = true;

  try {
    const response = await api.get("/usuarios/");
    usuarios.value = response.data;
  } catch (error) {
    toast.error("Error al cargar usuarios");
  } finally {
    cargando.value = false;
  }
};

const usuariosFiltrados = computed(() => {
  const filtrados = usuarios.value.filter((u) => {
    const texto = `
      ${u.nombre}
      ${u.apellidos}
      ${u.email}
      ${u.rol}
      ${u.instrumento}
      ${u.voz}
      ${u.telefono}
    `.toLowerCase();

    return texto.includes(busqueda.value.toLowerCase());
  });

  filtrados.sort((a, b) => {
    const valorA = (a[orden.value] || "").toString().toLowerCase();
    const valorB = (b[orden.value] || "").toString().toLowerCase();

    if (direccion.value === "asc") {
      return valorA.localeCompare(valorB);
    }

    return valorB.localeCompare(valorA);
  });

  return filtrados;
});

const limpiarNuevoUsuario = () => {
  nuevoUsuario.value = {
    nombre: "",
    apellidos: "",
    email: "",
    password: "",
    rol: "musico",
    instrumento: "",
    voz: "",
    telefono: ""
  };
};

const crearUsuario = async () => {
  if (!nuevoUsuario.value.nombre) {
    toast.error("El nombre es obligatorio");
    return;
  }

  if (!nuevoUsuario.value.apellidos) {
    toast.error("Los apellidos son obligatorios");
    return;
  }

  if (!nuevoUsuario.value.email) {
    toast.error("El email es obligatorio");
    return;
  }

  if (!nuevoUsuario.value.password) {
    toast.error("La contraseña es obligatoria");
    return;
  }

  if (!nuevoUsuario.value.rol) {
    toast.error("El rol es obligatorio");
    return;
  }

  if (nuevoUsuario.value.rol === "musico") {
    if (!nuevoUsuario.value.instrumento) {
      toast.error("El instrumento es obligatorio para músicos");
      return;
    }

    if (!nuevoUsuario.value.voz) {
      toast.error("La voz es obligatoria para músicos");
      return;
    }
  }

  try {
    await api.post("/auth/register", nuevoUsuario.value);

    toast.success("Usuario creado correctamente");
    limpiarNuevoUsuario();
    cargarUsuarios();

  } catch (error) {
    toast.error(error.response?.data?.error || "Error al crear usuario");
  }
};

const editarUsuario = (usuario) => {
  modoEdicion.value = true;

  usuarioEditando.value = {
    id: usuario.id,
    nombre: usuario.nombre || "",
    apellidos: usuario.apellidos || "",
    email: usuario.email || "",
    password: "",
    rol: usuario.rol || "musico",
    instrumento: usuario.instrumento || "",
    voz: usuario.voz || "",
    telefono: usuario.telefono || "",
    activo: usuario.activo
  };
};

const cerrarModal = () => {
  modoEdicion.value = false;
  usuarioEditando.value = null;
};

const guardarEdicion = async () => {
  if (!usuarioEditando.value.nombre) {
    toast.error("El nombre es obligatorio");
    return;
  }

  if (!usuarioEditando.value.apellidos) {
    toast.error("Los apellidos son obligatorios");
    return;
  }

  if (!usuarioEditando.value.email) {
    toast.error("El email es obligatorio");
    return;
  }

  if (!usuarioEditando.value.rol) {
    toast.error("El rol es obligatorio");
    return;
  }

  if (usuarioEditando.value.rol === "musico") {
    if (!usuarioEditando.value.instrumento) {
      toast.error("El instrumento es obligatorio para músicos");
      return;
    }

    if (!usuarioEditando.value.voz) {
      toast.error("La voz es obligatoria para músicos");
      return;
    }
  }

  try {
    await api.put(
      `/usuarios/${usuarioEditando.value.id}`,
      usuarioEditando.value
    );

    toast.success("Usuario actualizado correctamente");

    cerrarModal();
    cargarUsuarios();

  } catch (error) {
    toast.error(error.response?.data?.error || "Error al actualizar usuario");
  }
};

const eliminarUsuario = async (id) => {
  const result = await Swal.fire({
    title: "¿Dar de baja usuario?",
    text: "El usuario quedará marcado como inactivo.",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#dc2626",
    cancelButtonColor: "#64748b",
    confirmButtonText: "Sí, dar de baja",
    cancelButtonText: "Cancelar"
  });

  if (!result.isConfirmed) {
    return;
  }

  try {
    await api.delete(`/usuarios/${id}`);

    toast.success("Usuario dado de baja");

    cargarUsuarios();
  } catch (error) {
    toast.error("Error al dar de baja usuario");
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

const exportarUsuariosExcel = () => {
  const datos = usuariosFiltrados.value.map((u) => ({
    Nombre: u.nombre,
    Apellidos: u.apellidos,
    Email: u.email,
    Rol: u.rol,
    Instrumento: u.instrumento || "",
    Voz: u.voz || "",
    Teléfono: u.telefono || "",
    Activo: u.activo ? "Sí" : "No"
  }));

  const hoja = XLSX.utils.json_to_sheet(datos);
  const libro = XLSX.utils.book_new();

  XLSX.utils.book_append_sheet(libro, hoja, "Usuarios");

  XLSX.writeFile(libro, "usuarios_banda.xlsx");
};

onMounted(() => {
  cargarUsuarios();
});

</script>

<template>
  <section class="p-6 lg:p-10">
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-slate-900 dark:text-white">
        Usuarios
      </h1>

      <p class="mt-2 text-slate-600 dark:text-slate-300">
        Gestión completa de músicos y administradores.
      </p>
    </div>

    <div class="mb-8 rounded-2xl bg-white p-6 shadow-sm dark:bg-slate-900">
      <h2 class="mb-5 text-xl font-semibold text-slate-800 dark:text-white">
        Crear usuario
      </h2>

      <div class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
        <input
          v-model="nuevoUsuario.nombre"
          placeholder="Nombre"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        />

        <input
          v-model="nuevoUsuario.apellidos"
          placeholder="Apellidos"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        />

        <input
          v-model="nuevoUsuario.email"
          placeholder="Email"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        />

        <input
          v-model="nuevoUsuario.password"
          type="password"
          placeholder="Contraseña"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        />

        <input
          v-model="nuevoUsuario.instrumento"
          placeholder="Instrumento"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        />

        <input
          v-model="nuevoUsuario.voz"
          placeholder="Voz / Parte"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        />

        <input
          v-model="nuevoUsuario.telefono"
          placeholder="Teléfono"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        />

        <select
          v-model="nuevoUsuario.rol"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        >
          <option value="musico">Músico</option>
          <option value="admin">Administrador</option>
        </select>
      </div>

      <button
        @click="crearUsuario"
        class="mt-5 rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-700"
      >
        Crear usuario
      </button>
    </div>

    <div class="mb-6 flex justify-end">
      <input
        v-model="busqueda"
        placeholder="Buscar usuario..."
        class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
      />
    </div>

    <button
      @click="exportarUsuariosExcel"
      class="rounded-xl bg-green-600 px-5 py-3 font-semibold text-white hover:bg-green-700"
      >
      Exportar Excel
    </button>

    <div class="overflow-hidden rounded-2xl bg-white shadow-sm dark:bg-slate-900">
      <div v-if="cargando" class="p-10 text-center">
        <div
          class="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"
        ></div>

        <p class="text-slate-500 dark:text-slate-300">
          Cargando usuarios...
        </p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead class="bg-slate-50 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
            <tr>
              <th @click="ordenarPor('nombre')"class="cursor-pointer px-6 py-4 hover:text-blue-600">
                Nombre
              </th>
              <th @click="ordenarPor('email')"class="cursor-pointer px-6 py-4 hover:text-blue-600">
                Email
              </th>
              <th @click="ordenarPor('rol')"class="cursor-pointer px-6 py-4 hover:text-blue-600">
                Rol
              </th>
              <th @click="ordenarPor('instrumento')"class="cursor-pointer px-6 py-4 hover:text-blue-600">
                Instrumento
              </th>
              <th @click="ordenarPor('voz')"class="cursor-pointer px-6 py-4 hover:text-blue-600">
                Voz
              </th>
              <th @click="ordenarPor('estado')"class="cursor-pointer px-6 py-4 hover:text-blue-600">
                Estado
              </th>
              <th class="px-6 py-4">Acciones</th>
            </tr>
          </thead>

          <tbody class="divide-y divide-slate-200 dark:divide-slate-700">
            <tr
              v-for="u in usuariosFiltrados"
              :key="u.id"
              class="transition-colors duration-200 hover:bg-slate-50 dark:hover:bg-slate-800"
            >
              <td class="px-6 py-4 font-medium text-slate-900 dark:text-white">
                {{ u.nombre }} {{ u.apellidos }}
              </td>

              <td class="px-6 py-4 text-slate-600 dark:text-slate-300">
                {{ u.email }}
              </td>

              <td class="px-6 py-4">
                <span class="rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-700">
                  {{ u.rol }}
                </span>
              </td>

              <td class="px-6 py-4 text-slate-600 dark:text-slate-300">
                {{ u.instrumento || "-" }}
              </td>

              <td class="px-6 py-4 text-slate-600 dark:text-slate-300">
                {{ u.voz || "-" }}
              </td>

              <td class="px-6 py-4">
                <span
                  class="rounded-full px-3 py-1 text-xs font-semibold"
                  :class="
                    u.activo
                      ? 'bg-green-100 text-green-700'
                      : 'bg-red-100 text-red-700'
                  "
                >
                  {{ u.activo ? "Activo" : "Inactivo" }}
                </span>
              </td>

              <td class="flex gap-3 px-6 py-4">
                <button
                  @click="editarUsuario(u)"
                  class="rounded-lg bg-yellow-500 px-3 py-2 text-white hover:bg-yellow-600"
                >
                  Editar
                </button>

                <button
                  @click="eliminarUsuario(u.id)"
                  class="rounded-lg bg-red-600 px-3 py-2 text-white hover:bg-red-700"
                  :disabled="!u.activo"
                >
                  Baja
                </button>
              </td>
            </tr>

            <tr v-if="usuariosFiltrados.length === 0">
              <td
                colspan="7"
                class="px-6 py-8 text-center text-slate-500 dark:text-slate-300"
              >
                No se encontraron usuarios.
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
          Editar usuario
        </h2>

        <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
          <input
            v-model="usuarioEditando.nombre"
            placeholder="Nombre"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          />

          <input
            v-model="usuarioEditando.apellidos"
            placeholder="Apellidos"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          />

          <input
            v-model="usuarioEditando.email"
            placeholder="Email"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          />

          <input
            v-model="usuarioEditando.password"
            type="password"
            placeholder="Nueva contraseña"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          />

          <input
            v-model="usuarioEditando.instrumento"
            placeholder="Instrumento"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          />

          <input
            v-model="usuarioEditando.voz"
            placeholder="Voz / Parte"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          />

          <input
            v-model="usuarioEditando.telefono"
            placeholder="Teléfono"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          />

          <select
            v-model="usuarioEditando.rol"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          >
            <option value="musico">Músico</option>
            <option value="admin">Administrador</option>
          </select>
        </div>

        <div class="mt-6 flex justify-end gap-3">
          <button
            @click="cerrarModal"
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