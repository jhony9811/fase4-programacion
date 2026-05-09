# ==========================================================
# SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES Y RESERVAS
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# CURSO: PROGRAMACIÓN
# ==========================================================

# ==========================================================
# IMPORTACIONES
# ==========================================================
from abc import ABC, abstractmethod
from datetime import datetime
import os
import re

# ==========================================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================================
class DatoInvalidoError(Exception):
    pass


class ClienteInvalidoError(Exception):
    pass


class ServicioNoDisponibleError(Exception):
    pass


class ReservaError(Exception):
    pass


# ==========================================================
# FUNCIÓN PARA REGISTRAR LOGS
# ==========================================================
def registrar_log(mensaje):

    try:

        ruta = os.path.join(
            os.path.dirname(__file__),
            "errores.log"
        )

        with open(ruta, "a", encoding="utf-8") as archivo:

            fecha = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            archivo.write(
                f"[{fecha}] {mensaje}\n"
            )

    except Exception as error:

        print(
            "No fue posible guardar el log:",
            error
        )


# ==========================================================
# CLASE ABSTRACTA GENERAL
# ==========================================================
class Entidad(ABC):

    @abstractmethod
    def mostrar_informacion(self):
        pass


# ==========================================================
# CLASE CLIENTE
# ==========================================================
class Cliente(Entidad):

    def __init__(
        self,
        nombre,
        identificacion,
        correo,
        telefono
    ):

        # Encapsulación de atributos privados
        self.__nombre = self.validar_nombre(nombre)

        self.__identificacion = (
            self.validar_identificacion(
                identificacion
            )
        )

        self.__correo = self.validar_correo(correo)

        self.__telefono = self.validar_telefono(
            telefono
        )

    # ======================================================
    # VALIDACIONES
    # ======================================================
    def validar_nombre(self, nombre):

        if not nombre.strip():

            raise DatoInvalidoError(
                "El nombre no puede estar vacío."
            )

        if len(nombre.strip()) < 3:

            raise DatoInvalidoError(
                "El nombre debe tener mínimo 3 caracteres."
            )

        return nombre

    def validar_identificacion(
        self,
        identificacion
    ):
        try:
            # Intentamos convertir a entero. Si tiene letras, lanzará ValueError.
            int(identificacion)
        except ValueError as error_original:
            # ENCADENAMIENTO DE EXCEPCIONES (raise ... from ...)
            raise ClienteInvalidoError(
                "La identificación solo debe contener números."
            ) from error_original

        if len(identificacion) < 6:
            raise ClienteInvalidoError(
                "La identificación es demasiado corta."
            )

        return identificacion

    def validar_correo(self, correo):

        # Patrón estándar para correos electrónicos
        patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        
        if not re.match(patron, correo):
            raise DatoInvalidoError(
                "El correo electrónico no tiene un formato válido."
            )

        return correo

    def validar_telefono(self, telefono):

        try:
            # Intentamos convertir a entero.
            int(telefono)
        except ValueError as error_original:
            # ENCADENAMIENTO DE EXCEPCIONES
            raise DatoInvalidoError(
                "El teléfono solo debe contener números."
            ) from error_original
            
        if len(telefono) < 7:
            raise DatoInvalidoError(
                "El teléfono debe contener mínimo 7 números."
            )

        return telefono

    # ======================================================
    # GETTERS
    # ======================================================
    @property
    def nombre(self):
        return self.__nombre

    @property
    def identificacion(self):
        return self.__identificacion

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    # ======================================================
    # MOSTRAR INFORMACIÓN
    # ======================================================
    def mostrar_informacion(self):

        print("\n========== CLIENTE ==========")

        print(f"Nombre: {self.__nombre}")

        print(f"Identificación: {self.__identificacion}")

        print(f"Correo: {self.__correo}")

        print(f"Teléfono: {self.__telefono}")

    # ======================================================
    # RESUMEN
    # ======================================================
    def resumen(self):

        return (
            f"{self.__nombre} - "
            f"{self.__correo}"
        )


# ==========================================================
# CLASE ABSTRACTA SERVICIO
# ==========================================================
class Servicio(ABC):

    def __init__(
        self,
        nombre,
        tarifa_base
    ):

        self.nombre = nombre

        self.tarifa_base = tarifa_base

    @abstractmethod
    def calcular_costo(
        self,
        tiempo,
        impuesto=0,
        descuento=0
    ):
        pass

    @abstractmethod
    def descripcion_servicio(self):
        pass


