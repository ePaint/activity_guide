from typing import Any
from django import forms
from activity_guide.settings import MAX_ADS_PER_SECTION
from .models import Ad

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['image', 'click_action', 'click_action_target']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'click_action': forms.Select(),
            'click_action_target': forms.TextInput(),
        }

    def __init__(self, *args: Any, section: str = None, position: int = 0, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['click_action'].required = False
        self.fields['click_action_target'].required = False
        
    def save(self, commit=True):
        form_object = super().save(commit=False)
        image = self.cleaned_data.get('image')
            
        if image:
            self.instance.image = image
        
        print(f'Image: {image}. Instance: {self.instance}. Commit: {commit}')
        
        if commit:
            form_object.save()
        return form_object

class BaseAdsFormSet(forms.BaseModelFormSet):
    def __init__(self, *args: Any, location: str = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.queryset = Ad.objects.filter(location__location=location)
    
    def save(self):
        for form in self.forms:
            AdForm(data=form.cleaned_data, instance=form.instance).save()

class BaseHomepageTopAdsFormSet(BaseAdsFormSet):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, location='H', **kwargs)

class BaseSearchResultsTopAdsFormSet(BaseAdsFormSet):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, location='S', **kwargs)
        
class BaseSearchResultsSidebar1AdsFormSet(BaseAdsFormSet):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, location='S1', **kwargs)

class BaseSearchResultsSidebar2AdsFormSet(BaseAdsFormSet):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, location='S2', **kwargs)

class BaseCategoriesTopLeftAdsFormSet(BaseAdsFormSet):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, location='C1', **kwargs)

class BaseCategoriesTopMiddleAdsFormSet(BaseAdsFormSet):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, location='C2', **kwargs)

class BaseCategoriesTopRightAdsFormSet(BaseAdsFormSet):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, location='C3', **kwargs)

class BaseArtsCategorySidebarAdsFormSet(BaseAdsFormSet):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, location='ARTS', **kwargs)

class BaseSportsCategorySidebarAdsFormSet(BaseAdsFormSet):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, location='SPORTS', **kwargs)

class BaseSTEMCategorySidebarAdsFormSet(BaseAdsFormSet):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, location='STEM', **kwargs)


HomepageTopAdsFormSet = forms.modelformset_factory(Ad, form=AdForm, formset=BaseHomepageTopAdsFormSet, max_num=MAX_ADS_PER_SECTION, extra=MAX_ADS_PER_SECTION)
SearchResultsTopAdsFormSet = forms.modelformset_factory(Ad, form=AdForm, formset=BaseSearchResultsTopAdsFormSet, max_num=MAX_ADS_PER_SECTION, extra=MAX_ADS_PER_SECTION)
SearchResultsSidebar1AdsFormSet = forms.modelformset_factory(Ad, form=AdForm, formset=BaseSearchResultsSidebar1AdsFormSet, max_num=MAX_ADS_PER_SECTION, extra=MAX_ADS_PER_SECTION)
SearchResultsSidebar2AdsFormSet = forms.modelformset_factory(Ad, form=AdForm, formset=BaseSearchResultsSidebar2AdsFormSet, max_num=MAX_ADS_PER_SECTION, extra=MAX_ADS_PER_SECTION)
CategoriesTopLeftAdsFormSet = forms.modelformset_factory(Ad, form=AdForm, formset=BaseCategoriesTopLeftAdsFormSet, max_num=MAX_ADS_PER_SECTION, extra=MAX_ADS_PER_SECTION)
CategoriesTopMiddleAdsFormSet = forms.modelformset_factory(Ad, form=AdForm, formset=BaseCategoriesTopMiddleAdsFormSet, max_num=MAX_ADS_PER_SECTION, extra=MAX_ADS_PER_SECTION)
CategoriesTopRightAdsFormSet = forms.modelformset_factory(Ad, form=AdForm, formset=BaseCategoriesTopRightAdsFormSet, max_num=MAX_ADS_PER_SECTION, extra=MAX_ADS_PER_SECTION)
ArtsCategorySidebarAdsFormSet = forms.modelformset_factory(Ad, form=AdForm, formset=BaseArtsCategorySidebarAdsFormSet, max_num=MAX_ADS_PER_SECTION, extra=MAX_ADS_PER_SECTION)
SportsCategorySidebarAdsFormSet = forms.modelformset_factory(Ad, form=AdForm, formset=BaseSportsCategorySidebarAdsFormSet, max_num=MAX_ADS_PER_SECTION, extra=MAX_ADS_PER_SECTION)
STEMCategorySidebarAdsFormSet = forms.modelformset_factory(Ad, form=AdForm, formset=BaseSTEMCategorySidebarAdsFormSet, max_num=MAX_ADS_PER_SECTION, extra=MAX_ADS_PER_SECTION)

MODEL_FORM_SETS = {
    'H': HomepageTopAdsFormSet,
    'S': SearchResultsTopAdsFormSet,
    'S1': SearchResultsSidebar1AdsFormSet,
    'S2': SearchResultsSidebar2AdsFormSet,
    'C1': CategoriesTopLeftAdsFormSet,
    'C2': CategoriesTopMiddleAdsFormSet,
    'C3': CategoriesTopRightAdsFormSet,
    'ARTS': ArtsCategorySidebarAdsFormSet,
    'SPORTS': SportsCategorySidebarAdsFormSet,
    'STEM': STEMCategorySidebarAdsFormSet,
}
