from rest_framework import serializers
from .models import Company, Tag, Contact, Interaction


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ['owner']


class CompanySerializer(serializers.ModelSerializer):
    contact_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def get_contact_count(self, obj):
        return obj.contacts.count()


class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = '__all__'
        read_only_fields = ['created_at']


class ContactSerializer(serializers.ModelSerializer):
    interactions = InteractionSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        source='tags',
        write_only=True,
        required=False
    )

    full_name = serializers.SerializerMethodField()

    # 🔴 CRITICAL FIX: explicit company handling
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        required=False,
        allow_null=True
    )

    company_name = serializers.CharField(
        source='company.name',
        read_only=True
    )

    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"