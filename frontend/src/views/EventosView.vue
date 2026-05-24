<script setup>
import { ref, computed, onMounted } from "vue";
import { toast } from "vue-sonner";
import Swal from "sweetalert2";
import api from "../api/axios";

const eventos = ref([]);
const cargando = ref(true);

const usuario = JSON.parse(localStorage.getItem("usuario"));

const modoEdicion = ref(false);
const eventoEditando = ref(null);

const nuevoEvento = ref({
  titulo: "",
  descripcion: "",
  fecha: "",
  hora: "",
  ubicacion: "",
  tipo: "ensayo"
});

const mostrarRespondidos = ref(false);
const vistaEventos = ref("pendientes");

const eventosPendientes = computed(() => {
  if (usuario.rol !== "musico") {
    return eventos.value;
  }

  return eventos.value.filter((e) => !e.mi_asistencia);
});

const eventosRespondidos = computed(() => {
  if (usuario.rol !== "musico") {
    return [];
  }

  return eventos.value.filter((e) => e.mi_asistencia);
});

const eventosMostrados = computed(() => {
  if (usuario.rol !== "musico") {
    return eventos.value;
  }

  if (vistaEventos.value === "pendientes") {
    return eventos.value.filter((e) => !e.mi_asistencia);
  }

  if (vistaEventos.value === "respondidos") {
    return eventos.value.filter((e) => e.mi_asistencia);
  }

  if (vistaEventos.value === "ensayos") {
    return eventos.value.filter((e) => e.tipo === "ensayo");
  }

  if (vistaEventos.value === "eventos") {
    return eventos.value.filter(
      (e) => e.tipo === "concierto" || e.tipo === "procesion"
    );
  }

  return eventos.value;
});

const totalEnsayos = computed(() => {
  return eventos.value.filter((e) => e.tipo === "ensayo").length;
});

const totalEventosMusico = computed(() => {
  return eventos.value.filter(
    (e) => e.tipo === "concierto" || e.tipo === "procesion"
  ).length;
});

const cargarEventos = async () => {
  cargando.value = true;

  try {
    const response = await api.get("/eventos/");
    eventos.value = response.data;
  } catch (error) {
    toast.error("Error al cargar eventos");
  } finally {
    cargando.value = false;
  }
};

const limpiarNuevoEvento = () => {
  nuevoEvento.value = {
    titulo: "",
    descripcion: "",
    fecha: "",
    hora: "",
    ubicacion: "",
    tipo: "ensayo"
  };
};

const crearEvento = async () => {
  if (!nuevoEvento.value.titulo) {
    toast.error("El título es obligatorio");
    return;
  }

  if (!nuevoEvento.value.fecha) {
    toast.error("La fecha es obligatoria");
    return;
  }

  if (!nuevoEvento.value.hora) {
    toast.error("La hora es obligatoria");
    return;
  }

  if (!nuevoEvento.value.tipo) {
    toast.error("El tipo de evento es obligatorio");
    return;
  }

  try {
    await api.post("/eventos/", nuevoEvento.value);

    toast.success("Evento creado correctamente");

    limpiarNuevoEvento();
    cargarEventos();

  } catch (error) {
    toast.error(error.response?.data?.error || "Error al crear evento");
  }
};

const abrirEdicion = (evento) => {
  modoEdicion.value = true;

  eventoEditando.value = {
    id: evento.id,
    titulo: evento.titulo || "",
    descripcion: evento.descripcion || "",
    fecha: evento.fecha || "",
    hora: evento.hora || "",
    ubicacion: evento.ubicacion || "",
    tipo: evento.tipo || "ensayo"
  };
};

const cerrarEdicion = () => {
  modoEdicion.value = false;
  eventoEditando.value = null;
};

const guardarEdicion = async () => {
  if (!eventoEditando.value.titulo) {
    toast.error("El título es obligatorio");
    return;
  }

  if (!eventoEditando.value.fecha) {
    toast.error("La fecha es obligatoria");
    return;
  }

  if (!eventoEditando.value.hora) {
    toast.error("La hora es obligatoria");
    return;
  }

  if (!eventoEditando.value.tipo) {
    toast.error("El tipo de evento es obligatorio");
    return;
  }

  try {
    await api.put(
      `/eventos/${eventoEditando.value.id}`,
      eventoEditando.value
    );

    toast.success("Evento actualizado correctamente");

    cerrarEdicion();
    cargarEventos();

  } catch (error) {
    toast.error(error.response?.data?.error || "Error al actualizar evento");
  }
};

