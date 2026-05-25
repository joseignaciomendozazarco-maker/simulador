{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import turtle\
import random\
import math\
\
def ejecutar_simulacion():\
    print("\\n" + "="*50)\
    print("   SIMULADOR DE EXPEDICI\'d3N BIDIMENSIONAL: MARTE")\
    print("="*50)\
    print("Este programa simula el avance de un veh\'edculo en un mapa de -100 a 100.")\
    print("Deber\'e1s configurar los par\'e1metros iniciales para comenzar.")\
    print("-"*50)\
\
    # --- 1. PAR\'c1METROS INICIALES Y VALIDACI\'d3N DE DATOS ---\
    nombre = input("Introduce el nombre de tu Rover: ").strip()\
    if not nombre:\
        nombre = "Curiosity-X"\
\
    # Validaci\'f3n de posici\'f3n X\
    while True:\
        try:\
            pos_x = float(input("Posici\'f3n inicial X (-100 a 100): "))\
            if -100 <= pos_x <= 100:\
                break\
            print("Error: La coordenada debe estar entre -100 y 100.")\
        except ValueError:\
            print("Entrada inv\'e1lida. Introduzca un n\'famero.")\
\
    # Validaci\'f3n de posici\'f3n Y\
    while True:\
        try:\
            pos_y = float(input("Posici\'f3n inicial Y (-100 a 100): "))\
            if -100 <= pos_y <= 100:\
                break\
            print("Error: La coordenada debe estar entre -100 y 100.")\
        except ValueError:\
            print("Entrada inv\'e1lida. Introduzca un n\'famero.")\
\
    # Validaci\'f3n de \'c1ngulo\
    while True:\
        try:\
            angulo_inicial = float(input("\'c1ngulo inicial de direcci\'f3n (0 a 359 grados): "))\
            angulo = angulo_inicial % 360\
            break\
        except ValueError:\
            print("Entrada inv\'e1lida. Usando \'e1ngulo por defecto: 0\'b0")\
            angulo = 0.0\
            angulo_inicial = 0.0\
            break\
\
    # Validaci\'f3n de Recurso (Energ\'eda)\
    while True:\
        try:\
            energia = float(input("Cantidad inicial de Energ\'eda/Combustible (Recomendado: 100): "))\
            if energia > 0:\
                break\
            print("Error: La energ\'eda debe ser mayor que 0.")\
        except ValueError:\
            print("Entrada inv\'e1lida. Usando valor por defecto: 100")\
            energia = 100.0\
            break\
\
    # Definici\'f3n de Elementos del Mundo (3 tipos fijos en coordenadas espec\'edficas)\
    elementos_mundo = [\
        ("Estaci\'f3n de Recarga Solar", "bono", 30.0, 40.0, 20.0),\
        ("Zona de Grietas Rocosas", "obstaculo", -40.0, -20.0, 25.0),\
        ("Muestras Biol\'f3gicas (Meta Principal)", "meta", 50.0, -50.0, 15.0)\
    ]\
\
    # Guardar par\'e1metros iniciales para el reporte final\
    param_iniciales = \{\
        "nombre": nombre,\
        "x": pos_x,\
        "y": pos_y,\
        "angulo": angulo,\
        "energia": energia\
    \}\
\
    # --- 2. CONFIGURACI\'d3N DE VISUALIZACI\'d3N EN TURTLE ---\
    screen = turtle.Screen()\
    screen.setup(600, 600)\
    screen.title(f"Ruta de Expedici\'f3n: \{nombre\}")\
    screen.setworldcoordinates(-150, -150, 150, 150)\
    screen.clearscreen() # Limpia la pantalla en caso de reinicio\
\
    # Dibujado de l\'edmites del mundo\
    pintor = turtle.Turtle()\
    pintor.hideturtle()\
    pintor.speed(0)\
    pintor.penup()\
    pintor.color("red")\
    pintor.goto(-100, -100)\
    pintor.pendown()\
    for _ in range(4):\
        pintor.forward(200)\
        pintor.left(90)\
    \
    # Dibujar los elementos del mundo en la ventana de Turtle como referencia\
    for nom, tipo, ex, ey, rad in elementos_mundo:\
        pintor.penup()\
        pintor.goto(ex, ey - 5)\
        pintor.pendown()\
        if tipo == "bono": pintor.color("green")\
        elif tipo == "obstaculo": pintor.color("orange")\
        else: pintor.color("blue")\
        pintor.circle(5)\
        \
    # Inicializar el objeto rover en Turtle\
    rover = turtle.Turtle()\
    rover.shape("triangle")\
    rover.color("black")\
    rover.penup()\
    rover.goto(pos_x, pos_y)\
    rover.setheading(angulo)\
    rover.pendown()\
\
    # --- 3. MODO DE TEXTO Y DESARROLLO DE LA SIMULACI\'d3N (EL BUCLE) ---\
    print("\\n" + "="*50)\
    print("INICIO DE LA EXPEDICI\'d3N")\
    print("="*50)\
    print(f"Veh\'edculo: \{nombre\}")\
    print(f"Posici\'f3n Inicial: (\{pos_x\}, \{pos_y\})")\
    print(f"Direcci\'f3n Inicial: \{angulo\}\'b0")\
    print(f"Energ\'eda Inicial: \{energia\} unidades")\
    print(f"L\'edmites del mundo: Ejes X e Y de -100 a 100")\
    print(f"Condiciones de parada: Quedarse sin energ\'eda, salir del mapa o alcanzar la meta.")\
    print("="*50)\
    input("Presiona ENTER para iniciar la simulaci\'f3n por turnos...")\
\
    pasos = 0\
    causa_finalizacion = ""\
    meta_alcanzada = False\
    elementos_visitados = []\
\
    # Bucle principal de pasos sucesivos\
    while energia > 0:\
        pasos += 1\
        print(f"\\n>>> PASO N\'b0 \{pasos\} <<<")\
        \
        # Guardar estados anteriores para el reporte paso a paso\
        x_ant, y_ant = pos_x, pos_y\
        energia_ant = energia\
        \
        # Simulaci\'f3n de movimiento base\
        distancia_avance = 15.0\
        gasto_bateria = 10.0\
        energia -= gasto_bateria\
        print(f"[Acci\'f3n]: El motor avanza \{distancia_avance\} unidades en direcci\'f3n \{angulo:.1f\}\'b0.")\
\
        # Trigonometr\'eda para actualizar coordenadas\
        angulo_en_radianes = math.radians(angulo)\
        pos_x += distancia_avance * math.cos(angulo_en_radianes)\
        pos_y += distancia_avance * math.sin(angulo_en_radianes)\
        \
        # Actualizar posici\'f3n gr\'e1fica\
        rover.goto(pos_x, pos_y)\
        \
        # Control de l\'edmites del mundo\
        if pos_x > 100 or pos_x < -100 or pos_y > 100 or pos_y < -100:\
            causa_finalizacion = "El veh\'edculo sali\'f3 del \'e1rea permitida del mapa (-100 a 100)."\
            print(f"[Aviso]: \'a1L\'edmites alcanzados fuera de rango!")\
            break\
\
        # Evaluaci\'f3n de elementos del mundo\
        for nombre_objeto, tipo_objeto, obj_x, obj_y, radio_deteccion in elementos_mundo:\
            distancia_al_objeto = math.sqrt((pos_x - obj_x)**2 + (pos_y - obj_y)**2)\
            if distancia_al_objeto <= radio_deteccion:\
                if nombre_objeto not in elementos_visitados:\
                    elementos_visitados.append(nombre_objeto)\
                \
                if tipo_objeto == "bono":\
                    energia += 30.0\
                    print(f"[Mundo]: Entrando en zona '\{nombre_objeto\}'. \'a1Paneles solares desplegados! (+30 energ\'eda)")\
                elif tipo_objeto == "obstaculo":\
                    energia -= 20.0\
                    print(f"[Mundo]: \'a1Alerta! Terreno inestable en '\{nombre_objeto\}'. Consumo cr\'edtico (-20 energ\'eda)")\
                elif tipo_objeto == "meta":\
                    meta_alcanzada = True\
                    causa_finalizacion = "\'a1\'c9xito absoluto! Se ha alcanzado el objetivo principal de la misi\'f3n."\
                    print(f"[Mundo]: \'a1OBJETIVO LOCALIZADO! Has llegado con \'e9xito a: '\{nombre_objeto\}'.")\
                    break\
        \
        if meta_alcanzada:\
            break\
\
        # Sistema de eventos aleatorios din\'e1micos\
        if random.random() < 0.20:\
            evento_escogido = random.choice(["tormenta_arena", "rafaga_viento"])\
            if evento_escogido == "tormenta_arena":\
                energia -= 15.0\
                print("[Evento Aleatorio]: Tormenta de polvo ionizado. Los sistemas sufren da\'f1os (-15 energ\'eda).")\
            elif evento_escogido == "rafaga_viento":\
                angulo = (angulo + 90) % 360\
                rover.setheading(angulo)\
                print("[Evento Aleatorio]: Fuerte viento de costado. El rumbo del Rover ha sido desviado 90\'b0.")\
\
        # Informe detallado paso a paso por terminal\
        print(f" -> Trayectoria: Coordenadas (\{x_ant:.1f\}, \{y_ant:.1f\}) ===> Coordenadas (\{pos_x:.1f\}, \{pos_y:.1f\})")\
        print(f" -> Telemetr\'eda de Energ\'eda: \{energia_ant:.1f\} u. ===> \{energia:.1f\} u.")\
        print("[Explicaci\'f3n]: P\'e9rdida originada por el consumo de tracci\'f3n y el desplazamiento sobre el terreno.")\
        \
        # Variaci\'f3n autom\'e1tica del rumbo para el siguiente turno\
        angulo = (angulo + random.randint(-35, 35)) % 360\
        rover.setheading(angulo)\
\
    # Evaluaci\'f3n de cierre por falta de recursos\
    if energia <= 0 and not causa_finalizacion:\
        causa_finalizacion = "El sistema motriz se ha apagado. El Rover se qued\'f3 sin reservas de energ\'eda."\
\
    # --- 4. CONDICIONES DE FINALIZACI\'d3N E INFORME FINAL ---\
    resultado_final = "\'c9XITO TOTAL" if meta_alcanzada else "FRACASO DE LA MISI\'d3N"\
    if not meta_alcanzada and len(elementos_visitados) > 0:\
        resultado_final = "\'c9XITO PARCIAL (Exploraci\'f3n registrada)"\
\
    print("\\n" + "="*50)\
    print("               INFORME FINAL DE RESUMEN")\
    print("="*50)\
    print(f"\'95 Nombre del Objeto:           \{param_iniciales['nombre']\}")\
    print(f"\'95 Configuraci\'f3n Inicial:       X=\{param_iniciales['x']\}, Y=\{param_iniciales['y']\}, Direcci\'f3n=\{param_iniciales['angulo']\}\'b0, Energ\'eda=\{param_iniciales['energia']\} u.")\
    print(f"\'95 Posici\'f3n Final Alcanzada:    (\{pos_x:.2f\}, \{pos_y:.2f\})")\
    print(f"\'95 N\'famero de Pasos Totales:     \{pasos\}")\
    print(f"\'95 Recursos Restantes:          \{max(0.0, energia):.2f\} unidades de energ\'eda")\
    print(f"\'95 Sitios de inter\'e9s visitados: \{', '.join(elementos_visitados) if elementos_visitados else 'Ninguno'\}")\
    print(f"\'95 Causa del Cierre:            \{causa_finalizacion\}")\
    print(f"\'95 RESULTADO GLOBAL:            \{resultado_final\}")\
    print("="*50)\
\
# --- 5. BUCLE DE REINICIO ---\
if __name__ == "__main__":\
    while True:\
        ejecutar_simulacion()\
        reiniciar = input("\\n\'bfDeseas iniciar una nueva expedici\'f3n con otros par\'e1metros? (s/n): ").strip().lower()\
        if reiniciar != 's':\
            print("\\nCerrando simulador de expedici\'f3n. \'a1Gracias por usar el programa!")\
            turtle.bye()\
            break}