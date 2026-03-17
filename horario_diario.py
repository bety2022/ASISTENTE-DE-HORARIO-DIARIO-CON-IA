"""
ASISTENTE DE HORARIO DIARIO CON IA
Aplicación con interfaz Tkinter que gestiona tareas diarias,
aprende de los hábitos del usuario y proporciona motivación.

Autor: Claude AI
Fecha: Octubre 2025
"""

import pandas as pd
import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
import json
import os
from typing import List, Dict
import threading
import time

# ============= MÓDULO DE INTELIGENCIA ARTIFICIAL =============
class TaskLearningIA:
    """
    IA de Aprendizaje Automático que analiza patrones de comportamiento
    y predice tiempos óptimos y duraciones de tareas.
    """
    
    def __init__(self):
        self.task_history = []
        self.completion_patterns = {}
        self.productivity_hours = {}
        
    def registrar_tarea_completada(self, tarea: Dict):
        """Registra una tarea completada para aprendizaje"""
        self.task_history.append({
            'nombre': tarea['nombre'],
            'hora_inicio': tarea['hora'],
            'duracion_estimada': tarea['duracion'],
            'hora_completada': datetime.now().strftime("%H:%M"),
            'dia_semana': datetime.now().strftime("%A"),
            'completada': True
        })
        
        # Actualizar patrones
        self._actualizar_patrones()
    
    def _actualizar_patrones(self):
        """Analiza el historial y actualiza patrones de productividad"""
        if len(self.task_history) < 3:
            return
        
        # Analizar horas más productivas
        for tarea in self.task_history[-10:]:  # Últimas 10 tareas
            hora = int(tarea['hora_inicio'].split(':')[0])
            if hora not in self.productivity_hours:
                self.productivity_hours[hora] = 0
            self.productivity_hours[hora] += 1
        
        # Analizar duraciones por tipo de tarea
        for tarea in self.task_history:
            nombre = tarea['nombre'].lower()
            if nombre not in self.completion_patterns:
                self.completion_patterns[nombre] = []
            self.completion_patterns[nombre].append(tarea['duracion_estimada'])
    
    def predecir_duracion(self, nombre_tarea: str) -> int:
        """Predice la duración óptima basada en historial"""
        nombre_lower = nombre_tarea.lower()
        
        if nombre_lower in self.completion_patterns:
            duraciones = self.completion_patterns[nombre_lower]
            # Promedio ponderado (más peso a datos recientes)
            if len(duraciones) >= 3:
                promedio = sum(duraciones[-5:]) / len(duraciones[-5:])
                return int(promedio)
        
        return 30  # Valor por defecto
    
    def recomendar_hora_optima(self) -> str:
        """Recomienda la mejor hora para programar tareas"""
        if not self.productivity_hours:
            return "09:00"
        
        # Encuentra la hora más productiva
        hora_optima = max(self.productivity_hours, key=self.productivity_hours.get)
        return f"{hora_optima:02d}:00"
    
    def obtener_estadisticas(self) -> Dict:
        """Genera estadísticas de productividad"""
        total_tareas = len(self.task_history)
        if total_tareas == 0:
            return {
                'total_completadas': 0,
                'hora_mas_productiva': 'N/A',
                'tarea_mas_frecuente': 'N/A',
                'nivel_consistencia': 0
            }
        
        # Tarea más frecuente
        tareas_count = {}
        for t in self.task_history:
            nombre = t['nombre']
            tareas_count[nombre] = tareas_count.get(nombre, 0) + 1
        
        tarea_frecuente = max(tareas_count, key=tareas_count.get) if tareas_count else 'N/A'
        
        # Hora más productiva
        hora_prod = max(self.productivity_hours, key=self.productivity_hours.get) if self.productivity_hours else 'N/A'
        if hora_prod != 'N/A':
            try:
                hora_prod = f"{int(hora_prod):02d}:00"
            except ValueError:
                hora_prod = str(hora_prod)
        
        # Nivel de consistencia (0-100)
        consistencia = min(100, (total_tareas * 10))
        
        return {
            'total_completadas': total_tareas,
            'hora_mas_productiva': hora_prod,
            'tarea_mas_frecuente': tarea_frecuente,
            'nivel_consistencia': consistencia
        }


