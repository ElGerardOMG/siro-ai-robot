# Siro AI Robot

Repositorio base para programar un robot físico capaz de conversar, integrando múltiples tecnologías de IA, síntesis de voz y control de hardware. Si buscas crear un robot con:

- **Reconocimiento de voz**
- **Inteligencia artificial**
- **Síntesis de voz**
- **Control coordinado de servomotores**

Este repositorio puede ayudarte a lograrlo. Por defecto, el proyecto utiliza KokoroTTS, Vosk y la IA de Google, aunque puedes cambiar o ampliar estas tecnologías fácilmente.

---

## 📁 Estructura del proyecto

- **`docs/`** — Documentación (HTML, español, asistida por IA).
- **`resources`** — Recursos generales. Aquí deben ir los modelos.
- **`src/ai_talking_robot/`** — Código principal (integración, controladores, secuenciador, voz, IA, audio y entrada).
- **`robots/`** — Implementaciones funcionales de robots: El Charro Negro y Darth Vader.
- **`tools/`** — Herramientas útiles enfocadas en el manejo de los componentes físicos.
- **`test/`** — Tests manuales para probar funcionalidad básica de algunos módulos.

---

## 🚦 Requisitos e instalación

Sigue estos pasos para instalar y ejecutar el proyecto:

1. **Instala `uv`:**
   Si no lo tienes instalado, hazlo previamente.

2. **Clona el repositorio:**
   ```bash
   git clone https://github.com/ElGerardOMG/siro-ai-robot.git
   cd siro-ai-robot
   ```

3. **Instala dependencias:**
   ```bash
   uv sync
   ```

4. **Configura la API Key de Google:**
   Crea un archivo `secrets.json` dentro de la carpeta de tu robot (por ejemplo, `robots/darth_vader/`) con el siguiente contenido:
   
    ```json
    {
      "google_api_key": "AquiVaTuApiKey"
    }
    ```

5. **Descarga los modelos de Vosk y KokoroTTS:**
   - [Modelos de KokoroTTS (onnx + voices)](https://github.com/thewh1teagle/kokoro-onnx/releases)
   - [Modelos de Vosk](https://alphacephei.com/vosk/models)

   Descarga los modelos desde los enlaces anteriores y organízalos en la raíz del proyecto de la siguiente manera:
   ```
   /siro-ai-robot
   └── resources
       └── models
           ├── kokoro
           │   ├── kokoro-v1.0.onnx
           │   └── voices-v1.0.bin
           └── vosk-model-##-x.xx
   ```

6. **Activa el entorno virtual**
   ...
   - En **Linux**:
     ```bash
     source .venv/bin/activate
     ```
   - En **Windows**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
     
---

## 🚀 Ejecutar un robot de ejemplo

Desde la raíz del proyecto, con las dependencias y modelos instalados, ejecuta alguno de los robots:

- **Darth Vader:**  
  ```bash
  python -m robots.darth_vader.main
  ```

- **El Charro Negro:**  
  ```bash
  python -m robots.charro_negro.main
  ```

Cada robot utiliza su propio archivo `config.json` y `secrets.json`. Asegúrate de que estos archivos estén presentes en la carpeta correspondiente de cada robot antes de ejecutarlo.

---

## 💎 Créditos y agradecimientos

Este proyecto utiliza las siguientes tecnologías y proyectos de terceros:

- **Kokoro TTS (modelo ONNX)** — Síntesis de voz. Por [thewh1teagle](https://github.com/thewh1teagle/kokoro-onnx) — paquete bajo [MIT](https://github.com/thewh1teagle/kokoro-onnx/blob/main/LICENSE), modelo bajo Apache 2.0.
- **Vosk** — Reconocimiento de voz offline. Por [Alpha Cephei](https://alphacephei.com/vosk/) — [Apache License 2.0](https://github.com/alphacep/vosk-api/blob/master/COPYING).
- **Google AI (Gemini)** — Modelo de lenguaje para el diálogo. Por [Google](https://ai.google.dev/) — su uso está sujeto a los [términos del servicio de la API](https://ai.google.dev/terms).

Si utilizas o redistribuyes este proyecto, respeta las licencias y términos de cada uno de estos componentes.


Agradezco personalmente a mi profesor y compañeros del Laboratorio Siro. Gracias a su compañía, ayuda y entusiasmo logré aprender muchas cosas y estar en lugares donde nunca
pensé que estaría. Esto no sería posible sin ellos.