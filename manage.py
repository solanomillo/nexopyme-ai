#!/usr/bin/env python
"""Utilidad de línea de comandos de Django para NexoPyme AI."""

import os
import sys


def main() -> None:
    """Ejecuta los comandos administrativos de Django."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. Verificá que esté instalado y que el "
            "entorno virtual del proyecto esté activo."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
