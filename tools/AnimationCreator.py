#import io
import importlib.util
import pathlib
import os

from typing import Any
from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, Window, HSplit, FloatContainer, Float, ConditionalContainer
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import TextArea, Frame
from prompt_toolkit.layout import HorizontalAlign, Margin, WindowAlign
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.filters import Condition
from prompt_toolkit.application import get_app

from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum
from ai_talking_robot.sequencer.DefaultMoveSequencer import DefaultMoveSequencer
# Lista de tuplas (índice de valor del enum, ancho que ocupa en pantalla)
# El valor en el tamaño None es toda la pantalla
property_distribution = [
    (0,4, "CHN.."),
    ("name",None, "NAME"),
    ("value",4, "VAL."),
    (1,4, "MIN"),
    (2,4, "MAX"),
]

# Estilos
def get_component_style(selected: bool, activated: bool):
    activated_color="#ffffff"
    deactivated_color="#888888"
    
    selected_foreground_color="#000000"

    if activated:
        main_color = activated_color
    else:
        main_color = deactivated_color

    if selected:
        return f"bg:{main_color} fg:{selected_foreground_color}"
    else:
        return f"fg:{main_color}"


class ComponentInfo:
    def __init__(self, value, activated : bool = False):
        self.value = value
        self.activated = activated

class ParametersInfo:
    def __init__(self, time : float = 1.0):
        self.time = time
        self.type = PredefinedValues(["linear", "squared", "squareroot"])

class PredefinedValues:
    def __init__(self, values : list[str]):
        self._values = values
        self.current_index = 0

    @property
    def display_name(self):
        return self._values[self.current_index]
    
    @display_name.setter
    def display_name(self, value: str):
        try:
            newValue = self._values.index(value)
        except ValueError:
            newValue = 0
        
    def changeValue(self, value: int):
        self.current_index = (value + len(self._values)) % len(self._values)

move_sequencer = None
# Parameters info
total_parameters = 2

# Component Info
component_list : list[ComponentEnum] = []

total_components = 0
selected_component = -1

total_frames = 1
selected_frame = 0

#[Frame, component]
component_values : list[list[ComponentInfo]] = [] 
#[Frame].property
frame_parameters : list[ParametersInfo] = []

# UI Info
value_col = 0
row_list = []
frame_bar : VSplit
parameters_row_list : HSplit
#input_field : TextArea
next_operation_after_dialog = None
dialog_hidden = True

is_dialog_hidden = Condition(lambda: dialog_hidden)
is_dialog_visible = Condition(lambda: not dialog_hidden)

def start(sequencer : DefaultMoveSequencer, *componentEnums: type[ComponentEnum]):

    global component_list, component_values, total_components, move_sequencer

    move_sequencer = sequencer

    total_components = 0 

    component_values.append([])
    
    for componentEnum in componentEnums:
        for component in componentEnum:
            component_list.append(component)
            component_values[0].append(ComponentInfo(component.currentValue))
            total_components += 1

    first_frame_parameters = ParametersInfo()
    frame_parameters.append(first_frame_parameters)
    create_ui()


