from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

    #razon: 1 - es para inactivo
    #razon: 2 - es para rechazo
    #razon: 3 - es para otros estados

#notificar(publicacion,3)
#registrar(request, publicacion,'autor')
#debes implementar que el registro ocurra aqui, y que no se notifique cuando pasa a borrador
#pero si se debe registrar incluso el borrador
#en autor o editor o publicador es los roles y en la vista que depende de ellos ocurre el cambio
def notificar(publicacion, cambio, razon=""):
    subject = 'Cambio en tu Publicación'
    recipient_list = [publicacion.autor.email]
    from_email=settings.EMAIL_HOST_USER
    email_content = render_to_string('publicaciones/email.html', {
        'publicacion': publicacion,
        'cambio': cambio,
        'razon': razon,
        'from_email':from_email
    })

    if email_content:
        email = EmailMessage(subject, email_content, from_email, recipient_list)
        email.content_subtype = "html"
        email.send()
        print("Notificación enviada")

def publicar_no_moderada(usuario):
    """
    Verifica si el usuario tiene el permiso 'publicar_no_moderada' en alguno de sus roles.

    Parámetros:
        usuario (Usuario): El usuario cuyos roles se verificarán.

    Retorna:
        bool: True si el usuario tiene el permiso, False en caso contrario.
    """
    return usuario.roles.filter(permisos__codename='publicar_no_moderada').exists()

def tiene_permiso(usuario, nombre):
    """
    Verifica si el usuario tiene el permiso con el nombre que trae 'nombre' en alguno de sus roles.

    Parámetros:
        usuario (Usuario): El usuario cuyos roles se verificarán.

    Retorna:
        bool: True si el usuario tiene el permiso, False en caso contrario.
    """
    return usuario.roles.filter(permisos__codename=nombre).exists()

def tiene_rol(usuario, nombre):
    """
    Verifica si el usuario tiene el rol con el nombre que trae 'nombre' en alguno de sus roles.

    Parámetros:
        usuario (Usuario): El usuario cuyos roles se verificarán.

    Retorna:
        bool: True si el usuario tiene el permiso, False en caso contrario.
    """
    return usuario.roles.filter(nombre=nombre).exists()