# ==========================================================
# SERVICIO 1 - RESERVA DE SALAS
# ==========================================================
class ReservaSala(Servicio):

    def calcular_costo(
        self,
        horas,
        impuesto=0,
        descuento=0
    ):

        total = self.tarifa_base * horas

        total += total * impuesto

        total -= total * descuento

        return total

    def descripcion_servicio(self):

        return (
            "Reserva de salas empresariales "
            "por horas."
        )


# ==========================================================
# SERVICIO 2 - ALQUILER DE EQUIPOS
# ==========================================================
class AlquilerEquipo(Servicio):

    def calcular_costo(
        self,
        dias,
        impuesto=0,
        descuento=0
    ):

        total = self.tarifa_base * dias

        total += total * impuesto

        total -= total * descuento

        return total

    def descripcion_servicio(self):

        return (
            "Alquiler de equipos "
            "tecnológicos."
        )


# ==========================================================
# SERVICIO 3 - ASESORÍAS ESPECIALIZADAS
# ==========================================================
class AsesoriaEspecializada(Servicio):

    def calcular_costo(
        self,
        sesiones,
        impuesto=0,
        descuento=0
    ):

        total = self.tarifa_base * sesiones

        total += total * impuesto

        total -= total * descuento

        return total

    def descripcion_servicio(self):

        return (
            "Asesorías especializadas "
            "en programación."
        )


# ==========================================================
# CLASE RESERVA
# ==========================================================
class Reserva(Entidad):

    def __init__(
        self,
        cliente,
        servicio,
        duracion
    ):

        if duracion <= 0:

            raise ReservaError(
                "La duración debe ser mayor que cero."
            )

        self.cliente = cliente

        self.servicio = servicio

        self.duracion = duracion

        self.estado = "Pendiente"

    # ======================================================
    # CONFIRMAR RESERVA
    # ======================================================
    def confirmar(self):

        if self.estado == "Cancelada":

            raise ReservaError(
                "No se puede confirmar "
                "una reserva cancelada."
            )

        self.estado = "Confirmada"

    # ======================================================
    # CANCELAR RESERVA
    # ======================================================
    def cancelar(self):

        self.estado = "Cancelada"

    # ======================================================
    # PROCESAR RESERVA
    # ======================================================
    def procesar(
        self,
        impuesto=0,
        descuento=0
    ):

        if self.estado == "Cancelada":

            raise ReservaError(
                "No se puede procesar "
                "una reserva cancelada."
            )

        total = self.servicio.calcular_costo(
            self.duracion,
            impuesto,
            descuento
        )

        return total

    # ======================================================
    # MOSTRAR INFORMACIÓN
    # ======================================================
    def mostrar_informacion(self):

        print("\n========== RESERVA ==========")

        print(
            f"Cliente: {self.cliente.nombre}"
        )

        print(
            f"Servicio: {self.servicio.nombre}"
        )

        print(
            f"Duración: {self.duracion}"
        )

        print(
            f"Estado: {self.estado}"
        )


# ==========================================================
# LISTAS INTERNAS
# ==========================================================
clientes = []

reservas = []

servicios = [

    ReservaSala(
        "Sala VIP",
        50000
    ),

    AlquilerEquipo(
        "Portátiles",
        80000
    ),

    AsesoriaEspecializada(
        "Asesoría Python",
        120000
    )
]


