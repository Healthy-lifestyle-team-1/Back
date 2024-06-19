import django_filters
from .models import Product, Category, Tag


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        conjoined=True  # чтобы выбрать продукты, относящиеся ко всем указанным категориям
    )
    tag = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        conjoined=True  # чтобы выбрать продукты, относящиеся ко всем указанным тегам
    )
    image = django_filters.CharFilter(lookup_expr='icontains')
    calories__lt = django_filters.NumberFilter(field_name='calories', lookup_expr='lt')
    calories__gt = django_filters.NumberFilter(field_name='calories', lookup_expr='gt')
    proteins__lt = django_filters.NumberFilter(field_name='proteins', lookup_expr='lt')
    proteins__gt = django_filters.NumberFilter(field_name='proteins', lookup_expr='gt')
    fats__lt = django_filters.NumberFilter(field_name='fats', lookup_expr='lt')
    fats__gt = django_filters.NumberFilter(field_name='fats', lookup_expr='gt')
    carbs__lt = django_filters.NumberFilter(field_name='carbs', lookup_expr='lt')
    carbs__gt = django_filters.NumberFilter(field_name='carbs', lookup_expr='gt')
    price = django_filters.NumberFilter()
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    is_prepared = django_filters.ChoiceFilter(choices=Product.TYPES_OF_PREPARING)

    # Антифильтры
    not_title = django_filters.CharFilter(field_name='title', lookup_expr='iexact', exclude=True)
    not_category = django_filters.ModelMultipleChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        conjoined=True,
        exclude=True
    )
    not_tag = django_filters.ModelMultipleChoiceFilter(
        field_name='tag',
        queryset=Tag.objects.all(),
        conjoined=True,
        exclude=True
    )
    #not_calories = django_filters.NumberFilter(field_name='calories', lookup_expr='exact', exclude=True)
    #not_proteins = django_filters.NumberFilter(field_name='proteins', lookup_expr='exact', exclude=True)
    #not_fats = django_filters.NumberFilter(field_name='fats', lookup_expr='exact', exclude=True)
    #not_carbs = django_filters.NumberFilter(field_name='carbs', lookup_expr='exact', exclude=True)
    #not_price = django_filters.NumberFilter(field_name='price', lookup_expr='exact', exclude=True)
    not_is_prepared = django_filters.ChoiceFilter(field_name='is_prepared', choices=Product.TYPES_OF_PREPARING, exclude=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'category', 'tag', 'image',
                  'calories__lt', 'calories__gt',
                  'proteins__lt', 'proteins__gt',
                  'fats__lt', 'fats__gt',
                  'carbs__lt', 'carbs__gt',
                  'price', 'price__lt', 'price__gt',
                  'is_prepared', 'not_title', 'not_category', 'not_tag', 'not_is_prepared']