def create_ui():
    global row_list, selected_component, value_col, frame_bar, selected_frame, parameters_row_list, input_field

    # Crear la lista de frames
    frame_bar = VSplit(children = [Window(content=FormattedTextControl(text=f'[0]', style=get_component_style(True, True)),dont_extend_width=True)], height=1, align=HorizontalAlign.LEFT)
        
    # Crear la barra de parámetros
    parameters_row_list = [
        VSplit(children=[
            Window(content=FormattedTextControl(text = f"Time:"), width=8),
            Window(content=FormattedTextControl(text = "1.0"), dont_extend_width=True),
            Window(content=FormattedTextControl(text = "s"))
        ], height=1, style=get_component_style(selected=False, activated=True)),
        VSplit(children=[
            Window(content=FormattedTextControl(text = f"Type:"), width=8),
            Window(content=FormattedTextControl(text = "lineal"))
        ], height=1, style=get_component_style(selected=False, activated=True))
    ]

    # Crear los encabezados
    headers = []
    for idx, (propertyName, width, propertyTitle) in enumerate(property_distribution):
    
        if propertyName == "value":
            value_col = idx

        textControl = FormattedTextControl(text = f'{propertyTitle}')    
        headers.append(Window(content = textControl, width= width))


    # Crear la lista de componenets
    for component in component_list:
        row = []
        for propertyNumber, width, _ in property_distribution:

            if propertyNumber == "name":
                text = f'{component.__class__.__name__}.{component.name}'
            elif propertyNumber == "value":
                text = component.currentValue
            else:
                text = component.value[propertyNumber]

            textControl = FormattedTextControl(text = f'{text}')
            cell = Window(content = textControl, width= width)
            row.append(cell)
        
        row_list.append(VSplit(children=row, height=1, padding=2,style=get_component_style(selected=False, activated=False)))


    # Crear la lista de ventanas de ayuda y agruparlas dinámicamente en barras
    help_texts = [
        '[↑ ↓: Select component]',
        '[← →: Change value by 1]',
        '[Ctrl + ← or →: Change value by 10]',
        '[Space: Toggle component]',
        '[M: Set all to minimum values]',
        '[N: Deactivate all]',
        '[A D: Select Frame]',
        '[+: Add new frame]',
        '[Backspace: Delete current frame]',
        '[R: Play animation]',
        '[Ctrl + S: Save Animation]'
        '[Ctrl + O: Load Animation]'
        '[Ctrl+Q: Quit]',
    ]

    help_windows = [
        Window(
            content=FormattedTextControl(text=text),
            height=1
        )
        for text in help_texts
    ]

    # Parámetro para el tamaño de cada barra de ayuda
    help_bar_lengths = [3, 3, 3, 2]

    help_bars = []
    i = 0
    for length in help_bar_lengths:
        bar = VSplit(
            children=help_windows[i:i+length],
            align=HorizontalAlign.JUSTIFY,
            style="bg:#ffffff fg:#000000"
        )
        help_bars.append(bar)
        i += length

    # Armar el menú principal
    internal_container = HSplit(
            [frame_bar]
            +
            [Window(char="-", height=1)]
            +
            parameters_row_list
            +
            [Window(char="=", height=1)]
            +
            [VSplit(children=headers, height=1, padding=2)]
            +
            [Window(char="-", height=1)]
            +
            row_list
                     
        )

    # Agregar a la rowlist la lista de parámetros    
    row_list.extend(parameters_row_list)
    
    # Decorar el menú con un marco simple
    external_container = HSplit(children=[
        Window(content=None,height=1),
        VSplit(height=1, children=[
            Window(width=1), Window(char="█"), Window(width=1)   
        ]
        ),
        VSplit(children=[
            Window(width=1), Window(char="█", width=1), internal_container,  Window(char="█", width=1), Window(width=1)
        ]),
        VSplit(height=1, children=[
            Window(width=1), Window(char="█"), Window(width=1)   
        ]),
        Window(content=None,height=1),
        Window(content=None,height=None),
    ] 
    + help_bars)

    # Crear el dialog:
    input_field = TextArea(multiline=False, password=False)

    dialog_content = Frame(
        title="Input text",
        body=HSplit([
            input_field,
        ]), width=50
    )

    float_container = Float(
        content=ConditionalContainer(
            content=dialog_content,
            filter=is_dialog_visible
        ),
    )

    root_container = FloatContainer(content = external_container, floats=[float_container])
    
    kb = KeyBindings()

    @kb.add('c-q')
    def exit_(event):
        event.app.exit()

    @kb.add('up', filter = is_dialog_hidden)
    def _(event):
        change_selected_component(selected_component - 1)
        
    @kb.add('down', filter = is_dialog_hidden)
    def _(event):
        change_selected_component(selected_component + 1)

    @kb.add('left', filter = is_dialog_hidden)
    def _(event):
        sum_component_value(selected_component, -1)
    
    @kb.add('right', filter = is_dialog_hidden)
    def _(event):
        sum_component_value(selected_component, +1)

    @kb.add('c-left', filter = is_dialog_hidden)
    def _(event):
        sum_component_value(selected_component, -10)

    @kb.add('c-right', filter = is_dialog_hidden)
    def _(event):
        sum_component_value(selected_component, +10)

    @kb.add('space', filter = is_dialog_hidden)
    def _(event):
        toggle_component(selected_component)

    @kb.add('n', filter = is_dialog_hidden)
    @kb.add('N', filter = is_dialog_hidden)
    def _(event):
        deactivate_all_components()

    @kb.add('m', filter = is_dialog_hidden)
    @kb.add('M', filter = is_dialog_hidden)
    def _(event):
        restart_all_values()
    
    @kb.add('a', filter = is_dialog_hidden)
    @kb.add('A', filter = is_dialog_hidden)
    def _(event):
        change_selected_frame(selected_frame - 1)
    
    @kb.add('d', filter = is_dialog_hidden)
    @kb.add('D', filter = is_dialog_hidden)
    def _(event):
        change_selected_frame(selected_frame + 1)

    @kb.add('+', filter = is_dialog_hidden)
    def _(event):
        add_new_frame()

    @kb.add('backspace', filter = is_dialog_hidden)
    def _(event):
        delete_frame(selected_frame)
        change_selected_frame(selected_frame - 1)

    @kb.add('r', filter = is_dialog_hidden)
    @kb.add('R', filter = is_dialog_hidden)
    def _(event):
        execute_animation()
        pass

    @kb.add('c-s', filter = is_dialog_hidden)
    def _(event):
        global dialog_hidden, next_operation_after_dialog

        next_operation_after_dialog = save_animation

        dialog_content.title="Save animation as:"
        dialog_hidden = False

        event.app.layout.focus(input_field)

    @kb.add('c-o', filter = is_dialog_hidden)
    def _(event):
        global dialog_hidden, next_operation_after_dialog

        next_operation_after_dialog = load_animation

        dialog_content.title="Load animation from file:"
        dialog_hidden = False

        event.app.layout.focus(input_field)

    @kb.add('enter', filter=is_dialog_visible)
    def _(event):
        global dialog_hidden, next_operation_after_dialog

        input_text = input_field.text

        dialog_hidden = True   
        input_field.text = ""

        next_operation_after_dialog(input_text)
        #event.app.layout.focus(external_container.children[0])

    @kb.add('escape', filter=is_dialog_visible)
    def _(event):
        global dialog_hidden 
        dialog_hidden = True
        input_field.text = ""

    final_layout = Layout(root_container)
    #final_layout.focus(external_container.children[0])
    app = Application(key_bindings=kb, layout= final_layout, full_screen=True)
    app.run() 
    
