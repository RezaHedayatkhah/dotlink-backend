from wsgiref.validate import validator
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[
                UniqueValidator(
                    queryset=User.objects.all(),
                    message="اکانتی با این ایمیل وجود دارد"
            )],
            )
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']


    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "رمزهای عبور یکسان نیستند"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    current_password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password], allow_blank=True)
    confirm_password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'current_password', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs.get('current_password', None):
            if attrs.get('password', None):
                if self.context['request'].user.check_password(attrs.get('current_password', None)):
                    if attrs.get('password', None) != attrs.get('confirm_password', None):
                        raise serializers.ValidationError({"confirm_password": "پسوردها یکسان نیستند"})
                else:
                    raise serializers.ValidationError({"current_password": "پسورد اشتباه است"})
            else:
                raise serializers.ValidationError({'password': 'لطفا رمزعبور جدید را وارد کنید'})        

        return attrs    

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if validated_data.get('password', None):
            instance.set_password(validated_data['password'])
            instance.save()
        
        return instance