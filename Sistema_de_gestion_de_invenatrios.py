
from abc import ABC, abstractmethod
import unittest

class Inventariable(ABC):
	@abstractmethod
	def consultar_existencias(self):
		raise NotImplementedError


class Producto(Inventariable):

	def __init__(self, id_producto, nombre, precio, cantidad):
		self.id_producto = id_producto
		self.nombre = nombre
		self.precio = precio
		self.cantidad = cantidad

	@property
	def id_producto(self):
		return self.__id_producto

	@id_producto.setter
	def id_producto(self, valor):
		if valor is None or (isinstance(valor, str) and not valor.strip()):
			raise ValueError("El ID del producto no puede estar vacío.")
		self.__id_producto = valor

	@property
	def nombre(self):
		return self.__nombre

	@nombre.setter
	def nombre(self, valor):
		if not isinstance(valor, str) or not valor.strip():
			raise ValueError("El nombre debe ser un texto no vacío.")
		self.__nombre = valor.strip()

	@property
	def precio(self):
		return self.__precio

	@precio.setter
	def precio(self, valor):
		try:
			valor = float(valor)
		except (TypeError, ValueError):
			raise ValueError("El precio debe ser numérico.") from None
		if valor < 0:
			raise ValueError("El precio no puede ser negativo.")
		self.__precio = valor

	@property
	def cantidad(self):
		return self.__cantidad

	@cantidad.setter
	def cantidad(self, valor):
		if isinstance(valor, bool) or not isinstance(valor, int) or valor < 0:
			raise ValueError("La cantidad debe ser un entero no negativo.")
		self.__cantidad = valor

	def consultar_existencias(self):
		return self.cantidad

	@abstractmethod
	def calcular_valor_inventario(self):
		raise NotImplementedError

	@abstractmethod
	def mostrar_informacion(self):
		raise NotImplementedError


class Electronico(Producto):
	def __init__(self, id_producto, nombre, precio, cantidad, marca, garantia_meses):
		super().__init__(id_producto, nombre, precio, cantidad)
		if not isinstance(marca, str) or not marca.strip():
			raise ValueError("La marca debe ser un texto no vacío.")
		if isinstance(garantia_meses, bool) or not isinstance(garantia_meses, int) or garantia_meses < 0:
			raise ValueError("La garantía debe ser un entero no negativo.")
		self.marca = marca.strip()
		self.garantia_meses = garantia_meses

	def calcular_valor_inventario(self):
		return self.precio * self.cantidad

	def mostrar_informacion(self):
		return (f"Electrónico | ID: {self.id_producto} | {self.nombre} | "
				f"Marca: {self.marca} | Garantía: {self.garantia_meses} meses | "
				f"Precio: ${self.precio:.2f} | Cantidad: {self.cantidad}")


class Alimento(Producto):
	def __init__(self, id_producto, nombre, precio, cantidad, fecha_caducidad, categoria):
		super().__init__(id_producto, nombre, precio, cantidad)
		if not isinstance(fecha_caducidad, str) or not fecha_caducidad.strip():
			raise ValueError("La fecha de caducidad debe ser un texto no vacío.")
		if not isinstance(categoria, str) or not categoria.strip():
			raise ValueError("La categoría debe ser un texto no vacío.")
		self.fecha_caducidad = fecha_caducidad.strip()
		self.categoria = categoria.strip()

	def calcular_valor_inventario(self):
		return self.precio * self.cantidad

	def mostrar_informacion(self):
		return (f"Alimento | ID: {self.id_producto} | {self.nombre} | "
				f"Categoría: {self.categoria} | Caduca: {self.fecha_caducidad} | "
				f"Precio: ${self.precio:.2f} | Cantidad: {self.cantidad}")


class Ropa(Producto):
	def __init__(self, id_producto, nombre, precio, cantidad, talla, color, material):
		super().__init__(id_producto, nombre, precio, cantidad)
		for campo, valor in (("talla", talla), ("color", color), ("material", material)):
			if not isinstance(valor, str) or not valor.strip():
				raise ValueError(f"{campo.capitalize()} debe ser un texto no vacío.")
		self.talla = talla.strip()
		self.color = color.strip()
		self.material = material.strip()

	def calcular_valor_inventario(self):
		return self.precio * self.cantidad

	def mostrar_informacion(self):
		return (f"Ropa | ID: {self.id_producto} | {self.nombre} | Talla: {self.talla} | "
				f"Color: {self.color} | Material: {self.material} | "
				f"Precio: ${self.precio:.2f} | Cantidad: {self.cantidad}")