# ==========================================================
# REGISTRAR CLIENTE
# ==========================================================
def registrar_cliente():

    try:

        print(
            "\n========== "
            "REGISTRAR CLIENTE "
            "=========="
        )

        # ==========================================
        # VALIDAR NOMBRE
        # ==========================================
        while True:

            try:

                nombre = input(
                    "Ingrese nombre: "
                )

                if not nombre.strip():

                    raise DatoInvalidoError(
                        "El nombre no puede estar vacío."
                    )

                if len(nombre.strip()) < 3:

                    raise DatoInvalidoError(
                        "El nombre debe tener "
                        "mínimo 3 caracteres."
                    )

                break

            except DatoInvalidoError as error:

                print("\nERROR:", error)

                registrar_log(
                    f"Error nombre: {error}"
                )
            else:
                break # El else se ejecuta si el try no lanzó ninguna excepción
                

        # ==========================================
        # VALIDAR IDENTIFICACIÓN
        # ==========================================
        while True:

            try:

                identificacion = input(
                    "Ingrese identificación: "
                )

                if not identificacion.isdigit():

                    raise ClienteInvalidoError(
                        "La identificación "
                        "debe contener solo números."
                    )

                if len(identificacion) < 6:

                    raise ClienteInvalidoError(
                        "La identificación "
                        "es demasiado corta."
                    )

                break

            except ClienteInvalidoError as error:

                print("\nERROR:", error)

                registrar_log(
                    f"Error identificación: "
                    f"{error}"
                )
            else:
                break

        # ==========================================
        # VALIDAR CORREO
        # ==========================================
        while True:

            try:

                correo = input(
                    "Ingrese correo electrónico: "
                )

                patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

                if not re.match(patron, correo):
                    raise DatoInvalidoError(
                    "El correo electrónico no tiene un formato válido."
                )

            except DatoInvalidoError as error:

                print("\nERROR:", error)

                registrar_log(
                    f"Error correo: {error}"
                )
            else:
                break

        # ==========================================
        # VALIDAR TELÉFONO
        # ==========================================
        while True:

            try:

                telefono = input(
                    "Ingrese teléfono: "
                )

                if (
                    not telefono.isdigit()
                    or len(telefono) < 7
                ):

                    raise DatoInvalidoError(
                        "El teléfono debe contener "
                        "mínimo 7 números."
                    )

                break

            except DatoInvalidoError as error:

                print("\nERROR:", error)

                registrar_log(
                    f"Error teléfono: {error}"
                )
            else:
                break

        cliente = Cliente(
            nombre,
            identificacion,
            correo,
            telefono
        )

        clientes.append(cliente)

        print(
            "\nCLIENTE REGISTRADO "
            "CORRECTAMENTE"
        )

        cliente.mostrar_informacion()

        registrar_log(
            f"Cliente registrado: "
            f"{cliente.nombre}"
        )

    except Exception as error:

        print(
            "\nERROR INESPERADO:",
            error
        )

        registrar_log(
            f"Error inesperado cliente: "
            f"{error}"
        )

    finally:

        print("\nProceso finalizado.")

        print("-" * 50)


# ==========================================================
# MOSTRAR CLIENTES
# ==========================================================
def mostrar_clientes():

    if not clientes:

        print(
            "\nNo hay clientes registrados."
        )

        return

    print(
        "\n========== "
        "LISTA DE CLIENTES "
        "=========="
    )

    for indice, cliente in enumerate(
        clientes,
        start=1
    ):

        print(f"\nCliente #{indice}")

        cliente.mostrar_informacion()


# ==========================================================
# MOSTRAR SERVICIOS
# ==========================================================
def mostrar_servicios():

    print(
        "\n========== "
        "SERVICIOS DISPONIBLES "
        "=========="
    )

    for indice, servicio in enumerate(
        servicios,
        start=1
    ):

        print(
            f"\n{indice}. {servicio.nombre}"
        )

        print(
            servicio.descripcion_servicio()
        )

        print(
            f"Tarifa base: "
            f"${servicio.tarifa_base:,.0f}"
        )


