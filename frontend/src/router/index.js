import { createRouter, createWebHistory } from "vue-router";

import LoginView from "../views/LoginView.vue";
import DashboardView from "../views/DashboardView.vue";
import UsuariosView from "../views/UsuariosView.vue";
import EventosView from "../views/EventosView.vue";
import ObrasView from "../views/ObrasView.vue";
import ParticellasView from "../views/ParticellasView.vue";
import MisParticellasView from "../views/MisParticellasView.vue";
import AsistenciasEventoView from "../views/AsistenciasEventoView.vue";
import CalendarioView from "../views/CalendarioView.vue";
import PerfilView from "../views/PerfilView.vue";
import NotFoundView from "../views/NotFoundView.vue";
import InventarioView from "../views/InventarioView.vue";

const routes = [
  {
    path: "/",
    component: LoginView
  },
  {
    path: "/dashboard",
    component: DashboardView,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: "/usuarios",
    component: UsuariosView,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: "/eventos",
    component: EventosView,
    meta: { requiresAuth: true }
  },
  {
    path: "/obras",
    component: ObrasView,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: "/particellas",
    component: ParticellasView,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: "/mis-particellas",
    component: MisParticellasView,
    meta: { requiresAuth: true }
  },
  {
    path: "/eventos/:id/asistencias",
    component: AsistenciasEventoView,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: "/calendario",
    component: CalendarioView,
    meta: { requiresAuth: true }
  },
  {
    path: "/perfil",
    component: PerfilView,
    meta: { requiresAuth: true }
  },
  {
    path: "/inventario",
    component: InventarioView,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: "/:pathMatch(.*)*",
    component: NotFoundView
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to) => {
  const token = localStorage.getItem("token");

  const usuario = JSON.parse(
    localStorage.getItem("usuario")
  );

  if (to.meta.requiresAuth && !token) {
    return "/";
  }

  if (
    to.meta.requiresAdmin &&
    usuario?.rol !== "admin"
  ) {
    return "/eventos";
  }
});

export default router;