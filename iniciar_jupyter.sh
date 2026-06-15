#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAMBA_ROOT_PREFIX="${MAMBA_ROOT_PREFIX:-$HOME/micromamba}"
MICROMAMBA="${MICROMAMBA:-$HOME/micromamba/bin/micromamba}"

if [[ ! -x "$MICROMAMBA" ]]; then
  echo "No se encontró micromamba en $MICROMAMBA"
  echo "Instala el entorno con: ./setup_cpp_jupyter.sh"
  exit 1
fi

export MAMBA_ROOT_PREFIX

echo "Iniciando JupyterLab con kernel C++..."
echo "Kernels disponibles: xcpp11, xcpp14, xcpp17"
echo "Abre: http://localhost:8888"
echo

exec "$MICROMAMBA" run -n cpp-jupyter jupyter lab --notebook-dir="$SCRIPT_DIR" "$@"
