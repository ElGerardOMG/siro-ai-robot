
import importlib.util
import pathlib
import os
import re
import inspect
import sys

from typing import Any

from prompt_toolkit import Application
from prompt_toolkit.layout.containers import VSplit, Window, HSplit
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout import HorizontalAlign
from prompt_toolkit.key_binding import KeyBindings

from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum

selected_component = -1
newSelectedComponent = -1
value_col = 0
invert_col = 0
total_components = 0

component_enums = []
component_list : list[ComponentEnum] = []
component_values = []
component_invertions = []
row_list = []

def changeSelectedComponent(newSelectedComponent : int):
    global selected_component, previous_selected_component

    previous_selected_component = selected_component
    selected_component = (newSelectedComponent + total_components) % total_components
    update_ui_selected_row()

def sumComponentValue(component: int, value : Any):
    component_values[selected_component] = component_values[selected_component] + value
    update_ui_selected_row()

def toggle_invert_direction(component: int):
    component_invertions[selected_component] = not component_invertions[selected_component]
    update_ui_selected_row()

def reset_all():
    for indx in range(total_components):
        component_values[indx] = 0
        component_invertions[indx] = False
        row_list[indx].children[invert_col].content.text = f'{"YES" if component_invertions[indx] else "NO"}'
        row_list[indx].children[value_col].content.text = f'{component_values[indx]}'
    
def update_ui_selected_row():
    global previous_selected_component, selected_component

    selectedRow : list[Window] = row_list[selected_component]
    selectedRow.style = "bg:#ffffff fg:#000000"
    
    if previous_selected_component >= 0:
        previousSelectedRow : list[Window] = row_list[previous_selected_component]
        previousSelectedRow.style = "fg:#ffffff"

    selectedRow.children[invert_col].content.text = f'{"YES" if component_invertions[selected_component] else "NO"}'
    selectedRow.children[value_col].content.text = f'{component_values[selected_component]}'


def create_ui():
    global component_list, component_values, component_invertions, row_list, value_col, invert_col, total_components

    component_list = []
    component_values = []
    component_invertions = []

    for component_enum in component_enums:
        for component in component_enum:
            component_list.append(component)
            component_values.append(0)
            component_invertions.append(False)
            total_components += 1

    property_distribution = [
        (0,4, "CHN.."),
        ("name",None, "NAME"),
        ("value",4, "VAL."),
        ("invert", 4, "INV."),
        (1,4, "MIN"),
        (2,4, "MAX"),
    ]

    headers = []
    for idx, (propertyName, width, propertyTitle) in enumerate(property_distribution):

        if propertyName == "value":
            value_col = idx
        elif propertyName == "invert":
            invert_col = idx

        textControl = FormattedTextControl(text = f'{propertyTitle}')    
        headers.append(Window(content = textControl, width= width))

    row_list = []
    for indx, component in enumerate(component_list):
        row = []
        for propertyNumber, width, _ in property_distribution:

            if propertyNumber == "name":
                text = f'{component.__class__.__name__}.{component.name}'
            elif propertyNumber == "value":
                text = component_values[indx]
            elif propertyNumber == "invert":
                text = "NO"
            else:
                text = component.value[propertyNumber]

            textControl = FormattedTextControl(text = f'{text}')
            cell = Window(content = textControl, width= width)
            row.append(cell)
        
        row_list.append(VSplit(children=row, height=1, padding=2))


    # Crear la lista de ventanas de ayuda mediante un bucle for
    help_texts = [
        '[↑ ↓: Select component]',
        '[← →: Change value by 1]',
        '[Ctrl + ← or →: Change value by 10]',
        '[Space: Invert direction]',
        '[Ctrl+S: Next Step]',
    ]

    help_windows = [
        Window(
            content=FormattedTextControl(text=text),
            height=1
        )
        for text in help_texts
    ]

    help_bar_1 = VSplit(children=help_windows[:3],align=HorizontalAlign.CENTER)
    help_bar_2 = VSplit(children=help_windows[3:],align=HorizontalAlign.CENTER)

    help_bar_1.style = "bg:#ffffff fg:#000000"
    help_bar_2.style = "bg:#ffffff fg:#000000"
    internal_container = HSplit(
            [VSplit(children=headers, height=1, padding=2)]
            +
            [Window(char="=", height=1)]
            +
            row_list
                     
        )
    
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
        help_bar_1,
        help_bar_2
    ])


    kb = KeyBindings()

    @kb.add('c-s')
    def exit_(event):
        event.app.exit()

    @kb.add('up')
    def _(event):
        changeSelectedComponent(selected_component - 1)
        
    @kb.add('down')
    def _(event):
        changeSelectedComponent(selected_component + 1)

    @kb.add('left')
    def _(event):
        sumComponentValue(selected_component, -1)
    
    @kb.add('right')
    def _(event):
        sumComponentValue(selected_component, +1)

    @kb.add('c-left')
    def _(event):
        sumComponentValue(selected_component, -10)

    @kb.add('c-right')
    def _(event):
        sumComponentValue(selected_component, +10)
    
    @kb.add('N')
    @kb.add('n')
    def _(event):
        reset_all()

    @kb.add('space')
    def _(event):
        toggle_invert_direction(selected_component)

    app = Application(key_bindings=kb, layout=Layout(external_container), full_screen=True)
    app.run() 
        
        

    
