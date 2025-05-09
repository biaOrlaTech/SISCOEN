from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Setor, Categoria, Colaborador, Legenda, Plantao

class SetorResource(resources.ModelResource):
    class Meta:
        model = Setor
        import_id_fields = ['id']
        fields = ('id', 'nome', 'ramal', 'responsavel')

class CategoriaResource(resources.ModelResource):
    class Meta:
        model = Categoria
        import_id_fields = ['id']
        fields = ('id', 'nome')

class ColaboradorResource(resources.ModelResource):
    class Meta:
        model = Colaborador
        import_id_fields = ['id']
        fields = ('id', 'nome', 'categoria', 'matricula', 'coren', 'setor')

class PlantaoResource(resources.ModelResource):
    class Meta:
        model = Plantao
        import_id_fields = ['id']
        fields = ('id', 'colaborador', 'data', 'turno', 'observacao')

@admin.register(Setor)
class SetorAdmin(ImportExportModelAdmin):
    resource_class = SetorResource
    list_display = ('nome', 'ramal', 'responsavel')
    search_fields = ('nome', 'responsavel')

@admin.register(Categoria)
class CategoriaAdmin(ImportExportModelAdmin):
    resource_class = CategoriaResource
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Colaborador)
class ColaboradorAdmin(ImportExportModelAdmin):
    resource_class = ColaboradorResource
    list_display = ('nome', 'categoria', 'matricula', 'coren', 'setor')
    list_filter = ('categoria', 'setor')
    search_fields = ('nome', 'matricula', 'coren')

@admin.register(Legenda)
class LegendaAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'descricao')
    search_fields = ('sigla', 'descricao')

@admin.register(Plantao)
class PlantaoAdmin(ImportExportModelAdmin):
    resource_class = PlantaoResource
    list_display = ('colaborador', 'data', 'turno', 'observacao')
    list_filter = ('colaborador', 'turno', 'data', 'colaborador__setor')
    search_fields = ('colaborador__nome', 'observacao')
    list_per_page = 30
    ordering = ['colaborador__nome', 'data']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('colaborador').order_by('colaborador__nome', 'data')