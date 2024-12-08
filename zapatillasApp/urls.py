from django.urls import path
from zapatillasApp.views import agregar_al_carrito, agregar_talla, carrito, crear_producto, detalle_producto, editar_producto, eliminar_del_carrito, eliminar_producto, finalizar_compra, inicio, listar_productos, listarCatalogo

urlpatterns = [
    path('', inicio, name='mastertemplate'),
    path('catalogo/', listarCatalogo, name='catalogo'),
    path('productos/', listar_productos, name='listar_productos'),
    path('productos/crear/',crear_producto, name='crear_producto'),
    path('productos/editar/<int:pk>/', editar_producto, name='editar_producto'),
    path('productos/<int:producto_id>/agregar-talla/', agregar_talla, name='agregar_talla'),
    path('productos/eliminar/<int:pk>/', eliminar_producto, name='eliminar_producto'),
    path('detalle_producto/<int:pk>/', detalle_producto, name='detalle_producto'),
    path('carrito/', carrito, name='carrito'),
    path('agregar-al-carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<str:producto_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('finalizar-compra/', finalizar_compra, name='finalizar_compra'),
]