# Funciones para los componentes
def change_selected_component(newSelectedComponent : int):
    global selected_component
    previous_selected = selected_component
    
    selected_component = (newSelectedComponent + total_components + total_parameters*2) % (total_components + total_parameters) - total_parameters
    
    update_row_ui(previous_selected)
    update_row_ui(selected_component)
    
def sum_component_value(component: int, value : Any):
    if component < 0:
        change_parameter_value(component, value)
        return
    elif not component_values[selected_frame][component].activated:
        return
        
    component_list[component].currentValue = component_list[component].currentValue + value
    component_values[selected_frame][component].value = component_list[component].currentValue
    update_row_ui(component)

def toggle_component(component: int):
    if component < 0:
        return
    component_values[selected_frame][component].activated = not component_values[selected_frame][component].activated 

    if component_values[selected_frame][component].activated:
        component_list[component].currentValue = component_values[selected_frame][component].value 
    else:
        component_list[component].currentValue = None

    update_row_ui(component)

def restart_all_values():
    for indx in range(total_components):
        component_values[selected_frame][indx].value = component_list[indx].min_value
        component_list[indx].currentValue = component_list[indx].min_value
    update_all_component_values()

def deactivate_all_components():
    for indx in range(total_components):
        component_values[selected_frame][indx].activated = False
        component_list[indx].currentValue = None
        update_row_ui(indx)

def change_parameter_value(component: int, value: int):
    if component == -2:
        frame_parameters[selected_frame].time += value / 10.0
        frame_parameters[selected_frame].time = max(frame_parameters[selected_frame].time, 0.0)
    elif component == -1:
        frame_parameters[selected_frame].type.changeValue(frame_parameters[selected_frame].type.current_index + value)
    else:
        return
    update_parameter_ui(component)

def update_parameter_ui(component: int):    
    if component == -2:
        row_list[component].get_children()[1].content.text = f'{frame_parameters[selected_frame].time:.1f}'
    elif component == -1:
        row_list[component].get_children()[1].content.text = f'{frame_parameters[selected_frame].type.display_name}'
    else:
        return
    pass

# Funciones para los frames
def add_new_frame():
    global frame_bar, total_frames, component_values
    component_values.append([])
    frame_parameters.append(ParametersInfo())

    for indx in range(total_components):
        if total_frames > 0:
            previous_frame_component = component_values[total_frames - 1][indx]
        else:
            previous_frame_component = ComponentInfo(component_list[indx].min_value, False)

        component_values[total_frames].append(
            ComponentInfo(previous_frame_component.value, previous_frame_component.activated)
        )

    frame_bar.children.append(Window(content=FormattedTextControl(text=f'[{total_frames}]'),dont_extend_width=True))
    total_frames += 1

