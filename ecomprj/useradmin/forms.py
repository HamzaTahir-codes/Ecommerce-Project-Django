from django import forms
from core.models import Product,Category

class AddProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter Product Title", "class":"form-control"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Enter Product Description", "class":"form-control"}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={"placeholder":"$New Price", "class":"form-control"}))
    old_price = forms.DecimalField(widget=forms.NumberInput(attrs={"placeholder":"$Old Price", "class":"form-control"}))
    specifications = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Product Specifications if Any", "class":"form-control"}))
    stock_count = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder":"How many in Stock?", "class":"form-control"}))
    life = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder":"Life of the Product", "class":"form-control"}))
    mfd = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"placeholder":"e.g: 2024-08-09", "class":"form-control", "type": "datetime-local"}),input_formats=["%Y-%m-%d"])
    tags = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter Tags separated by commas", "class":"form-control"}))
    type = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Product Type, e.g. Organic", "class":"form-control"}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(),widget=forms.Select(attrs={"class":"form-control"}))
    digital = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class":"form-check-input"}))
    
    class Meta:
        model = Product
        fields = [
            'title',
            'image',
            'description',
            'price',
            'old_price',
            'specifications',
            'stock_count',
            'life',
            'mfd',
            'digital',
            'tags',
            'type',
            'category'
        ]
