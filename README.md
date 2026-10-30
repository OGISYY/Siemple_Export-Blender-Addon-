# Simple Export (Blender Add-on)

Exporta en lote objetos o colecciones a **FBX** u **OBJ** con un solo clic, cada uno en su propio archivo.

Compatible con **Blender 4.0+** (como add-on clásico) y **Blender 4.2+** (como extensión).

## Instalación

1. Descarga `simple_export-x.y.z.zip` desde [Releases](https://github.com/OGISYY/Siemple_Export-Blender-Addon-/releases)
   o genéralo tú mismo (ver [Generar el zip](#generar-el-zip)).
2. En Blender:
   - **4.2 o superior:** `Edit > Preferences > Get Extensions > ▾ (arriba a la derecha) > Install from Disk...` y elige el zip.
   - **4.0 / 4.1:** `Edit > Preferences > Add-ons > Install...`, elige el zip y activa **Simple Export**.

> No uses el botón verde *Code > Download ZIP* de GitHub para instalar: ese zip tiene otra estructura de carpetas.

## Uso

Abre el panel en `Vista 3D > Sidebar (N) > Simple Export`.

| Opción | Descripción |
| --- | --- |
| **Directory** | Carpeta de destino. `//` = carpeta del `.blend` (hay que guardar el archivo antes). Si no existe se crea. |
| **Prefix / Suffix** | Texto que se añade al nombre del archivo, p. ej. `SM_` + `Silla` + `_LOD0`. |
| **Object Types** | Tipos de objeto que se exportan (Mesh, Curve, Armature, Empty...). |
| **Format** | FBX u OBJ. |
| **Mode** | `Objects`: un archivo por objeto. `Collections`: un archivo por colección (con los objetos directos de esa colección; los que están sueltos en la *Scene Collection* se exportan con el nombre de la escena). |
| **Limit to** | `Selected`: solo los objetos seleccionados. `Visible`: todos los objetos visibles. |
| **Apply Modifiers** | Aplica los modificadores al exportar. |
| **Apply Transform** | (Solo FBX) Opción *Apply Transform* del exportador FBX (`bake_space_transform`). |
| **Preset** | Usa un preset de exportación de Blender. Créalo en `File > Export > FBX/OBJ`, ajusta las opciones y guárdalo con el botón `+` de *Operator Presets*. |

Al terminar se restauran la selección, el objeto activo y el modo (Edit, Object...) que tenías.

## Generar el zip

```bash
python build.py
```

Crea `dist/simple_export-<versión>.zip` listo para instalar (súbelo a *Releases* en GitHub para distribuirlo).

## Licencia

[GPL-3.0-or-later](LICENSE)