const eliminarEvento = async (evento) => {
  const result = await Swal.fire({
    title: "¿Eliminar evento?",
    text: `Se eliminará "${evento.titulo}". Esta acción no se puede deshacer.`,
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
    await api.delete(`/eventos/${evento.id}`);

    toast.success("Evento eliminado correctamente");

    cargarEventos();
  } catch (error) {
    toast.error(error.response?.data?.error || "Error al eliminar evento");
  }
};

const responderAsistencia = async (eventoId, estado) => {
  let comentario = "";

  if (estado === "no_asistira") {
    const result = await Swal.fire({
      title: "Motivo de ausencia",
      input: "textarea",
      inputLabel: "Indica por qué no podrás asistir",
      inputPlaceholder: "Escribe el motivo...",
      showCancelButton: true,
      confirmButtonText: "Enviar",
      cancelButtonText: "Cancelar",
      confirmButtonColor: "#dc2626",
      cancelButtonColor: "#64748b",
      inputValidator: (value) => {
        if (!value) {
          return "Debes indicar un motivo";
        }
      }
    });

    if (!result.isConfirmed) {
      return;
    }

    comentario = result.value;
  }

  try {
    await api.post("/asistencias/", {
      evento_id: eventoId,
      estado,
      comentario
    });

    toast.success("Asistencia registrada");
    cargarEventos();
  } catch (error) {
    toast.error("Error al registrar asistencia");
  }
};

onMounted(() => {
  cargarEventos();
});
</script>

<template>
  <section class="p-6 lg:p-10">
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-slate-900 dark:text-white">
        Eventos
      </h1>

      <p class="mt-2 text-slate-600 dark:text-slate-300">
        Gestión de ensayos, conciertos y procesiones.
      </p>
    </div>

    <div
      v-if="usuario.rol === 'admin'"
      class="mb-8 rounded-2xl bg-white p-6 shadow-sm dark:bg-slate-900"
    >
      <h2 class="mb-5 text-xl font-semibold text-slate-800 dark:text-white">
        Crear evento
      </h2>

      <div class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
        <input
          v-model="nuevoEvento.titulo"
          placeholder="Título"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        />

        <input
          v-model="nuevoEvento.descripcion"
          placeholder="Descripción"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        />

        <input
          type="date"
          v-model="nuevoEvento.fecha"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        />

        <input
          type="time"
          v-model="nuevoEvento.hora"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        />

        <input
          v-model="nuevoEvento.ubicacion"
          placeholder="Ubicación"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        />

        <select
          v-model="nuevoEvento.tipo"
          class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
        >
          <option value="ensayo">Ensayo</option>
          <option value="concierto">Concierto</option>
          <option value="procesion">Procesión</option>
        </select>
      </div>

      <button
        @click="crearEvento"
        class="mt-5 rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-700"
      >
        Crear evento
      </button>
    </div>

    <div
      v-if="usuario.rol === 'musico'"
      class="mb-6 flex flex-wrap gap-3"
    >
      <button
        @click="vistaEventos = 'pendientes'"
        class="rounded-xl px-5 py-3 font-semibold"
        :class="
          vistaEventos === 'pendientes'
            ? 'bg-blue-600 text-white'
            : 'bg-white text-slate-700 dark:bg-slate-900 dark:text-slate-200'
        "
      >
        Pendientes ({{ eventosPendientes.length }})
      </button>

      <button
        @click="vistaEventos = 'respondidos'"
        class="rounded-xl px-5 py-3 font-semibold"
        :class="
          vistaEventos === 'respondidos'
            ? 'bg-blue-600 text-white'
            : 'bg-white text-slate-700 dark:bg-slate-900 dark:text-slate-200'
        "
      >
        Respondidos ({{ eventosRespondidos.length }})
      </button>

      <button
        @click="vistaEventos = 'ensayos'"
        class="rounded-xl px-5 py-3 font-semibold"
        :class="
          vistaEventos === 'ensayos'
            ? 'bg-blue-600 text-white'
            : 'bg-white text-slate-700 dark:bg-slate-900 dark:text-slate-200'
        "
      >
        Ensayos ({{ totalEnsayos }})
      </button>

      <button
        @click="vistaEventos = 'eventos'"
        class="rounded-xl px-5 py-3 font-semibold"
        :class="
          vistaEventos === 'eventos'
            ? 'bg-blue-600 text-white'
            : 'bg-white text-slate-700 dark:bg-slate-900 dark:text-slate-200'
        "
      >
        Eventos ({{ totalEventosMusico }})
      </button>
    </div>

    <div
      v-if="cargando"
      class="rounded-2xl bg-white p-10 text-center shadow-sm dark:bg-slate-900"
    >
      <div
        class="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"
      ></div>

      <p class="text-slate-500 dark:text-slate-300">
        Cargando eventos...
      </p>
    </div>

    <div
      v-else-if="eventosMostrados.length === 0"
      class="rounded-2xl bg-white p-10 text-center shadow-sm dark:bg-slate-900"
    >
      <p class="text-lg font-semibold text-slate-700 dark:text-slate-200">
        No hay eventos disponibles.
      </p>

      <p class="mt-2 text-slate-500 dark:text-slate-300">
        Actualmente no tienes eventos en esta sección.
      </p>
    </div>

    <div
      v-else
      class="grid grid-cols-1 gap-6 xl:grid-cols-2"
    >
      <div
        v-for="evento in eventosMostrados"
        :key="evento.id"
        class="rounded-2xl bg-white p-6 shadow-sm transition-all duration-200 hover:-translate-y-1 hover:shadow-lg dark:bg-slate-900"
      >
        <div class="mb-4 flex items-start justify-between gap-4">
          <div>
            <h2 class="text-2xl font-bold text-slate-900 dark:text-white">
              {{ evento.titulo }}
            </h2>

            <p class="mt-1 text-slate-500 dark:text-slate-300">
              {{ evento.descripcion }}
            </p>
          </div>

          <span
            class="rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-700 dark:bg-blue-900 dark:text-blue-200"
          >
            {{ evento.tipo }}
          </span>
        </div>

        <div class="space-y-2 text-sm text-slate-600 dark:text-slate-300">
          <p>📅 {{ evento.fecha }}</p>
          <p>🕒 {{ evento.hora }}</p>
          <p>📍 {{ evento.ubicacion }}</p>
        </div>

        <div
          v-if="usuario.rol === 'musico' && evento.mi_asistencia"
          class="mt-5 rounded-xl p-4"
          :class="
            evento.mi_asistencia.estado === 'asistira'
              ? 'bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-200'
              : 'bg-red-50 text-red-700 dark:bg-red-900/30 dark:text-red-200'
          "
        >
          <p class="font-semibold">
            Respuesta registrada:
            {{
              evento.mi_asistencia.estado === 'asistira'
                ? 'Asistiré'
                : 'No asistiré'
            }}
          </p>

          <p
            v-if="evento.mi_asistencia.comentario"
            class="mt-1 text-sm"
          >
            Motivo: {{ evento.mi_asistencia.comentario }}
          </p>
        </div>

        <div
          v-if="usuario.rol === 'musico'"
          class="mt-6 flex gap-3"
        >
          <button
            @click="responderAsistencia(evento.id, 'asistira')"
            class="rounded-xl bg-green-600 px-4 py-3 font-semibold text-white hover:bg-green-700"
          >
            Asistiré
          </button>

          <button
            @click="responderAsistencia(evento.id, 'no_asistira')"
            class="rounded-xl bg-red-600 px-4 py-3 font-semibold text-white hover:bg-red-700"
          >
            No asistiré
          </button>
        </div>

        <div
          v-if="usuario.rol === 'admin'"
          class="mt-6 flex flex-wrap gap-3"
        >
          <router-link
            :to="`/eventos/${evento.id}/asistencias`"
            class="rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-700"
          >
            Ver asistencias
          </router-link>

          <button
            @click="abrirEdicion(evento)"
            class="rounded-xl bg-yellow-500 px-4 py-3 font-semibold text-white hover:bg-yellow-600"
          >
            Editar
          </button>

          <button
            @click="eliminarEvento(evento)"
            class="rounded-xl bg-red-600 px-4 py-3 font-semibold text-white hover:bg-red-700"
          >
            Eliminar
          </button>
        </div>
      </div>
    </div>

    <div
      v-if="modoEdicion"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-6"
    >
      <div class="w-full max-w-3xl rounded-2xl bg-white p-6 dark:bg-slate-900">
        <h2 class="mb-5 text-2xl font-bold text-slate-900 dark:text-white">
          Editar evento
        </h2>

        <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
          <input
            v-model="eventoEditando.titulo"
            placeholder="Título"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          />

          <input
            v-model="eventoEditando.descripcion"
            placeholder="Descripción"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          />

          <input
            type="date"
            v-model="eventoEditando.fecha"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          />

          <input
            type="time"
            v-model="eventoEditando.hora"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          />

          <input
            v-model="eventoEditando.ubicacion"
            placeholder="Ubicación"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          />

          <select
            v-model="eventoEditando.tipo"
            class="rounded-xl border px-4 py-3 dark:border-slate-700 dark:bg-slate-800"
          >
            <option value="ensayo">Ensayo</option>
            <option value="concierto">Concierto</option>
            <option value="procesion">Procesión</option>
          </select>
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