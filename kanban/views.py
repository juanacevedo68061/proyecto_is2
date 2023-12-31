from django.shortcuts import render
from publicaciones.models import Publicacion_solo_text
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from publicaciones.models import Publicacion_solo_text
from django.db.models import Q
from uuid import UUID
from django.http import Http404
from publicaciones.utils import tiene_rol
from roles.decorators import permiso_requerido
from django.contrib.auth.decorators import login_required
from .models import Registro
from administracion.models import Categoria
from publicaciones.utils import notificar
from login.models import Usuario
from datetime import datetime

@permiso_requerido
@login_required
def kanban(request):
    """
    Vista para el panel de kanban.

    Esta función obtiene y clasifica las publicaciones basadas en sus estados ('borrador', 'rechazado', 'revision', 'publicar', 'publicado'). 
    Solo se consideran las publicaciones que están activas y pertenecen a categorías moderadas.

    Parameters:
    -----------
    request : HttpRequest
        Objeto de solicitud HTTP.

    Returns:
    --------
    HttpResponse
        Respuesta HTTP con el tablero Kanban renderizado.

    Context Variables:
    ------------------
    - `publicaciones_borrador` : QuerySet
        Publicaciones con estado 'borrador' o 'rechazado' que no están destinadas al editor.
    - `publicaciones_revision` : QuerySet
        Publicaciones con estado 'revision' o 'rechazado' destinadas al editor.
    - `publicaciones_publicar` : QuerySet
        Publicaciones con estado 'publicar'.
    - `publicaciones_publicado` : QuerySet
        Publicaciones con estado 'publicado'.
    - `categorias` : QuerySet
        Categorías que están moderadas.

    Template:
    ---------
    - 'kanban/tablero.html'
    """
    publicaciones_borrador = Publicacion_solo_text.objects.filter(
    Q(estado='borrador', activo=True, categoria__moderada=True) |
    Q(estado='rechazado', para_editor=False, activo=True, categoria__moderada=True)
    )
    publicaciones_revision = Publicacion_solo_text.objects.filter(
    Q(estado='revision', activo=True, categoria__moderada=True) |
    Q(estado='rechazado', para_editor=True, activo=True, categoria__moderada=True)
    )
    publicaciones_publicar = Publicacion_solo_text.objects.filter(estado='publicar', activo=True, categoria__moderada=True)
    publicaciones_publicado = Publicacion_solo_text.objects.filter(estado='publicado', activo=True, categoria__moderada=True)

    categorias = Categoria.objects.filter(moderada=True)
    context = {
        'publicaciones_borrador': publicaciones_borrador,
        'publicaciones_revision': publicaciones_revision,
        'publicaciones_publicar': publicaciones_publicar,
        'publicaciones_publicado': publicaciones_publicado,
        'categorias': categorias
    }

    return render(request, 'kanban/tablero.html', context)