# ============= MÓDULO DE GESTIÓN DE DATOS =============
class DataManager:
    """Maneja la persistencia de datos con medidas de seguridad básicas"""
    
    def __init__(self, filename='tareas_data.json'):
        self.filename = filename
        
    def guardar_tareas(self, tareas: List[Dict], ia_data: Dict):
        """Guarda tareas y datos de IA en archivo JSON"""
        try:
            data = {
                'tareas': tareas,
                'ia_history': ia_data,
                'last_update': datetime.now().isoformat()
            }
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar: {e}")
    
    def cargar_tareas(self) -> tuple:
        """Carga tareas y datos de IA desde archivo"""
        if not os.path.exists(self.filename):
            return [], {}
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('tareas', []), data.get('ia_history', {})
        except Exception as e:
            print(f"Error al cargar: {e}")
            return [], {}


# ============= APLICACIÓN PRINCIPAL =============
class HorarioDiarioApp:
    """Aplicación principal con interfaz Tkinter"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Asistente de Horario Diario con IA")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Inicializar componentes
        self.ia = TaskLearningIA()
        self.data_manager = DataManager()
        # ...en el método __init__ de HorarioDiarioApp...
        self.tareas_df = pd.DataFrame(columns=[
    'nombre', 'hora', 'duracion', 'prioridad', 'completada', 'fecha_creacion'
])
        
        self.notificacion_activa = True
        
        # Cargar datos previos
        self._cargar_datos()
        
        # Crear interfaz
        self._crear_interfaz()
        
        # Iniciar hilo de notificaciones
        self._iniciar_notificaciones()
    
    
    def _cargar_datos(self):
        """Carga datos guardados anteriormente"""
        tareas, ia_data = self.data_manager.cargar_tareas()
        self.tareas_df = pd.DataFrame(tareas) if tareas else pd.DataFrame(columns=[
            'nombre', 'hora', 'duracion', 'prioridad', 'completada', 'fecha_creacion'
        ])
      
        
        if ia_data:
            self.ia.task_history = ia_data.get('task_history', [])
            self.ia.completion_patterns = ia_data.get('completion_patterns', {})
            self.ia.productivity_hours = ia_data.get('productivity_hours', {})
    
        
    def _guardar_datos(self):
        """Guarda todos los datos"""
        ia_data = {
            'task_history': self.ia.task_history,
            'completion_patterns': self.ia.completion_patterns,
            'productivity_hours': self.ia.productivity_hours
        }
        self.data_manager.guardar_tareas(self.tareas_df.to_dict(orient='records'), ia_data)

    
    def _crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        
        # === TÍTULO ===
        titulo_frame = tk.Frame(self.root, bg='#8e44ad', height=60)
        titulo_frame.pack(fill='x')
        titulo_frame.pack_propagate(False)
        
        tk.Label(titulo_frame, text="🎯 Mi Horario Diario", 
                font=('Arial', 18, 'bold'), bg='#8e44ad', fg='white').pack(pady=15)
        

    # === CONTENEDOR PRINCIPAL ===
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)

    # Configurar grid weights para 3 columnas
        main_container.columnconfigure(0, weight=1)  # Calendario
        main_container.columnconfigure(1, weight=2)  # Panel tareas
        main_container.columnconfigure(2, weight=2)  # Panel IA y motivación
        main_container.rowconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)

    # === CALENDARIO ===
        calendario_frame = tk.LabelFrame(main_container, text="📅 Calendario", 
                                     font=('Arial', 11, 'bold'), bg='white', padx=10, pady=10)
        calendario_frame.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(0, 5), pady=(0, 0))

        self.calendario = Calendar(calendario_frame, selectmode='day', year=datetime.now().year, 
                               month=datetime.now().month, day=datetime.now().day, date_pattern='yyyy-mm-dd')
        self.calendario.pack(fill='both', expand=True)
        self.calendario.bind("<<CalendarSelected>>", self._mostrar_tareas_del_dia)

    # === PANEL IZQUIERDO: Agregar Tarea ===
        left_panel = tk.LabelFrame(main_container, text="➕ Nueva Tarea", 
                               font=('Arial', 11, 'bold'), bg='white', padx=15, pady=15)
        left_panel.grid(row=0, column=1, sticky='nsew', padx=(0, 5))
        
    
        # Campo Nombre
        tk.Label(left_panel, text="Nombre de la tarea:", bg='white').pack(anchor='w')
        self.entry_nombre = tk.Entry(left_panel, font=('Arial', 13), width=25)
        self.entry_nombre.pack(fill='x', pady=2)

        # Campo Hora
        tk.Label(left_panel, text="Hora (HH:MM):", bg='white').pack(anchor='w')
        self.entry_hora = tk.Entry(left_panel, font=('Arial', 13), width=10)
        self.entry_hora.pack(fill='x', pady=2)

        # Campo Duración
        tk.Label(left_panel, text="Duración (min):", bg='white').pack(anchor='w')
        self.entry_duracion = tk.Entry(left_panel, font=('Arial', 13), width=5)
        self.entry_duracion.insert(0, "30")
        self.entry_duracion.pack(fill='x', pady=2)

        # Campo Prioridad
        tk.Label(left_panel, text="Prioridad:", bg='white').pack(anchor='w')
        self.combo_prioridad = ttk.Combobox(left_panel, values=["Alta", "Media", "Baja"], state="readonly", font=('Arial', 13), width=10)
        self.combo_prioridad.current(1)
        self.combo_prioridad.pack(fill='x', pady=2)

        # Botón Agregar Tarea
        tk.Button(left_panel, text="➕ Agregar Tarea", command=self._agregar_tarea,
                  bg='#2980b9', fg='white', font=('Arial', 13, 'bold'), cursor='hand2').pack(pady=8)

        # Botones IA
        ia_btn_frame = tk.Frame(left_panel, bg='white')
        ia_btn_frame.pack(fill='x', pady=(5, 0))
        tk.Button(ia_btn_frame, text="🤖 Recomendar Hora", command=self._ia_recomendar_hora,
                  bg='#16a085', fg='white', cursor='hand2').pack(side='left', padx=5)
        tk.Button(ia_btn_frame, text="⏳ Predecir Duración", command=self._ia_predecir_duracion,
                  bg='#f39c12', fg='white', cursor='hand2').pack(side='left', padx=5)  
        

    # === PANEL DERECHO: Lista de Tareas ===
        right_panel = tk.LabelFrame(main_container, text="📋 Mis Tareas de Hoy", 
                                font=('Arial', 13, 'bold'), bg='white', padx=10, pady=10)
        right_panel.grid(row=1, column=1, sticky='nsew', padx=(0, 5), pady=(10, 0))
  
        # Lista de tareas
        self.lista_tareas = tk.Listbox(right_panel, font=('Arial', 13), height=18, selectmode=tk.SINGLE)
        self.lista_tareas.pack(fill='both', expand=True, padx=5, pady=5)

        # Botones para completar y eliminar tarea
        btn_frame = tk.Frame(right_panel, bg='white')
        btn_frame.pack(fill='x', pady=(5, 0))
        tk.Button(btn_frame, text="✓ Completar", command=self._completar_tarea,
                  bg='#27ae60', fg='white', cursor='hand2').pack(side='left', padx=5)
        tk.Button(btn_frame, text="🗑 Eliminar", command=self._eliminar_tarea,
                  bg='#c0392b', fg='white', cursor='hand2').pack(side='left', padx=5)


    # === PANEL IA y Motivación ===
        bottom_panel = tk.Frame(main_container, bg='#f0f0f0')
        bottom_panel.grid(row=0, column=2, rowspan=2, sticky='nsew', padx=(5, 0), pady=(0, 0))

        # Estadísticas IA
        stats_frame = tk.LabelFrame(bottom_panel, text="🤖 Estadísticas de IA", 
                                    font=('Arial', 13, 'bold'), bg='#ecf0f1', padx=10, pady=10)
        stats_frame.pack(side='left', fill='y', expand=False, padx=(0, 5))
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=3, font=('Arial', 12), 
                                                     bg='white', wrap='word')
        self.stats_text.pack(fill='both', expand=True)
        
        # Motivación
        motiv_frame = tk.LabelFrame(bottom_panel, text="💪 Motivación", 
                                    font=('Arial', 13, 'bold'), bg='#ecf0f1', padx=10, pady=10)
        motiv_frame.pack(side='left', fill='both', expand=True, padx=(5, 0))
        
        self.motivacion_label = tk.Label(motiv_frame, text="¡Estás haciendo un gran trabajo! 🌟",
                                         font=('Arial', 25), bg='#ecf0f1', wraplength=350, justify='center')
        self.motivacion_label.pack(expand=True)
        
        tk.Button(motiv_frame, text="🔄 Nueva Motivación", command=self._actualizar_motivacion,
                 bg='#9b59b6', fg='white', cursor='hand2').pack(pady=5)
        
        # Configurar grid weights
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=2)
        main_container.rowconfigure(0, weight=1)
        
        # Actualizar vista inicial
        self._actualizar_lista_tareas()
        self._actualizar_estadisticas()
    
    def _ia_recomendar_hora(self):
        """Usa IA para recomendar mejor hora"""
        hora_recomendada = self.ia.recomendar_hora_optima()
        self.entry_hora.delete(0, tk.END)
        self.entry_hora.insert(0, hora_recomendada)
        messagebox.showinfo("IA Recomienda", 
                           f"Basándome en tus patrones, te recomiendo: {hora_recomendada}\n"
                           "¡Esta es tu hora más productiva! 🚀")
    
    def _ia_predecir_duracion(self):
        """Usa IA para predecir duración de tarea"""
        nombre = self.entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Atención", "Primero ingresa el nombre de la tarea")
            return
        
        duracion_pred = self.ia.predecir_duracion(nombre)
        self.entry_duracion.delete(0, tk.END)
        self.entry_duracion.insert(0, str(duracion_pred))
        messagebox.showinfo("IA Predice", 
                           f"Según tu historial, esta tarea te tomará unos {duracion_pred} minutos 🎯")
    
   
    def _agregar_tarea(self):
        """Agrega una nueva tarea"""
        # ...después de agregar la nueva tarea...
        self.tareas_df['hora_dt'] = pd.to_datetime(self.tareas_df['hora'], format='%H:%M')  # AGREGUE LINEA 371-372-373 BORRAR
        self.tareas_df = self.tareas_df.sort_values('hora_dt').reset_index(drop=True)
        self.tareas_df = self.tareas_df.drop(columns=['hora_dt'])
        
        nombre = self.entry_nombre.get().strip()
        hora = self.entry_hora.get().strip()
        duracion = self.entry_duracion.get().strip()
        prioridad = self.combo_prioridad.get()
    
    # Validaciones
        if not nombre or not hora:
            messagebox.showwarning("Atención", "Por favor completa todos los campos obligatorios")
            return
    
        try:
            datetime.strptime(hora, "%H:%M")
            duracion_int = int(duracion)
        except ValueError:
            messagebox.showerror("Error", "Formato inválido. Usa HH:MM para hora y números para duración")
            return
    
        nueva_tarea = {
            'nombre': nombre,
            'hora': hora,
            'duracion': duracion_int,
            'prioridad': prioridad,
            'completada': False,
            'fecha_creacion': datetime.now().isoformat()
        }
        
        self.tareas_df = pd.concat([self.tareas_df, pd.DataFrame([nueva_tarea])], ignore_index=True)
        self.tareas_df = self.tareas_df.sort_values('hora').reset_index(drop=True)
    
    # Limpiar campos
        self.entry_nombre.delete(0, tk.END)
        self.entry_hora.delete(0, tk.END)
        self.entry_duracion.delete(0, tk.END)
        self.entry_duracion.insert(0, "30")
    
        self._actualizar_lista_tareas()
        self._guardar_datos()
    
        messagebox.showinfo("¡Éxito!", f"✅ Tarea '{nombre}' agregada para las {hora}")

    
    def _actualizar_lista_tareas(self):
        """Actualiza la visualización de tareas"""
        self.lista_tareas.delete(0, tk.END)

        if self.tareas_df.empty:
            self.lista_tareas.insert(tk.END, "No hay tareas programadas para hoy")
            return

    # Convertir la columna 'hora' a tipo datetime y ordenar
        tareas_ordenadas = self.tareas_df.copy()
        tareas_ordenadas['hora_dt'] = pd.to_datetime(tareas_ordenadas['hora'], format='%H:%M')
        tareas_ordenadas = tareas_ordenadas.sort_values('hora_dt')

        for i, tarea in tareas_ordenadas.iterrows():
            estado = "✓" if tarea['completada'] else "○"
            prioridad_icon = "🔴" if tarea['prioridad'] == 'Alta' else "🟡" if tarea['prioridad'] == 'Media' else "🟢"
            texto = f"{estado} {tarea['hora']} | {prioridad_icon} {tarea['nombre']} ({tarea['duracion']}min)"
            self.lista_tareas.insert(tk.END, texto)
            if tarea['completada']:
                self.lista_tareas.itemconfig(i, fg='gray')
                
     
    def _mostrar_tareas_del_dia(self, event=None):
        fecha_seleccionada = self.calendario.get_date()  # formato 'yyyy-mm-dd'
        self.lista_tareas.delete(0, tk.END)
        tareas_del_dia = self.tareas_df[self.tareas_df['fecha_creacion'].str.startswith(fecha_seleccionada)]
        if tareas_del_dia.empty:
            self.lista_tareas.insert(tk.END, "No hay tareas para este día")
            return
        tareas_del_dia['hora_dt'] = pd.to_datetime(tareas_del_dia['hora'], format='%H:%M')
        tareas_del_dia = tareas_del_dia.sort_values('hora_dt')
        for i, tarea in tareas_del_dia.iterrows():
            estado = "✓" if tarea['completada'] else "○"
            prioridad_icon = "🔴" if tarea['prioridad'] == 'Alta' else "🟡" if tarea['prioridad'] == 'Media' else "🟢"
            texto = f"{estado} {tarea['hora']} | {prioridad_icon} {tarea['nombre']} ({tarea['duracion']}min)"
            self.lista_tareas.insert(tk.END, texto)
            if tarea['completada']:
                self.lista_tareas.itemconfig(i, fg='gray')

    def _completar_tarea(self):
        """Marca una tarea como completada"""
        seleccion = self.lista_tareas.curselection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una tarea primero")
            return
    
        idx = seleccion[0]
        if self.tareas_df.at[idx, 'completada']:
            messagebox.showinfo("Info", "Esta tarea ya está completada")
            return
    
        self.tareas_df.at[idx, 'completada'] = True
    
    # Registrar en IA
        tarea = self.tareas_df.iloc[idx].to_dict()
        self.ia.registrar_tarea_completada(tarea)
    
        self._actualizar_lista_tareas()
        self._actualizar_estadisticas()
        self._guardar_datos()
    
        messagebox.showinfo("¡Bien hecho! 🎉", 
                           f"¡Excelente! Has completado: {tarea['nombre']}\n¡Sigue así! 💪")

    def _eliminar_tarea(self):
        """Elimina una tarea"""
        seleccion = self.lista_tareas.curselection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una tarea primero")
            return
    
        idx = seleccion[0]
        tarea = self.tareas_df.iloc[idx].to_dict()
    
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{tarea['nombre']}'?"):
            self.tareas_df = self.tareas_df.drop(idx).reset_index(drop=True)
            self._actualizar_lista_tareas()
            self._guardar_datos()
     
    def _actualizar_estadisticas(self):
        """Actualiza el panel de estadísticas de IA"""
        stats = self.ia.obtener_estadisticas()
        
        texto = f"""📊 ANÁLISIS DE PRODUCTIVIDAD IA