# ==========================================================
# CREAR RESERVA
# ==========================================================
def crear_reserva():

    try:

        if not clientes:

            raise ReservaError(
                "Debe registrar al menos "
                "un cliente."
            )

        print(
            "\n========== "
            "CREAR RESERVA "
            "=========="
        )

        # ==========================================
        # MOSTRAR CLIENTES
        # ==========================================
        for indice, cliente in enumerate(
            clientes,
            start=1
        ):

            print(
                f"{indice}. "
                f"{cliente.nombre} - "
                f"{cliente.identificacion}"
            )

        opcion_cliente = int(
            input(
                "\nSeleccione cliente: "
            )
        )

        cliente = clientes[
            opcion_cliente - 1
        ]

        # ==========================================
        # MOSTRAR SERVICIOS
        # ==========================================
        mostrar_servicios()

        opcion_servicio = int(
            input(
                "\nSeleccione servicio: "
            )
        )

        servicio = servicios[
            opcion_servicio - 1
        ]

        duracion = int(
            input(
                "\nIngrese duración "
                "(horas/días/sesiones): "
            )
        )

        impuesto = float(
            input(
                "Ingrese impuesto "
                "(Ejemplo 0.19): "
            )
        )

        descuento = float(
            input(
                "Ingrese descuento "
                "(Ejemplo 0.10): "
            )
        )

        if impuesto < 0:

            raise ValueError(
                "El impuesto no puede "
                "ser negativo."
            )

        if (
            descuento < 0
            or descuento > 1
        ):

            raise ValueError(
                "El descuento debe "
                "estar entre 0 y 1."
            )

        reserva = Reserva(
            cliente,
            servicio,
            duracion
        )

        reserva.confirmar()

        total = reserva.procesar(
            impuesto,
            descuento
        )

        reservas.append(reserva)

        # ==========================================
        # FACTURA
        # ==========================================
        subtotal = (
            servicio.tarifa_base
            * duracion
        )

        valor_impuesto = (
            subtotal * impuesto
        )

        valor_descuento = (
            subtotal * descuento
        )

        print(
            "\n========== "
            "FACTURA "
            "=========="
        )

        print(
            f"Cliente: {cliente.nombre}"
        )

        print(
            f"Servicio: {servicio.nombre}"
        )

        print(
            f"Tarifa base: "
            f"${servicio.tarifa_base:,.0f}"
        )

        print(
            f"Duración: {duracion}"
        )

        print(
            f"\nSubtotal: "
            f"${subtotal:,.0f}"
        )

        print(
            f"Impuesto: "
            f"${valor_impuesto:,.0f}"
        )

        print(
            f"Descuento: "
            f"${valor_descuento:,.0f}"
        )

        print(
            f"\nTOTAL A PAGAR: "
            f"${total:,.0f}"
        )

        registrar_log(
            f"Reserva creada para "
            f"{cliente.nombre}"
        )

    except IndexError as error:

        print(
            "\nERROR: Opción inválida."
        )

        registrar_log(
            f"Error de selección: "
            f"{error}"
        )

    except ValueError as error:

        print(
            "\nERROR:",
            error
        )

        registrar_log(
            f"Error de valor: "
            f"{error}"
        )

    except ReservaError as error:

        print(
            "\nERROR EN RESERVA:",
            error
        )

        registrar_log(
            f"Error reserva: "
            f"{error}"
        )

    except Exception as error:

        print(
            "\nERROR INESPERADO:",
            error
        )

        registrar_log(
            f"Error inesperado "
            f"reserva: {error}"
        )

    finally:

        print("\nProceso finalizado.")

        print("-" * 50)


# ==========================================================
# MOSTRAR RESERVAS
# ==========================================================
def mostrar_reservas():

    if not reservas:

        print(
            "\nNo existen reservas "
            "registradas."
        )

        return

    print(
        "\n========== "
        "LISTA DE RESERVAS "
        "=========="
    )

    for indice, reserva in enumerate(
        reservas,
        start=1
    ):

        print(f"\nReserva #{indice}")

        reserva.mostrar_informacion()


# ==========================================================
# CANCELAR RESERVA
# ==========================================================
def cancelar_reserva():

    try:

        if not reservas:

            raise ReservaError(
                "No existen reservas "
                "registradas."
            )

        mostrar_reservas()

        opcion = int(
            input(
                "\nSeleccione el número "
                "de la reserva a cancelar: "
            )
        )

        reserva = reservas[
            opcion - 1
        ]

        reserva.cancelar()

        print(
            "\nRESERVA CANCELADA "
            "CORRECTAMENTE"
        )

        registrar_log(
            f"Reserva cancelada de "
            f"{reserva.cliente.nombre}"
        )

    except IndexError as error:

        print(
            "\nERROR: Reserva inválida."
        )

        registrar_log(
            f"Error cancelando reserva: "
            f"{error}"
        )

    except Exception as error:

        print(
            "\nERROR:",
            error
        )

        registrar_log(
            f"Error inesperado "
            f"cancelando: {error}"
        )

    finally:

        print("\nProceso finalizado.")

        print("-" * 50)