@permiso_requerido
@login_required
@csrf_exempt
def actualizar(request):
    """
    Actualiza el estado de una publicación basándose en el nuevo estado proporcionado en la solicitud POST.
    
    La función primero verifica si el método de solicitud es POST. A continuación, extrae el `id_publicacion` 
    y `nuevo_estado` de la solicitud. Luego, hay varias comprobaciones y condiciones para determinar la validez
    del cambio de estado y para realizar actualizaciones apropiadas. Si se cumple una condición inválida, 
    la función devuelve un objeto JsonResponse con un mensaje de error adecuado.
    
    Parameters:
    -----------
    request : HttpRequest
    La solicitud HTTP del cliente. Espera que el método de la solicitud sea POST y que contenga
    `id_publicacion` y `nuevo_estado` en el cuerpo de la solicitud.

    Returns:
    --------
    JsonResponse
    Una respuesta JSON que puede contener varios estados:
    - `vuelve`: Indica si la publicación debe regresar a su estado anterior.
    - `autor`: Indica si hay un error relacionado con el autor de la publicación.
    - `accion`: Indica si una cierta transición de estado no es permitida.
    - `reason_required`: Indica si se necesita una razón para una transición de estado.
    - `rol`: Indica si hay un error relacionado con el rol del usuario que realiza la solicitud.
    - `error`: Mensajes de error generales, como "No se encontró la publicación" o "ID no es válido".
    - `message`: Mensajes adicionales como "Método no permitido" para solicitudes que no son POST.

    Raises: 
    -------
    ValueError, Http404, Publicacion_solo_text.DoesNotExist
        Estas excepciones se manejan internamente y se devuelven como respuestas JSON con mensajes de error adecuados.
    """

    if request.method == 'POST':
        publicacion_id = request.POST.get('id_publicacion')        
        nuevo_estado = request.POST.get('nuevo_estado')

        estado_valor = {
            "rechazado": 0,
            "borrador": 1,
            "revision": 2,
            "publicar": 3,
            "publicado": 4
        }

        if nuevo_estado in estado_valor:
            try:
                publicacion_id = UUID(publicacion_id)
                publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
                anterior = publicacion.estado
                nuevo = nuevo_estado
                publicacion.estado = nuevo
                
                #asignacion temporal si estan rechazados
                if anterior == "rechazado" and publicacion.para_editor:
                    anterior="revision"
                elif anterior == "rechazado" and not publicacion.para_editor:
                    anterior = "borrador"
                
                #No se permiten recambios de estado en la misma columna
                if anterior == "borrador" and nuevo == "borrador":
                    return JsonResponse({'vuelve': True})
                if anterior == "revision" and nuevo == "revision":
                    return JsonResponse({'vuelve': True})
                if anterior == "publicar" and nuevo == "publicar":
                    return JsonResponse({'vuelve': True})
                if anterior == "publicado" and nuevo == "publicado":
                    return JsonResponse({'vuelve': True})
                                                
                #esta accion se restringe para el que no es el autor
                if nuevo == "revision" and anterior == "borrador" and not request.user == publicacion.autor:
                    return JsonResponse({'autor': True})
                
                #acciones no permitidas
                #publicado a revision
                #publicado a borrador
                #borrador a publicar
                #borrador a publicado
                #revision a publicado
                if anterior == "publicado" and nuevo == "revision":
                    return JsonResponse({'accion': False})
                if anterior == "publicado" and nuevo == "borrador":
                    return JsonResponse({'accion': False})
                if anterior == "borrador" and nuevo == "publicar":
                    return JsonResponse({'accion': False})
                if anterior == "borrador" and nuevo == "publicado":
                    return JsonResponse({'accion': False})
                if anterior == "revision" and nuevo == "publicado":
                    return JsonResponse({'accion': False})

                #Estas acciones corresponden a rechazos
                if nuevo == "borrador" and anterior == "revision" and tiene_rol(request.user, "editor"):
                    return JsonResponse({'reason_required': True})
                elif nuevo == "borrador" and anterior == "revision" and not tiene_rol(request.user, "editor"):
                    return JsonResponse({'rol': "editor"})
                if nuevo == "revision" and anterior == "publicar" and tiene_rol(request.user, "publicador"):
                    return JsonResponse({'reason_required': True})
                elif nuevo == "revision" and anterior == "publicar" and not tiene_rol(request.user, "publicador"):
                    return JsonResponse({'rol': "publicador"})
                if nuevo == "borrador" and anterior == "publicar" and tiene_rol(request.user, "publicador"):
                    return JsonResponse({'reason_required': True})
                elif nuevo == "borrador" and anterior == "publicar" and not tiene_rol(request.user, "publicador"):
                    return JsonResponse({'rol': "publicador"})
                
                #acciones que corresponden a ciertos roles
                if nuevo == "publicar" and anterior == "revision" and not tiene_rol(request.user, "editor"):
                    return JsonResponse({'rol': "editor"})
                if nuevo == "publicado" and anterior == "publicar" and not tiene_rol(request.user, "publicador"):
                    return JsonResponse({'rol': "publicador"})
                if nuevo == "publicar" and anterior == "publicado" and not tiene_rol(request.user, "publicador"):
                    return JsonResponse({'rol': "publicador"})
                
                print(publicacion.estado)
                print(publicacion.para_editor)
                print(publicacion.semaforo)
                
                publicacion.semaforo = "rojo"                
                if publicacion.estado == "publicado":
                    publicacion.semaforo = "verde"
                    publicacion.fecha_publicacion = datetime.now().date()

                publicacion.save()
                if not publicacion.estado == "borrador":
                    notificar(publicacion,3)

                registrar(request, publicacion, anterior)
                
                return JsonResponse({'vuelve': True})
            except (ValueError, Http404, Publicacion_solo_text.DoesNotExist) as e:
                return JsonResponse({'error': 'No se encontró la publicación o el ID no es válido'}, status=400)
        else:
            return JsonResponse({'error': 'Estado no válido'}, status=400)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

