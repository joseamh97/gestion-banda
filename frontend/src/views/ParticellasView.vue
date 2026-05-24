<script setup>
import { ref, onMounted, computed } from "vue";
import { toast } from "vue-sonner";
import Swal from "sweetalert2";
import api from "../api/axios";

const obras = ref([]);
const particellas = ref([]);
const busqueda = ref("");
const cargando = ref(true);

const modoEdicion = ref(false);
const particellaEditando = ref(null);
const archivoEditando = ref(null);
const seleccionadas = ref([]);

const formulario = ref({
  obra_id: "",
  instrumento: "",
  voz: "",
  archivos_pdf: []
});

const orden = ref("obra");
const direccion = ref("asc");
const inputArchivo = ref(null);

const particellasFiltradas = computed(() => {

  const filtradas = particellas.value.filter((p) => {

    const texto =
      `${p.obra} ${p.instrumento} ${p.voz}`.toLowerCase();

    return texto.includes(
      busqueda.value.toLowerCase()
    );
  });

  filtradas.sort((a, b) => {

    const valorA =
      (a[orden.value] || "").toString().toLowerCase();

    const valorB =
      (b[orden.value] || "").toString().toLowerCase();

    if (direccion.value === "asc") {
      return valorA.localeCompare(valorB);
    }

    return valorB.localeCompare(valorA);
  });

  return filtradas;
});

const cargarObras = async () => {
  const response = await api.get("/obras/");
  obras.value = response.data;
};

const cargarParticellas = async () => {
  cargando.value = true;

  try {
    const response = await api.get("/particellas/");
    particellas.value = response.data;
  } catch (error) {
    toast.error("Error al cargar particellas");
  } finally {
    cargando.value = false;
  }
};

const seleccionarArchivo = (event) => {
  formulario.value.archivos_pdf = Array.from(event.target.files);
};

const seleccionarArchivoEdicion = (event) => {
  archivoEditando.value = event.target.files[0];
};

const limpiarFormulario = () => {
  formulario.value = {
    obra_id: "",
    instrumento: "",
    voz: "",
    archivos_pdf: []
  };

  if (inputArchivo.value) {
    inputArchivo.value.value = "";
  }
};
const subirParticella = async () => {
  if (!formulario.value.obra_id) {
    toast.error("Debes seleccionar una obra");
    return;
  }

  if (formulario.value.archivos_pdf.length === 0) {
    toast.error("Debes seleccionar al menos un PDF");
    return;
  }

  try {
    const formData = new FormData();

    formData.append("obra_id", formulario.value.obra_id);

    if (formulario.value.instrumento) {
      formData.append("instrumento", formulario.value.instrumento);
    }

    if (formulario.value.voz) {
      formData.append("voz", formulario.value.voz);
    }

    formulario.value.archivos_pdf.forEach((archivo) => {
      formData.append("archivo_pdf", archivo);
    });

    await api.post("/particellas/", formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    });

    toast.success("Particellas subidas correctamente");

    limpiarFormulario();
    cargarParticellas();

  } catch (error) {
    toast.error(error.response?.data?.error || "Error al subir particellas");
  }
};

const abrirPDF = (ruta) => {
  window.open(`http://127.0.0.1:5000/${ruta}`, "_blank");
};

const abrirEdicion = (particella) => {
  modoEdicion.value = true;
  archivoEditando.value = null;

  particellaEditando.value = {
    id: particella.id,
    obra_id: particella.obra_id,
    instrumento:
      particella.instrumento === "Pendiente"
        ? ""
        : particella.instrumento,
    voz:
      particella.voz === "Pendiente"
        ? ""
        : particella.voz,
    archivo_pdf: particella.archivo_pdf
  };
};

const cerrarEdicion = () => {
  modoEdicion.value = false;
  particellaEditando.value = null;
  archivoEditando.value = null;
};

const guardarEdicion = async () => {
  if (!particellaEditando.value.obra_id) {
    toast.error("Debes seleccionar una obra");
    return;
  }

  try {
    const formData = new FormData();

    formData.append("obra_id", particellaEditando.value.obra_id);
    formData.append("instrumento",
      particellaEditando.value.instrumento || "Pendiente"
    );
    formData.append("voz",
      particellaEditando.value.voz || "Pendiente"
    );

    if (archivoEditando.value) {
      formData.append("archivo_pdf", archivoEditando.value);
    }

    await api.put(
      `/particellas/${particellaEditando.value.id}`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      }
    );

    toast.success("Particella actualizada correctamente");

    cerrarEdicion();
    cargarParticellas();

  } catch (error) {
    toast.error(error.response?.data?.error || "Error al actualizar particella");
  }
};