# ==========================================================
# SIMULACIÓN DE 10 OPERACIONES (REQUISITO DE RÚBRICA)
# ==========================================================
def simular_operaciones():
    print("\n" + "="*60)
    print(" INICIANDO SIMULACIÓN AUTOMÁTICA DE 10 OPERACIONES ")
    print("="*60)

    # 1. Cliente válido
    print("\n1. Registrando cliente válido...")
    try:
        c1 = Cliente("Juan Perez", "102030", "juan@unad.edu.co", "3001234567")
        clientes.append(c1)
        print("Éxito - Cliente creado.")
    except Exception as e: print(f" Falló: {e}")

    # 2. Cliente inválido (Nombre corto)
    print("\n2. Registrando cliente con nombre inválido...")
    try:
        c2 = Cliente("A", "102030", "a@unad.edu.co", "3001234567")
    except Exception as e: print(f"Excepción atrapada correctamente: {e}")

    # 3. Cliente inválido (Encadenamiento de excepciones en Identificación)
    print("\n3. Registrando cliente con identificación no numérica (Encadenamiento)...")
    try:
        c3 = Cliente("Maria", "ABCDEF", "maria@unad.edu.co", "3001234567")
    except Exception as e:
        print(f"Excepción atrapada: {e}")
        if e.__cause__:
            print(f"Causa original de Python atrapada: {e.__cause__}")

    # 4. Cliente inválido (Correo erróneo)
    print("\n4. Registrando cliente con correo inválido...")
    try:
        c4 = Cliente("Carlos", "123456", "carlos.com", "3001234567")
    except Exception as e: print(f"xcepción atrapada correctamente: {e}")

    # 5. Cliente válido 2
    print("\n5. Registrando segundo cliente válido...")
    try:
        c5 = Cliente("Luisa Gomez", "987654", "luisa@unad.edu.co", "3109876543")
        clientes.append(c5)
        print("Éxito - Cliente creado.")
    except Exception as e: print(f"Falló: {e}")

    # 6. Reserva válida
    print("\n6. Creando reserva válida para Sala VIP...")
    try:
        r1 = Reserva(clientes[0], servicios[0], 5) # 5 horas
        reservas.append(r1)
        print("Éxito - Reserva creada.")
    except Exception as e: print(f"Falló: {e}")

    # 7. Reserva inválida (Duración negativa)
    print("\n7. Creando reserva con duración negativa...")
    try:
        r2 = Reserva(clientes[0], servicios[1], -2)
    except Exception as e: print(f"Excepción atrapada correctamente: {e}")

    # 8. Confirmar reserva
    print("\n8. Confirmando reserva...")
    try:
        reservas[0].confirmar()
        print(f"Éxito - Estado actual: {reservas[0].estado}")
    except Exception as e: print(f"Falló: {e}")

    # 9. Procesar reserva (Sobrecarga/Polimorfismo con impuestos y descuentos)
    print("\n9. Procesando costos de reserva...")
    try:
        costo = reservas[0].procesar(impuesto=0.19, descuento=0.10)
        print(f"Éxito - Costo total calculado: ${costo:,.0f}")
    except Exception as e: print(f"Falló: {e}")

    # 10. Procesar reserva cancelada (Manejo de estados)
    print("\n10. Intentando procesar una reserva cancelada...")
    try:
        reservas[0].cancelar()
        reservas[0].procesar() # Esto debe lanzar error porque ya se canceló
    except Exception as e: print(f"Excepción atrapada correctamente: {e}")

    print("\n" + "="*60)
    print(" SIMULACIÓN FINALIZADA - EL PROGRAMA NO SE CAYÓ ")
    print("="*60)

    input("\nPresione la tecla ENTER para volver al menú principal...")

# ==========================================================
# MENÚ PRINCIPAL
# ==========================================================
def menu():

    while True:

        try:

            print("\n")

            print("=" * 60)

            print(
                " SOFTWARE FJ - "
                "SISTEMA DE RESERVAS "
            )

            print("=" * 60)

            print("1. Registrar cliente")

            print("2. Mostrar clientes")

            print("3. Mostrar servicios")

            print("4. Crear reserva")

            print("5. Mostrar reservas")

            print("6. Cancelar reserva")

            print("7. Salir")

            print("8. Simular operaciones")

            opcion = input(
                "\nSeleccione una opción: "
            )

            # ======================================
            # OPCIONES
            # ======================================
            if opcion == "1":

                registrar_cliente()

            elif opcion == "2":

                mostrar_clientes()

            elif opcion == "3":

                mostrar_servicios()

            elif opcion == "4":

                crear_reserva()

            elif opcion == "5":

                mostrar_reservas()

            elif opcion == "6":

                cancelar_reserva()

            elif opcion == "7":

                print(
                    "\nSaliendo del sistema..."
                )
                registrar_log(
                    "Sistema finalizado "
                    "correctamente."
                )
                break

            elif opcion == "8":
                
                simular_operaciones()

            else:

                print(
                    "\nOpción inválida."
                )

        except KeyboardInterrupt:

            print(
                "\n\nSistema interrumpido "
                "por el usuario."
            )

            registrar_log(
                "Sistema interrumpido "
                "manualmente."
            )

            break

        except Exception as error:

            print(
                "\nERROR GENERAL:",
                error
            )

            registrar_log(
                f"Error general menú: "
                f"{error}"
            )


# ==========================================================
# EJECUCIÓN PRINCIPAL
# ==========================================================
if __name__ == "__main__":

    menu()