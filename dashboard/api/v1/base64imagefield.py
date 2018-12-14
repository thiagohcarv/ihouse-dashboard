import base64
from drf_extra_fields.fields import Base64ImageField as Base64ImageFieldDRF
from rest_framework import serializers


class Base64ImageField(Base64ImageFieldDRF):

    def to_representation(self, file):
        if self.represent_in_base64:
            try:
                return base64.b64encode(file.read()).decode()
            except Exception:
                try:
                    with open(file.path, 'rb') as f:
                        return base64.b64encode(f.read()).decode()
                except Exception:
                    pass

                raise IOError("Error encoding file")
        else:
            return super(Base64ImageField, self).to_representation(file)


class ImageSerializer(serializers.Serializer):

    image = Base64ImageField(represent_in_base64=True, required=False)
    file = Base64ImageField(represent_in_base64=True, required=False)

    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError('Nenhum arquivo foi submetido.', code='required')

        return value