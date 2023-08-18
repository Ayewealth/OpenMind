from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.request import Request

from user.models import *


# --------------------------------------- User model --------------------------------

class UserSerializer(ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='user_detail', lookup_field='username')

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'name',
            'username',
            'email',
            'password',
            'url',
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        Token.objects.create(user=user)
        return user


class UserProfileSerializer(ModelSerializer):
    user = UserSerializer()
    profile_url = serializers.HyperlinkedIdentityField(
        view_name='user_profile_details', lookup_field='pk')

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'profile_pics',
            'bio',
            'profile_url',
        ]

    def update(self, instance, validated_data):
        try:
            user_data = validated_data.pop('user')
            user = instance.user

            instance.profile_pics = validated_data.get(
                'profile_pics', instance.profile_pics)
            instance.bio = validated_data.get('bio', instance.bio)
            instance.save()

            user.name = user_data.get('name', user.name)
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            user.password = user_data.get('password', user.password)
            user.save()
        except:
            # pass
            return super().update(instance, validated_data)

        return instance


# -------------------------------------------------------- Instructor models --------------------------------


class InstructorSerializer(ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='instructor_detail', lookup_field='username')

    class Meta:
        model = Instructor
        fields = [
            'id',
            'name',
            'username',
            'email',
            'password',
            'url',
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        Token.objects.create(user=user)
        return user


class InstructorProfileSerializer(ModelSerializer):
    user = InstructorSerializer()
    profile_url = serializers.HyperlinkedIdentityField(
        view_name='instructor_profile_details', lookup_field='pk')

    class Meta:
        model = InstructorProfile
        fields = [
            'id',
            'user',
            'bio',
            'profile_pics',
            'bank_name',
            'account_name',
            'account_number',
            'profile_url',
        ]

    def update(self, instance, validated_data):
        try:
            user_data = validated_data.pop('user')
            user = instance.user

            instance.profile_pics = validated_data.get(
                'profile_pics', instance.profile_pics)
            instance.bio = validated_data.get('bio', instance.bio)
            instance.bank_name = validated_data.get(
                'bank_name', instance.bank_name)
            instance.account_name = validated_data.get(
                'account_name', instance.account_name)
            instance.account_number = validated_data.get(
                'account_number', instance.account_number)
            instance.save()

            user.name = user_data.get('name', user.name)
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            user.password = user_data.get('password', user.password)
            user.save()
        except:
            # pass
            return super().update(instance, validated_data)

        return instance

# ----------------------------------------------------- Reviews


class ReviewSerializer(ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    course = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'course',
            'rating',
            'comment',
        ]

# -------------------------------------------------------- Courses models --------------------------------


class CourseSerializer(ModelSerializer):
    instructor = serializers.CharField(
        source='instructor.username', read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'what_you_learn',
            'requirements',
            'description',
            'targeted_audience',
            'instructor',
            'price',
            'duration_in_hours',
            "reviews",
        ]


# ---------------------------------------------------------- Cart ------------------------------------------------
class CartCourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'price',
        ]


class CartItemSerializer(ModelSerializer):
    course = CartCourseSerializer(many=False)
    sub_total = serializers.SerializerMethodField(method_name="subTotal")

    class Meta:
        model = Cartitems
        fields = ['id', 'cart', 'course', 'quantity', 'sub_total']

    def subTotal(self, cartitem: Cartitems):
        return cartitem.quantity * cartitem.course.price


class CartSerializer(ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField(method_name="total")

    class Meta:
        model = Cart
        fields = [
            'id',
            'items',
            'grand_total'
        ]

    def total(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.course.price for item in items])
        return total


class AddCartItemSerializer(ModelSerializer):
    course_id = serializers.IntegerField()

    def validate_course_id(self, value):
        if not Course.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                "There is no such course with this ID")
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        course_id = self.validated_data['course_id']
        quantity = self.validated_data['quantity']

        try:
            cartitem = Cartitems.objects.get(
                cart_id=cart_id, course_id=course_id)
            cartitem.quantity += quantity
            cartitem.save()

            self.instance = cartitem

        except:
            self.instance = Cartitems.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = Cartitems
        fields = [
            'id',
            'course_id',
            'quantity',
        ]


class UpdateCartItemSerialer(ModelSerializer):
    class Meta:
        model = Cartitems
        fields = [
            'quantity',
        ]
