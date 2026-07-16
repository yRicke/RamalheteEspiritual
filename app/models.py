from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Ramalhete(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    missa_comunhao = models.IntegerField()
    visita_ao_santissimo = models.IntegerField()
    tercos = models.IntegerField()
    exame_de_consciencia = models.IntegerField()
    leitura_espiritual_meditacao = models.IntegerField()
    sacrificio = models.IntegerField()

    def __str__(self):
        return f"Ramalhete de {self.usuario.username} em {self.data.strftime('%d/%m/%Y %H:%M:%S')}"
        
    def editar_ramalhete(self, missa_comunhao=None, visita_ao_santissimo=None, exame_de_consciencia=None, leitura_espiritual_meditacao=None, sacrificio=None):
        if missa_comunhao is not None:
            self.missa_comunhao = missa_comunhao
        if visita_ao_santissimo is not None:
            self.visita_ao_santissimo = visita_ao_santissimo
        if exame_de_consciencia is not None:
            self.exame_de_consciencia = exame_de_consciencia
        if leitura_espiritual_meditacao is not None:
            self.leitura_espiritual_meditacao = leitura_espiritual_meditacao
        if sacrificio is not None:
            self.sacrificio = sacrificio
        self.save()
    
    @classmethod
    def get_ramalhete_por_usuario(cls, usuario):
        return cls.objects.filter(usuario=usuario).order_by('-data')
    
    @classmethod
    def get_total_missas_comunhao_por_usuario_mes_ano(cls, usuario, mes, ano):
        return cls.objects.filter(usuario=usuario, data__month=mes, data__year=ano).aggregate(total=models.Sum('missa_comunhao'))['total'] or 0
    
    @classmethod
    def get_total_visitas_ao_santissimo_por_usuario_mes_ano(cls, usuario, mes, ano):
        return cls.objects.filter(usuario=usuario, data__month=mes, data__year=ano).aggregate(total=models.Sum('visita_ao_santissimo'))['total'] or 0
    
    @classmethod
    def get_total_tercos_por_usuario_mes_ano(cls, usuario, mes, ano):
        return cls.objects.filter(usuario=usuario, data__month=mes, data__year=ano).aggregate(total=models.Sum('tercos'))['total'] or 0
    
    @classmethod
    def get_total_exames_de_consciencia_por_usuario_mes_ano(cls, usuario, mes, ano):
        return cls.objects.filter(usuario=usuario, data__month=mes, data__year=ano).aggregate(total=models.Sum('exame_de_consciencia'))['total'] or 0
    
    @classmethod
    def get_total_leituras_espirituais_por_usuario_mes_ano(cls, usuario, mes, ano):
        return cls.objects.filter(usuario=usuario, data__month=mes, data__year=ano).aggregate(total=models.Sum('leitura_espiritual_meditacao'))['total'] or 0
    
    @classmethod
    def get_total_sacrificios_por_usuario_mes_ano(cls, usuario, mes, ano):
        return cls.objects.filter(usuario=usuario, data__month=mes, data__year=ano).aggregate(total=models.Sum('sacrificio'))['total'] or 0
    
    @classmethod
    def get_total_geral_por_usuario_mes_ano(cls, usuario, mes, ano):
        return {"missa_comunhao": cls.get_total_missas_comunhao_por_usuario_mes_ano(usuario, mes, ano),
                "visita_ao_santissimo": cls.get_total_visitas_ao_santissimo_por_usuario_mes_ano(usuario, mes, ano),
                "tercos": cls.get_total_tercos_por_usuario_mes_ano(usuario, mes, ano),
                "exame_de_consciencia": cls.get_total_exames_de_consciencia_por_usuario_mes_ano(usuario, mes, ano),
                "leitura_espiritual_meditacao": cls.get_total_leituras_espirituais_por_usuario_mes_ano(usuario, mes, ano),
                "sacrificio": cls.get_total_sacrificios_por_usuario_mes_ano(usuario, mes, ano)
                }
    

    