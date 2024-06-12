import django_filters
from .models import Product, Allergy, Category


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        conjoined=True  # чтобы выбрать продукты, относящиеся ко всем указанным категориям
    )
    calories = django_filters.NumberFilter()
    proteins = django_filters.NumberFilter()
    fats = django_filters.NumberFilter()
    carbs = django_filters.NumberFilter()
    price = django_filters.NumberFilter()
    contraindications = django_filters.ModelMultipleChoiceFilter(
        queryset=Allergy.objects.all(),
        conjoined=True  # чтобы выбрать продукты, которые имеют все указанные противопоказания
    )
    is_prepared = django_filters.BooleanFilter()

    # Антифильтры
    not_name = django_filters.CharFilter(field_name='name', lookup_expr='iexact', exclude=True)
    not_category = django_filters.ModelMultipleChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        conjoined=True,
        exclude=True
    )
    not_calories = django_filters.NumberFilter(field_name='calories', lookup_expr='exact', exclude=True)
    not_proteins = django_filters.NumberFilter(field_name='proteins', lookup_expr='exact', exclude=True)
    not_fats = django_filters.NumberFilter(field_name='fats', lookup_expr='exact', exclude=True)
    not_carbs = django_filters.NumberFilter(field_name='carbs', lookup_expr='exact', exclude=True)
    not_price = django_filters.NumberFilter(field_name='price', lookup_expr='exact', exclude=True)
    not_contraindications = django_filters.ModelMultipleChoiceFilter(
        field_name='contraindications',
        queryset=Allergy.objects.all(),
        conjoined=True,
        exclude=True
    )
    not_is_prepared = django_filters.BooleanFilter(field_name='is_prepared', exclude=True)

    class Meta:
        model = Product
        fields = ['name', 'category', 'calories', 'proteins',
                  'fats', 'carbs', 'price', 'contraindications',
                  'is_prepared', 'not_name', 'not_category', 'not_calories',
                  'not_proteins', 'not_fats', 'not_carbs', 'not_price',
                  'not_contraindications', 'not_is_prepared']
