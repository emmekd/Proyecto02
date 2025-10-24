import json
import datetime
import os
from typing import Dict, List, Any

class SistemaGestion:
    def __init__(self):
        self.clientes = {}
        self.productos = {}
        self.compras = []
        self.visitas = {}
        self.cargar_datos()
    
    def cargar_datos(self):
        """Cargar datos desde archivos JSON"""
        try:
            with open('clientes.json', 'r') as f:
                self.clientes = json.load(f)
        except FileNotFoundError:
            self.clientes = {}
        
        try:
            with open('productos.json', 'r') as f:
                self.productos = json.load(f)
        except FileNotFoundError:
            self.productos = {}
        
        try:
            with open('compras.json', 'r') as f:
                self.compras = json.load(f)
        except FileNotFoundError:
            self.compras = []
        
        try:
            with open('visitas.json', 'r') as f:
                self.visitas = json.load(f)
        except FileNotFoundError:
            self.visitas = {}
    
    def guardar_datos(self):
        """Guardar datos en archivos JSON"""
        with open('clientes.json', 'w') as f:
            json.dump(self.clientes, f, indent=2)
        
        with open('productos.json', 'w') as f:
            json.dump(self.productos, f, indent=2)
        
        with open('compras.json', 'w') as f:
            json.dump(self.compras, f, indent=2)
        
        with open('visitas.json', 'w') as f:
            json.dump(self.visitas, f, indent=2)

