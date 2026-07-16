from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Ramalhete(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    missa_comunhao = models.IntegerField()
    visita_ao_santissimo = models.IntegerField()
    exame_de_consciencia = models.IntegerField()
    leitura_espiritual_meditacao = models.IntegerField()
    sacrificio = models.IntegerField()

    def __str__(self):
        return f"Ramalhete de {self.usuario.username} em {self.data.strftime('%d/%m/%Y %H:%M:%S')}"
    
    def excluir_ramalhete_por_id(self, ramalhete_id):
        try:
            ramalhete = Ramalhete.objects.get(id=ramalhete_id)
            ramalhete.delete()
            return True
        except Ramalhete.DoesNotExist:
            return False
        
    def editar_ramalhete_por_id(self, ramalhete_id, missa_comunhao=None, visita_ao_santissimo=None, exame_de_consciencia=None, leitura_espiritual_meditacao=None, sacrificio=None):
        try:
            ramalhete = Ramalhete.objects.get(id=ramalhete_id)
            if missa_comunhao is not None:
                ramalhete.missa_comunhao = missa_comunhao
            if visita_ao_santissimo is not None:
                ramalhete.visita_ao_santissimo = visita_ao_santissimo
            if exame_de_consciencia is not None:
                ramalhete.exame_de_consciencia = exame_de_consciencia
            if leitura_espiritual_meditacao is not None:
                ramalhete.leitura_espiritual_meditacao = leitura_espiritual_meditacao
            if sacrificio is not None:
                ramalhete.sacrificio = sacrificio
            ramalhete.save()
            return True
        except Ramalhete.DoesNotExist:
            return False
        
    def buscar_ramalhete_por_usuario(self, usuario):
        return Ramalhete.objects.filter(usuario=usuario).order_by('-data')
    
    def get_total_ramalhetes_por_mes_ano(self, usuario, mes, ano):
        return Ramalhete.objects.filter(usuario=usuario, data__month=mes, data__year=ano).count()