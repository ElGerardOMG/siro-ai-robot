#!/usr/bin/env python3
"""
Curses-based sequence editor for movements.
Genera y edita listas de movimientos del tipo:

SampleSequence = [
    {
        "parameters": {"time": 3.1, "type": "linear"},
        "components": { ServoChannelNames.ELBOW_R: 2, ... }
    },
    ...
]

Características principales implementadas:
- Línea de tiempo horizontal (A / D para moverse entre movimientos)
- Lista vertical de componentes y su valor/estado (Up/Down para seleccionar)
- Espacio para activar/desactivar componente (excepto Time)
- Left/Right para disminuir/aumentar en 1
- Ctrl+Left / Ctrl+Right (cuando el terminal lo soporte) aumenta/disminuye en 10
- Teclas: G=Guardar (solicita nombre), O=Abrir (solicita nombre), R=Reproducir animación
  C=Copiar movimiento actual a otro index, X=Poner componentes a 0 y desactivar

Limitaciones:
- La detección de Ctrl+Arrow depende del terminal y puede no funcionar en todos los entornos.
  He añadido detección para varias secuencias de teclas comunes y una alternativa con '>' y '<'
  para cambio por 10 en caso de que su terminal no envíe códigos distintos para Ctrl+Arrow.

"""
from __future__ import annotations
import curses
import curses.ascii
import json
import os
import re
from enum import Enum
from typing import Any, Dict, List, Tuple


from src.ia_talking_robot.sequencer.DefaultMoveSequencer import DefaultMoveSequencer
from src.ia_talking_robot.controllers.MockController import MockController

# AQUÍ PONER LA RUTA DEL COMPONENT NAME DEFINITION
from src.ia_talking_robot.sequencer.SampleComponentDefinition import *

# INICIALIZACIÓN DE LOS COMPONENTES, SE UTILIZA UN IMPORT DENTRO DE UN TRY PARA PODER
# UTILIZAR ESTA HERRAMIENTAe EN OTRO SISTEMA DIFERENTE A LA RASPBERRY PI

try:
    from src.ia_talking_robot.controllers.LedController import LedController
    ledController = LedController(3)
except Exception:
    ledController = MockController(3, "Led")
  
try:
    from src.ia_talking_robot.controllers.AdafruitServoController import AdafruitServoController
    servoController = AdafruitServoController(16)
except Exception:
    servoController = MockController(16, "Servo")
  
sequencer = DefaultMoveSequencer(
    {
        (servoController, Servos),
        (ledController, Leds)
    }
)

# Constants
MIN_VAL = 0
MAX_VAL = 255
DEFAULT_TYPE = "linear"

# Helper: pretty name for component: "ServoChannelNames.ELBOW_R"
def comp_display_name(member: Enum) -> str:
    return f"{member.__class__.__name__}.{member.name}"

# Build full component master list
ALL_COMPONENTS: List[Enum] = []
ALL_COMPONENTS.extend(list(Servos))
ALL_COMPONENTS.extend(list(Leds))

# Convert from display name to enum member
def name_to_member(name: str) -> Enum:
    # expect form "ServoChannelNames.ELBOW_R"
    cls_name, member_name = name.split('.', 1)
    if cls_name == 'ServoChannelNames':
        return getattr(Servos, member_name)
    elif cls_name == 'LedChannelNames':
        return getattr(Leds, member_name)
    else:
        raise KeyError(name)