class GestionClientes:
    def __init__(self, sistema: SistemaGestion):
        self.sistema = sistema
    
    def registrar_cliente(self):
        """Registrar un nuevo cliente"""
        print("\n--- REGISTRAR NUEVO CLIENTE ---")
        nombre = input("Nombre del cliente: ").strip()
        telefono = input("Teléfono del cliente: ").strip()
        
        if nombre in self.sistema.clientes:
            print("❌ El cliente ya existe.")
            return
        
        self.sistema.clientes[nombre] = {
            'telefono': telefono,
            'fecha_registro': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Inicializar contador de visitas
        self.sistema.visitas[nombre] = 0
        
        self.sistema.guardar_datos()
        print("✅ Cliente registrado exitosamente.")
    
    def eliminar_cliente(self):
        """Eliminar un cliente"""
        print("\n--- ELIMINAR CLIENTE ---")
        nombre = input("Nombre del cliente a eliminar: ").strip()
        
        if nombre not in self.sistema.clientes:
            print("❌ Cliente no encontrado.")
            return
        
        confirmacion = input(f"¿Está seguro de eliminar a {nombre}? (s/n): ").lower()
        if confirmacion == 's':
            del self.sistema.clientes[nombre]
            if nombre in self.sistema.visitas:
                del self.sistema.visitas[nombre]
            self.sistema.guardar_datos()
            print("✅ Cliente eliminado exitosamente.")
    
    def consultar_editar_cliente(self):
        """Consultar y editar información del cliente"""
        print("\n--- CONSULTAR/EDITAR CLIENTE ---")
        nombre = input("Nombre del cliente: ").strip()
        
        if nombre not in self.sistema.clientes:
            print("❌ Cliente no encontrado.")
            return
        
        cliente = self.sistema.clientes[nombre]
        visitas = self.sistema.visitas.get(nombre, 0)
        
        print(f"\n📋 Información de {nombre}:")
        print(f"   Teléfono: {cliente['telefono']}")
        print(f"   Visitas: {visitas}")
        print(f"   Fecha de registro: {cliente['telefono']}")
        
        opcion = input("\n¿Desea editar la información? (s/n): ").lower()
        if opcion == 's':
            nuevo_telefono = input(f"Nuevo teléfono (actual: {cliente['telefono']}): ").strip()
            if nuevo_telefono:
                self.sistema.clientes[nombre]['telefono'] = nuevo_telefono
                self.sistema.guardar_datos()
                print("✅ Información actualizada.")
    
    def listar_clientes(self):
        """Listar todos los clientes"""
        print("\n--- LISTA DE CLIENTES ---")
        if not self.sistema.clientes:
            print("No hay clientes registrados.")
            return
        
        for i, (nombre, info) in enumerate(self.sistema.clientes.items(), 1):
            visitas = self.sistema.visitas.get(nombre, 0)
            print(f"{i}. {nombre} - Tel: {info['telefono']} - Visitas: {visitas}")

class GestionProductos:
    def __init__(self, sistema: SistemaGestion):
        self.sistema = sistema
        self.categorias = ['Electrónicos', 'Ropa', 'Hogar', 'Deportes', 'Otros']
    
    def mostrar_menu_categorias(self):
        """Mostrar menú de productos por categorías"""
        print("\n--- CATEGORÍAS DE PRODUCTOS ---")
        for i, categoria in enumerate(self.categorias, 1):
            print(f"{i}. {categoria}")
        
        try:
            opcion = int(input("\nSeleccione una categoría: "))
            if 1 <= opcion <= len(self.categorias):
                self.mostrar_productos_categoria(self.categorias[opcion-1])
            else:
                print("❌ Opción inválida.")
        except ValueError:
            print("❌ Por favor ingrese un número válido.")
    
    def mostrar_productos_categoria(self, categoria):
        """Mostrar productos de una categoría específica"""
        print(f"\n--- PRODUCTOS DE {categoria.upper()} ---")
        productos_categoria = {k: v for k, v in self.sistema.productos.items() 
                             if v['categoria'] == categoria}
        
        if not productos_categoria:
            print("No hay productos en esta categoría.")
            return
        
        for i, (nombre, info) in enumerate(productos_categoria.items(), 1):
            print(f"{i}. {nombre} - ${info['precio']:.2f} - Stock: {info['stock']}")
    
    def agregar_producto(self):
        """Agregar un nuevo producto"""
        print("\n--- AGREGAR PRODUCTO ---")
        nombre = input("Nombre del producto: ").strip()
        
        if nombre in self.sistema.productos:
            print("❌ El producto ya existe.")
            return
        
        print("\nCategorías disponibles:")
        for i, categoria in enumerate(self.categorias, 1):
            print(f"{i}. {categoria}")
        
        try:
            categoria_opcion = int(input("Seleccione categoría: "))
            if not 1 <= categoria_opcion <= len(self.categorias):
                print("❌ Categoría inválida.")
                return
            categoria = self.categorias[categoria_opcion-1]
        except ValueError:
            print("❌ Opción inválida.")
            return
        
        try:
            precio = float(input("Precio del producto: "))
            stock = int(input("Stock inicial: "))
        except ValueError:
            print("❌ Precio y stock deben ser números válidos.")
            return
        
        self.sistema.productos[nombre] = {
            'categoria': categoria,
            'precio': precio,
            'stock': stock
        }
        
        self.sistema.guardar_datos()
        print("✅ Producto agregado exitosamente.")
    
    def editar_producto(self):
        """Editar información de un producto"""
        print("\n--- EDITAR PRODUCTO ---")
        nombre = input("Nombre del producto a editar: ").strip()
        
        if nombre not in self.sistema.productos:
            print("❌ Producto no encontrado.")
            return
        
        producto = self.sistema.productos[nombre]
        print(f"\nProducto: {nombre}")
        print(f"Categoría: {producto['categoria']}")
        print(f"Precio: ${producto['precio']:.2f}")
        print(f"Stock: {producto['stock']}")
        
        print("\n¿Qué desea editar?")
        print("1. Precio")
        print("2. Stock")
        print("3. Categoría")
        
        try:
            opcion = int(input("Seleccione opción: "))
            if opcion == 1:
                nuevo_precio = float(input("Nuevo precio: "))
                self.sistema.productos[nombre]['precio'] = nuevo_precio
            elif opcion == 2:
                nuevo_stock = int(input("Nuevo stock: "))
                self.sistema.productos[nombre]['stock'] = nuevo_stock
            elif opcion == 3:
                print("\nCategorías disponibles:")
                for i, cat in enumerate(self.categorias, 1):
                    print(f"{i}. {cat}")
                nueva_cat = int(input("Nueva categoría: "))
                if 1 <= nueva_cat <= len(self.categorias):
                    self.sistema.productos[nombre]['categoria'] = self.categorias[nueva_cat-1]
                else:
                    print("❌ Categoría inválida.")
                    return
            else:
                print("❌ Opción inválida.")
                return
            
            self.sistema.guardar_datos()
            print("✅ Producto actualizado exitosamente.")
            
        except ValueError:
            print("❌ Valor inválido.")

class RegistroCompras:
    def __init__(self, sistema: SistemaGestion):
        self.sistema = sistema
    
    def registrar_compra(self):
        """Registrar una nueva compra"""
        print("\n--- REGISTRAR COMPRA ---")
        nombre_cliente = input("Nombre del cliente: ").strip()
        
        if nombre_cliente not in self.sistema.clientes:
            print("❌ Cliente no registrado.")
            return
        
        # Registrar visita automáticamente
        if nombre_cliente in self.sistema.visitas:
            self.sistema.visitas[nombre_cliente] += 1
        else:
            self.sistema.visitas[nombre_cliente] = 1
        
        productos_compra = []
        total = 0
        
        while True:
            print("\nProductos disponibles:")
            for i, (nombre, info) in enumerate(self.sistema.productos.items(), 1):
                print(f"{i}. {nombre} - ${info['precio']:.2f} - Stock: {info['stock']}")
            
            producto_nombre = input("\nNombre del producto (o 'fin' para terminar): ").strip()
            if producto_nombre.lower() == 'fin':
                break
            
            if producto_nombre not in self.sistema.productos:
                print("❌ Producto no encontrado.")
                continue
            
            try:
                cantidad = int(input("Cantidad: "))
                if cantidad <= 0:
                    print("❌ La cantidad debe ser mayor a 0.")
                    continue
                
                producto = self.sistema.productos[producto_nombre]
                if cantidad > producto['stock']:
                    print("❌ Stock insuficiente.")
                    continue
                
                # Actualizar stock
                self.sistema.productos[producto_nombre]['stock'] -= cantidad
                
                subtotal = producto['precio'] * cantidad
                total += subtotal
                
                productos_compra.append({
                    'producto': producto_nombre,
                    'cantidad': cantidad,
                    'precio_unitario': producto['precio'],
                    'subtotal': subtotal
                })
                
                print(f"✅ Producto agregado. Subtotal: ${subtotal:.2f}")
                
            except ValueError:
                print("❌ Cantidad inválida.")
        
        if productos_compra:
            compra = {
                'cliente': nombre_cliente,
                'fecha': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'productos': productos_compra,
                'total': total
            }
            
            self.sistema.compras.append(compra)
            self.sistema.guardar_datos()
            print(f"\n✅ Compra registrada exitosamente.")
            print(f"📦 Total de la compra: ${total:.2f}")
        else:
            print("❌ No se registraron productos en la compra.")

class Reportes:
    def __init__(self, sistema: SistemaGestion):
        self.sistema = sistema
    
    def clientes_frecuentes(self):
        """Generar reporte de clientes más frecuentes"""
        print("\n--- CLIENTES MÁS FRECUENTES ---")
        
        if not self.sistema.visitas:
            print("No hay datos de visitas.")
            return
        
        clientes_ordenados = sorted(self.sistema.visitas.items(), 
                                  key=lambda x: x[1], reverse=True)
        
        for i, (cliente, visitas) in enumerate(clientes_ordenados[:10], 1):
            telefono = self.sistema.clientes.get(cliente, {}).get('telefono', 'N/A')
            print(f"{i}. {cliente} - Tel: {telefono} - Visitas: {visitas}")
    
    def productos_populares(self):
        """Generar reporte de productos más vendidos"""
        print("\n--- PRODUCTOS MÁS VENDIDOS ---")
        
        if not self.sistema.compras:
            print("No hay datos de compras.")
            return
        
        ventas_productos = {}
        
        for compra in self.sistema.compras:
            for producto in compra['productos']:
                nombre = producto['producto']
                cantidad = producto['cantidad']
                if nombre in ventas_productos:
                    ventas_productos[nombre] += cantidad
                else:
                    ventas_productos[nombre] = cantidad
        
        productos_ordenados = sorted(ventas_productos.items(), 
                                   key=lambda x: x[1], reverse=True)
        
        for i, (producto, cantidad) in enumerate(productos_ordenados[:10], 1):
            print(f"{i}. {producto} - Vendidos: {cantidad}")

def autenticar_usuario():
    """Sistema de autenticación para el dueño"""
    print("\n--- INICIO DE SESIÓN ---")
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    
    # Credenciales predeterminadas (cambiar en producción)
    if usuario == "admin" and contraseña == "admin123":
        return True
    else:
        print("❌ Credenciales incorrectas.")
        return False

def main():
    """Función principal del sistema"""
    if not autenticar_usuario():
        return
    
    sistema = SistemaGestion()
    gestion_clientes = GestionClientes(sistema)
    gestion_productos = GestionProductos(sistema)
    registro_compras = RegistroCompras(sistema)
    reportes = Reportes(sistema)
    
    while True:
        print("\n" + "="*50)
        print("          SISTEMA DE GESTIÓN COMERCIAL")
        print("="*50)
        print("1. Gestión de Clientes")
        print("2. Gestión de Productos")
        print("3. Registrar Compra")
        print("4. Reportes")
        print("5. Salir")
        print("-"*50)
        
        try:
            opcion = int(input("Seleccione una opción: "))
            
            if opcion == 1:
                # Submenú Gestión de Clientes
                print("\n--- GESTIÓN DE CLIENTES ---")
                print("1. Registrar nuevo cliente")
                print("2. Eliminar cliente")
                print("3. Consultar/editar cliente")
                print("4. Listar todos los clientes")
                
                sub_opcion = int(input("Seleccione opción: "))
                if sub_opcion == 1:
                    gestion_clientes.registrar_cliente()
                elif sub_opcion == 2:
                    gestion_clientes.eliminar_cliente()
                elif sub_opcion == 3:
                    gestion_clientes.consultar_editar_cliente()
                elif sub_opcion == 4:
                    gestion_clientes.listar_clientes()
                else:
                    print("❌ Opción inválida.")
            
            elif opcion == 2:
                # Submenú Gestión de Productos
                print("\n--- GESTIÓN DE PRODUCTOS ---")
                print("1. Ver menú por categorías")
                print("2. Agregar producto")
                print("3. Editar producto")
                
                sub_opcion = int(input("Seleccione opción: "))
                if sub_opcion == 1:
                    gestion_productos.mostrar_menu_categorias()
                elif sub_opcion == 2:
                    gestion_productos.agregar_producto()
                elif sub_opcion == 3:
                    gestion_productos.editar_producto()
                else:
                    print("❌ Opción inválida.")
            
            elif opcion == 3:
                registro_compras.registrar_compra()
            
            elif opcion == 4:
                # Submenú Reportes
                print("\n--- REPORTES ---")
                print("1. Clientes más frecuentes")
                print("2. Productos más vendidos")
                
                sub_opcion = int(input("Seleccione opción: "))
                if sub_opcion == 1:
                    reportes.clientes_frecuentes()
                elif sub_opcion == 2:
                    reportes.productos_populares()
                else:
                    print("❌ Opción inválida.")
            
            elif opcion == 5:
                print("¡Hasta luego!")
                break
            
            else:
                print("❌ Opción inválida. Por favor seleccione 1-5.")
        
        except ValueError:
            print("❌ Por favor ingrese un número válido.")

if __name__ == "__main__":
    main()