from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Usuario, Inmueble, Comuna, SolicitudArriendo

# Servicios para Usuario

def crear_usuario(form):
    user = form.save()
    usuario = Usuario.objects.create(
        user=user,
        nombres=form.cleaned_data.get('nombres'),
        apellidos=form.cleaned_data.get('apellidos'),
        rut=form.cleaned_data.get('rut'),
        direccion=form.cleaned_data.get('direccion'),
        telefono=form.cleaned_data.get('telefono'),
        tipo_usuario=form.cleaned_data.get('tipo_usuario')
    )
    return usuario

def actualizar_usuario(usuario_id, **kwargs):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    for key, value in kwargs.items():
        setattr(usuario, key, value)
    usuario.save()
    return usuario

# Servicios para Inmueble

def obtener_comunas(region_id):
    return Comuna.objects.filter(region_id=region_id).order_by('nombre')

def listar_inmuebles():
    return Inmueble.objects.all()

def obtener_inmueble(inmueble_id):
    return get_object_or_404(Inmueble, id=inmueble_id)

def crear_inmueble(form, usuario):
    inmueble = form.save(commit=False)
    inmueble.arrendador = usuario
    inmueble.save()
    return inmueble

def actualizar_inmueble(inmueble_id, **kwargs):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    for key, value in kwargs.items():
        setattr(inmueble, key, value)
    inmueble.save()
    return inmueble

def borrar_inmueble(inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    inmueble.delete()


# Crear un grupo de Arrendadores 

arrendadores_group, created = Group.objects.get_or_create(name='Arrendadores')

# Asignar permisos al grupo 

permission = Permission.objects.get(name='Can add Inmueble') 
arrendadores_group.permissions.add(permission)


# Servicios para SolicitudArriendo

def crear_solicitud_arriendo(form, usuario, inmueble):
    solicitud = form.save(commit=False)
    solicitud.arrendatario = usuario
    solicitud.inmueble = inmueble
    solicitud.save()
    return solicitud

def listar_solicitudes(usuario):
    inmuebles = Inmueble.objects.filter(arrendador=usuario)
    return SolicitudArriendo.objects.filter(inmueble__in=inmuebles)



def exportar_inmuebles_por_comuna():
    inmuebles = Inmueble.objects.all()
    inmuebles_por_comuna = {}

    for x in inmuebles:
        comuna = x.comuna
        if comuna not in inmuebles_por_comuna:
            inmuebles_por_comuna[comuna] = []
        inmuebles_por_comuna[comuna].append(x)

    with open('arriendoapp/consultas/inmuebles_por_comuna.txt', 'w', encoding='utf-8') as archivo:
        for comuna, inmuebles in inmuebles_por_comuna.items():
            contador = 0
            archivo.write(f'---Comuna: {comuna.nombre}\n')
            for x in inmuebles:
                contador += 1
                archivo.write(f"Inmueble {contador}\n -Nombre: {x.nombre}\n -Descripcion: {x.descripcion}\n")
            archivo.write("\n")


def exportar_inmuebles_por_region():
    inmuebles = Inmueble.objects.all()
    inmuebles_por_region = {}

    for x in inmuebles:
        region = x.region
        if region not in inmuebles_por_region:
            inmuebles_por_region[region] = []
        inmuebles_por_region[region].append(x)

    with open('arriendoapp/consultas/inmuebles_por_region.txt', 'w', encoding='utf-8') as archivo:
        for region, inmuebles in inmuebles_por_region.items():
            contador = 0
            archivo.write(f'---Region: {region.nombre}\n')
            for x in inmuebles:
                contador += 1
                archivo.write(f"Inmueble {contador}\n -Nombre: {x.nombre}\n -Descripcion: {x.descripcion}\n")
            archivo.write("\n")