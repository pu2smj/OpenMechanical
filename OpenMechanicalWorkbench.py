# -*- coding: utf-8 -*-

# OpenMechanicalWorkbench.py
# Compatível com FreeCAD 0.19+ e FreeCAD 1.x

import os
import traceback

import FreeCAD as App
import FreeCADGui as Gui


__title__ = "Open Mechanical Workbench"
__version__ = "1.0.1"
__author__ = "OpenMechanicalWorkbench Contributors"


# ----------------------------------------------------------------------------
# Caminhos
# ----------------------------------------------------------------------------

BASE_PATH = os.path.dirname(__file__)
ICONS_PATH = os.path.join(BASE_PATH, "Resources", "icons")
TRANSLATIONS_PATH = os.path.join(BASE_PATH, "Resources", "translations")


def icon_path(filename):
    """
    Retorna o caminho absoluto do ícone se ele existir.
    Se não existir, retorna string vazia.
    """
    path = os.path.join(ICONS_PATH, filename)
    if os.path.exists(path):
        return path
    return ""


def load_translations():
    """
    Carrega o tradutor Qt para o locale do sistema.
    Procura arquivos .qm em Resources/translations/.
    """
    try:
        from PySide6 import QtCore
    except ImportError:
        try:
            from PySide2 import QtCore
        except ImportError:
            App.Console.PrintMessage(
                "OpenMechanical: PySide not available, translations disabled.\n"
            )
            return

    locale = QtCore.QLocale.system().name()
    translator = QtCore.QTranslator()
    loaded = translator.load(f"OpenMechanical_{locale}", TRANSLATIONS_PATH)
    if loaded:
        QtCore.QCoreApplication.installTranslator(translator)
        App.Console.PrintMessage(
            f"OpenMechanical: translator loaded for locale '{locale}'.\n"
        )
    else:
        App.Console.PrintMessage(
            f"OpenMechanical: no translator found for locale '{locale}'.\n"
        )


# ----------------------------------------------------------------------------
# Funções auxiliares
# ----------------------------------------------------------------------------

def active_or_new_document(document_name):
    """
    Retorna o documento ativo ou cria um novo se não houver documento ativo.
    """
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument(document_name)
    return doc


def fit_view():
    """
    Ajusta a vista ao conteúdo, se possível.
    """
    try:
        Gui.SendMsgToActiveView("ViewFit")
    except Exception:
        pass


# ----------------------------------------------------------------------------
# Criação das peças
# ----------------------------------------------------------------------------

def make_bearing():
    import sys
    import os
    import traceback
    
    try:
        addon_path = os.path.dirname(os.path.abspath(__file__))
        if addon_path not in sys.path:
            sys.path.insert(0, addon_path)
        
        App.Console.PrintMessage(f"OpenMechanical: addon_path = {addon_path}\n")
        
        from BearingWorkbench.BearingSelectionDialog import select_bearing
        from BearingWorkbench.main import Bearing
        
        App.Console.PrintMessage("OpenMechanical: Selection dialog opening...\n")
        selected = select_bearing()
        
        if selected:
            App.Console.PrintMessage(f"OpenMechanical: Bearing selected: {selected}\n")
            bearing = Bearing(selected)
            bearing.build()
            fit_view()
            App.Console.PrintMessage("OpenMechanical: Bearing generated successfully!\n")
        else:
            App.Console.PrintMessage("OpenMechanical: Selection cancelled by user.\n")
    except Exception as e:
        App.Console.PrintError(f"OpenMechanical: Error creating bearing:\n{traceback.format_exc()}\n")


def make_bushing():
    import Part

    doc = active_or_new_document("Bushing")

    outer = Part.makeCylinder(15, 25)
    inner = Part.makeCylinder(8, 25)
    shape = outer.cut(inner)

    obj = doc.addObject("Part::Feature", "Bushing")
    obj.Shape = shape

    doc.recompute()
    fit_view()


def make_coupling():
    import Part

    doc = active_or_new_document("Coupling")

    cyl1 = Part.makeCylinder(20, 10)
    cyl2 = Part.makeCylinder(20, 10, App.Vector(0, 0, 10))
    shape = cyl1.fuse(cyl2)

    obj = doc.addObject("Part::Feature", "Coupling")
    obj.Shape = shape

    doc.recompute()
    fit_view()


def make_oring():
    import sys
    import os
    import traceback

    try:
        addon_path = os.path.dirname(os.path.abspath(__file__))
        if addon_path not in sys.path:
            sys.path.insert(0, addon_path)

        App.Console.PrintMessage("OpenMechanical: O-ring selection dialog opening...\n")

        from ORingWorkbench.ORingSelectionDialog import select_oring
        from ORingWorkbench.main import ORing

        selected, selected_color = select_oring()

        if selected:
            App.Console.PrintMessage(f"OpenMechanical: O-ring selected: {selected}\n")
            ring = ORing(selected, color=selected_color)
            ring.build()
            fit_view()
            App.Console.PrintMessage("OpenMechanical: O-ring generated successfully!\n")
        else:
            App.Console.PrintMessage("OpenMechanical: Selection cancelled by user.\n")
    except Exception as e:
        App.Console.PrintError(f"OpenMechanical: Error creating o-ring:\n{traceback.format_exc()}\n")


