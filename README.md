# Desafío backend Django

Desarrolla una API REST utilizando Django para gestionar un sistema de sociedades, socios y administradores.

## Endpoints requeridos:

- **Crear una sociedad**: Un endpoint que permita crear una nueva sociedad. Una sociedad tiene al menos un nombre y un RUT.

- **Crear un socio**: Un endpoint que permita crear un nuevo socio dentro de una sociedad. Un socio tiene al menos un nombre, RUT, dirección y participación

- **Crear un administrador**: Un endpoint que permita crear un administrador dentro de una sociedad. Un administrador tiene al menos un nombre, RUT y una lista de facultades como "Abrir una cuenta corriente", "Firmar cheques" o "Firmar contratos".

- **Eliminar una sociedad**: Un endpoint que permita eliminar una sociedad existente.

- **Obtener sociedades que contengan al socio o al administrador con el RUT indicado**: Un endpoint que devuelva todas las sociedades en las que está asociado un socio o administrador específico. El RUT del socio o administrador se pasará como parámetro en la URL.

- **Obtener socios y administradores que están en la sociedad con el RUT indicado**: Un endpoint  que devuelva todos los socios y administradores que están asociados a una sociedad específica.

## Ejemplo dataset

- **Legalbot SPA**
  - RUT: 76.192.448-K
  - Socios:
    - **Esteban López López**
      - RUT: 10.456.983-9
      - Dirección: Av siempre viva 2436
      - Participación: 50%
    - **Juan García García**
      - RUT: 15.192.932-6
      - Dirección: Av holanda 2222
      - Participación: 50%
  - Administradores:
    - **Esteban López López**
      - RUT: 10.456.983-9
      - Facultades:
        - Abrir cuentas corrientes
        - Firmar contratos de compraventa
        - Firmar cheques
    - **Miguel Gonzalez Gonzalez**
      - RUT: 12.432.567-K
      - Facultades:
        - Firmar cheques

## Requisitos técnicos:

- Utiliza Django para desarrollar la API.
- Incluye algunos test unitarios
    

## Puntos extras (opcionales, puedes seleccionar sólo uno):

- Implementa autenticación y autorización en la API para proteger los endpoints.
- Incluir un test de integración o E2E

## Entrega

- Sube tu código a un repositorio en github e invitanos (si es que es privado)
