# 🤝 Guía para Contribuir

¡Gracias por tu interés en contribuir! Aquí te explico cómo hacerlo.

---

## 🐛 Reportar un Bug

1. Ve a la pestaña **Issues** en GitHub
2. Haz clic en **New Issue**
3. Incluye:
   - Descripción clara del problema
   - Pasos para reproducirlo
   - Sistema operativo y versión de Python
   - Captura de pantalla o mensaje de error

---

## 💡 Sugerir una Funcionalidad

1. Abre un **Issue** con el título: `[Feature] Tu idea aquí`
2. Describe qué problema resuelve
3. Explica cómo debería funcionar

---

## 🔧 Contribuir con Código

### Requisitos previos
- Python 3.7+
- Git instalado

### Pasos

```bash
# 1. Haz fork del repositorio en GitHub

# 2. Clona tu fork
git clone https://github.com/tu-usuario/asistente-horario-ia.git
cd asistente-horario-ia

# 3. Crea una rama con nombre descriptivo
git checkout -b feature/nombre-de-tu-cambio

# 4. Haz tus cambios en el código

# 5. Verifica que la app sigue funcionando
python horario.py

# 6. Haz commit siguiendo la convención
git commit -m "feat: descripción corta del cambio"

# 7. Sube tu rama
git push origin feature/nombre-de-tu-cambio

# 8. Abre un Pull Request en GitHub
```

---

## 📝 Convención de Commits

| Prefijo | Cuándo usarlo |
|---|---|
| `feat:` | Nueva funcionalidad |
| `fix:` | Corrección de bug |
| `docs:` | Cambios en documentación |
| `style:` | Formato, espacios (sin lógica) |
| `refactor:` | Refactorización sin cambiar comportamiento |
| `test:` | Agregar o corregir tests |

**Ejemplos:**
```
feat: agregar exportación de tareas a CSV
fix: corregir error al cargar tareas vacías
docs: actualizar sección de instalación en README
```

---

## ✅ Checklist antes de abrir un Pull Request

- [ ] La aplicación corre sin errores
- [ ] El código está comentado en español
- [ ] El README fue actualizado si es necesario
- [ ] El commit sigue la convención

---

¡Gracias por contribuir! 🎉
