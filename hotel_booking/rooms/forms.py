from django import forms
from .models import Quanhuyen

class RoomFilterForm(forms.Form):
    PRICE_RANGES = (
        ('', 'Any Price'),
        ('under_1000000', 'Under 1,000,000đ'),
        ('1000000_2000000', '1,000,000đ - 2,000,000đ'),
        ('2000000_3000000', '2,000,000đ - 3,000,000đ'),
        ('over_3000000', 'Over 3,000,000đ'),
    )
    SORT_OPTIONS = (
        ('popular', 'Most Popular'),
        ('price_low_high', 'Price: Low to High'),
        ('price_high_low', 'Price: High to Low'),
    )
    BED_OPTIONS = (
        ('', 'Any'),
        ('1', '1 Bed'),
        ('2', '2 Beds'),
        ('3+', '3+ Beds'),
    )

    district = forms.ModelChoiceField(
        queryset=Quanhuyen.objects.all(),
        required=False,
        empty_label="All Districts",
        widget=forms.RadioSelect(attrs={'class': 'form-radio text-blue-600'})
    )
    
    price_range = forms.ChoiceField(
        choices=PRICE_RANGES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-radio text-blue-600'})
    )

    sort_by = forms.ChoiceField(
        choices=SORT_OPTIONS,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-radio text-blue-600'})
    )

    beds = forms.ChoiceField(
        choices=BED_OPTIONS,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-radio text-blue-600'})
    )