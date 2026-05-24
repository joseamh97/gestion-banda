<script setup>
import { ref } from "vue";
import { toast } from "vue-sonner";
import api from "../api/axios";

const usuarioGuardado = JSON.parse(
  localStorage.getItem("usuario")
);

const usuario = ref({
  ...usuarioGuardado
});

const guardarPerfil = async () => {
  if (!usuario.value.nombre || !usuario.value.apellidos || !usuario.value.email) {
    toast.error("Nombre, apellidos y email son obligatorios");
    return;
  }

  try {
    const response = await api.put(
      "/usuarios/me",
      usuario.value
    );

    localStorage.setItem(
      "usuario",
      JSON.stringify(response.data.usuario)
    );

    usuario.value = response.data.usuario;

    toast.success(
      "Perfil actualizado correctamente"
    );

  } catch (error) {
    toast.error(
      error.response?.data?.error || "Error al actualizar perfil"
    );
  }
};
</script>

<template>

<section class="p-6 lg:p-10">

  <div class="mb-8">

    <h1
      class="
        text-4xl
        font-bold
        text-slate-900
        dark:text-white
      "
    >
      Mi perfil
    </h1>

    <p
      class="
        mt-2
        text-slate-600
        dark:text-slate-300
      "
    >
      Consulta y modifica tus datos.
    </p>

  </div>

  <div
    class="
      max-w-4xl
      rounded-2xl
      bg-white
      p-6
      shadow-sm
      dark:bg-slate-900
    "
  >

    <div
      class="
        mb-8
        flex
        items-center
        gap-4
      "
    >

      <div
        class="
          flex
          h-20
          w-20
          items-center
          justify-center
          rounded-full
          bg-blue-600
          text-3xl
          font-bold
          text-white
        "
      >
        {{ usuario.nombre.charAt(0) }}
      </div>

      <div>

        <h2
          class="
            text-2xl
            font-bold
            text-slate-900
            dark:text-white
          "
        >
          {{ usuario.nombre }}
          {{ usuario.apellidos }}
        </h2>

        <p
          class="
            text-slate-500
            dark:text-slate-300
          "
        >
          {{ usuario.rol }}
        </p>

      </div>

    </div>

    <div
      class="
        grid
        grid-cols-1
        gap-4
        md:grid-cols-2
      "
    >

      <div>

        <label
          class="
            mb-2
            block
            text-sm
            font-semibold
            text-slate-700
            dark:text-slate-300
          "
        >
          Nombre
        </label>

        <input
          v-model="usuario.nombre"
          class="
            w-full
            rounded-xl
            border
            px-4
            py-3
            dark:border-slate-700
            dark:bg-slate-800
          "
        />

      </div>

      <div>

        <label
          class="
            mb-2
            block
            text-sm
            font-semibold
            text-slate-700
            dark:text-slate-300
          "
        >
          Apellidos
        </label>

        <input
          v-model="usuario.apellidos"
          class="
            w-full
            rounded-xl
            border
            px-4
            py-3
            dark:border-slate-700
            dark:bg-slate-800
          "
        />

      </div>

      <div>

        <label
          class="
            mb-2
            block
            text-sm
            font-semibold
            text-slate-700
            dark:text-slate-300
          "
        >
          Email
        </label>

        <input
          v-model="usuario.email"
          class="
            w-full
            rounded-xl
            border
            px-4
            py-3
            dark:border-slate-700
            dark:bg-slate-800
          "
        />

      </div>

      <div>

        <label
          class="
            mb-2
            block
            text-sm
            font-semibold
            text-slate-700
            dark:text-slate-300
          "
        >
          Teléfono
        </label>

        <input
          v-model="usuario.telefono"
          class="
            w-full
            rounded-xl
            border
            px-4
            py-3
            dark:border-slate-700
            dark:bg-slate-800
          "
        />

      </div>

      <div>

        <label
          class="
            mb-2
            block
            text-sm
            font-semibold
            text-slate-700
            dark:text-slate-300
          "
        >
          Instrumento
        </label>

        <input
          disabled
          v-model="usuario.instrumento"
          class="
            w-full
            rounded-xl
            border
            bg-slate-100
            px-4
            py-3
            dark:border-slate-700
            dark:bg-slate-800
          "
        />

      </div>

      <div>

        <label
          class="
            mb-2
            block
            text-sm
            font-semibold
            text-slate-700
            dark:text-slate-300
          "
        >
          Voz / Parte
        </label>

        <input
          disabled
          v-model="usuario.voz"
          class="
            w-full
            rounded-xl
            border
            bg-slate-100
            px-4
            py-3
            dark:border-slate-700
            dark:bg-slate-800
          "
        />

      </div>

    </div>

    <button
      @click="guardarPerfil"
      class="
        mt-6
        rounded-xl
        bg-blue-600
        px-5
        py-3
        font-semibold
        text-white
        hover:bg-blue-700
      "
    >
      Guardar cambios
    </button>

  </div>

</section>

</template>