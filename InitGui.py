# InitGui.py

def _openmechanical_startup():
    import os
    import sys
    import traceback

    import FreeCAD as App
    import FreeCADGui as Gui

    MODULE_FILE = "OpenMechanicalWorkbench.py"
    MOD_NAME = "OpenMechanical"

    candidates = []

    # Pasta Mod do usuário
    try:
        candidates.append(
            os.path.join(
                App.getUserAppDataDir(),
                "Mod",
                MOD_NAME
            )
        )
    except Exception:
        pass

    # Pasta Mod da instalação do FreeCAD
    try:
        candidates.append(
            os.path.join(
                App.getHomePath(),
                "Mod",
                MOD_NAME
            )
        )
    except Exception:
        pass

    # Caminhos comuns no Windows
    try:
        home = os.path.expanduser("~")

        candidates.append(
            os.path.join(
                home,
                "AppData",
                "Roaming",
                "FreeCAD",
                "Mod",
                MOD_NAME
            )
        )

        candidates.append(
            os.path.join(
                home,
                "AppData",
                "Roaming",
                "FreeCAD",
                "v1-1",
                "Mod",
                MOD_NAME
            )
        )

    except Exception:
        pass

    module_dir = None

    for path in candidates:
        try:
            path = os.path.abspath(os.path.normpath(path))

            if os.path.isdir(path) and os.path.isfile(os.path.join(path, MODULE_FILE)):
                module_dir = path
                break

        except Exception:
            pass

    if module_dir:
        if module_dir not in sys.path:
            sys.path.insert(0, module_dir)

        App.Console.PrintMessage(f"[INFO] Diretório do addon: {module_dir}\n")

    else:
        App.Console.PrintError("[ERRO] Não foi possível encontrar o diretório do OpenMechanicalWorkbench.\n")

        for path in candidates:
            App.Console.PrintError(f"[DEBUG] Caminho testado: {path}\n")

    try:
        import OpenMechanicalWorkbench

        Gui.addWorkbench(
            OpenMechanicalWorkbench.OpenMechanicalWorkbench()
        )

        App.Console.PrintMessage("[OK] Open Mechanical Workbench carregada com sucesso!\n")

    except Exception:
        App.Console.PrintError("[ERRO] Falha ao carregar Open Mechanical Workbench:\n")
        App.Console.PrintError(traceback.format_exc())

        if module_dir:
            App.Console.PrintError(f"[DEBUG] module_dir = {module_dir}\n")
        else:
            App.Console.PrintError("[DEBUG] module_dir = None\n")


try:
    _openmechanical_startup()

except Exception:
    try:
        import traceback
        import FreeCAD as App

        App.Console.PrintError("[ERRO] Erro crítico na inicialização da Open Mechanical Workbench:\n")
        App.Console.PrintError(traceback.format_exc())

    except Exception:
        print("[ERRO] Erro crítico na inicialização da Open Mechanical Workbench.")

        try:
            import traceback
            print(traceback.format_exc())

        except Exception:
            pass