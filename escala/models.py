from django.db import models
import uuid

class Setor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100)
    ramal = models.CharField(max_length=20, blank=True, null=True)
    responsavel = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=50, unique=True)  # Ex: ENF, TUS, ADM

    def __str__(self):
        return self.nome

class Colaborador(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    matricula = models.CharField(max_length=30)
    coren = models.CharField(max_length=30, blank=True, null=True)
    setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome

class Legenda(models.Model):
    sigla = models.CharField(max_length=10, unique=True)
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.sigla} - {self.descricao}"

class Plantao(models.Model):
    TURNO_CHOICES = [
        ("M", "Manhã"),
        ("T", "Tarde"),
        ("N", "Noite"),
        ("AB", "Abono"),
        ("FE", "Férias"),
        ("F", "Folga"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    colaborador = models.ForeignKey("Colaborador", on_delete=models.CASCADE)
    data = models.DateField()
    turno = models.CharField(max_length=2, choices=TURNO_CHOICES, default="F")
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.colaborador.nome} - {self.data} ({self.get_turno_display()})"