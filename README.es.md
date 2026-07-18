<div align="center">

# PrecioAlPeso

![Logo](assets/icon.png)

[🇬🇧 English](README.en.md) | **🇪🇸 Español**

**Una aplicación para Android que te ayuda a comparar productos calculando su precio equivalente según su peso.**

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Kivy](https://img.shields.io/badge/Kivy-Framework-success.svg)](https://kivy.org/)
[![Android](https://img.shields.io/badge/Android-Supported-brightgreen.svg)](https://www.android.com/)
[![License: GPL v3 or later](https://img.shields.io/badge/License-GPLv3%2B-blue.svg)](LICENSE)

</div>

---

# 📱 Capturas

<table>
  <tr>
    <td valign="top">
      <img src="assets/app.png" alt="pantalla principal" width="250">
    </td>
    <td valign="top">
      <img src="assets/seleccion.png" alt="selección" width="250">
    </td>
    <td valign="top">
      <img src="assets/resultado.png" alt="unidad de peso" width="250">
    </td>
  </tr>
</table>

---

# Características

- Calcula automáticamente el precio equivalente según el peso.
- Introduce dos valores y el tercero se calcula automáticamente.
- Desarrollada para Android.

---

# Tecnologías utilizadas

- Python 3
- Kivy
- Buildozer

---

# 📥 Instalación

## Opción 1 (Recomendada)

### Descargar la APK

Descarga la [**última versión**](https://github.com/rottencio/PrecioAlPeso/releases/latest)

O descarga versiones anteriores desde la sección [**Releases**](https://github.com/rottencio/PrecioAlPeso/releases) de este repositorio.

### Copiar la APK al dispositivo Android

Puedes hacerlo mediante:
- USB
- Google Drive
- Telegram
- Bluetooth
- Cualquier otro método de transferencia de archivos

### Instalar la aplicación

Dado que la aplicación no se distribuye a través de Google Play, Android puede mostrar una advertencia indicando que proviene de una fuente desconocida.

Permite la instalación desde la aplicación que usaste para abrir el archivo APK (Archivos, Chrome, Drive, etc.) y luego continúa con la instalación.

<table>
  <tr>
    <td valign="top">
      <img src="assets/appsDesconocidas.png" alt="permitir app desconocidas" width="250">
    </td>
    <td valign="middle">
      <img src="assets/detalles.png" alt="pincha en detalles" width="250">
    </td>
    <td valign="middle">
      <img src="assets/instalardetodasformas.png" alt="instalar" width="250">
    </td>
  </tr>
</table>

---

## Opción 2 — Ejecutar desde el código fuente

### Clonar el repositorio

>Bash
```bash
git clone https://github.com/rottencio/PrecioAlPeso.git
cd PrecioAlPeso
```

### Crear un entorno virtual

Linux / macOS / WSL
>Bash
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell)
>PowerShell
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Instalar dependencias
>Bash
```bash
pip install kivy cython
```

### Ejecutar
>Bash
```bash
python main.py
```

---

# Compilación para Android ![icono Android](assets/icons8-android.png)

La compilación debe realizarse desde Linux o WSL.

## Instalar dependencias del sistema
>Bash
```Bash
sudo apt update

sudo apt install -y \
    git \
    zip \
    unzip \
    openjdk-17-jdk \
    python3-pip \
    python3-venv \
    build-essential \
    autoconf \
    automake \
    libtool \
    cmake \
    pkg-config \
    libffi-dev \
    libssl-dev \
    zlib1g-dev \
    pipx
```

## Instalar Buildozer
>Bash
```bash
pipx install buildozer
```

## Compilar
>Bash
```bash
buildozer android debug
```

La APK aparecerá en:

```text
bin/
```

---

# 📄 Licencia

Este proyecto se distribuye bajo la **Licencia Pública General GNU v3.0 (GPL-3.0)**. <br>
La información sobre los derechos de autor se encuentra en [COPYRIGHT](COPYRIGHT).

---

# 👤 Autor

[**rottencio**](https://github.com/rottencio)

# 🙏 Créditos
Los recursos de terceros y agradecimientos se encuentran en [CREDITS.md](CREDITS.md).