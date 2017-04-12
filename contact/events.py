from event.models import TeamEvent, TeamEventCategory

def create_new_contact_team_event(user, contact):
  creator = user.customer_profile
  team = creator.team

  if team:
    team_event_category = TeamEventCategory.objects.get(name='contact_added')
    metadata = {
      'new_contact_id': str(contact.id),
      'new_contact_full_name': contact.get_full_name(),
      'new_contact_company': contact.company,
      'event_category_name': team_event_category.name,
      'creator_name': creator.user.get_full_name(),
    }

    team_event = TeamEvent(
      created_by=creator,
      team=team,
      category=team_event_category,
      metadata=metadata,
    )
    team_event.save()

def create_update_contact_team_event(user, contact):
  creator = user.customer_profile
  team = creator.team

  if team:
    team_event_category = TeamEventCategory.objects.get(name='contact_updated')
    metadata = {
      'contact_id': str(contact.id),
      'contact_full_name': contact.get_full_name(),
      'contact_company': contact.company,
      'event_category_name': team_event_category.name,
      'creator_name': creator.user.get_full_name(),
    }

    team_event = TeamEvent(
      created_by=creator,
      team=team,
      category=team_event_category,
      metadata=metadata,
    )
    team_event.save()

def create_follow_up_team_event(user, follow_up):
  creator = user.customer_profile
  team = creator.team

  if team:
    contact = follow_up.contact
    team_event_category = TeamEventCategory.objects.get(name='contact_follow_up_added')
    metadata = {
      'contact_id': str(contact.id),
      'contact_full_name': contact.get_full_name(),
      'contact_company': contact.company,
      'follow_up_date': follow_up.begin_date.isoformat(),
      'event_category_name': team_event_category.name,
      'creator_name': creator.user.get_full_name(),
    }

    team_event = TeamEvent(
      created_by=creator,
      team=team,
      category=team_event_category,
      metadata=metadata,
    )
    team_event.save()