import hashlib
import random
import os

# Colores para la terminal de Termux
VERDE = '\033[92m'
CIAN = '\033[96m'
ROJO = '\033[91m'
AMARILLO = '\033[93m'
RESET = '\033[0m'

XLAT1_BASE = "+b(29e*j1VMEKLyC})8&m#~W>qxdRp0wkrUo[D7,XTcA\"lI.v%{gJh4G\\-=O@5`_3i<?Z';FNQuY]szf$!BS/|t:Pn6^Ha"

def inicializar_motor_secreto(password):
    hash_bytes = hashlib.sha256(password.encode('utf-8')).digest()
    semilla = int.from_bytes(hash_bytes, 'big')
    rng = random.Random(semilla)

    lista_xlat = list(XLAT1_BASE)
    rng.shuffle(lista_xlat)
    xlat1_mutada = "".join(lista_xlat)

    tabla_t = []
    for _ in range(3):
        fila = [0, 1, 2]
        rng.shuffle(fila)
        tabla_t.append(fila)

    return xlat1_mutada, tabla_t

def crazy(a, d, tabla_t):
    res = 0
    p = 1
    for _ in range(10):
        res += tabla_t[d % 3][a % 3] * p
        a //= 3
        d //= 3
        p *= 3
    return res

def rot(x):
    return (x // 3) + (x % 3) * 19683

def encriptar_a_malbolge(mensaje, password):
    xlat1_secreta, tabla_t_secreta = inicializar_motor_secreto(password)
    a, c, d = 0, 0, 0
    memoria = [0] * 59049
    codigo_chars = []

    for idx in range(100):
        memoria[idx] = (idx * 73 + 33) % 94 + 33

    def agregar_instruccion(inst_objetivo):
        nonlocal a, c, d
        for ascii_code in range(33, 127):
            if (ascii_code + c) % 94 == inst_objetivo:
                codigo_chars.append(chr(ascii_code))
                memoria[c] = ascii_code
                if inst_objetivo == 40:
                    d = memoria[d]
                elif inst_objetivo == 39:
                    memoria[d] = rot(memoria[d])
                    a = memoria[d]
                elif inst_objetivo == 62:
                    memoria[d] = crazy(a, memoria[d], tabla_t_secreta)
                    a = memoria[d]
                memoria[c] = ord(xlat1_secreta[memoria[c] - 33])
                c = (c + 1) % 59049
                d = (d + 1) % 59049
                return True
        return False

    for char in mensaje:
        target = ord(char)
        cola = [(a, c, d, {}, [])]
        visitados = set()
        camino_encontrado = None

        while cola:
            curr_a, curr_c, curr_d, mem_diff, pasos = cola.pop(0)
            if curr_a % 256 == target and len(pasos) > 0:
                camino_encontrado = pasos
                break
            if len(pasos) >= 5:
                continue
            
            estado = (curr_a % 256, curr_c % 94, curr_d % 94)
            if estado in visitados:
                continue
            visitados.add(estado)

            for inst in:
                for ascii_code in range(33, 127):
                    if (ascii_code + curr_c) % 94 == inst:
                        nueva_mem = mem_diff.copy()
                        nueva_mem[curr_c] = ascii_code
                        val_d = nueva_mem.get(curr_d, memoria[curr_d])
                        next_a = curr_a
                        if inst == 39:
                            val_rot = rot(val_d)
                            nueva_mem[curr_d] = val_rot
                            next_a = val_rot
                        elif inst == 62:
                            val_crz = crazy(curr_a, val_d, tabla_t_secreta)
                            nueva_mem[curr_d] = val_crz
                            next_a = val_crz
                        cola.append((next_a, curr_c + 1, curr_d + 1, nueva_mem, pasos + [inst]))
                        break

        if camino_encontrado:
            for paso in camino_encontrado:
                agregar_instruccion(paso)
            agregar_instruccion(5)
        else:
            print(f"{AMARILLO}[!] Caracter omitido por limite de ruta: '{char}'{RESET}")

    agregar_instruccion(81)
    return "".join(codigo_chars)

def desencriptar_malbolge(codigo, password):
    xlat1_secreta, tabla_t_secreta = inicializar_motor_secreto(password)
    memoria = [0] * 59049
    for idx in range(100):
        memoria[idx] = (idx * 73 + 33) % 94 + 33

    i = 0
    for char in codigo:
        if 33 <= ord(char) <= 126:
            memoria[i] = ord(char)
            i += 1
            
    while i < 59049:
        memoria[i] = crazy(memoria[i - 1], memoria[i - 2], tabla_t_secreta)
        i += 1

    a, c, d = 0, 0, 0
    salida = []
    pasos = 0

    while pasos < 100000:
        if not (33 <= memoria[c] <= 126):
            break
        instruccion = (memoria[c] + c) % 94
        if instruccion == 4:
            c = memoria[d]
        elif instruccion == 5:
            salida.append(chr(a % 256))
        elif instruccion == 39:
            memoria[d] = rot(memoria[d])
            a = memoria[d]
        elif instruccion == 40:
            d = memoria[d]
        elif instruccion == 62:
            memoria[d] = crazy(a, memoria[d], tabla_t_secreta)
            a = memoria[d]
        elif instruccion == 81:
            break
        if 33 <= memoria[c] <= 126:
            memoria[c] = ord(xlat1_secreta[memoria[c] - 33])
        c = (c + 1) % 59049
        d = (d + 1) % 59049
        pasos += 1

    return "".join(salida)

def menu():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"{CIAN}========================================{RESET}")
        print(f"{VERDE}       MALBOLGE-CRYPT v1.0 (Termux)     {RESET}")
        print(f"{CIAN}========================================{RESET}")
        print("1. Encriptar mensaje a Malbolge")
        print("2. Desencriptar codigo Malbolge")
        print("3. Salir")
        opcion = input(f"\n{AMARILLO}Elige una opcion [1-3]: {RESET}")

        if opcion == '1':
            msg = input("\nEscribe el mensaje secreto: ")
            pwd = input("Crea una contraseña: ")
            print(f"\n{CIAN}[*] Generando codigo polimorfico...{RESET}")
            cifrado = encriptar_a_malbolge(msg, pwd)
            print(f"\n{VERDE}[+] Codigo Malbolge generado:{RESET}\n")
            print(cifrado)
            input(f"\n{AMARILLO}Presiona Enter para continuar...{RESET}")

        elif opcion == '2':
            cod = input("\nPega el codigo Malbolge: ")
            pwd = input("Ingresa la contraseña: ")
            print(f"\n{CIAN}[*] Ejecutando maquina virtual ternaria...{RESET}")
            descifrado = desencriptar_malbolge(cod, pwd)
            print(f"\n{VERDE}[+] Mensaje recuperado:{RESET} {descifrado}")
            input(f"\n{AMARILLO}Presiona Enter para continuar...{RESET}")

        elif opcion == '3':
            print(f"\n{VERDE}¡Hasta luego, bro!{RESET}")
            break

if __name__ == "__main__":
    menu()
