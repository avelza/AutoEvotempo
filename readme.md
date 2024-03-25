# AutoEvoTempo

AutoEvoTempo es un script de Python diseñado para automatizar tareas específicas en la web utilizando Selenium. Este script puede realizar acciones como navegar a una página web, tomar capturas de pantalla, y enviar emails automáticos con los resultados de sus operaciones.

## Requisitos

Para ejecutar este script, necesitarás Python 3 y algunas dependencias adicionales, incluyendo Selenium y PIL (Python Imaging Library). Asegúrate de tener instalado Python 3 y pip, y luego instala las dependencias necesarias con el siguiente comando:

```
pip install selenium Pillow
```

## Configuración

Antes de ejecutar el script, necesitas configurar algunas variables y posiblemente ajustar las rutas de los archivos y las credenciales de email en el script. Estos ajustes se realizan en las secciones marcadas con `# Ajustes` dentro del script.

## Archivo de Configuración Externo

El script AutoEvoTempo utiliza un archivo de configuración externo para manejar diversas variables y rutas necesarias para su ejecución. Este enfoque permite una fácil personalización y adaptación del script a diferentes entornos y preferencias de usuario sin necesidad de modificar el código fuente directamente.

### Ubicación y Formato

El archivo de configuración debe estar ubicado en el directorio especificado por la variable de entorno `evotempo_path` y debe llamarse `config.txt`. Este archivo utiliza el formato estándar de archivos de configuración INI, que organiza las opciones en secciones, cada una declarada por un título entre corchetes `[]`, con configuraciones individuales dentro de cada sección especificadas como pares de clave-valor.

### Secciones y Claves

El archivo de configuración debe contener las siguientes secciones y claves:

- `[Paths]`
  - `log`: Ruta al archivo donde se guardarán los logs del script.
  - `screenshot_path`: Ruta al archivo donde se guardarán las capturas de pantalla generadas por el script.
  - `url_evotempo`: URL de la página web a la que el script accederá para realizar las operaciones automatizadas.

- `[Settings]`
  - `pass_email_notif`: Contraseña del email desde el cual se enviarán las notificaciones.
  - `email_admin`: Dirección de correo electrónico a la cual se enviarán las notificaciones del resultado de la ejecución del script.

### Ejemplo de Archivo de Configuración

Aquí tienes un ejemplo básico de cómo podría verse el archivo `config.txt`:

```ini
[Paths]
log=/path/to/your/logfile.log
screenshot_path=/path/to/your/screenshot.jpg
url_evotempo=https://example.com

[Settings]
pass_email_notif=yourEmailPassword
email_admin=admin@example.com
```

## Configuración de la Variable de Entorno

Para mejorar la seguridad y flexibilidad del script AutoEvoTempo, se utiliza una variable de entorno para especificar la ruta al archivo de configuración. Esto evita tener que incluir datos sensibles directamente en el código. Aquí te explicamos cómo fijar esta variable de entorno tanto en el entorno `zsh` (Z Shell) como en la configuración `launchd` para la automatización en macOS.

### Fijando la Variable en Z Shell (zsh)

Para usuarios de macOS, `zsh` es el shell predeterminado desde macOS Catalina. Para establecer la variable de entorno `evotempo_path` en `zsh`, sigue estos pasos:

1. **Abrir el archivo de configuración de zsh**: Abre el archivo `.zshrc` en tu directorio home (`~`) con tu editor de texto preferido. Si el archivo no existe, puedes crearlo.

   ```shell
   open -a TextEdit ~/.zshrc
    ````
2. **Agregar la variable de entorno**: Al final del archivo .zshrc, agrega la siguiente línea, sustituyendo /path/to/your/configuration/directory por la ruta real donde se encuentra tu archivo de configuración config.txt.
```
export evotempo_path="/path/to/your/configuration/directory"
```
3. **Aplicar los cambios**: Para que los cambios surtan efecto, cierra y vuelve a abrir tu terminal, o ejecuta el comando 
```
source ~/.zshrc.
```

### Fijando la Variable en el plist para launchd
Cuando automatizas la ejecución del script AutoEvoTempo con launchd, necesitas especificar la variable de entorno dentro del archivo .plist que configura la tarea programada. Aquí se muestra cómo hacerlo:

1. Editar el archivo plist: Abre tu archivo .plist (por ejemplo, `com.user.autoevo.plist`) en un editor de texto.
2. Agregar la variable de entorno: Dentro del diccionario <dict> que define las EnvironmentVariables, agrega una entrada para evotempo_path de la siguiente manera:
    ```xml
    <key>EnvironmentVariables</key>
    <dict>
        <key>evotempo_path</key>
        <string>/path/to/your/configuration/directory</string>
    </dict>
    ```
3. Asegúrate de reemplazar `/path/to/your/configuration/directory` con la ruta correcta a tu directorio de configuración.
Guardar y cargar el plist: Guarda los cambios en tu archivo .plist y vuelve a cargarlo con launchctl para que la nueva configuración tenga efecto.
    ```
    launchctl unload ~/Library/LaunchAgents/com.user.autoevo.plist
    launchctl load ~/Library/LaunchAgents/com.user.autoevo.plist
    ```
Al establecer la variable de entorno tanto en tu shell como en el entorno de launchd, aseguras que el script pueda acceder al archivo de configuración necesario sin exponer rutas o datos sensibles directamente en el código o en la línea de comandos.
## Uso

Para ejecutar el script, simplemente navega al directorio donde se encuentra el archivo y ejecuta:
```
python3 AutoEvoTempo.py
```

## Automatización en Mac con `launchd`

Para automatizar la ejecución del script en un Mac, puedes utilizar `launchd` creando un archivo `.plist` con la configuración de la tarea programada. Aquí tienes un ejemplo de cómo configurar este archivo y establecer la variable de entorno necesaria:

1. **Crear el archivo plist:** Crea un archivo con la configuración deseada para programar la ejecución del script. Por ejemplo, `com.user.autoevo.plist` en el directorio `~/Library/LaunchAgents/`. Asegúrate de ajustar las rutas según tu configuración. El contenido del archivo `plist` sería algo como lo proporcionado para el script AutoEvoTempo.

2. **Configuración de la variable de entorno:** Dentro del archivo `.plist`, has establecido una variable de entorno `evotempo_path` que el script utiliza para determinar las rutas de los archivos de configuración y de registro. Asegúrate de que esta ruta sea correcta y apunte al directorio donde se almacena tu archivo de configuración `config.txt`.

3. **Cargar y activar la tarea:** Una vez que hayas creado tu archivo `.plist`, debes cargarlo con `launchctl` para programar la ejecución de tu script. Abre Terminal y ejecuta:

launchctl load ~/Library/LaunchAgents/com.user.autoevo.plist

4. **Verificar:** Para asegurarte de que tu tarea está programada correctamente, puedes utilizar el comando:
```
launchctl list | grep autoevo
```
Esto debería mostrarte tu tarea si está cargada y activa.

5. **Desactivación y eliminación:** Si necesitas desactivar o eliminar la tarea programada, puedes utilizar `launchctl unload` con la misma ruta del archivo `.plist`.
```
launchctl unload ~/Library/LaunchAgents/com.user.autoevo.plist
```
Recuerda que cualquier cambio en el archivo `.plist` requerirá que lo descargues y lo cargues nuevamente para que los cambios tengan efecto.




## Ejemplo de plist para launchd

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.autoevo</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Users/kuser/PyProjects/AutoEvoTempo/AutoEvoTempo.py</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>evotempo_path</key>
        <string>/Users/kuser/PyProjects/AutoEvoTempo</string>
    </dict>
    <key>RunAtLoad</key>
    <false/>
    <key>StartCalendarInterval</key>
    <array>
        <dict>
            <key>Hour</key>
            <integer>9</integer>
            <key>Minute</key>
            <integer>0</integer>
            <key>Weekday</key>
            <integer>1</integer> <!-- Monday -->
        </dict>
        <dict>
            <key>Hour</key>
            <integer>9</integer>
            <key>Minute</key>
            <integer>1</integer>
            <key>Weekday</key>
            <integer>2</integer> <!-- Tuesday -->
        </dict>
        <dict>
            <key>Hour</key>
            <integer>9</integer>
            <key>Minute</key>
            <integer>2</integer>
            <key>Weekday</key>
            <integer>3</integer> <!-- Wednesday -->
        </dict>
        <dict>
            <key>Hour</key>
            <integer>9</integer>
            <key>Minute</key>
            <integer>1</integer>
            <key>Weekday</key>
            <integer>4</integer> <!-- Thursday -->
        </dict>
        <dict>
            <key>Hour</key>
            <integer>9</integer>
            <key>Minute</key>
            <integer>0</integer>
            <key>Weekday</key>
            <integer>5</integer> <!-- Friday -->
        </dict>
    </array>
    <key>StandardErrorPath</key>
    <string>/tmp/com.user.autoevo.err</string>
    <key>StandardOutPath</key>
    <string>/tmp/com.user.autoevo.out</string>
</dict>
</plist>

```