class Inventario:
	def __init__(self):
		self.__productos = {}

	def registrar_producto(self, producto):
		if not isinstance(producto, Producto):
			raise TypeError("Solo se pueden registrar objetos de tipo Producto.")
		if producto.id_producto in self.__productos:
			raise ValueError(f"Ya existe un producto con ID {producto.id_producto}.")
		self.__productos[producto.id_producto] = producto

	def mostrar_productos(self):
		return list(self.__productos.values())

	def buscar_producto(self, id_producto):
		return self.__productos.get(id_producto)

	def actualizar_existencias(self, id_producto, cantidad):
		producto = self.buscar_producto(id_producto)
		if producto is None:
			return False
		producto.cantidad = cantidad
		return True

	def eliminar_producto(self, id_producto):
		return self.__productos.pop(id_producto, None) is not None

	def calcular_valor_total(self):
		return sum(producto.calcular_valor_inventario()
				   for producto in self.__productos.values())


def crear_productos_ejemplo():
	return [
		Electronico(1, "Audífonos", 25.50, 10, "Acme", 12),
		Alimento(2, "Arroz", 3.25, 20, "2026-12-31", "Granos"),
		Ropa(3, "Playera", 15.00, 5, "M", "Azul", "Algodón"),
	]


def main():
	inventario = Inventario()
	productos = crear_productos_ejemplo()
	for producto in productos:
		inventario.registrar_producto(producto)

	print("=== Productos del inventario ===")
	for producto in inventario.mostrar_productos():
		print(producto.mostrar_informacion())
		print(f"Valor en inventario: ${producto.calcular_valor_inventario():.2f}\n")
	print(f"Valor total: ${inventario.calcular_valor_total():.2f}")


class PruebasInventario(unittest.TestCase):

	def setUp(self):
		self.productos = crear_productos_ejemplo()
		self.inventario = Inventario()
		for producto in self.productos:
			self.inventario.registrar_producto(producto)

	def test_no_se_puede_crear_producto_abstracto(self):
		with self.assertRaises(TypeError):
			Producto(10, "Base", 1, 1)

	def test_clases_derivadas_y_existencias(self):
		self.assertEqual([p.consultar_existencias() for p in self.productos], [10, 20, 5])
		self.assertIsInstance(self.productos[0], Producto)

	def test_calculo_de_valor_por_tipo(self):
		self.assertEqual([p.calcular_valor_inventario() for p in self.productos],
						 [255.0, 65.0, 75.0])

	def test_polimorfismo_de_informacion(self):
		textos = [p.mostrar_informacion() for p in self.productos]
		self.assertIn("Electrónico", textos[0])
		self.assertIn("Alimento", textos[1])
		self.assertIn("Ropa", textos[2])

	def test_registro_y_busqueda(self):
		encontrado = self.inventario.buscar_producto(2)
		self.assertIs(encontrado, self.productos[1])
		self.assertIsNone(self.inventario.buscar_producto(999))
		with self.assertRaises(ValueError):
			self.inventario.registrar_producto(self.productos[0])

	def test_actualizacion_de_existencias(self):
		self.assertTrue(self.inventario.actualizar_existencias(1, 7))
		self.assertEqual(self.inventario.buscar_producto(1).cantidad, 7)
		self.assertFalse(self.inventario.actualizar_existencias(999, 1))

	def test_eliminacion(self):
		self.assertTrue(self.inventario.eliminar_producto(2))
		self.assertIsNone(self.inventario.buscar_producto(2))
		self.assertFalse(self.inventario.eliminar_producto(2))

	def test_valor_total(self):
		self.assertEqual(self.inventario.calcular_valor_total(), 395.0)

	def test_validacion_de_cantidad(self):
		with self.assertRaises(ValueError):
			self.productos[0].cantidad = -1


if __name__ == "__main__":
	main()
