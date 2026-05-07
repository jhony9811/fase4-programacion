# ================================
# IMPORTACIONES
# ================================
import os
import re
from datetime import datetime


# ================================
# EXCEPCIONES PERSONALIZADAS
# ================================
class DatoInvalidoError(Exception):
    pass


class ClienteInvalidoError(Exception):
    pass


# ================================
# FUNCIÓN PARA REGISTRAR ERRORES
# ================================
def registrar_log(mensaje):

    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(ruta_actual, "errores.log")

    with open(ruta, "a", encoding="utf-8") as archivo:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo.write(f"[{fecha}] {mensaje}\n")

    print(f"📝 LOG guardado correctamente en: {ruta}")


# ================================
# CLASE CLIENTE
# ================================
class Cliente:

    def __init__(self, nombre, identificacion, correo, telefono):

        # Limpieza automática de datos
        nombre = nombre.strip()
        identificacion = str(identificacion).strip()
        correo = correo.strip()
        telefono = str(telefono).strip()

        self.nombre = self.validar_nombre(nombre)
        self.identificacion = self.validar_identificacion(identificacion)
        self.correo = self.validar_correo(correo)
        self.telefono = self.validar_telefono(telefono)

    # ----------------------------
    # VALIDACIONES
    # ----------------------------

    def validar_nombre(self, nombre):

        if len(nombre) < 3:
            raise DatoInvalidoError(
                "El nombre debe tener mínimo 3 caracteres."
            )

        return nombre

    def validar_identificacion(self, identificacion):

        if not identificacion.isdigit():
            raise ClienteInvalidoError(
                "La identificación solo debe contener números."
            )

        return identificacion

    def validar_correo(self, correo):

        # Expresión regular profesional
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(patron, correo):
            raise DatoInvalidoError(
                "El correo electrónico no tiene un formato válido."
            )

        return correo

    def validar_telefono(self, telefono):

        if not telefono.isdigit() or len(telefono) < 7:
            raise DatoInvalidoError(
                "El teléfono debe contener mínimo 7 números."
            )

        return telefono

    # ----------------------------
    # MOSTRAR INFORMACIÓN
    # ----------------------------

    def mostrar_informacion(self):

        print("\n📋 INFORMACIÓN DEL CLIENTE")
        print("-" * 40)

        print(f" Nombre: {self.nombre}")
        print(f" ID: {self.identificacion}")
        print(f" Correo: {self.correo}")
        print(f" Teléfono: {self.telefono}")

        print("-" * 40)


# ================================
# FUNCIÓN DE PRUEBA
# ================================
def probar_clientes():

    clientes_prueba = [

        # Correcto
        ("Juan", "123456789", "juan@gmail.com", "3117550699"),

        # Nombre corto
        ("Jo", "123456789", "juan@gmail.com", "3117550699"),

        # ID inválido
        ("Carlos", "ABC123", "carlos@gmail.com", "3117550699"),

        # Correo inválido
        ("Ana", "123456789", "anaemail.com", "3117550699"),

        # Teléfono corto
        ("Luis", "123456789", "luis@gmail.com", "123")
    ]

    print("\n")
    print("=" * 55)
    print("🚀 INICIANDO VALIDACIÓN DE CLIENTES")
    print("=" * 55)

    for datos in clientes_prueba:

        try:

            cliente = Cliente(*datos)

        except (ClienteInvalidoError, DatoInvalidoError) as error:

            print("\n❌ ERROR CONTROLADO")
            print("-" * 40)
            print(f"📌 Detalle: {error}")

            registrar_log(f"Error con datos {datos}: {error}")

        except Exception as error:

            print("\n⚠️ ERROR INESPERADO")
            print("-" * 40)
            print(f"📌 Detalle: {error}")

            registrar_log(f"Error inesperado: {error}")

        else:

            print("\n" + "=" * 50)
            print("✅ CLIENTE REGISTRADO CORRECTAMENTE")
            print("=" * 50)

            cliente.mostrar_informacion()

            registrar_log(
                f"Cliente registrado correctamente: {cliente.nombre}"
            )

        finally:

            print("\n" + "#" * 55)

    print("\n🎯 VALIDACIÓN FINALIZADA")
    print("=" * 55)


# ================================
# EJECUCIÓN PRINCIPAL
# ================================
if __name__ == "__main__":
    probar_clientes()