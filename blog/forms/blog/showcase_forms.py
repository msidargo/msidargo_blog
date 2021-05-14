# Django imports
from django import forms
from django.forms import TextInput, Select, FileInput

# Third-party app imports
from ckeditor.widgets import CKEditorWidget

# Blog app imports
from blog.models.showcase_models import Showcase
from blog.models.category_models import Category


class ShowcaseCreateForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.filter(
                                      approved=True),
                                      empty_label="Select Category",
                                      widget=forms.Select(attrs=
                                                          {
                                                              "class": "form-control selectpicker",
                                                              "type": "text",
                                                              "name": "showcase-category",
                                                              "id": "showcaseCategory",
                                                              "data-live-search": "true"
                                                          }
                                      )
                                    )

    class Meta:

        # Showcase status constants
        DRAFTED = "DRAFTED"
        PUBLISHED = "PUBLISHED"

        # CHOICES
        STATUS_CHOICES = (
            (DRAFTED, 'Draft'),
            (PUBLISHED, 'Publish'),
        )

        model = Showcase
        fields = ["title", "category", "image", "image_credit", "body", "tags", "status"]
        widgets = {
            'title': TextInput(attrs={
                                     'name': "showcase-title",
                                     'class': "form-control",
                                     'placeholder': "Enter Showcase Title",
                                     'id': "showcaseTitle"
                                     }),

            'image': FileInput(attrs={
                                        "class": "form-control clearablefileinput",
                                        "type": "file",
                                        "id": "showcaseImage",
                                        "name": "showcase-image"
                                      }

                               ),

            'image_credit': TextInput(attrs={
                'name': "image_credit",
                'class': "form-control",
                'placeholder': "Example: made4dev.com (Premium Programming T-shirts)",
                'id': "image_credit"
            }),

            'body': forms.CharField(widget=CKEditorWidget(config_name="default", attrs={
                       "rows": 5, "cols": 20,
                       'id': 'content',
                       'name': "showcase_content",
                       'class': "form-control",
                       })),

            'tags': TextInput(attrs={
                                     'name': "tags",
                                     'class': "form-control",
                                     'placeholder': "Example: sports, game, politics",
                                     'id': "tags",
                                     'data-role': "tagsinput"
                                     }),

            'status': Select(choices=STATUS_CHOICES,
                             attrs=
                             {
                                 "class": "form-control selectpicker",
                                 "name": "status", "type": "text",
                                 "id": "showcaseStatus",
                                 "data-live-search": "true",
                                 "title": "Select Status"
                             }
                             ),
        }


class ShowcaseUpdateForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.filter(
                                      approved=True),
                                      empty_label="Select Category",
                                      widget=forms.Select(attrs=
                                                          {
                                                              "class": "form-control selectpicker",
                                                              "type": "text",
                                                              "name": "showcase-category",
                                                              "id": "showcaseCategory",
                                                              "data-live-search": "true"
                                                          }
                                      )
                                    )

    class Meta:
        # Showcase status constants
        DRAFTED = "DRAFTED"
        PUBLISHED = "PUBLISHED"

        # CHOICES
        STATUS_CHOICES = (
            (DRAFTED, 'Draft'),
            (PUBLISHED, 'Publish'),
        )

        model = Showcase
        fields = ["title", "category", "image", "image_credit", "body", "tags", "status"]
        widgets = {
            'title': TextInput(attrs={
                'name': "showcase-title",
                'class': "form-control",
                'placeholder': "Enter Showcase Title",
                'id': "showcaseTitle"
            }),

            'image_credit': TextInput(attrs={
                'name': "image_credit",
                'class': "form-control",
                'placeholder': "Example: made4dev.com (Premium Programming T-shirts)",
                'id': "image_credit"
            }),

            'status': Select(choices=STATUS_CHOICES,
                             attrs=
                             {
                                 "class": "form-control selectpicker",
                                 "name": "status", "type": "text",
                                 "id": "showcaseStatus",
                                 "data-live-search": "true",
                                 "title": "Select Status"
                             }
                             ),
            'body': forms.CharField(widget=CKEditorWidget(config_name="default", attrs={
                       "rows": 5, "cols": 20,
                       'id': 'content',
                       'name': "showcase_content",
                       'class': "form-control",
                       })),

            'image': FileInput(attrs={
                "class": "form-control clearablefileinput",
                "type": "file",
                "id": "showcaseImage",
                "name": "showcase-image",
            }

            ),

        }
