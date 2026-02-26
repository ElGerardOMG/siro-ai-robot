from pdb import Restart
from typing import Any
from numpy import vsplit
from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, Window, HSplit
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout import HorizontalAlign, Margin, WindowAlign
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import get_app

from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum

# Lista de tuplas (índice de valor del enum, ancho que ocupa en pantalla)
# El valor en el tamaño None es toda la pantalla
property_distribution = [
    (0,4, "CHN.."),
    ("name",None, "NAME"),
    ("value",4, "VAL."),
    (1,4, "MIN"),
    (2,4, "MAX"),
]

value_col = 0

component_list : list[ComponentEnum] = []
component_values = []
row_list = []
total_components = 0

selected_component = -1
previous_selected_component = -1

def start(*componentEnums: type[ComponentEnum]):

    global component_list, component_values, total_components
    total_components = 0 
    
    for componentEnum in componentEnums:
        for component in componentEnum:
            component_list.append(component)
            component_values.append(component.currentValue)
            total_components += 1

    create_ui()
    
    

def changeSelectedComponent(newSelectedComponent : int):
    global selected_component, previous_selected_component

    previous_selected_component = selected_component
    selected_component = (newSelectedComponent + total_components) % total_components
    
    update_ui_selected_row()

def sumComponentValue(component: int, value : Any):
    component_list[component].currentValue = component_list[component].currentValue + value
    component_values = component_list[component].currentValue
    update_ui_selected_row()

def restartAllValues():
    for component in component_list:
        component.currentValue = component.min_value
    update_ui_all_rows()

def setNoneAllValues():
    for component in component_list:
        component.currentValue = None
    update_ui_all_rows()

def create_ui():
    global row_list, selected_component, value_col

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
        
        row_list.append(VSplit(children=row, height=1, padding=2))


    # Crear la lista de ventanas de ayuda mediante un bucle for
    help_texts = [
        '[↑ ↓: Select component]',
        '[← →: Change value by 1]',
        '[Ctrl + ← or →: Change value by 10]',
        '[Ctrl+Q: Quit]',
        '[N: Set all None]',
        '[M: Set all minimum values]',
    ]

    help_windows = [
        Window(
            content=FormattedTextControl(text=text, style="bg:#ffffff fg:#000000"),
            height=1
        )
        for text in help_texts
    ]

    help_bar_1 = VSplit(children=help_windows[:3],align=HorizontalAlign.CENTER)
    help_bar_2 = VSplit(children=help_windows[3:],align=HorizontalAlign.CENTER)

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

    @kb.add('c-q')
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

    @kb.add('n')
    def _(event):
        setNoneAllValues()

    @kb.add('m')
    def _(event):
        restartAllValues()

    app = Application(key_bindings=kb, layout=Layout(external_container), full_screen=True)
    app.run() 


def update_ui_selected_row():
    global previous_selected_component, selected_component

    selectedRow : list[Window] = row_list[selected_component].get_children()
    for window in selectedRow:
        window.content.style = "bg:#ffffff fg:#000000"

    if previous_selected_component >= 0:
        previousSelectedRow : list[Window] = row_list[previous_selected_component].get_children()
        for window in previousSelectedRow:
            window.content.style = "fg:#ffffff"
        
    selectedRow[value_col].content.text = f'{component_list[selected_component].currentValue}'

def update_ui_all_rows():
    for indx, row in enumerate(row_list):
        row.get_children()[value_col].content.text = f'{component_list[indx].currentValue}'

    update_ui_selected_row()

"""

kb = KeyBindings()

#buffer1 = Buffer()  # Editable buffer.

totalElements = 10

element_list = []
element_table = []
for i in range(totalElements):
    #element_table.append([])
    #element_table[i]["CHANNEL"] = 

    element_list.append(VSplit(children= [
        Window(content=FormattedTextControl(text=f'{i*2}'), width=2),
        Window(content=FormattedTextControl(text=f'Display {i*500}'),),
        Window(content=FormattedTextControl(text=f'300'), width=4),
        Window(content=FormattedTextControl(text=f'400'), width=4),
        Window(content=FormattedTextControl(text=f'500'), width=4),
    ], height=1, padding=2,
        
    ))
        
        
        

    
    


root_container = HSplit(element_list)

currentFocus = 0

def changeFocus(value):
    global currentFocus
    something : Window = root_container.get_children()[currentFocus]
    text : FormattedTextControl = something.content
    text.style = "fg:#ffffff"
    
    currentFocus = (currentFocus + value + totalElements) % totalElements
    get_app().layout.focus(root_container.get_children()[currentFocus])
    something : Window = root_container.get_children()[currentFocus]
    text : FormattedTextControl = something.content
    text.style = "bg:#ffffff fg:#000000"
    
layout = Layout(root_container)

root_container.
@kb.add('c-q')
def exit_(event):
    event.app.exit()

@kb.add('up')
def e_(event):
    changeFocus(-1)

@kb.add('down')
def d_(event):
    changeFocus(1)

@kb.add('left')
def _(event):
    global root_container
    root_container.width -= 1

@kb.add('right')
def _(event):
    global root_container
    root_container.width += 1



app = Application(key_bindings=kb, layout=layout, full_screen=True)
app.run() # You won't be able to Exit this app

"""
