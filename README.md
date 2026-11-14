# 🔐 Malbolge-Crypt (Termux Edition)

**Malbolge-Crypt** es un motor criptográfico experimental y polimórfico construido sobre una variante modificada de **Malbolge**, el lenguaje de programación esotérico más difícil del mundo. 

A diferencia del Malbolge tradicional (que solo ofusca código y puede ejecutarse en cualquier intérprete público), **Malbolge-Crypt** muta la arquitectura matemática base-3 del lenguaje utilizando una contraseña secreta mediante un hash **SHA-256**. Sin la clave exacta, el código generado es matemáticamente indescifrable.

---

## ⚙️ ¿Cómo funciona por dentro?

1. **Derivación de Llave (SHA-256):** Al ingresar una contraseña, el sistema genera una semilla criptográfica única.
2. **Mutación de Auto-Encriptación (`XLAT1`):** Desordena dinámicamente la tabla interna de 94 caracteres que Malbolge usa para mutar sus propias instrucciones después de ejecutarlas.
3. **Alteración de la *Crazy Operation* (`tabla_t`):** Reconfigura la tabla de verdad ternaria (base-3) que gobierna las operaciones lógicas de la máquina virtual.
4. **Compilador Inverso (Búsqueda BFS):** Busca automáticamente las secuencias de rotaciones (`rotr`) y operaciones locas (`crz`) necesarias para construir cada carácter del mensaje y fabrica un programa ejecutable válido.

---

## 📲 Instalación y Uso en Termux

Esta herramienta **no requiere librerías externas**; funciona únicamente con los módulos nativos de Python.

### 1. Actualizar paquetes e instalar dependencias
Abre Termux y ejecuta los siguientes comandos:

```bash
pkg update && pkg upgrade -y
pkg install git python -y
```

### 2. Clonar el repositorio
*(Recuerda reemplazar `TU-USUARIO` con tu nombre de usuario de GitHub)*

```bash
git clone https://github.com
cd Malbolge-Crypt
```

### 3. Ejecutar la herramienta

```bash
python malbolge_crypt.py
```

---

## 🚀 Ejemplo de Funcionamiento

* **Mensaje original:** `Mision cumplida, bro!`
* **Contraseña:** `SuperSecreto2026`
* **Salida generada (Código Malbolge polimórfico):**
  ```text
  ('&%:9]!~}|z2Vxwv-,POqponl$Hjig%eB@@>}=<M:9wv6WsU2T|nm-,jcL(I&%$#"
  ```

> **Nota:** Si intentas ejecutar este código en un intérprete estándar de Malbolge o ingresas una contraseña incorrecta en **Malbolge-Crypt**, la máquina virtual ternaria colapsará o devolverá caracteres sin sentido.

---

## 📂 Estructura del Proyecto

```text
Malbolge-Crypt/
├── malbolge_crypt.py    # Script principal interactivo (Encriptador y VM)
└── README.md            # Documentación del proyecto
```

---

## ⚠️ Aviso Legal / Disclaimer

Este proyecto fue creado con fines **educativos, experimentales y de investigación** sobre lenguajes esotéricos y lógica ternaria. El autor no se hace responsable del uso indebido de esta herramienta.

