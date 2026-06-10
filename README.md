# Aplicación Web para la Gestión de Bandas de Música

Trabajo Fin de Grado del Grado en Ingeniería Informática
Escuela Politécnica Superior de Córdoba
Universidad de Córdoba

---

## Descripción

Este proyecto consiste en el desarrollo de una aplicación web orientada a la gestión interna de bandas de música. La plataforma permite centralizar la administración de usuarios, obras musicales, particellas, eventos, asistencias e inventario, facilitando la organización diaria de una agrupación musical.

El sistema cuenta con dos tipos principales de usuarios: administrador y músico. El administrador puede gestionar la información general de la banda, mientras que cada músico puede acceder a sus particellas correspondientes y consultar los eventos programados.

---

## Funcionalidades principales

* Autenticación de usuarios mediante JWT.
* Gestión de usuarios con roles diferenciados.
* Gestión de obras musicales y particellas en PDF.
* Acceso a particellas según instrumento y voz.
* Gestión de eventos: ensayos, conciertos y procesiones.
* Confirmación de asistencia a eventos.
* Gestión de inventario.
* Dashboard con estadísticas generales.
* Exportación de datos a Excel.
* Interfaz responsive con modo claro y oscuro.

---

## Tecnologías utilizadas

### Backend

* Python
* Flask
* Flask-JWT-Extended
* SQLAlchemy
* Flask-Migrate
* MySQL

### Frontend

* Vue 3
* Vite
* Vue Router
* Axios
* Tailwind CSS
* SweetAlert2
* XLSX

---

## Estructura del proyecto

```text
banda/
│
├── backend/
│   │
│   ├── app.py                 # Punto de entrada principal de Flask
│   ├── config.py              # Configuración de la aplicación
│   ├── extensions.py          # Inicialización de extensiones
│   ├── models.py              # Modelos de base de datos
│   ├── requirements.txt       # Dependencias Python
│   ├── .env.example           # Ejemplo de variables de entorno
│   │
│   ├── migrations/            # Migraciones de base de datos
│   │
│   ├── routes/                # Rutas y lógica de la API
│   │   ├── auth_routes.py
│   │   ├── usuarios_routes.py
│   │   ├── obras_routes.py
│   │   ├── particellas_routes.py
│   │   ├── eventos_routes.py
│   │   ├── dashboard_routes.py
│   │   ├── inventario_routes.py
│   │   └── asistencias_routes.py
│   │
│   └── uploads/               # PDFs y archivos subidos
│
├── frontend/
│   │
│   ├── package.json           # Dependencias Node.js
│   ├── vite.config.js         # Configuración de Vite
│   ├── tailwind.config.js     # Configuración Tailwind CSS
│   │
│   ├── public/                # Recursos públicos
│   │
│   └── src/
│       │
│       ├── main.js            # Punto de entrada Vue
│       ├── App.vue            # Componente principal
│       ├── style.css          # Estilos globales
│       │
│       ├── router/            # Configuración de rutas
│       │   └── index.js
│       │
│       ├── services/          # Configuración Axios/API
│       │   └── axios.js
│       │
│       ├── components/        # Componentes reutilizables
│       │   ├── Navbar.vue
│       │   ├── Sidebar.vue
│       │   └── StatsChart.vue
│       │
│       └── views/             # Vistas principales
│           ├── LoginView.vue
│           ├── DashboardView.vue
│           ├── UsuariosView.vue
│           ├── ObrasView.vue
│           ├── ParticellasView.vue
│           ├── MisParticellasView.vue
│           ├── EventosView.vue
│           ├── AsistenciasEventoView.vue
│           ├── InventarioView.vue
│           ├── PerfilView.vue
│           └── NotFoundView.vue
│
├── README.md                  # Documentación principal
└── .gitignore                 # Archivos ignorados por Git
```

## Instalación y ejecución

### Backend

Acceder a la carpeta del backend:

```bash
cd backend
```

Crear y activar un entorno virtual:

```bash
python -m venv venv
```

En Windows:

```bash
venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Configurar las variables de entorno en un archivo `.env`:

```env
DB_USER=usuario
DB_PASSWORD=contraseña
DB_HOST=localhost
DB_NAME=banda_db
JWT_SECRET_KEY=clave_secreta
```

Ejecutar el servidor:

```bash
flask run
```

---

### Frontend

Acceder a la carpeta del frontend:

```bash
cd frontend
```

Instalar dependencias:

```bash
npm install
```

Ejecutar el servidor de desarrollo:

```bash
npm run dev
```

---

## Base de datos

La aplicación utiliza MySQL como sistema gestor de base de datos.
Las migraciones se gestionan mediante Flask-Migrate.

Comandos principales:

```bash
flask db init
flask db migrate -m "Migración inicial"
flask db upgrade
```

---

## Seguridad

El sistema utiliza autenticación mediante JSON Web Tokens (JWT), permitiendo proteger las rutas privadas y diferenciar el acceso según el rol del usuario.

El archivo `.env` no debe subirse al repositorio, ya que contiene información sensible como credenciales de base de datos y claves secretas.

---

## Autor

José Antonio Méndez Heredia

---

## Proyecto académico

Trabajo Fin de Grado
Grado en Ingeniería Informática
Universidad de Córdoba
