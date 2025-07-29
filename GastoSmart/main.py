import json
import os
import datetime
import pandas as pd

ARCHIVO_USUARIOS = "usuarios.json"
ARCHIVO_DATOS = "registros.json"

def cargar_usuarios():
    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, 'r') as file:
            return json.load(file)
    return {}

def guardar_usuarios(usuarios):
    with open(ARCHIVO_USUARIOS, 'w') as file:
        json.dump(usuarios, file, indent=4)

def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, 'r') as file:
            datos = json.load(file)
            if isinstance(datos, dict):
                return datos
    return {}

def guardar_datos(data):
    with open(ARCHIVO_DATOS, 'w') as file:
        json.dump(data, file, indent=4)

usuarios = cargar_usuarios()
datos = cargar_datos()
usuario_actual = None
presupuestos = {}
metas_ahorro = {}

def registrar_usuario():
    print("\n--- Registro ---")
    usuario = input("Nombre de usuario: ").strip()
    if usuario in usuarios:
        print("⚠️ El usuario ya existe.")
        return None
    contraseña = input("Contraseña: ").strip()
    usuarios[usuario] = {"contraseña": contraseña}
    guardar_usuarios(usuarios)
    print("✅ Usuario registrado.")
    return usuario

def iniciar_sesion():
    print("\n--- Iniciar sesión ---")
    usuario = input("Nombre de usuario: ").strip()
    contraseña = input("Contraseña: ").strip()
    if usuario in usuarios and usuarios[usuario]["contraseña"] == contraseña:
        print("✅ Sesión iniciada.")
        return usuario
    else:
        print("❌ Usuario o contraseña incorrectos.")
        return None

def registrar_transaccion():
    global datos
    tipo = input("\n¿Es un Gasto o un Ingreso? (G/I): ").strip().upper()
    if tipo not in ['G', 'I']:
        print("Tipo inválido.")
        return
    try:
        monto = float(input("Monto: "))
    except ValueError:
        print("Monto inválido.")
        return
    categoria = input("Categoría: ").strip()
    fecha = input("Fecha (dd/mm/aaaa): ").strip()
    if not fecha:
        fecha = datetime.date.today().strftime("%d/%m/%Y")

    transaccion = {
        "tipo": "Gasto" if tipo == 'G' else "Ingreso",
        "monto": monto,
        "categoria": categoria,
        "fecha": fecha
    }

    if usuario_actual not in datos:
        datos[usuario_actual] = []
    datos[usuario_actual].append(transaccion)
    guardar_datos(datos)
    print("✅ Transacción guardada.")

def mostrar_resumen_grafico():
    if usuario_actual not in datos or not datos[usuario_actual]:
        print("No hay transacciones.")
        return

    mes_actual = datetime.date.today().month
    año_actual = datetime.date.today().year
    df = pd.DataFrame(datos[usuario_actual])
    df['fecha'] = pd.to_datetime(df['fecha'], format="%d/%m/%Y", errors='coerce')
    df_mes = df[(df['fecha'].dt.month == mes_actual) & (df['fecha'].dt.year == año_actual)]

    if df_mes.empty:
        print("No hay transacciones para este mes.")
        return

    resumen = df_mes.groupby('categoria')['monto'].sum()
    print("\n--- Resumen del mes ---")
    for categoria, monto in resumen.items():
        print(f"{categoria}: Bs. {monto:.2f}")

def configurar_presupuesto():
    categoria = input("\nCategoría para el presupuesto: ").strip()
    try:
        monto = float(input("Monto máximo permitido: "))
        presupuestos[categoria] = monto
        print(f"✅ Presupuesto establecido: {categoria} → Bs. {monto:.2f}")
    except ValueError:
        print("Monto inválido.")

def recibir_alertas():
    if usuario_actual not in datos:
        print("No hay transacciones.")
        return
    alertas = False
    for t in datos[usuario_actual]:
        if t['tipo'] == "Gasto" and t['categoria'] in presupuestos:
            if t['monto'] > presupuestos[t['categoria']]:
                print(f"⚠️ Gasto excesivo en '{t['categoria']}': Bs. {t['monto']:.2f} (límite: {presupuestos[t['categoria']]})")
                alertas = True
    if not alertas:
        print("No se han detectado gastos excesivos.")

def predecir_patrones_futuros():
    if usuario_actual not in datos or not datos[usuario_actual]:
        print("No hay transacciones.")
        return
    df = pd.DataFrame(datos[usuario_actual])
    df['fecha'] = pd.to_datetime(df['fecha'], format="%d/%m/%Y", errors='coerce')
    df = df[df['tipo'] == "Gasto"]
    pred = df.groupby('categoria')['monto'].mean()
    print("\n--- Predicción mensual por categoría ---")
    for cat, monto in pred.items():
        print(f"{cat}: Bs. {monto:.2f} (promedio mensual)")

def establecer_metas_ahorro():
    categoria = input("Categoría de ahorro: ").strip()
    try:
        meta = float(input("Meta mensual (Bs): "))
        metas_ahorro[categoria] = meta
        print(f"✅ Meta establecida: {categoria} → Bs. {meta:.2f}")
    except ValueError:
        print("Monto inválido.")

def mostrar_menu():
    while True:
        print(f"\n--- GastoSmart: Usuario {usuario_actual} ---")
        print("1. Registrar gasto o ingreso")
        print("2. Ver resumen gráfico mensual")
        print("3. Configurar presupuesto mensual")
        print("4. Establecer metas de ahorro")
        print("5. Recibir alertas por gastos excesivos")
        print("6. Predecir patrones de gasto futuro")
        print("7. Cerrar sesión")
        opcion = input("Elige una opción: ").strip()

        if opcion == '1':
            registrar_transaccion()
        elif opcion == '2':
            mostrar_resumen_grafico()
        elif opcion == '3':
            configurar_presupuesto()
        elif opcion == '4':
            establecer_metas_ahorro()
        elif opcion == '5':
            recibir_alertas()
        elif opcion == '6':
            predecir_patrones_futuros()
        elif opcion == '7':
            print("👋 Cerrando sesión...")
            break
        else:
            print("Opción inválida.")

def inicio():
    global usuario_actual
    while True:
        print("\n--- Bienvenido a GastoSmart ---")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == '1':
            usuario_actual = iniciar_sesion()
            if usuario_actual:
                mostrar_menu()
        elif opcion == '2':
            usuario_actual = registrar_usuario()
            if usuario_actual:
                mostrar_menu()
        elif opcion == '3':
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    inicio()
