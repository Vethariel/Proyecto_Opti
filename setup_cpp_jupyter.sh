#!/usr/bin/env bash
set -euo pipefail

MAMBA_ROOT_PREFIX="${MAMBA_ROOT_PREFIX:-$HOME/micromamba}"
MICROMAMBA="${MICROMAMBA:-$HOME/micromamba/bin/micromamba}"
ENV_NAME="cpp-jupyter"

echo "==> Descargando micromamba (si hace falta)..."
if [[ ! -x "$MICROMAMBA" ]]; then
  mkdir -p "$MAMBA_ROOT_PREFIX/bin"
  curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj -C "$MAMBA_ROOT_PREFIX" bin/micromamba
  mv "$MAMBA_ROOT_PREFIX/bin/micromamba" "$MICROMAMBA"
fi

export MAMBA_ROOT_PREFIX

echo "==> Creando entorno '$ENV_NAME' con xeus-cling y JupyterLab..."
"$MICROMAMBA" create -y -n "$ENV_NAME" -c conda-forge xeus-cling jupyterlab ipywidgets

echo
echo "Listo. Kernels instalados:"
"$MICROMAMBA" run -n "$ENV_NAME" jupyter kernelspec list

echo
echo "Para empezar:"
echo "  chmod +x iniciar_jupyter.sh"
echo "  ./iniciar_jupyter.sh"
