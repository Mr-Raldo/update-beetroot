from rest_framework import serializers
from .models import Profile, Subscription, Wallet, WalletTransaction

class ProfileSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Profile
        fields = '__all__'

    # @staticmethod
    def get_image_url(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        else:
            return ''

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'

class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = '__all__'
