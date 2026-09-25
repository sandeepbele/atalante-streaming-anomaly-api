import json

import jsonschema
from django import forms
from .models import PostgresSourceModel
from django.utils.safestring import mark_safe
from collections import OrderedDict
from typing import List, Dict

class PostgresSourceForm(forms.Form):

    field_class_attr = "form-control form-control-sm"

    def_id = forms.CharField(widget=forms.HiddenInput)
    type = forms.CharField(widget=forms.HiddenInput)
    #

    name = forms.CharField(required=True,initial="my-postgres-db",
                           widget=forms.TextInput(attrs={"class":field_class_attr}),
                           help_text="Name for this source")
    host = forms.CharField(required=True,
                           initial="localhost",
                           widget=forms.TextInput(attrs={"class":field_class_attr}),
                           help_text="Hostname of the database.")
    port = forms.IntegerField(required=True, initial=5432,
                              widget=forms.NumberInput(attrs={"class":field_class_attr}),
                              help_text="Port of the database.")
    database = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": field_class_attr}),
                               help_text="Database to connect to.")
    schemas = forms.CharField(required=True, initial="public",
                              widget=forms.TextInput(attrs={"class":field_class_attr}),
                              help_text="The list of schemas (case sensitive, comma-separated) to sync from. Defaults to public.")
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={"class":field_class_attr}),
                               help_text="Postgres username.")
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"class":field_class_attr}),
                               help_text="Postgres password.")
    advanced_settings_default = {
                                    "ssl": False,
                                    "replication_method":{"method":"Standard"},
                                    "tunnel_method":{"tunnel_method":"NO_TUNNEL"},
                                    "ssl_mode": {"mode": "disable"},
                                 }

    advanced_settings = forms.CharField(required=False,
                                        initial= json.dumps(advanced_settings_default),
                                        widget=forms.Textarea(attrs={"class":field_class_attr}),
                                        help_text="Advanced settings related to SSL and replication methods.")

    def get_source_config(self):

        return {
            **{ field: self.cleaned_data[field] for field in ['host','port','database','username','password'] },
            'schemas': self.cleaned_data['schemas'].split(","),
            **json.loads(self.cleaned_data['advanced_settings'])
        }

    def getName(self):
        return self.cleaned_data['name']

    def getLabel(self):
        return "Postgres"

'''

# Create a Django form object dynamically based on the schema
class JsonSchemaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.schema = kwargs.get("schema")
        #if self.schema is not None:
        for field_name, field_data in self.data["properties"].items():
            field_type = None
            if field_data["type"] == "string":
                if field_data.get("format") == "email":
                    field_type = forms.EmailField
                else:
                    field_type = forms.CharField
            elif field_data["type"] == "number":
                field_type = forms.DecimalField
            if field_type:
                self.fields[field_name] = field_type(required=("name" in self.data.get("required", [])))

    def clean(self):
        super().clean()
        # Validate the form data against the JSON schema
        jsonschema.validate(dict(self.cleaned_data), self.data)
'''

from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


