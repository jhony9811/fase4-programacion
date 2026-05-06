# ================================
# IMPORTACIONES
# ================================
import os
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
    ruta = os.path.join(os.path.dirname(__file__), "errores.log")
    
    with open(ruta, "a", encoding="utf-8") as archivo:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo.write(f"[{fecha}] {mensaje}\n")

    print("LOG guardado en:", ruta)


# ================================
# CLASE CLIENTE
# ================================
class Cliente:

    def __init__(self, nombre, identificacion, correo, telefono):
        self.nombre = self.validar_nombre(nombre)
        self.identificacion = self.validar_identificacion(identificacion)
        self.correo = self.validar_correo(correo)
        self.telefono = self.validar_telefono(telefono)

    # ----------------------------
    # VALIDACIONES
    # ----------------------------
    def validar_nombre(self, nombre):
        if len(nombre) < 3:
            raise DatoInvalidoError("El nombre debe tener mínimo 3 caracteres.")
        return nombre

    def validar_identificacion(self, identificacion):
        if not identificacion.isdigit():
            raise ClienteInvalidoError("La identificación solo debe contener números.")
        return identificacion

    def validar_correo(self, correo):
        if "@" not in correo or "." not in correo:
            raise DatoInvalidoError("El correo electrónico no tiene un formato válido.")
        return correo

    def validar_telefono(self, telefono):
        if not telefono.isdigit() or len(telefono) < 7:
            raise DatoInvalidoError("El teléfono debe contener mínimo 7 números.")
        return telefono

    # ----------------------------
    # MOSTRAR INFORMACIÓN
    # ----------------------------
    def mostrar_informacion(self):
        print("Cliente registrado:")
        print("Nombre:", self.nombre)
        print("ID:", self.identificacion)
        print("Correo:", self.correo)
        print("Teléfono:", self.telefono)


# ================================
# FUNCIÓN DE PRUEBA
# ================================
def probar_clientes():

    clientes_prueba = [
        ("Juan", "123456789", "juan@gmail.com", "3117550699"),  # correcto
        ("Jo", "123456789", "juan@gmail.com", "3117550699"),    # nombre corto
        ("Carlos", "ABC123", "carlos@gmail.com", "3117550699"), # ID inválido
        ("Ana", "123456789", "anaemail.com", "3117550699"),     # correo inválido
        ("Luis", "123456789", "luis@gmail.com", "123")          # teléfono corto
    ]

    for datos in clientes_prueba:
        try:
            cliente = Cliente(*datos)

        except (ClienteInvalidoError, DatoInvalidoError) as error:
            print("ERROR CONTROLADO:", error)
            registrar_log(f"Error con datos {datos}: {error}")

        except Exception as error:
            print("ERROR INESPERADO:", error)
            registrar_log(f"Error inesperado: {error}")

        else:
            print("CLIENTE REGISTRADO CORRECTAMENTE")
            cliente.mostrar_informacion()

        finally:
            print("-" * 40)


# ================================
# EJECUCIÓN PRINCIPAL
# ================================
if __name__ == "__main__":
    probar_clientes()