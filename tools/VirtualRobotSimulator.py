import socket
import json
import threading
from vpython import *

# --- CONFIGURACIÓN DE RED (UDP) ---
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Permite reutilizar el puerto inmediatamente si se cierra el programa
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(False) # No bloquear el loop de animación

print(f"📡 Simulador escuchando en {UDP_IP}:{UDP_PORT}")

# --- CONFIGURACIÓN VISUAL 3D (El Esqueleto) ---
scene.title = "Simulador de Robot - Debugging de Servos"
scene.width = 800
scene.height = 600
scene.background = color.gray(0.1)
scene.camera.pos = vector(0, 0, 15)

# Materiales
mat_joint = color.orange
mat_bone = color.white

# 1. TORSO (Base estática)
torso = box(pos=vector(0, -2, 0), size=vector(4, 6, 2), color=color.blue, opacity=0.5)

# 2. CUELLO Y CABEZA
# Grupo lógico para el cuello
neck_base = cylinder(pos=vector(0, 1, 0), axis=vector(0, 1, 0), radius=0.5, color=mat_joint)
head = box(pos=vector(0, 1.5, 0), size=vector(2, 2.5, 2), color=mat_bone)
jaw = box(pos=vector(0, 0.5, 1), size=vector(1.5, 0.5, 1.5), color=color.red)

# Agrupamos cabeza y mandíbula para que roten juntas con el cuello
head_group = compound([head, jaw], origin=vector(0, 1, 0))
head_group.pos = vector(0, 2, 0) # Posición inicial sobre el cuello

# 3. BRAZOS (Jerarquía simple)
def create_arm(side_factor):
    sh_z_pivot = sphere(pos=vector(2.5 * side_factor, 0, 0), radius=0.6, color=mat_joint)
    upper_arm = cylinder(pos=vector(2.5 * side_factor,0,0), axis=vector(0, -3.5, 0), radius=0.4, color=mat_bone)
    elbow_pivot = sphere(pos=vector(2.5 * side_factor, -3.5, 0), radius=0.5, color=mat_joint)
    fore_arm = cylinder(pos=vector(2.5 * side_factor, -3.5, 0), axis=vector(0, -3, 0), radius=0.3, color=mat_bone)
    
    arm = {
        "sh_z": sh_z_pivot, "upper_arm": upper_arm,
        "elbow": elbow_pivot, "fore_arm": fore_arm, "side": side_factor
    }
    
    # NUEVO: Guardamos el "Estado Cero" exacto de los vectores
    arm["orig"] = {
        "up_pos": vector(upper_arm.pos), "up_axis": vector(upper_arm.axis), "up_up": vector(upper_arm.up),
        "elb_pos": vector(elbow_pivot.pos),
        "fore_pos": vector(fore_arm.pos), "fore_axis": vector(fore_arm.axis), "fore_up": vector(fore_arm.up)
    }
    return arm

left_arm = create_arm(1)
right_arm = create_arm(-1)

# --- ESTADO DE LOS SERVOS (Diccionario para guardar ángulos actuales) ---
# Guardamos los ángulos actuales para calcular el "delta" de rotación
# Nombre: [Valor del ángulo, Desfase, Multiplicador]
# Valor de ángulo: Valor donde se guarda el valor del ángulo actual
# Desfase: Se suma el ángulo real para ajustarlo.
# Multiplicador: Útil para cambiar la dirección de cambio, puede ser 1 o -1
current_angles = {
    "JAW": [0, 0, 1], 
    "NECK_X": [0, 0, 1],
    "NECK_Y": [0, 0, 1],
    "SHOULDER_L_X": [0, 0, 1], 
    "SHOULDER_L_Z": [0, 90, -1], 
    "ELBOW_L": [0, 0, -1],
    "SHOULDER_R_X": [0, 0, -1], 
    "SHOULDER_R_Z": [0, 90, -1],
    "ELBOW_R": [0, 0, -1]
}

