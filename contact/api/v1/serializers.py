from contact.models import Contact, FollowUp, Correspondence
from investment.models import InvestmentType
from region.models import Region
from investment.api.v1.serializers import InvestmentTypeSerializer
from region.api.v1.serializers import RegionSerializer
from rest_framework import serializers


class FollowUpSerializer(serializers.ModelSerializer):
  class Meta:
    model = FollowUp
    fields = ('id', 'begin_date', 'frequency', 'contact')


class CorrespondenceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Correspondence
    fields = ('id', 'created_at', 'correspondence_type', 'item_id', 'contact', 'date')


class ContactSerializer(serializers.ModelSerializer):
  region_preferences = RegionSerializer(many=True, read_only=False, required=False)
  investment_type_preferences = InvestmentTypeSerializer(many=True, read_only=False, required=False)
  upcoming_follow_up = serializers.SerializerMethodField()
  correspondences = CorrespondenceSerializer(required=False, many=True, read_only=True)

  def get_upcoming_follow_up(self, obj):
        return obj.get_upcoming_follow_up()

  class Meta:
    model = Contact
    fields = ('id', 'first_name', 'last_name', 
      'email', 'phone', 'company',
      'minimum_investment_size', 'maximum_investment_size',
      'minimum_irr_return', 'maximum_irr_return',
      'region_preferences', 'investment_type_preferences',
      'notes', 'creator', 'upcoming_follow_up', 'correspondences',
    )

  def create(self, validated_data):
    region_preferences_data = validated_data.pop('region_preferences', [])
    investment_type_preferences_data = validated_data.pop('investment_type_preferences', [])
    contact = Contact.objects.create(**validated_data)
    
    for region_preference_data in region_preferences_data:
      region = Region.objects.get(id=region_preference_data['id'])
      contact.region_preferences.add(region)

    for investment_type_preference_data in investment_type_preferences_data:
      investment_type = InvestmentType.objects.get(id=investment_type_preference_data['id'])
      contact.investment_type_preferences.add(investment_type)
    
    return contact

  def update(self, instance, validated_data):
    region_preferences_data = validated_data.pop('region_preferences', None)
    investment_type_preferences_data = validated_data.pop('investment_type_preferences', None)

    for key, val in validated_data.items():
      setattr(instance, key, val)

    instance.save()

    if region_preferences_data is not None:  # only go through updating if the argument was passed
      instance.region_preferences.clear()
      for region_preference_data in region_preferences_data:
        region = Region.objects.get(id=region_preference_data['id'])
        instance.region_preferences.add(region)

    if investment_type_preferences_data is not None:  # only go through updating if the argument was passed
      instance.investment_type_preferences.clear()
      for investment_type_preference_data in investment_type_preferences_data:
        investment_type = InvestmentType.objects.get(id=investment_type_preference_data['id'])
        instance.investment_type_preferences.add(investment_type)
    
    return instance


class ContactCompanySerialzier(serializers.ModelSerializer):
  emails = serializers.ListField(child = serializers.CharField())
  first_names = serializers.ListField(child = serializers.CharField())
  last_names = serializers.ListField(child = serializers.CharField())

  class Meta:
    model = Contact
    fields = ('company',
      'minimum_investment_size', 'maximum_investment_size',
      'minimum_irr_return', 'maximum_irr_return', 'emails',
      'first_names', 'last_names',
    )