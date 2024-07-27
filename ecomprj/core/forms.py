from django import forms
from .models import ProductReview

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Add a Review"}))

    class Meta:
        model = ProductReview
        fields = ["review", "rating"]

