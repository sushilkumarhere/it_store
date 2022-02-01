from django import forms
from .models import ItemDist, ItemModel ,ItemPurchase ,ItemScrap

class DateInput(forms.DateInput):
    input_type = 'date'

class item_list_update(forms.ModelForm):
    class Meta:
        model = ItemDist
        fields = '__all__'

        widgets = {
            'purchase_date': DateInput(attrs={'type': 'date'})
                  }

class Create_ItmDist_Form(forms.ModelForm):
    class Meta:
        model = ItemDist
        fields = '__all__'

        widgets = {
            'purchase_date': DateInput(attrs={'type': 'date'})
                  }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_model'].queryset = ItemModel.objects.none()

        # self.fields['item_sl'].widget.attrs['placeholder'] = 'Item Sl'
        # self.fields['item_configuration'].widget.attrs['placeholder'] = 'Item Configuration'
        for field_name, field in self.fields.items():  # use place holder
            self.fields[field_name].widget.attrs['placeholder'] = field.label

        if 'item_name' in self.data:
            try:
                item_name_id = int(self.data.get('item_name'))
                self.fields['item_model'].queryset = ItemModel.objects.filter(item_name_id=item_name_id).order_by(
                    'model_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['item_model'].queryset = self.instance.item_name.item_model_set.order_by('item_model')


class Item_purchase_create_Form(forms.ModelForm):
    class Meta:
        model = ItemPurchase
        fields = '__all__'

        widgets = {
            'item_purchase_date': DateInput(attrs={'type': 'date'})
           
                  }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_model'].queryset = ItemModel.objects.none()

        # self.fields['item_sl'].widget.attrs['placeholder'] = 'Item Sl'
        # self.fields['item_configuration'].widget.attrs['placeholder'] = 'Item Configuration'
        for field_name, field in self.fields.items():  # use place holder
            self.fields[field_name].widget.attrs['placeholder'] = field.label

        if 'item_name' in self.data:
            try:
                item_name_id = int(self.data.get('item_name'))
                self.fields['item_model'].queryset = ItemModel.objects.filter(item_name_id=item_name_id).order_by(
                    'model_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['item_model'].queryset = self.instance.item_name.item_model_set.order_by('item_model')


class purchase_item_update_form(forms.ModelForm):
    class Meta:
        model = ItemPurchase
        fields = '__all__'

        widgets = {
            'purchase_date': DateInput(attrs={'type': 'date'})
                    }

# Create a Scrap Form

class Create_scrap_Form(forms.ModelForm):
    class Meta:
        model = ItemScrap
        fields = '__all__'

        widgets = {
            'purchase_date': DateInput(attrs={'type': 'date'}),
            'item_scarp_date': DateInput(attrs={'type': 'date'})           
                  }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_model'].queryset = ItemModel.objects.none()

       
        for field_name, field in self.fields.items():  # use place holder
            self.fields[field_name].widget.attrs['placeholder'] = field.label

        if 'item_name' in self.data:
            try:
                item_name_id = int(self.data.get('item_name'))
                self.fields['item_model'].queryset = ItemModel.objects.filter(item_name_id=item_name_id).order_by(
                    'model_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['item_model'].queryset = self.instance.item_name.item_model_set.order_by('item_model')
