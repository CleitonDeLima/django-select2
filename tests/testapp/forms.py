from django import forms
from django.utils.encoding import force_str

from django_select2.forms import (
    HeavySelect2MultipleWidget,
    HeavySelect2Widget,
    ModelSelect2MultipleWidget,
    ModelSelect2TagWidget,
    ModelSelect2Widget,
    Select2MultipleWidget,
    Select2Widget,
)
from tests.testapp import models
from tests.testapp.models import Album, City, Country


class TitleSearchFieldMixin:
    search_fields = ["title__icontains", "pk__startswith"]


class TitleModelSelect2Widget(TitleSearchFieldMixin, ModelSelect2Widget):
    pass


class TitleModelSelect2MultipleWidget(
    TitleSearchFieldMixin, ModelSelect2MultipleWidget
):
    pass


class GenreSelect2TagWidget(TitleSearchFieldMixin, ModelSelect2TagWidget):
    model = models.Genre

    def create_value(self, value):
        self.get_queryset().create(title=value)


class ArtistCustomTitleWidget(ModelSelect2Widget):
    model = models.Artist
    search_fields = ["title__icontains"]

    def label_from_instance(self, obj):
        return force_str(obj.title).upper()


class GenreCustomTitleWidget(ModelSelect2Widget):
    model = models.Genre
    search_fields = ["title__icontains"]

    def label_from_instance(self, obj):
        return force_str(obj.title).upper()


class ArtistDataViewWidget(HeavySelect2Widget):
    data_view = "heavy_data_1"


class PrimaryGenreDataUrlWidget(HeavySelect2Widget):
    data_url = "/heavy_data_2/"


class AlbumSelect2WidgetForm(forms.ModelForm):
    class Meta:
        model = models.Album
        fields = (
            "artist",
            "primary_genre",
        )
        widgets = {
            "artist": Select2Widget,
            "primary_genre": Select2Widget,
        }


class AlbumSelect2MultipleWidgetForm(forms.ModelForm):
    class Meta:
        model = models.Album
        fields = (
            "genres",
            "featured_artists",
        )
        widgets = {
            "genres": Select2MultipleWidget,
            "featured_artists": Select2MultipleWidget,
        }


class AlbumModelSelect2WidgetForm(forms.ModelForm):
    class Meta:
        model = models.Album
        fields = (
            "artist",
            "primary_genre",
        )
        widgets = {
            "artist": ArtistCustomTitleWidget(),
            "primary_genre": GenreCustomTitleWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["primary_genre"].initial = 2


class AlbumModelSelect2MultipleWidgetRequiredForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = (
            "genres",
            "featured_artists",
        )
        widgets = {
            "genres": TitleModelSelect2MultipleWidget,
            "featured_artists": TitleModelSelect2MultipleWidget,
        }


class ArtistModelSelect2MultipleWidgetForm(forms.Form):
    title = forms.CharField(max_length=50)
    genres = forms.ModelMultipleChoiceField(
        widget=ModelSelect2MultipleWidget(
            queryset=models.Genre.objects.all(),
            search_fields=["title__icontains"],
        ),
        queryset=models.Genre.objects.all(),
        required=True,
    )

    featured_artists = forms.ModelMultipleChoiceField(
        widget=ModelSelect2MultipleWidget(
            queryset=models.Artist.objects.all(),
            search_fields=["title__icontains"],
        ),
        queryset=models.Artist.objects.all(),
        required=False,
    )


NUMBER_CHOICES = [
    (1, "One"),
    (2, "Two"),
    (3, "Three"),
    (4, "Four"),
]


class Select2WidgetForm(forms.Form):
    number = forms.ChoiceField(
        widget=Select2Widget, choices=NUMBER_CHOICES, required=False
    )


class HeavySelect2WidgetForm(forms.Form):
    artist = forms.ChoiceField(widget=ArtistDataViewWidget(), choices=NUMBER_CHOICES)
    primary_genre = forms.ChoiceField(
        widget=PrimaryGenreDataUrlWidget(),
        required=False,
        choices=NUMBER_CHOICES,
    )


class HeavySelect2MultipleWidgetForm(forms.Form):
    title = forms.CharField(max_length=50)
    genres = forms.MultipleChoiceField(
        widget=HeavySelect2MultipleWidget(
            data_view="heavy_data_1",
            choices=NUMBER_CHOICES,
            attrs={"data-minimum-input-length": 0},
        ),
        choices=NUMBER_CHOICES,
    )
    featured_artists = forms.MultipleChoiceField(
        widget=HeavySelect2MultipleWidget(
            data_view="heavy_data_2",
            choices=NUMBER_CHOICES,
            attrs={"data-minimum-input-length": 0},
        ),
        choices=NUMBER_CHOICES,
        required=False,
    )

    def clean_title(self):
        if len(self.cleaned_data["title"]) < 3:
            raise forms.ValidationError("Title must have more than 3 characters.")
        return self.cleaned_data["title"]


class ModelSelect2TagWidgetForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ["genres"]
        widgets = {"genres": GenreSelect2TagWidget}


class AddressChainedSelect2WidgetForm(forms.Form):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        label="Country",
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            max_results=500,
            dependent_fields={"city": "cities"},
            attrs={"data-minimum-input-length": 0},
        ),
    )

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label="City",
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            dependent_fields={"country": "country"},
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )

    city2 = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label="City not Interdependent",
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            dependent_fields={"country": "country"},
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )


class GroupieForm(forms.ModelForm):
    class Meta:
        model = models.Groupie
        fields = "__all__"
        widgets = {"obsession": ArtistCustomTitleWidget}