🎯 Tareas completadas: {stats['total_completadas']}
⏰ Tu mejor hora: {stats['hora_mas_productiva']}
⭐ Tarea más frecuente: {stats['tarea_mas_frecuente']}
📈 Nivel de consistencia: {stats['nivel_consistencia']}%

💡 La IA aprende de tus patrones y mejora sus
   recomendaciones con cada tarea completada.
"""
        
        self.stats_text.delete('1.0', tk.END)
        self.stats_text.insert('1.0', texto)
    
    def _actualizar_motivacion(self):
        """Actualiza mensaje motivacional"""
        frases = [
            "¡Cada tarea completada es un paso hacia tus metas! 🎯",
            "Tu esfuerzo de hoy es tu éxito de mañana 💪",
            "¡Estás haciendo un trabajo increíble! 🌟",
            "La constancia es la clave del éxito ⭐",
            "¡Sigue así! Cada día eres mejor 🚀",
            "Tu productividad está en su mejor momento 📈",
            "¡Eres imparable! Continúa con ese ritmo 🔥",
            "Cada tarea es una victoria. ¡Celebra! 🎉"
        ]
        
        import random
        self.motivacion_label.config(text=random.choice(frases))
    
    def _iniciar_notificaciones(self):
        """Inicia el sistema de notificaciones en segundo plano"""
        def verificar_tareas():
            while self.notificacion_activa:
                hora_actual = datetime.now().strftime("%H:%M")
                
                
                for _, tarea in self.tareas_df.iterrows():
                    if tarea['hora'] == hora_actual and not tarea['completada']:
                        self.root.after(0, lambda t=tarea: messagebox.showinfo(
                            "⏰ Recordatorio",
                            f"¡Es hora de: {t['nombre']}!\nDuración estimada: {t['duracion']} minutos"
                        ))
                               
                time.sleep(60)  # Verificar cada minuto
        
        thread = threading.Thread(target=verificar_tareas, daemon=True)
        thread.start()
    
    def cerrar_aplicacion(self):
        """Cierra la aplicación guardando datos"""
        self.notificacion_activa = False
        self._guardar_datos()
        self.root.destroy()


# ============= EJECUCIÓN PRINCIPAL =============
if __name__ == "__main__":
    root = tk.Tk()
    app = HorarioDiarioApp(root)
    root.protocol("WM_DELETE_WINDOW", app.cerrar_aplicacion)
    root.mainloop()