class JSONSchemaForm(forms.Form):

    def __init__(self, json_schema, *args, **kwargs):
        super(JSONSchemaForm, self).__init__(*args, **kwargs)
        self.json_schema = json_schema
        self.display_none_fields = {}
        self.ordered_field_keys = {}
        self.previous_field_order = 0
        self.fields = OrderedDict()
        parsed_fields = self.parse_schema(json_schema)
        for order in sorted(self.ordered_field_keys.keys()):
            field_name = self.ordered_field_keys[order]
            self.fields[field_name] = parsed_fields[field_name]

        print(self.fields)

    def parse_schema(self, schema):

        fields = OrderedDict()
        properties = schema.get('properties', {})
        required_fields = set(schema.get('required', []))

        for field_name, field_schema in properties.items():
            field_type = field_schema.get('type')
            field_title = field_schema.get('title', field_name.capitalize())
            field_description = field_schema.get('description', '')
            order = field_schema.get('order', 0)
            if order not in self.ordered_field_keys:
                self.ordered_field_keys[order] = field_name
                self.previous_field_order = order

            field_args = {
                'label': field_title,
                'help_text': field_description,
                'required': field_name in required_fields
            }

            if field_type == 'string' and field_schema.get('const') is None:
                field_args['widget'] = forms.TextInput()
                field_args['initial'] = field_schema.get('default', '')
                fields[field_name] = forms.CharField(**field_args)
            elif field_type == 'integer':
                field_args['widget'] = forms.NumberInput()
                field_args['initial'] = field_schema.get('default', 0)
                fields[field_name] = forms.IntegerField(**field_args)
            elif field_type == 'boolean':
                field_args['widget'] = forms.RadioSelect()
                field_args['initial'] = field_schema.get('default', False)
                fields[field_name] = forms.BooleanField(**field_args)
            elif field_type == 'object':
                if 'oneOf' in field_schema:
                    related_fields = self.parse_one_of(field_name, field_schema['oneOf'])
                    related_order = self.previous_field_order + 0.01
                    for related_field in related_fields:
                        self.ordered_field_keys[related_order] = related_field
                        related_order += 0.01
                    fields.update(related_fields)
                else:
                    fields.update(self.parse_schema(field_schema))

            elif field_type == 'array':
                item_type = field_schema.get('items', {}).get('type')
                if item_type == 'string':
                    field_args['widget'] = forms.TextInput()
                    field_args['initial'] = ",".join(field_schema.get('default', ''))
                    fields[field_name] = forms.CharField(**field_args)
                elif item_type == 'object':
                    field_args['fields'] = self.parse_schema(field_schema.get('items', {}))
                    fields[field_name] = forms.FormSet(**field_args)
                else:
                    field_args['widget'] = forms.SelectMultiple()
                    field_args['choices'] = [(i, i) for i in field_schema.get('items', [])]
                    field_args['initial'] = field_schema.get('default', [])
                    fields[field_name] = forms.MultipleChoiceField(**field_args)

        return fields

    def parse_one_of(self, field_name, one_of):
        fields = {}
        choices = []
        fields_for_selectbox = {}
        for i, field_schema in enumerate(one_of):
            title = field_schema.get('title', field_name.capitalize())
            choice_val = None
            for key, value in field_schema.get('properties', {}).items():
                if 'const' in value:
                    choices.append((value['const'], title))
                    choice_val =  value['const']
                    break;

            related_fields: Dict[str,forms.Field] = self.parse_schema(field_schema)
            class_name = f"{choice_val.replace(' ','_')}_fields"
            parent_class = f"parent_is_{field_name}"

            for f_name, field in related_fields.items():

                if f_name in self.display_none_fields:
                    self.display_none_fields[f_name]['class'] = f"{self.display_none_fields[f_name]['class']} {class_name}"
                else:
                    self.display_none_fields[f_name] = { 'class': f"{class_name}",'parent_class': f"{parent_class}", 'style': "display:none" }

            fields_for_selectbox.update(related_fields)

        condition_field_args = {
            'label': field_name.capitalize(),
            'help_text': '',
            'required': True,
            'choices': choices,
            'widget': forms.Select(attrs={'onchange': 'showSelect(event)'})
        }
        fields[field_name] = forms.ChoiceField(**condition_field_args)
        fields.update(fields_for_selectbox)

        return fields


