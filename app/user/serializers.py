from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
  """serializer for user object"""

  class Meta:
    model = get_user_model()
    fields = ('email', 'password', 'name')
    extra_kwargs = {'password':{'write_only': True, 'min_length': 4}}
  

  def create(self, validated_data):
    """creates and returns a new user with encrypted password"""
    return get_user_model().objects.create_user(**validated_data)

  def update(self, instance, validated_data):
    """updates a user and returns password after setting it correctly"""
    password = validated_data.pop('password', None)
    user = super().update(instance, validated_data)

    if password:
      user.set_password(password)
      user.save()
    
    return user


class AuthTokenSerializer(serializers.Serializer):
  """serializer for user auth object"""
  email = serializers.CharField()
  password = serializers.CharField(
    style={'input_type': 'password'},
    trim_whitespace=False
  )

  def validate(self, attrs):
    """validates and authenticates user"""
    email= attrs.get('email')
    password = attrs.get('password')

    user = authenticate(
      request=self.context.get('request'),
      username=email,
      password=password
    )
    if not user:
      msg = ('Unable to authenticate')
      raise serializers.ValidationError(msg, code='authentication')
    attrs['user'] = user
    return attrs