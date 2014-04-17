from django import forms

from merchandise.models import BundleOrder, ItemOrder, SIZE_CHOICES

class BundleOrderForm(forms.ModelForm):
    class Meta:
        model = BundleOrder
        exclude = ('school', 'bundle')

    def __init__(self, *args, **kwargs):    
        """If there's an item in this bundle with a size, show that field."""
        super(BundleOrderForm, self).__init__(*args, **kwargs)
        bundle = kwargs['initial']['bundle']
        for item in bundle.items.all():
            if item.has_size:
                self.fields['size'] = forms.ChoiceField(choices=SIZE_CHOICES,
                                                        label='Shirt size')


class ItemOrderForm(forms.ModelForm):
    class Meta:
        model = ItemOrder
        exclude = ('item', 'school', 'bundle_order')

    def __init__(self, *args, **kwargs):
        """If this item has no size attribute, hide that field."""
        super(ItemOrderForm, self).__init__(*args, **kwargs)
        item = kwargs['initial']['item']
        if not item.has_size:
            del self.fields['size']
        else:
            self.fields['size'].required = True
