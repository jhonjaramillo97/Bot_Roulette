"""
Script para empaquetar Roulette Sniper Pro en un solo .exe
Requiere: pip install pyinstaller
"""

import os
import subprocess
import sys
import shutil


def build_react_dashboard():
    """Compila el dashboard React y copia los archivos a Flask static."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    react_dir = os.path.join(root, "react-dashboard")
    static_dir = os.path.join(root, "bot_ruleta", "dashboard", "static")
    assets_dir = os.path.join(static_dir, "assets")

    print("=" * 50)
    print(">>> Compilando dashboard React...")
    print("=" * 50)

    nodejs_path = r"C:\Program Files\nodejs"
    env = os.environ.copy()
    if os.path.exists(nodejs_path) and nodejs_path not in env.get("PATH", ""):
        env["PATH"] = nodejs_path + os.pathsep + env.get("PATH", "")

    if not os.path.exists(react_dir):
        print("WARN: react-dashboard/ no encontrado, saltando build React.")
        return

    if not os.path.exists(os.path.join(react_dir, "node_modules")):
        print("-> Instalando dependencias npm...")
        subprocess.check_call(["npm", "install"], cwd=react_dir, env=env, shell=True)

    print("-> npm run build...")
    subprocess.check_call(["npm", "run", "build"], cwd=react_dir, env=env, shell=True)

    if os.path.exists(assets_dir):
        shutil.rmtree(assets_dir, ignore_errors=True)
    os.makedirs(assets_dir, exist_ok=True)

    dist_dir = os.path.join(react_dir, "dist")
    shutil.copy(os.path.join(dist_dir, "index.html"), static_dir)
    for f in os.listdir(os.path.join(dist_dir, "assets")):
        shutil.copy(os.path.join(dist_dir, "assets", f), assets_dir)

    print("OK: Dashboard React copiado a bot_ruleta/dashboard/static/")
    print()


def build(production=False):
    """Empaqueta el proyecto en un .exe. Si production=True, usa DEV_MODE=False."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tunnel_path = os.path.join(root, "bot_ruleta", "tunnel.py")
    original_tunnel = None

    if production and os.path.exists(tunnel_path):
        print(">>> Modo PRODUCCION: DEV_MODE=False (dominio fijo)")
        with open(tunnel_path, "r", encoding="utf-8") as f:
            original_tunnel = f.read()
        with open(tunnel_path, "w", encoding="utf-8") as f:
            f.write(original_tunnel.replace("DEV_MODE = True", "DEV_MODE = False"))

    try:
        _do_build()
    finally:
        if original_tunnel:
            with open(tunnel_path, "w", encoding="utf-8") as f:
                f.write(original_tunnel)


def _do_build():
    # Build React dashboard first
    build_react_dashboard()

    # Rutas base — build_exe.py esta en scripts/, el codigo fuente en bot_ruleta/
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bot_ruleta")
    main_script = os.path.join(base_dir, "gui_app.py")
    icon_path = os.path.join(base_dir, "icon.ico")

    # Asegurarse de que las dependencias están instaladas
    print("Verificando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", os.path.join(base_dir, "requirements.txt")])
    except Exception as e:
        print(f"WARN: Error instalando requerimientos: {e}")

    # Asegurarse de que pyinstaller está instalado
    try:
        import PyInstaller
    except ImportError:
        print("Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Construir comando de PyInstaller
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=RouletteSniperPro",
        "--onefile",
        "--windowed",  # Sin consola negra
        "--clean",
        "--noconfirm",
    ]

    # Incluir ícono si existe
    if os.path.exists(icon_path):
        cmd.append(f"--icon={icon_path}")
        separator = ";" if os.name == 'nt' else ":"
        cmd.append(f"--add-data={icon_path}{separator}.")

    # Incluir datos estáticos del dashboard (Flask)
    dashboard_static = os.path.join(base_dir, "dashboard", "static")
    if os.path.exists(dashboard_static):
        cmd.append(f"--add-data={dashboard_static};dashboard/static")

    # Intentar obtener la ruta de customtkinter para incluirla explícitamente
    try:
        import customtkinter
        ctk_path = os.path.dirname(customtkinter.__file__)
        cmd.append(f"--add-data={ctk_path};customtkinter")
        print(f"-> Incluyendo customtkinter desde: {ctk_path}")
    except ImportError:
        print("WARN: No se pudo encontrar customtkinter para inclusion explicita.")

    # Incluir dependencias y asegurar que se recolecte todo
    cmd.append("--collect-all=customtkinter")
    cmd.append("--collect-all=PIL")
    cmd.append("--collect-all=selenium")
    cmd.append("--collect-all=undetected_chromedriver")
    
    # Forzar inclusion de metadatos y datos especificos que fallan en --onefile
    cmd.append("--copy-metadata=selenium")
    cmd.append("--copy-metadata=undetected-chromedriver")
    cmd.append("--collect-data=selenium")
    cmd.append("--collect-data=customtkinter")
    
    cmd.append("--collect-submodules=customtkinter")
    cmd.append("--hidden-import=undetected_chromedriver")
    cmd.append("--hidden-import=selenium")
    cmd.append("--hidden-import=PIL")
    cmd.append("--hidden-import=urllib")
    cmd.append("--hidden-import=tkinter")
    cmd.append("--hidden-import=waitress")  # Dashboard production server
    cmd.append("--exclude-module=pytest")
    cmd.append("--exclude-module=IPython")

    cmd.append(main_script)

    print("="*50)
    print(">>> Construyendo Roulette Sniper Pro.exe...")
    print("="*50)
    
    # Ejecutar PyInstaller
    subprocess.check_call(cmd)
    
    print("="*50)
    print("[OK] Build completado exitosamente.")
    print("El ejecutable está en la carpeta 'dist'")
    print("="*50)

if __name__ == "__main__":
    prod = "--production" in sys.argv
    build(production=prod)