@permiso_requerido
@login_required
@csrf_exempt
def motivo(request):
    """
    Vista para proporcionar un motivo al rechazar una publicación en el tablero Kanban.

    Permite agregar un motivo al rechazar una publicación y cambia su estado.

    Parameters:
    -----------
    request : HttpRequest
        La solicitud HTTP recibida.

    Returns:
    --------
    JsonResponse
        Una respuesta JSON con el resultado de la operación.
    """
    if request.method == 'POST':
        publicacion_id = request.POST.get('id_publicacion')
        publicacion_id = UUID(publicacion_id)
        publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
        motivo = request.POST.get('motivo')
        nuevo = request.POST.get('nuevo')
        if motivo:
            print(motivo)
            
            if nuevo == "revision":
                publicacion.para_editor = True
                motivo = motivo + ", su publicación se pasó al Editor"
            elif nuevo == "borrador":
                publicacion.para_editor = False
            anterior = publicacion.estado
            publicacion.estado ="rechazado"
            publicacion.semaforo = "rojo"
            publicacion.save()          
            notificar(publicacion,2, motivo) 
            registrar(request, publicacion, anterior) 
            print(publicacion.estado)
            print(publicacion.para_editor)
            
            return JsonResponse({'vuelve': True})
        else:
            return JsonResponse({'vuelve': True})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
@login_required
def historial(request, publicacion_id):
    """
    Devuelve el historial de registros de una publicación.
    
    Esta función recupera y muestra el historial de registros relacionados con una publicación
    específica. Si el usuario que realiza la solicitud no tiene un rol de "editor" o "publicador", 
    sólo se muestran los registros en los que dicho usuario es el responsable.
    
    Parameters:
    -----------
    request : HttpRequest
        La solicitud HTTP del cliente.
    publicacion_id : str
        El identificador único de la publicación para la cual se solicita el historial.

    Returns:
    --------
    HttpResponse
        Una respuesta HTTP que contiene el renderizado de la página 'kanban/historial.html' 
        con los registros asociados a la publicación.

    """
    registros = Registro.objects.filter(publicacion_id=publicacion_id)
    if not tiene_rol(request.user, "editor") and not tiene_rol(request.user, "publicador"):
        registros = Registro.objects.filter(publicacion_id=publicacion_id, responsable=request.user)
    return render(request, 'kanban/historial.html', {'registros': registros})

@login_required
def registrar(request, publicacion, anterior):

    """
    Registra un cambio de estado en una publicación.

    Esta función crea un nuevo registro en el modelo `Registro` que documenta
    el cambio de estado de una publicación. Guarda información sobre el usuario 
    responsable, la publicación afectada, el estado anterior y el nuevo estado. 
    Además, asocia los roles del usuario al registro.

    Parameters:
    -----------
    request : HttpRequest
        El objeto de solicitud HTTP.
    publicacion : Publicacion_solo_text
        El objeto de la publicación cuyo estado ha cambiado.
    anterior : str
        El estado anterior de la publicación.

    Returns:
    --------
    None
        La función no devuelve ningún valor, pero crea un nuevo registro en la base de datos.

    Note:
    -----
    Se espera que esta función se llame después de cualquier cambio en el estado 
    de una publicación para mantener un historial de dichos cambios.
    """
    usuario = request.user
    roles = usuario.roles.all()
    nuevo_registro = Registro.objects.create(
        responsable=usuario,
        publicacion_id=publicacion.id_publicacion,
        publicacion_titulo=publicacion.titulo,
        anterior = anterior,
        nuevo=publicacion.estado,
    )
    nuevo_registro.roles.set(roles)
    nuevo_registro.save()