class SequenceEditor:
    def __init__(self):
        self.sequence: List[Dict[str, Any]] = []
        if not self.sequence:
            self.sequence = [
                {"parameters": {"time": 3.1, "type": DEFAULT_TYPE}, "components": {}},
            ]
        self.current_idx = 0
        self.comp_cursor = 0
        self.stdscr = None

    def _setComponentValue(self, component: Enum, value: int):
        # Falta implementar
        pass

    def ensure_movement_exists(self, idx: int):
        while idx >= len(self.sequence):
            self.sequence.append({"parameters": {"time": 1.0, "type": DEFAULT_TYPE}, "components": {}})

    def get_component_value(self, movement: Dict[str, Any], comp: Enum) -> int:
        return int(movement.get('components', {}).get(comp, 0))

    def is_component_active(self, movement: Dict[str, Any], comp: Enum) -> bool:
        return comp in movement.get('components', {})

    def set_component_value_for_movement(self, movement: Dict[str, Any], comp: Enum, value: int, active: bool=True):
        #value = max(MIN_VAL, min(MAX_VAL, int(value)))
        value = max(comp.MIN(), min(comp.MAX(), int(value)))
        comps = movement.setdefault('components', {})
        if active:
            comps[comp] = value
        else:
            if comp in comps:
                del comps[comp]
        try:
            self._setComponentValue(comp, value)
        except Exception:
            pass

    def toggle_component_active(self, movement: Dict[str, Any], comp: Enum):
        if self.is_component_active(movement, comp):
            self.set_component_value_for_movement(movement, comp, 0, active=False)
        else:
            self.set_component_value_for_movement(movement, comp, self.get_component_value(movement, comp), active=True)

    def save_to_file(self, filename: str):
        if not filename.endswith('.py'):
            filename = filename + '.py'
        varname = os.path.splitext(os.path.basename(filename))[0]
        header = 'from ....src.ia_talking_robot.sequencer.ComponentNameDefinition import *\n\n'
        body_lines = [f"{varname} = ["]
        for movement in self.sequence:
            params = movement.get('parameters', {})
            time_val = params.get('time', 1)
            body_lines.append('    {')
            body_lines.append('        "parameters":{')
            body_lines.append(f'            "time" : {repr(time_val)},')
            body_lines.append(f'            "type" : "{DEFAULT_TYPE}"')
            body_lines.append('        },')
            comps = movement.get('components', {})
            if comps:
                body_lines.append('        "components":{')
                for comp, val in comps.items():
                    name = comp_display_name(comp)
                    body_lines.append(f'            {name} : {int(val)},')
                body_lines.append('        }')
            else:
                body_lines.append('        "components":{}')
            body_lines.append('    },')
        body_lines.append(']')

        content = header + '\n'.join(body_lines) + '\n'
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, f"Saved to {filename}"
        except Exception as e:
            return False, str(e)

    def load_from_file(self, filename: str):
        if not filename.endswith('.py'):
            filename = filename + '.py'
        if not os.path.exists(filename):
            return False, f"File not found: {filename}"
        source = open(filename, 'r', encoding='utf-8').read()
        ns = {
            'ServoChannelNames': Servos,
            'LedChannelNames': Leds,
            "__name__": "__main__",
        }
        try:
            exec(source, ns)
        except Exception as e:
            return False, f"Error executing file: {e}"
        candidate = None
        for k, v in ns.items():
            if k.startswith('__'):
                continue
            if isinstance(v, list) and v:
                ok = True
                for item in v:
                    if not isinstance(item, dict) or 'parameters' not in item or 'components' not in item:
                        ok = False
                        break
                if ok:
                    candidate = v
                    break
        if candidate is None:
            return False, 'No suitable sequence variable found in file.'
        seq = []
        for item in candidate:
            params = item.get('parameters', {}).copy()
            comps_raw = item.get('components', {})
            comps: Dict[Enum, int] = {}
            for k, val in comps_raw.items():
                if isinstance(k, str):
                    try:
                        member = name_to_member(k)
                    except Exception:
                        continue
                    comps[member] = int(val)
                else:
                    comps[k] = int(val)
            seq.append({"parameters": params, "components": comps})
        self.sequence = seq
        self.current_idx = 0
        self.comp_cursor = 0
        return True, f"Loaded {filename}"

    def copy_current_to(self, target_idx: int):
        if target_idx < 0:
            return False, "Invalid target index"
        self.ensure_movement_exists(target_idx)
        src = self.sequence[self.current_idx]
        dst = self.sequence[target_idx]
        dst['parameters'] = {k: v for k, v in src.get('parameters', {}).items()}
        dst['components'] = {k: int(v) for k, v in src.get('components', {}).items()}
        return True, f"Copied movement {self.current_idx} -> {target_idx}"

    def zero_and_disable_current(self):
        cur = self.sequence[self.current_idx]
        cur['components'] = {}
        return True, "Current movement components zeroed and disabled"

    def draw(self, stdscr):
        self.stdscr = stdscr
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        top_h = 3
        bottom_h = 4
        mid_h = max(5, h - top_h - bottom_h)

        timeline_win = stdscr.subwin(top_h, w, 0, 0)
        self.draw_timeline(timeline_win, 0, 0, top_h, w)

        comp_win = stdscr.subwin(mid_h, w, top_h, 0)
        self.draw_components(comp_win, 0, 0, mid_h, w)

        help_win = stdscr.subwin(bottom_h, w, top_h + mid_h, 0)
        self.draw_help(help_win, 0, 0, bottom_h, w)

        stdscr.refresh()

    def draw_timeline(self, win, y, x, h, w):
        win.erase()
        win.box()
        win.addstr(0, 2, ' Timeline ')
        pad = 2
        line = ''
        for i in range(len(self.sequence)):
            token = f"[{i}]"
            if i == self.current_idx:
                token = f">{token}<"
            line += token + ' ' * pad
        if len(line) > w - 4:
            line = line[:w - 7] + '...'
        try:
            win.addstr(1, 2, line)
        except curses.error:
            pass
        win.noutrefresh()

    def draw_components(self, win, y, x, h, w):
        win.erase()
        win.box()
        win.addstr(0, 2, ' Components (Time at top, not toggleable) ')
        cur = self.sequence[self.current_idx]
        entries: List[Tuple[str, Any, bool, int]] = []
        tval = cur.get('parameters', {}).get('time', 1.0)
        entries.append(('Time', tval, True, None))
        for comp in ALL_COMPONENTS:
            name = comp_display_name(comp)
            active = self.is_component_active(cur, comp)
            val = self.get_component_value(cur, comp)
            channel = comp.value()
            entries.append((name, val, active, channel))

        name_w = min(max(len(e[0]) for e in entries) + 2, int(w * 0.4))
        val_w = 6
        state_w = 8

        start_line = 1
        visible = h - 2
        top_idx = max(0, self.comp_cursor - visible + 1) if self.comp_cursor >= visible else 0
        for i in range(top_idx, min(len(entries), top_idx + visible)):
            disp, val, active, channel = entries[i]
            line_idx = start_line + (i - top_idx)
            highlight = (i == self.comp_cursor)
            name_col = disp.ljust(name_w)[:name_w]
            val_col = str(val).rjust(val_w)
            state_col = ('ON' if active else 'OFF').rjust(state_w)
            if i == 0:
                prefix = ' *  '
            else:
                prefix = ('{: ^4}'.format(channel))
            text = f"{prefix}{name_col} {val_col} {state_col}"
            try:
                if highlight:
                    win.addstr(line_idx, 1, text[:w - 2], curses.A_REVERSE)
                else:
                    attr = curses.A_NORMAL
                    if not active and i != 0:
                        attr |= curses.A_DIM
                    win.addstr(line_idx, 1, text[:w - 2], attr)
            except curses.error:
                pass
        win.noutrefresh()

    def draw_help(self, win, y, x, h, w):
        win.erase()
        win.box()
        win.addstr(0, 2, ' Controls ')
        lines = [
            "A/D: Move timeline left/right   Up/Down: Select component",
            "Left/Right: -/+1   Ctrl+Left/Right or </>: -/+10   Space: toggle component",
            "G: Guardar  O: Abrir  R: Reproducir Animación C: Copiar movimiento  X: Zero+Disable",
            "Q: Salir"
        ]
        for i, l in enumerate(lines):
            try:
                win.addstr(1 + i, 2, l[:w - 4])
            except curses.error:
                pass
        win.noutrefresh()

    def prompt(self, prompt_text: str) -> str:
        h, w = self.stdscr.getmaxyx()
        pw = max(40, len(prompt_text) + 20)
        ph = 3
        sy = (h - ph) // 2
        sx = max(0, (w - pw) // 2)
        win = curses.newwin(ph, pw, sy, sx)
        win.box()
        try:
            win.addstr(1, 2, prompt_text)
        except curses.error:
            pass
        curses.echo()
        curses.curs_set(1)
        win.refresh()
        win.move(1, 2 + len(prompt_text) + 1)
        s = win.getstr(1, 2 + len(prompt_text) + 1, 60)
        try:
            text = s.decode('utf-8') if isinstance(s, bytes) else str(s)
        except Exception:
            text = str(s)
        curses.noecho()
        curses.curs_set(0)
        return text.strip()

    def run(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        stdscr.nodelay(False)
        stdscr.keypad(True)

        while True:
            self.draw(stdscr)
            key = stdscr.getch()
            if key in (ord('q'), ord('Q')):
                break
            if key in (ord('a'), ord('A')):
                self.current_idx = max(0, self.current_idx - 1)
                self.comp_cursor = min(self.comp_cursor, len(ALL_COMPONENTS))
                continue
            if key in (ord('d'), ord('D')):
                self.current_idx = min(len(self.sequence) - 1, self.current_idx + 1)
                continue
            if key == curses.KEY_UP:
                self.comp_cursor = max(0, self.comp_cursor - 1)
                continue
            if key == curses.KEY_DOWN:
                self.comp_cursor = min(1 + len(ALL_COMPONENTS) - 1, self.comp_cursor + 1)
                continue
            if key == ord(' '):
                cur = self.sequence[self.current_idx]
                if self.comp_cursor == 0:
                    continue
                comp = ALL_COMPONENTS[self.comp_cursor - 1]
                self.toggle_component_active(cur, comp)
                continue
            step = 0
            if key in (curses.KEY_LEFT, curses.KEY_RIGHT):
                step = -1 if key == curses.KEY_LEFT else 1
            elif key in (curses.KEY_SLEFT, curses.KEY_SRIGHT):
                step = -10 if key == curses.KEY_SLEFT else 10
            elif key in (545, 560, 393, 402):
                step = -10 if key in (545, 393) else 10
            elif key in (ord('<'), ord(',')):
                step = -10
            elif key in (ord('>'), ord('.')):
                step = 10

            if step != 0:
                if self.comp_cursor == 0:
                    cur = self.sequence[self.current_idx]
                    val = float(cur.get('parameters', {}).get('time', 1.0))
                    val += step * 0.1
                    if val < 0:
                        val = 0
                    val = round(val, 1)
                    cur['parameters']['time'] = val
                else:
                    cur = self.sequence[self.current_idx]
                    comp = ALL_COMPONENTS[self.comp_cursor - 1]
                    active = self.is_component_active(cur, comp)
                    if not active:
                        active = True
                    old = self.get_component_value(cur, comp)
                    new = old + step
                    new = max(MIN_VAL, min(MAX_VAL, new))
                    self.set_component_value_for_movement(cur, comp, new, active=active)
                continue

            if key in (ord('g'), ord('G')):
                fname = self.prompt('Guardar como (nombre o ruta .py):')
                if fname:
                    ok, msg = self.save_to_file(fname)
                    self.show_message(msg)
                continue
            if key in (ord('o'), ord('O')):
                fname = self.prompt('Abrir archivo (ruta .py):')
                if fname:
                    ok, msg = self.load_from_file(fname)
                    self.show_message(msg)
                continue
            if key in (ord('r'), ord('R')):
                self.on_R()
                continue
            if key in (ord('c'), ord('C')):
                s = self.prompt('Copiar a (índice destino, 0-based):')
                try:
                    ti = int(s)
                    ok, msg = self.copy_current_to(ti)
                except Exception:
                    ok, msg = False, 'Índice inválido'
                self.show_message(msg)
                continue
            if key in (ord('x'), ord('X')):
                ok, msg = self.zero_and_disable_current()
                self.show_message(msg)
                continue

    def show_message(self, text: str, timeout: float = 1.5):
        # transient message at bottom
        h, w = self.stdscr.getmaxyx()
        y = h - 2
        try:
            self.stdscr.addstr(y, 2, (' ' * (w - 4)))
            self.stdscr.addstr(y, 2, text[:w - 4])
            self.stdscr.refresh()
            curses.napms(int(timeout * 1000))
        except curses.error:
            pass

    def on_R(self):
        # Placeholder for user's R action
        self.show_message('Reproduciendo animación')
        sequencer.executeSequence(self.sequence);
        


def main():
    editor = SequenceEditor()
    curses.wrapper(editor.run)

if __name__ == '__main__':
    main()
