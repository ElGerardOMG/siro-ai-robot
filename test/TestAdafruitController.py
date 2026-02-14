from ..ia_talking_robot.controllers.AdafruitServoController import AdafruitServoController
from ..ia_talking_robot.controllers.AComponentController import AComponentController
from ..ia_talking_robot.sequencer.SampleComponentDefinition import *

import curses

def main(stdscr):
    # Desactivar el cursor
    curses.curs_set(0)
    stdscr.nodelay(0)
    stdscr.keypad(True)

    controlador = AdafruitServoController()

    # Obtener la lista de nombres de los motores definidos en ComponentNameDefinition
    motores = [ServoChannelNames.JAW, ServoChannelNames.NECK_X, ServoChannelNames.NECK_Y, ServoChannelNames.SHOULDER_L_X, ServoChannelNames.SHOULDER_L_Z, ServoChannelNames.SHOULDER_R_X, ServoChannelNames.SHOULDER_R_Z, ServoChannelNames.ELBOW_L, ServoChannelNames.ELBOW_R]
    valores = {motor: 90 for motor in motores}  # Valor inicial, por ejemplo 90 grados
    seleccionado = 0
    VALOR_DEFAULT = 90

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Control de Servomotores (↑↓ seleccionar, ←→ mover, Espacio=None/Default, N=None todos, Q=Salir)")
        for idx, motor in enumerate(motores):
            nombre_motor = ServoChannelNames(motor).name  # Obtener el nombre del enum
            if idx == seleccionado:
                stdscr.attron(curses.A_REVERSE)
            val = valores[motor]
            stdscr.addstr(idx + 2, 2, f"{nombre_motor} ({motor}): {val}")
            if idx == seleccionado:
                stdscr.attroff(curses.A_REVERSE)
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP:
            seleccionado = (seleccionado - 1) % len(motores)
        elif key == curses.KEY_DOWN:
            seleccionado = (seleccionado + 1) % len(motores)
        elif key == curses.KEY_LEFT:
            if valores[motores[seleccionado]] is not None:
                valores[motores[seleccionado]] = max(0, valores[motores[seleccionado]] - 5)
                controlador.setComponentValue(motores[seleccionado], valores[motores[seleccionado]])
        elif key == curses.KEY_RIGHT:
            if valores[motores[seleccionado]] is not None:
                valores[motores[seleccionado]] = min(180, valores[motores[seleccionado]] + 5)
                controlador.setComponentValue(motores[seleccionado], valores[motores[seleccionado]])
        elif key == ord(' '):
            motor_actual = motores[seleccionado]
            if valores[motor_actual] is None:
                valores[motor_actual] = VALOR_DEFAULT
                controlador.setComponentValue(motor_actual, VALOR_DEFAULT)
            else:
                valores[motor_actual] = None
                controlador.setComponentValue(motor_actual, None)
        elif key in (ord('n'), ord('N')):
            for motor in motores:
                valores[motor] = None
                controlador.setComponentValue(motor, None)
        elif key in (ord('q'), ord('Q')):
            for motor in motores:
                valores[motor] = None
                controlador.setComponentValue(motor, None)
            break

if __name__ == "__main__":
    curses.wrapper(main)