const eliminarParticella = async (particella) => {
  const result = await Swal.fire({
    title: "¿Eliminar particella?",
    text: `Se eliminará la particella de ${particella.instrumento} ${particella.voz}.`,
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
    await api.delete(`/particellas/${particella.id}`);

    toast.success("Particella eliminada correctamente");

    cargarParticellas();
  } catch (error) {
    toast.error("Error al eliminar particella");
  }
};

const eliminarSeleccionadas = async () => {

  if (seleccionadas.value.length === 0) {
    toast.error("No has seleccionado particellas");
    return;
  }

  const result = await Swal.fire({
    title: "¿Eliminar particellas?",
    text: `Se eliminarán ${seleccionadas.value.length} particellas.`,
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

    await Promise.all(
      seleccionadas.value.map((id) =>
        api.delete(`/particellas/${id}`)
      )
    );

    toast.success(
      "Particellas eliminadas correctamente"
    );

    seleccionadas.value = [];

    cargarParticellas();

  } catch (error) {

    toast.error(
      "Error al eliminar particellas"
    );
  }
};

const ordenarPor = (campo) => {

  if (orden.value === campo) {

    direccion.value =
      direccion.value === "asc"
        ? "desc"
        : "asc";

  } else {

    orden.value = campo;
    direccion.value = "asc";
  }
};

onMounted(() => {
  cargarObras();
  cargarParticellas();
});
</script>

<template>
  <section class="p-6 lg:p-10">
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-slate-900 dark:text-white">
        Particellas
      </h1>

      <p class="mt-2 text-slate-600 dark:text-slate-300">
        Sube, organiza, edita y elimina particellas PDF por obra, instrumento y voz.
      </p>
    </div>

    <div class="mb-8 rounded-2xl bg-white p-6 shadow-sm dark:bg-slate-900">
      <h2 class="mb-5 text-xl font-semibold text-slate-800 dark:text-white">
        Subir nueva particella
      </h2>

      <div class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
        <select
          v-model="formulario.obra_id"
          class="rounded-xl border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-800"
        >
          <option value="">Selecciona obra</option>

          <option v-for="obra in obras" :key="obra.id" :value="obra.id">
            {{ obra.titulo }}
          </option>
        </select>

        <input
          v-model="formulario.instrumento"
          class="rounded-xl border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-800"
          placeholder="Instrumento"
        />

        <input
          v-model="formulario.voz"
          class="rounded-xl border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-800"
          placeholder="Voz / Parte"
        />

        <input
          type="file"
          multiple
          accept=".pdf"
          ref="inputArchivo"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800 file:mr-4 file:rounded-lg file:border-0 file:bg-blue-600 file:px-4 file:py-2 file:text-white hover:file:bg-blue-700"
          @change="seleccionarArchivo"
        />
      </div>

      <button
        @click="subirParticella"
        class="mt-5 rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-700"
      >
        Subir PDF
      </button>
    </div>

    <div class="overflow-hidden rounded-2xl bg-white shadow-sm dark:bg-slate-900">
      <div class="flex flex-col gap-4 border-b border-slate-200 px-6 py-4 dark:border-slate-700 md:flex-row md:items-center md:justify-between">
        <h2 class="text-xl font-semibold text-slate-800 dark:text-white">
          Listado de particellas
        </h2>
        <div class="mt-3">
          <button
            v-if="seleccionadas.length > 0"
            @click="eliminarSeleccionadas"
            class="rounded-xl bg-red-600 px-5 py-3 text-sm font-semibold text-white hover:bg-red-700"
          >
            Eliminar seleccionadas ({{ seleccionadas.length }})
          </button>
        </div>
        <input
          v-model="busqueda"
          class="w-full rounded-xl border px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-800 md:w-80"
          placeholder="Buscar por obra, instrumento o voz"
        />
      </div>

      <div v-if="cargando" class="p-10 text-center">
        <div
          class="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"
        ></div>

        <p class="text-slate-500 dark:text-slate-300">
          Cargando particellas...
        </p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead class="bg-slate-50 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
            <tr>
              <th @click="ordenarPor('obra')" class="cursor-pointer px-6 py-4 hover:text-blue-600">
                Obra
              </th>
              <th @click="ordenarPor('instrumento')" class="cursor-pointer px-6 py-4 hover:text-blue-600">
                Instrumento
              </th>
              <th @click="ordenarPor('voz')" class="cursor-pointer px-6 py-4 hover:text-blue-600">
                Voz
              </th>
              <th class="px-6 py-4 text-right">Acciones</th>
            </tr>
            <th class="px-6 py-4">
              <input
                type="checkbox"
                :checked="
                  particellasFiltradas.length > 0 &&
                  seleccionadas.length === particellasFiltradas.length
                "
                @change="
                  seleccionadas =
                    $event.target.checked
                      ? particellasFiltradas.map((p) => p.id)
                      : []
                "
              />
            </th>
          </thead>

          <tbody class="divide-y divide-slate-200 dark:divide-slate-700">
            <tr
              v-for="p in particellasFiltradas"
              :key="p.id"
              class="transition-colors duration-200 hover:bg-slate-50 dark:hover:bg-slate-800"
            >
              <td class="px-6 py-4">
                <input
                  type="checkbox"
                  :value="p.id"
                  v-model="seleccionadas"
                />
              </td>
              <td class="px-6 py-4 font-medium text-slate-900 dark:text-white">
                {{ p.obra }}
              </td>

              <td class="px-6 py-4">
                <span
                  class="rounded-full px-3 py-1 text-xs font-semibold"
                  :class="
                    p.instrumento === 'Pendiente'
                      ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-200'
                      : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-200'
                  "
                >
                  {{ p.instrumento }}
                </span>
              </td>

              <td class="px-6 py-4">
                <span class="rounded-full bg-purple-100 px-3 py-1 text-xs font-semibold text-purple-700 dark:bg-purple-900 dark:text-purple-200">
                  {{ p.voz }}
                </span>
              </td>

              <td class="px-6 py-4">
                <div class="flex justify-end gap-3">
                  <button
                    @click="abrirPDF(p.archivo_pdf)"
                    class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700"
                  >
                    Ver PDF
                  </button>

                  <button
                    @click="abrirEdicion(p)"
                    class="rounded-lg bg-yellow-500 px-4 py-2 text-sm font-semibold text-white hover:bg-yellow-600"
                  >
                    Editar
                  </button>

                  <button
                    @click="eliminarParticella(p)"
                    class="rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-700"
                  >
                    Eliminar
                  </button>
                </div>
              </td>
            </tr>

            <tr v-if="particellasFiltradas.length === 0">
              <td colspan="5" class="px-6 py-8 text-center text-slate-500 dark:text-slate-300">
                No se encontraron particellas.
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
          Editar particella
        </h2>

        <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
          <select
            v-model="particellaEditando.obra_id"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          >
            <option value="">Selecciona obra</option>

            <option v-for="obra in obras" :key="obra.id" :value="obra.id">
              {{ obra.titulo }}
            </option>
          </select>

          <input
            v-model="particellaEditando.instrumento"
            placeholder="Instrumento"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          />

          <input
            v-model="particellaEditando.voz"
            placeholder="Voz / Parte"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          />

          <input
            type="file"
            accept=".pdf"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800 file:mr-4 file:rounded-lg file:border-0 file:bg-blue-600 file:px-4 file:py-2 file:text-white hover:file:bg-blue-700"
            @change="seleccionarArchivoEdicion"
          />
        </div>

        <p class="mt-4 text-sm text-slate-500 dark:text-slate-300">
          Si no seleccionas un nuevo PDF, se mantendrá el archivo actual.
        </p>

        <div
          v-if="particellaEditando.archivo_pdf"
          class="mt-4 rounded-xl bg-slate-100 p-4 dark:bg-slate-800"
          >
          <p class="text-sm font-semibold text-slate-700 dark:text-slate-200">
            PDF actual
          </p>

          <p class="mt-1 break-all text-sm text-slate-500 dark:text-slate-300">
            {{
              particellaEditando.archivo_pdf.split("/").pop()
            }}
          </p>
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