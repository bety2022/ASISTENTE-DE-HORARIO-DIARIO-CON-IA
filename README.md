# 🎯 Asistente de Horario Diario con IA

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-green?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Pandas-Data-yellow?style=for-the-badge&logo=pandas)
![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

> Aplicación de escritorio inteligente que gestiona tus tareas diarias, aprende de tus hábitos y te mantiene motivado. 🚀

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Cómo Funciona la IA](#-cómo-funciona-la-ia)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## ✨ Características

| Característica | Descripción |
|---|---|
| 📅 **Calendario Interactivo** | Visualiza y filtra tareas por día |
| 🤖 **IA de Aprendizaje** | Aprende tus patrones y recomienda horas óptimas |
| ⏰ **Recordatorios Automáticos** | Notificaciones en tiempo real |
| 🎨 **Interfaz Intuitiva** | Diseño limpio con prioridades por color |
| 💾 **Guardado Automático** | Persistencia en JSON sin base de datos |
| 📊 **Estadísticas** | Análisis de productividad en tiempo real |
| 💪 **Motivación** | Frases motivacionales personalizadas |

---

## 📸 Capturas de Pantalla

> 💡 *Agrega aquí capturas de pantalla de tu aplicación*

```
screenshot_principal.png   → Vista general de la app
screenshot_calendario.png  → Filtrado por fecha
screenshot_estadisticas.png → Panel de IA
```

---

## 🛠 Requisitos

- Python **3.7** o superior
- pip (gestor de paquetes)

### Dependencias externas

```
pandas>=1.3.0
tkcalendar>=1.6.1
```

> `tkinter`, `json`, `threading` y demás ya vienen incluidos con Python.

---

## 🚀 Instalación

### 1. Clona el repositorio

```bash
git clone https://github.com/tu-usuario/asistente-horario-ia.git
cd asistente-horario-ia
```

### 2. (Opcional) Crea un entorno virtual

```bash
# Crear
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en Mac/Linux
source venv/bin/activate
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecuta la aplicación

```bash
python horario.py
```

---

## 📖 Uso

### Agregar una tarea
1. Escribe el **nombre** de la tarea
2. Ingresa la **hora** en formato `HH:MM`
3. Define la **duración** en minutos
4. Selecciona la **prioridad** (Alta 🔴 / Media 🟡 / Baja 🟢)
5. Haz clic en **➕ Agregar Tarea**

### Usar la IA
- **🤖 Recomendar Hora** → La IA sugiere tu hora más productiva
- **⏳ Predecir Duración** → Estima el tiempo basado en tu historial

### Completar / Eliminar tareas
- Selecciona una tarea de la lista
- Usa **✓ Completar** o **🗑 Eliminar**

### Filtrar por fecha
- Haz clic en cualquier día del **calendario** para ver sus tareas

---

## 📁 Estructura del Proyecto

```
asistente-horario-ia/
│
├── horario.py          # Aplicación principal
├── requirements.txt    # Dependencias del proyecto
├── .gitignore          # Archivos ignorados por Git
├── LICENSE             # Licencia MIT
├── CONTRIBUTING.md     # Guía para contribuir
├── README.md           # Este archivo
│
└── tareas_data.json    # ⚠️ Se genera automáticamente (no subir a Git)
```

---

## 🧠 Cómo Funciona la IA

La clase `TaskLearningIA` implementa un sistema de aprendizaje basado en historial:

```
Tarea completada
      ↓
Registra hora, duración y día
      ↓
Analiza patrones (últimas 10 tareas)
      ↓
Actualiza horas productivas + duraciones promedio
      ↓
Genera recomendaciones personalizadas
```

**Algoritmo de predicción de duración:**
- Toma las últimas 5 ocurrencias de una tarea similar
- Calcula el promedio ponderado
- Retorna `30 min` como valor por defecto si no hay historial

**Nivel de consistencia:**
- Aumenta `+10%` por cada tarea completada
- Máximo: `100%`

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Lee [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

```bash
# 1. Haz fork del proyecto
# 2. Crea tu rama
git checkout -b feature/nueva-funcionalidad

# 3. Haz commit de tus cambios
git commit -m "feat: descripción del cambio"

# 4. Sube tu rama
git push origin feature/nueva-funcionalidad

# 5. Abre un Pull Request
```

### Convención de commits

| Prefijo | Uso |
|---|---|
| `feat:` | Nueva funcionalidad |
| `fix:` | Corrección de bug |
| `docs:` | Cambios en documentación |
| `style:` | Formato, sin cambios lógicos |
| `refactor:` | Refactorización de código |

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más información.

---

## 👤 Autor

**Carolina Lopez**
- GitHub: [@bety2022](https://github.com/bety2022)

---

⭐ Si este proyecto te fue útil, ¡dale una estrella en GitHub!
