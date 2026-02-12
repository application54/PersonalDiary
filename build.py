# Модуль компиляции приложения

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Проверка наличия PyInstaller
def check_pyinstaller():
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

# Установка PyInstaller
def install_pyinstaller():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

# Компиляция портативного EXE файла
def compile_portable_exe():
    print("")
    print("Приложение компилируется...")
    current_dir = Path(__file__).parent
    src_dir = current_dir / "src"
    main_script = src_dir / "main.py"
    icon_file = current_dir / "icon.ico"
    if not main_script.exists():
        print(f"Ошибка: Файл {main_script} не найден!")
        return False
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=Личный дневник",
        "--clean",
        "--noconfirm",
        f"--add-data={src_dir};src",
        str(main_script)
    ]
    if icon_file.exists():
        cmd.insert(8, f"--icon={icon_file}")
    else:
        ""
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("")
        print("Приложение успешно скомпилировано!")
        portable_dir = current_dir / "App"
        portable_dir.mkdir(exist_ok=True)
        dist_dir = current_dir / "dist"
        if dist_dir.exists():
            exe_files = list(dist_dir.glob("*.exe"))
            if exe_files:
                for exe in exe_files:
                    shutil.copy2(exe, portable_dir / exe.name)
                    print("")
                    print(f"Приложение находиться в папке 'App'")
        for folder in [dist_dir, current_dir / "build"]:
            if folder.exists():
                shutil.rmtree(folder)
        spec_file = current_dir / "Личный дневник.spec"
        if spec_file.exists():
            spec_file.unlink()
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка: {e}")
        return False

# Главная функция компилятора
def main():
    print("")
    print("=" * 21)
    print("Компилятор Приложения")
    print("=" * 21)
    if not check_pyinstaller():
        install_pyinstaller()
    success = compile_portable_exe()
    if success:
        ""
    else:
        ""

if __name__ == "__main__":
    main()