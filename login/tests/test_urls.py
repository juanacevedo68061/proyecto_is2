from django.test import SimpleTestCase
from django.urls import reverse, resolve
from login import views

class UrlsTests(SimpleTestCase):
    def test_inicio_sesion_url_resuelta(self):
        url = reverse('login:inicio_sesion')
        self.assertEqual(resolve(url).func, views.inicio_sesion)

    def test_registro_url_resuelta(self):
        url = reverse('login:registro')
        self.assertEqual(resolve(url).func, views.registro)

    def test_cerrar_sesion_url_resuelta(self):
        url = reverse('login:cerrar_sesion')
        self.assertEqual(resolve(url).func, views.cerrar_sesion)

    def test_perfil_usuario_url_resuelta(self):
        url = reverse('login:perfil')
        self.assertEqual(resolve(url).func, views.perfil_usuario)

    def test_perfil_actualizar_url_resuelta(self):
        url = reverse('login:perfil_actualizar')
        self.assertEqual(resolve(url).func, views.perfil_actualizar)
