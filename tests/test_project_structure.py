"""Pruebas DB-free de la estructura de la fundación (T-13)."""

from pathlib import Path

import django.contrib.admin
import unfold
from django.conf import settings

REQUIRED_FILES = (
    "apps/__init__.py",
    "apps/core/__init__.py",
    "apps/core/apps.py",
    "apps/core/admin.py",
    "templates/base.html",
    "templates/home.html",
    "templates/components/navbar.html",
    "templates/components/footer.html",
    "static/css/main.css",
    "docs/README.md",
    "tests/__init__.py",
)

FORBIDDEN_CORE_FILES = ("models.py", "views.py", "services.py")

OWN_FRONTEND_FILES = (
    "templates/base.html",
    "templates/home.html",
    "templates/components/navbar.html",
    "templates/components/footer.html",
    "static/css/main.css",
)


def _base_dir() -> Path:
    """Devuelve el directorio raíz del proyecto."""
    return Path(settings.BASE_DIR)


def test_required_foundation_files_exist() -> None:
    """Existen los archivos mínimos de estructura y de la fundación visual."""
    base_dir = _base_dir()
    missing = [
        relative for relative in REQUIRED_FILES if not (base_dir / relative).is_file()
    ]
    assert missing == [], f"Faltan archivos requeridos: {missing}"


def test_core_app_has_no_models_or_migrations() -> None:
    """apps/core es infraestructura: sin modelos, vistas ni migraciones."""
    core_dir = _base_dir() / "apps" / "core"
    for filename in FORBIDDEN_CORE_FILES:
        assert not (core_dir / filename).exists(), (
            f"apps/core/{filename} no debe existir"
        )
    assert not (core_dir / "migrations").exists()


def test_no_business_apps_were_created() -> None:
    """El paquete apps solo contiene CoreConfig como app de infraestructura."""
    apps_dir = _base_dir() / "apps"
    entries = {
        entry.name for entry in apps_dir.iterdir() if entry.name != "__pycache__"
    }
    assert entries == {"__init__.py", "accounts", "audit", "core"}


def test_own_templates_and_css_do_not_reference_unfold() -> None:
    """Las plantillas y el CSS propios no dependen de assets de Unfold."""
    base_dir = _base_dir()
    for relative in OWN_FRONTEND_FILES:
        text = (base_dir / relative).read_text(encoding="utf-8")
        assert "unfold" not in text.lower(), f"{relative} referencia Unfold"


def test_admin_templates_do_not_include_main_css() -> None:
    """Las plantillas de Admin no dependen de static/css/main.css."""
    admin_templates_dirs = (
        Path(django.contrib.admin.__file__).parent / "templates",
        Path(unfold.__file__).parent / "templates",
    )
    checked = 0
    for templates_dir in admin_templates_dirs:
        assert templates_dir.is_dir(), f"No existe {templates_dir}"
        for template_path in templates_dir.rglob("*.html"):
            text = template_path.read_text(encoding="utf-8", errors="ignore")
            assert "main.css" not in text, (
                f"La plantilla de Admin {template_path} incluye main.css"
            )
            checked += 1
    assert checked > 0, "No se revisó ninguna plantilla de Admin"
