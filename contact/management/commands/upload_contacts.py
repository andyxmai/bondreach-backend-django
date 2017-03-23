import csv
import os
from contact.models import Contact
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
  help = 'Uploads contacts from Outlook contacts'

  def handle(self, *args, **options):
    # Variables - CHANGE THESE
    creator_id = '4873d0ab-ef1e-4979-a089-1dfece80907c'
    region_name_id_map = {
      'West': 'e5f0938e-ad3e-4cc5-a7d0-bdb8164ba839',
      'Northeast': '72582df9-d000-46c5-90f8-b8875b5f8ffd',
      'South': 'bc3de2c8-1936-47d0-a090-3b77a58f160f/',
      'Midwest': '44cc6449-aef6-41cd-b510-89e044e797fb'
    }
    investment_type_id_map = {
      'Industrial': '74565a77-1544-47cd-b689-2f97b4f7d4f5',
      'Office': 'f5b2e7e0-11b5-4d0e-958f-3d7bd62a1f72',
      'Multifamily': '70c599e1-96cc-4033-befc-83351d57c1d7',
      'Retail': '1a19ee23-3366-48a3-ba6b-7aecdd6b536c',
      'Hospitality': 'df1fcfcf-4147-445c-b3a9-c14edddf7650',
      'Land': 'cebc6a14-fac6-4895-83bf-357d1d12f18c'
    }

    # contacts_file = open(os.path.join(settings.BASE_DIR, 'zach_sm.csv'))
    with open(os.path.join(settings.BASE_DIR, 'zach_sm.csv'), 'r', encoding="ISO-8859-1") as csvfile:
      contactreader = csv.DictReader(csvfile)
      counter = 0

      for row in contactreader:
        if row['First Name'] == '':
          continue

        # Investment types, the icky one!
        original_investment_types_str = row['Categories'].replace('Multi-Housing', 'Multifamily').replace('Hotel', 'Hospitality')
        override_investment_types_str = row['investment type preference']
        investment_type_preferences_set = set()
        if original_investment_types_str:
          original_investment_types = original_investment_types_str.split(';')
          if len(original_investment_types):
            if 'Multifamily' in original_investment_types or 'Hospitality' in original_investment_types:
              for original_investment_type in original_investment_types:
                if original_investment_type != 'Single Family' and original_investment_type != 'Lender':
                  investment_type_id = investment_type_id_map[original_investment_type]
                  investment_type_preferences_set.add(investment_type_id)

              # Overrides
              if override_investment_types_str:
                override_investment_types = override_investment_types_str.split(',')
                for override_investment_type in override_investment_types:
                  investment_type_id = investment_type_id_map[override_investment_type]
                  investment_type_preferences_set.add(investment_type_id)
            else:
              continue
        else:
          investment_type_id = investment_type_id_map['Multifamily']
          investment_type_preferences_set.add(investment_type_id)


        
        phone = row['Business Phone'].replace('(', '').replace(')', '').replace('-', '').replace(' ', '').replace('.', '').replace('+1', '')
        
        minimum_investment_size = row['min investment size'].replace(',', '')
        maximum_investment_size = row['max investment size'].replace(',', '')


        default_region_preferences = ['West', 'Northeast', 'Midwest', 'South']
        region_preferences_str = row['region preference']
        override_region_preferences_list = []
        if region_preferences_str:
          override_region_preferences_list = region_preferences_str.split(',')

        region_preferences = []
        if len(override_region_preferences_list):
          for override_region_preference in override_region_preferences_list:
            region_preference_id = region_name_id_map[override_region_preference]
            region_preferences.append(region_preference_id) 
        else:
          for region_preference in default_region_preferences:
            region_preference_id = region_name_id_map[region_preference]
            region_preferences.append(region_preference_id)  



        # Contact attributes
        first_name = row['First Name']
        last_name = row['Last Name']
        email = row['E-mail Address']
        company = row['Company']
        phone = row['Business Phone'].replace('(', '').replace(')', '').replace('-', '').replace(' ', '').replace('.', '').replace('+1', '')
        minimum_investment_size = int(minimum_investment_size) if minimum_investment_size else 0
        maximum_investment_size = int(maximum_investment_size) if maximum_investment_size else 2000000000
        minimum_irr_return = int(row['min return']) if row['min return'] else 0
        maximum_irr_return = int(row['max return']) if row['max return'] else 100
        investment_type_preferences = list(investment_type_preferences_set)
        region_preferences = region_preferences
        notes = row['Notes']

        contact = Contact(
          first_name=first_name,
          last_name=last_name,
          email=email,
          phone=phone,
          company=company,
          minimum_investment_size=minimum_investment_size,
          maximum_investment_size=maximum_investment_size,
          minimum_irr_return=minimum_irr_return,
          maximum_irr_return=maximum_irr_return,
          notes=notes,
          creator_id=creator_id,
        )
        contact.save()
        for investment_type_preference_id in investment_type_preferences:
          contact.investment_type_preferences.add(investment_type_preference_id)
        for region_preferences_id in region_preferences:
          contact.region_preferences.add(region_preferences_id)

        counter += 1
        self.stdout.write(self.style.SUCCESS('Successfully added contact "%s"' % str(last_name)))
