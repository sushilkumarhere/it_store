from stock.models import ItemDist ,ItemPurchase
import django_filters


class Item_dstFilter(django_filters.FilterSet):
    class Meta:
        model = ItemDist
        fields = ['item_name', 'item_model', 'acblock', 'inst','room_type', ]

    def __init__(self, *args, **kwargs):
        super(Item_dstFilter, self).__init__(*args, **kwargs)
        # at sturtup user doen't push Submit button, and QueryDict (in data) is empty
        if self.data == {}:
            self.queryset = self.queryset.none()

class Item_PurchaseFilter(django_filters.FilterSet):
    class Meta:
        model = ItemPurchase
        fields = ['item_name', 'item_model', ]

    def __init__(self, *args, **kwargs):
        super(Item_PurchaseFilter, self).__init__(*args, **kwargs)
        # at sturtup user doen't push Submit button, and QueryDict (in data) is empty
        if self.data == {}:
            self.queryset = self.queryset.none()

class Item_ScrapFilter(django_filters.FilterSet):
    class Meta:
        model = ItemPurchase
        fields = ['item_name', 'item_model', ]

    def __init__(self, *args, **kwargs):
        super(Item_ScrapFilter, self).__init__(*args, **kwargs)
        # at sturtup user doen't push Submit button, and QueryDict (in data) is empty
        if self.data == {}:
            self.queryset = self.queryset.none()