if __name__ == "__main__":
    
    component_enums = []

    while True:
        print("Please input the ComponentEnums to load ('0' when done): ")
        response = input(">")
        if response == '0':
            break
        
        try:
            path = pathlib.Path(response)
            module_name = path.stem  

            spec = importlib.util.spec_from_file_location(module_name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception:
            print("Invalid file. Please specify a valid .py file")
            continue
        # Find all classes in the module that inherit from ComponentEnum (excluding ComponentEnum itself)
        members = inspect.getmembers(module, inspect.isclass)

        if len(members) <= 0:
            print("This file doens't contain any valid ComponentEnum members")
            continue

        for name, obj in members:
            if issubclass(obj, ComponentEnum) and obj is not ComponentEnum:
                component_enums.append(obj)
                print(f'Loaded: {obj.__name__}')

    if len(component_enums) == 0:
        print("Aborting.")
        sys.exit()

    create_ui()

    component_names = []
    for component in component_list:
        component_names.append(f"{component.__class__.__name__}.{component.name}")

    print("Please input a folder where animations are located")
    folder_path = input(">")

    # Get all files in the specified folder
    if not os.path.isdir(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        sys.exit(1)

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    if not files:
        print(f"No files found in folder '{folder_path}'.")
        sys.exit(1)

    print("\nThe following animations will be dephased:")
    for idx, filename in enumerate(files, 1):
        print(f"{idx}. {filename}")

    print("\nProceed? (y/n)")
    confirm = input(">")

    if confirm.lower() != 'y':
        print("Aborting.")
        sys.exit(0)

    pattern = re.compile(
        r'^(\s*[A-Za-z_][A-Za-z0-9_.]*\.[A-Za-z0-9_.]+\s*:\s*)(\d+)(\s*,?\s*)$',
        re.MULTILINE
    )

    def replace_value(match):
        prefix, num_str, suffix = match.groups() 

        try:
            indx = component_names.index(prefix.replace(":","").strip())

            if component_invertions[indx]:
                new_val = component_values[indx] - int(num_str)
            else:
                new_val = int(num_str) - component_values[indx]

            new_val = min(max(new_val, component_list[indx].min_value), component_list[indx].max_value)

            return f"{prefix}{new_val}{suffix}"
        except ValueError:
            return f"{prefix}{num_str}{suffix}"

    for filename in files:
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r+', encoding='utf-8') as f:
            content = f.read()
            new_content = pattern.sub(replace_value, content)
            f.seek(0)
            f.write(new_content)
            f.truncate()
        print(f"Updated: {filename}")