def delete_frame(frame_to_delete: int):
    global frame_bar, total_frames

    if total_frames <= 1:
        return

    frame_bar.children.pop(frame_to_delete)
    component_values.pop(frame_to_delete)
    frame_parameters.pop(frame_to_delete)

    total_frames -= 1

    for indx, frame in enumerate(frame_bar.children):
        frame.content.text = f"[{indx}]"

def change_selected_frame(new_selected_frame : int):
    global selected_frame, frame_bar

    if 0 <= selected_frame < total_frames:
        frame_bar.children[selected_frame].content.style = get_component_style(selected=False, activated=True)
    
    selected_frame = (new_selected_frame + total_frames) % total_frames

    for indx, component in enumerate(component_list):
        if component_values[selected_frame][indx].activated:
            component.currentValue = component_values[selected_frame][indx].value
        else:
            component.currentValue = None

    frame_bar.children[selected_frame].content.style = get_component_style(selected=True, activated=True)

    update_all_component_values()

    for i in range(-1, -3, -1):
        update_parameter_ui(i) 

# Funciones para actualizar UI
def update_row_ui(row: int):
    if row < 0:
        row_list[row].style = get_component_style(selected_component == row, True)
        return

    style = get_component_style(
        selected= selected_component == row, 
        activated = component_values[selected_frame][row].activated
    )

    row_list[row].style = style
    row_list[row].get_children()[value_col].content.text = f'{component_list[row].currentValue}'

def update_all_component_values():
    for indx in range(total_components):
        update_row_ui(indx)

# Funciones de archivos
def create_animation_object() -> list[dict[str, Any]]:
    sequence : list[Any] = []

    for frame in range(total_frames):
        movement_dict : dict[str, Any] = {}

        parameters_dict : dict[str, Any] = {}
        parameters_dict["time"] = frame_parameters[frame].time
        parameters_dict["type"] = frame_parameters[frame].type.display_name
  
        components_dict : dict[ComponentEnum, Any] = {}

        for component in range(total_components):
            if component_values[frame][component].activated:
                components_dict[component_list[component]] = component_values[frame][component].value

        movement_dict["parameters"] = parameters_dict   
        movement_dict["components"] = components_dict

        sequence.append(movement_dict)
    
    return sequence

def execute_animation():
    move_sequencer.executeSequence(sequence = create_animation_object())

def pretty_print_dict(object, output, indent=0, ignore_first_indentation = False):

    value_indent = 0 if ignore_first_indentation else indent

    if isinstance(object, dict):
        print("  " * value_indent + "{", file=output)
        for key, value in object.items():   
            pretty_print_dict(key, output, indent + 1, False)
            #print("  " * (indent+1) + "\"" + str(key) + "\": ", end="", file=output)
            print(" : ", file=output, end = "")
            pretty_print_dict(value, output, indent + 1, True)
            print(",", file=output)
        print("  " * indent + "}",end="", file=output)

    elif isinstance(object, list):
        print("  " * value_indent + "[", file=output)
        for value in object:
            pretty_print_dict(value, output, indent + 1)
            print(",", file=output) 

        print("  " * indent + "]",end="", file=output)
    elif isinstance(object, str):
        print("  " * value_indent + "\"" + str(object) + "\"", end="", file=output)
    else:
        print("  " * value_indent + str(object), end="", file=output)

def save_animation(filename: str):
    animation = create_animation_object()
    # Ensure the filename has .py extension
    if not filename.lower().endswith(".py"):
        filename += ".py"

    name = os.path.basename(filename)

    with open(filename, "w", encoding="utf-8") as f:
        print(f"{name[:-3]} = ", end="", file=f)
        pretty_print_dict(animation, f, indent=0, ignore_first_indentation=True)

def load_animation(filename: str):
    global total_frames
    ruta = pathlib.Path(filename)
    nombre_modulo = ruta.stem  

    spec = importlib.util.spec_from_file_location(nombre_modulo, ruta)
    
    modulo = importlib.util.module_from_spec(spec)
    
    spec.loader.exec_module(modulo)
    elemento = getattr(modulo, nombre_modulo)

    frame_parameters.clear()
    total_frames = 0
    frame_bar.children.clear()
    component_values.clear()

    for frame_indx, frame in enumerate(elemento):

        add_new_frame() 
        
        frame_parameters[frame_indx].time = frame["parameters"]["time"]
        frame_parameters[frame_indx].type.display_name = frame["parameters"]["type"]
        
        for component, value in frame["components"].items():
            component_indx = component_list.index(component)
            component_values[frame_indx][component_indx].value = value
            component_values[frame_indx][component_indx].activated = True
        
    update_all_component_values()
    change_selected_frame(0)
    

    