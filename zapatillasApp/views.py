from pyexpat.errors import messages
from django.forms import inlineformset_factory, modelformset_factory
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render
from tiendaProject import settings
from zapatillasApp.forms import ProductoForm, TallaForm, TallaFormSet
from zapatillasApp.models import Producto, Talla

def inicio(request):
    return render(request,'mastertemplate.html')

def listarCatalogo(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/catalogo.html', {'productos': productos})

@permission_required('zapatillasApp.add_producto')
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        formset = TallaFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            producto = form.save()
            formset.instance = producto
            formset.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()
        formset = TallaFormSet()
    return render(request, 'productos/crear_producto.html', {'form': form, 'formset': formset})


@permission_required('app.view_producto')
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/listar_productos.html', {'productos': productos})

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    tallas = producto.tallas.all()
    return render(request, 'detalle_producto.html', {'producto': producto, 'tallas': tallas})

@permission_required('app.change_producto', raise_exception=True)
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    TallaFormSet = inlineformset_factory(Producto, Talla, fields=('talla', 'cantidad'), extra=1, can_delete=True)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        formset = TallaFormSet(request.POST, instance=producto)
        
        print('POST data:', request.POST)
        print('Formset data:', formset.data)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            
            return redirect('detalle_producto', pk=producto.pk)
            
    else:
        form = ProductoForm(instance=producto)
        formset = TallaFormSet(instance=producto)
    
    return render(request, 'productos/editar_producto.html', {
        'form': form,
        'formset': formset,
        'producto': producto
    })


@permission_required('app.delete_producto')
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'productos/eliminar_producto.html', {'producto': producto})


def detalle_producto(request, pk):
    producto = Producto.objects.get(cod_producto=pk)
    return render(request, 'tienda/detalle_producto.html', {'producto': producto})

def notificar_stock_bajo(): 
    umbral = 10
    tallas_bajo_stock = Talla.objects.filter(cantidad__lt=umbral)

    for talla in tallas_bajo_stock:
        producto = talla.producto
        if producto:
            subject = f"Stock Bajo para la Talla {talla.talla} de {producto.nombre}"
            message = f"El producto '{producto.nombre}' con talla {talla.talla} tiene un stock de {talla.cantidad} unidades, que está por debajo del umbral ({umbral} unidades)."
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

def carrito(request):
    carrito = request.session.get('carrito', {})
    for key, item in carrito.items():
        item['subtotal'] = int(item['cantidad'] * item['precio'])
    total = int(sum(item['subtotal'] for item in carrito.values()))
    return render(request, 'tienda/carrito.html', {'carrito': carrito, 'total': total})


def agregar_al_carrito(request, producto_id):
    if request.method == "POST":
        talla_seleccionada = request.POST.get('talla')
        producto = get_object_or_404(Producto, cod_producto=producto_id)
        talla = get_object_or_404(Talla, producto=producto, talla=talla_seleccionada)

        if talla.cantidad > 0:
            carrito = request.session.get('carrito', {})
            clave_carrito = f"{producto_id}-{talla_seleccionada}"
            if clave_carrito in carrito:
                carrito[clave_carrito]['cantidad'] += 1
            else:
                carrito[clave_carrito] = {
                    'nombre': producto.nombre,
                    'precio': float(producto.precio),
                    'cantidad': 1,
                    'talla': talla_seleccionada,
                }

            talla.cantidad -= 1
            talla.save()
            notificar_stock_bajo()
            request.session['carrito'] = carrito
        else:
            messages.error(request, "La talla seleccionada no está disponible.")

        return redirect('carrito')
        
def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto_id, talla = producto_id.split('-')
    clave_carrito = f"{producto_id}-{talla}"
    if clave_carrito in carrito:
        producto = get_object_or_404(Producto, cod_producto=producto_id)
        talla_obj = get_object_or_404(Talla, producto=producto, talla=talla)

        talla_obj.cantidad += carrito[clave_carrito]['cantidad']
        talla_obj.save()

        del carrito[clave_carrito]
    request.session['carrito'] = carrito
    return redirect('carrito')

def agregar_talla(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    if request.method == 'POST':
        talla_form = TallaForm(request.POST)

        if talla_form.is_valid():
            talla = talla_form.save(commit=False)
            talla.producto = producto
            talla.save()

        return redirect('detalle_producto', pk=producto.cod_producto)
    else:
        talla_form = TallaForm()

    return render(request, 'productos/agregar_talla.html', {'form': talla_form, 'producto': producto})

def finalizar_compra(request):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        if not carrito:
            return JsonResponse({'mensaje': 'El carrito está vacío'})
        total_venta = 0
        for item in carrito.values():
            total_venta += float(item['precio']) * item['cantidad']
        request.session['carrito'] = {}
        return JsonResponse({'mensaje': 'Compra finalizada', 'total': total_venta})
    return JsonResponse({'mensaje': 'Método no permitido'}, status=405)