class JSONSchemaForm2(forms.Form):

    def __init__(self, json_schema, source_type,source_def_id, *args, **kwargs):
        super(JSONSchemaForm2, self).__init__(*args, **kwargs)
        if json_schema is not None:
            self.json_schema = json_schema
            self.display_none_fields = {}
            self.fields = OrderedDict()
            self.fields.update(self.parse_schema_2(json_schema))
            self.fields['configured_source'] = forms.CharField(widget=forms.HiddenInput(), initial=source_type)
            self.fields['source_def_id'] = forms.CharField(widget=forms.HiddenInput(), initial=source_def_id)

    def parse_schema_2(self, schema):

        fields = OrderedDict()

        properties = schema.get('properties', {})
        required_fields = set(schema.get('required', []))

        sorted_fields = sorted(properties.items(), key=lambda field_schema_tuple: field_schema_tuple[1].get('order', 999))
        for field_name, field_schema in sorted_fields:
            field_args = {
                'label': field_schema.get('title', field_name.capitalize()),
                'help_text': field_schema.get('description', ''),
                #'required': field_name in required_fields
                'required': False
            }

            field_extractor = {
                'string': self.parse_string,
                'integer': self.parse_integer,
                'boolean': self.parse_boolean,
                'object': self.parse_object,
                'array': self.parse_array,
            }
            field_type = field_schema.get('type')
            if field_type in field_extractor:
                fields.update(field_extractor[field_type](field_name, field_schema, field_args))
            else:
                raise Exception(f"Unknown field type {field_type}")

        return fields

    def parse_string(self, field_name, field_schema, field_args):
        if field_schema.get('const') is not None:
            return {}
        if 'password' in field_name.lower():
            field_args['widget'] = forms.PasswordInput(attrs={"class": "form-control form-control-sm"})
        else:
            field_args['widget'] = forms.TextInput(attrs={"class": "form-control form-control-sm"})
        field_args['initial'] = field_schema.get('default', '')
        return {field_name: forms.CharField(**field_args)}

    def parse_integer(self, field_name, field_schema, field_args):
        field_args['widget'] = forms.NumberInput(attrs={"class": "form-control form-control-sm"})
        field_args['initial'] = field_schema.get('default', 0)
        return {field_name: forms.IntegerField(**field_args)}

    def parse_boolean(self, field_name, field_schema, field_args):
        field_args['widget'] = forms.CheckboxInput(attrs={"class": "","style":"position: relative;"})
        field_args['initial'] = field_schema.get('default', False)
        return {field_name: forms.BooleanField(**field_args)}

    def parse_object(self, field_name, field_schema, field_args):
        if 'oneOf' in field_schema:
            return self.parse_one_of(field_name, field_schema['oneOf'])
        else:
            return self.parse_schema(field_schema)

    def parse_one_of(self, field_name, one_of):

        fields = OrderedDict()
        choices = []
        fields_for_selectbox = OrderedDict()
        for i, field_schema in enumerate(one_of):
            title = field_schema.get('title', field_name.capitalize())
            choice_val = None
            for key, value in field_schema.get('properties', {}).items():
                if 'const' in value:
                    choices.append((value['const'], title))
                    choice_val =  value['const']
                    break;

            related_fields: Dict[str,forms.Field] = self.parse_schema_2(field_schema)
            class_name = f"{choice_val.replace(' ','_')}_fields"
            parent_class = f"parent_is_{field_name}"

            for f_name, field in related_fields.items():
                if f_name in self.display_none_fields:
                    self.display_none_fields[f_name]['class'] = f"{self.display_none_fields[f_name]['class']} {class_name}"
                else:
                    self.display_none_fields[f_name] = { 'class': f"{class_name}",'parent_class': f"{parent_class}", 'style': "display:none" }

            fields_for_selectbox.update(related_fields)

        condition_field_args = {
            'label': field_name.capitalize(),
            'help_text': '',
            'required': False,
            'choices': choices,
            'widget': forms.Select(attrs={'onchange': 'showSelect(event)',"class": "form-control form-control-sm" })
        }
        fields[field_name] = forms.ChoiceField(**condition_field_args)
        fields.update(fields_for_selectbox)

        return fields

    def parse_array(self, field_name, field_schema, field_args):
        field_args['widget'] = forms.SelectMultiple(attrs={"class": "form-control form-control-sm" })
        field_args['choices'] = [(i, i) for i in field_schema.get('default', [])]
        field_args['initial'] = field_schema.get('default', [])
        return {field_name: forms.MultipleChoiceField(**field_args) }


class SourceFormFactory():

    __form_mapping = {
        'source-postgres': PostgresSourceForm,
    }

    @staticmethod
    def get_form(source_type,**kwargs):
        return SourceFormFactory.__form_mapping[source_type](**kwargs) or None
