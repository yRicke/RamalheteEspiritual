from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Ramalhete


def create_ramalhete(usuario, data, **values):
    defaults = {
        'missa_comunhao': 0,
        'visita_ao_santissimo': 0,
        'tercos': 0,
        'exame_de_consciencia': 0,
        'leitura_espiritual_meditacao': 0,
        'sacrificio': 0,
    }
    defaults.update(values)
    return Ramalhete.objects.create(usuario=usuario, data=data, **defaults)


class AdminDashboardTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin_teste',
            password='AdminSeguro!2468',
        )
        self.usuario = User.objects.create_user(
            username='usuario_teste',
            password='UsuarioSeguro!2468',
        )

    def test_superuser_sees_admin_dashboard_without_calendar(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse('home'))

        self.assertTemplateUsed(response, 'admin_home.html')
        self.assertContains(response, 'Painel do Ramalhete Espiritual')
        self.assertNotContains(response, 'id="calendarPanel"')

    def test_regular_user_still_sees_personal_calendar(self):
        self.client.force_login(self.usuario)

        response = self.client.get(reverse('home'))

        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'id="calendarPanel"')
        self.assertNotContains(response, 'Usuarios cadastrados')

    def test_admin_summary_adds_all_regular_users_and_ignores_superusers(self):
        outro_usuario = User.objects.create_user(
            username='outro_usuario',
            password='OutroSeguro!2468',
        )
        create_ramalhete(
            self.usuario,
            date(2026, 7, 2),
            missa_comunhao=1,
            visita_ao_santissimo=2,
            tercos=3,
        )
        create_ramalhete(
            outro_usuario,
            date(2026, 7, 8),
            missa_comunhao=4,
            visita_ao_santissimo=5,
            tercos=6,
        )
        create_ramalhete(
            self.admin,
            date(2026, 7, 10),
            missa_comunhao=100,
        )
        self.client.force_login(self.admin)

        response = self.client.get(reverse('resumo_admin_mensal', args=[2026, 7]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['missa_comunhao'], 5)
        self.assertEqual(response.json()['visita_ao_santissimo'], 7)
        self.assertEqual(response.json()['tercos'], 9)

    def test_regular_user_cannot_access_admin_endpoints(self):
        self.client.force_login(self.usuario)

        summary_response = self.client.get(reverse('resumo_admin_mensal', args=[2026, 7]))
        create_response = self.client.post(
            reverse('criar_usuario'),
            {'username': 'indevido', 'password': 'SenhaIndevida!2468'},
        )
        edit_response = self.client.post(
            reverse('editar_usuario', args=[self.usuario.id]),
            {'username': 'alterado', 'is_active': 'on'},
        )

        self.assertEqual(summary_response.status_code, 403)
        self.assertEqual(create_response.status_code, 403)
        self.assertEqual(edit_response.status_code, 403)
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.username, 'usuario_teste')

    def test_superuser_can_create_user(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('criar_usuario'),
            {
                'username': 'novo_usuario',
                'password': 'NovaContaSegura!2468',
            },
        )

        self.assertRedirects(response, reverse('home'))
        usuario = User.objects.get(username='novo_usuario')
        self.assertTrue(usuario.check_password('NovaContaSegura!2468'))
        self.assertFalse(usuario.is_staff)
        self.assertFalse(usuario.is_superuser)

    def test_superuser_can_rename_deactivate_and_reset_password(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('editar_usuario', args=[self.usuario.id]),
            {
                'username': 'usuario_editado',
                'password': 'SenhaRedefinida!2468',
            },
        )

        self.assertRedirects(response, reverse('home'))
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.username, 'usuario_editado')
        self.assertFalse(self.usuario.is_active)
        self.assertTrue(self.usuario.check_password('SenhaRedefinida!2468'))

    def test_public_registration_route_is_removed(self):
        response = self.client.get('/registrar/')

        self.assertEqual(response.status_code, 404)

    def test_login_page_has_no_registration_option(self):
        response = self.client.get(reverse('entrar'))

        self.assertNotContains(response, 'Criar nova conta')
        self.assertNotContains(response, 'Criar conta')