# --- LÓGICA DE ACTUALIZACIÓN ---
def update_robot(data):
    global current_angles
    
    try:
        if data['angle'] is None:
            return
            
        servo = data['servo']
        offset = current_angles[servo][1]
        multiplier = current_angles[servo][2]

        # Convertir a radianes porque vpython usa radianes, pero los servos usualmente grados
        target_angle_deg = float(data['angle']) * multiplier + offset
        

        target_angle = radians(target_angle_deg)
        
        # Calcular cuánto hay que rotar desde la posición actual (Delta)
        delta = target_angle - radians(current_angles.get(servo, [0])[0] )

        #offset = current_angles[servo][1]
        #multiplier = - current_angles[servo][2]
        current_angles[servo][0] = target_angle_deg # Actualizar memoria
        


        # Aplicar rotaciones
        
        # --- CABEZA ---
        if servo == "NECK_X": # Rotación "No"
            head_group.rotate(angle=delta, axis=vector(0, 1, 0), origin=neck_base.pos)
        elif servo == "NECK_Y": # Rotación "Sí"
            head_group.rotate(angle=delta, axis=vector(1, 0, 0), origin=neck_base.pos)
        
        # --- BRAZOS (Ahora usan cinemática directa) ---
        elif "SHOULDER_L" in servo or "ELBOW_L" in servo:
            update_arm_kinematics(left_arm, "L")
            
        elif "SHOULDER_R" in servo or "ELBOW_R" in servo:
            update_arm_kinematics(right_arm, "R")

    except Exception as e:
        print(f"Error procesando: {e}")

def update_arm_kinematics(arm, side_str):
    # Paso A: Reiniciar al Estado Cero
    orig = arm["orig"]
    arm["upper_arm"].pos, arm["upper_arm"].axis, arm["upper_arm"].up = vector(orig["up_pos"]), vector(orig["up_axis"]), vector(orig["up_up"])
    arm["elbow"].pos = vector(orig["elb_pos"])
    arm["fore_arm"].pos, arm["fore_arm"].axis, arm["fore_arm"].up = vector(orig["fore_pos"]), vector(orig["fore_axis"]), vector(orig["fore_up"])
    
    # Paso B: Leer los ángulos absolutos actuales de la memoria
    ang_x = radians(current_angles[f"SHOULDER_{side_str}_X"][0])
    ang_z = radians(current_angles[f"SHOULDER_{side_str}_Z"][0])
    ang_elbow = radians(current_angles[f"ELBOW_{side_str}"][0])
    
    shoulder_pos = arm["sh_z"].pos
    
    # Paso C: Aplicar rotaciones en ORDEN ESTRICTO (1° Z, 2° X)
    for part in [arm["upper_arm"], arm["elbow"], arm["fore_arm"]]:
        part.rotate(angle=ang_x, axis=vector(0,0,1), origin=shoulder_pos) # Z (Lateral)
        
    for part in [arm["upper_arm"], arm["elbow"], arm["fore_arm"]]:
        part.rotate(angle=ang_z, axis=vector(1,0,0), origin=shoulder_pos) # X (Frontal)
        
    # Paso D: Rotar el codo
    # Como el hombro ya rotó, el eje X del codo también debe rotarse para que doble correctamente
    eje_codo = vector(1,0,0).rotate(angle=ang_x, axis=vector(0,0,1)).rotate(angle=ang_z, axis=vector(1,0,0))
    arm["fore_arm"].rotate(angle=ang_elbow, axis=eje_codo, origin=arm["elbow"].pos)

   

# --- LOOP PRINCIPAL ---
print("Presiona Ctrl+C en la terminal para cerrar correctamente.")
try:
    while True:
        rate(60) # 60 FPS
        
        try:
            # Intentar recibir datos del socket
            data, addr = sock.recvfrom(1024) 
            decoded = json.loads(data.decode())
            
            # Esperamos formato: {"servo": "NECK_X", "angle": 45}
            if isinstance(decoded, list): # Si enviamos lista de comandos
                for cmd in decoded:
                    update_robot(cmd)
            else:
                update_robot(decoded)
                
        except BlockingIOError:
            pass # No hay datos, seguimos dibujando
        except json.JSONDecodeError:
            print("Error en formato JSON")


except KeyboardInterrupt:
    print("\nCerrando simulador...")

finally:
    # Esto se ejecuta SIEMPRE, haya error o no
    sock.close()
    print("Puerto liberado. Adiós.")