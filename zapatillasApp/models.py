from django.db import models

class Cliente(models.Model):
    rut = models.CharField(max_length=12, primary_key=True)
    nombre_cliente = models.CharField(max_length=100)
    correo = models.EmailField()
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre_cliente

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre_proveedor = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_proveedor


class Producto(models.Model):
    cod_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True) 
    cod_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)


    def __str__(self):
        return self.nombre

class Talla(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='tallas')
    talla = models.CharField(max_length=10)
    cantidad = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.producto.nombre} - Talla {self.talla}"


class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    cod_producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    cantidad_stock = models.PositiveIntegerField()
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cod_producto.nombre


class AlertaStock(models.Model):
    id_alerta = models.AutoField(primary_key=True)
    cod_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_actual = models.PositiveIntegerField()
    fecha_alerta = models.DateTimeField()

    def __str__(self):
        return self.cod_producto.nombre


class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    cod_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    rut = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_venta = models.DateTimeField()
    tipo_venta = models.CharField(max_length=50)
    cantidad = models.PositiveIntegerField()
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.id_venta, self.cod_producto.nombre


class ReporteVentas(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    cod_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    total_vendido = models.PositiveIntegerField()
    fecha_reporte = models.DateTimeField()

    def __str__(self):
        return self.id_reporte, self.cod_producto.nombre