def make_seal():
    import Part

    doc = active_or_new_document("Seal")

    outer = Part.makeCylinder(20, 5)
    inner = Part.makeCylinder(15, 5)
    shape = outer.cut(inner)

    obj = doc.addObject("Part::Feature", "Seal")
    obj.Shape = shape

    doc.recompute()
    fit_view()


# ----------------------------------------------------------------------------
# Comando genérico
# ----------------------------------------------------------------------------

class Command:
    """
    Comando genérico para FreeCAD.

    No FreeCAD, um comando Python precisa implementar pelo menos:
      - GetResources()
      - Activated()
      - IsActive()

    Não é necessário herdar de Gui.Command.
    """

    def __init__(self, menu_text, tooltip, icon_file, action_function):
        self.menu_text = menu_text
        self.tooltip = tooltip
        self.icon_file = icon_file
        self.action_function = action_function

    def GetResources(self):
        resources = {
            "MenuText": self.menu_text,
            "ToolTip": self.tooltip,
        }

        icon = icon_path(self.icon_file)
        if icon:
            resources["Pixmap"] = icon

        return resources

    def Activated(self):
        try:
            self.action_function()
        except Exception:
            App.Console.PrintError(f"Error executing '{self.menu_text}':\n")
            App.Console.PrintError(traceback.format_exc())

    def IsActive(self):
        return True


# ----------------------------------------------------------------------------
# Registro dos comandos
# ----------------------------------------------------------------------------

_REGISTERED_COMMANDS = {}


def register_commands():
    """
    Registra os comandos no FreeCAD.

    Importante:
      - O primeiro argumento do Gui.addCommand() é o nome global do comando.
      - O segundo argumento deve ser uma instância de objeto de comando.
      - Este método funciona tanto em FreeCAD antigo quanto no FreeCAD 1.x.
    """

    commands = (
        (
            "BearingCommand",
            Command(
                "Bearing",
                "Create a rolling bearing with selection dialog",
                "Bearing.svg",
                make_bearing,
            ),
        ),
        (
            "BushingCommand",
            Command(
                "Bushing",
                "Create a bushing",
                "Bushing.svg",
                make_bushing,
            ),
        ),
        (
            "CouplingCommand",
            Command(
                "Coupling",
                "Create a coupling",
                "Coupling.svg",
                make_coupling,
            ),
        ),
        (
            "ORingCommand",
            Command(
                "O-Ring",
                "Create an O-Ring",
                "ORing.svg",
                make_oring,
            ),
        ),
        (
            "SealCommand",
            Command(
                "Seal",
                "Create a seal",
                "Seal.svg",
                make_seal,
            ),
        ),
    )

    for command_name, command_object in commands:
        try:
            Gui.addCommand(command_name, command_object)
            _REGISTERED_COMMANDS[command_name] = command_object
        except Exception:
            App.Console.PrintError(f"Error registering command '{command_name}':\n")
            App.Console.PrintError(traceback.format_exc())


register_commands()


# ----------------------------------------------------------------------------
# Workbench
# ----------------------------------------------------------------------------

class OpenMechanicalWorkbench(Gui.Workbench):
    """
    Open Mechanical Workbench.
    """

    MenuText = "Open Mechanical"
    ToolTip = "Open-source mechanical component library"
    Icon = icon_path("OpenMechanicalWorkbench.svg")

    def __init__(self):
        self.main_commands = [
            "BearingCommand",
            "BushingCommand",
            "CouplingCommand",
            "ORingCommand",
            "SealCommand",
        ]

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def _available_commands(self, command_names):
        """
        Retorna apenas comandos realmente registrados.
        Isso evita 'Unknown command' caso algum registro falhe.
        """
        return [name for name in command_names if name in _REGISTERED_COMMANDS]

    def Initialize(self):
        """
        Chamado quando a bancada é ativada pela primeira vez.
        """
        load_translations()

        main_commands = self._available_commands(self.main_commands)

        if not main_commands:
            App.Console.PrintError(
                "Open Mechanical Workbench: no commands available.\n"
            )
            return

        # Toolbar/menu principal
        self.appendToolbar("Open Mechanical", main_commands)
        self.appendMenu("Open Mechanical", main_commands)

        # Toolbars/menus separados por categoria
        groups = (
            ("Bearings", ["BearingCommand"]),
            ("Bushings", ["BushingCommand"]),
            ("Couplings", ["CouplingCommand"]),
            ("O-Rings", ["ORingCommand"]),
            ("Seals", ["SealCommand"]),
        )

        for title, command_names in groups:
            available = self._available_commands(command_names)
            if available:
                self.appendToolbar(title, available)
                self.appendMenu(title, available)

    def Activated(self):
        App.Console.PrintMessage("Open Mechanical Workbench activated!\n")

    def Deactivated(self):
        pass

    def ContextMenu(self, recipient):
        """
        Menu de contexto com botão direito.
        """
        commands = self._available_commands(self.main_commands)
        if commands:
            self.appendContextMenu("Open Mechanical", commands)