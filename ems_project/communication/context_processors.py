from communication.models import Message

def unread_message_count(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(receiver=request.user, read=False).count()
        return {'unread_count_global': count}
    return {}


from communication.models import Announcement, AnnouncementRead
from users.models import User

def unread_announcement_count(request):
    if request.user.is_authenticated:
        from django.db.models import Q
        user = request.user
        # All visible announcements for this user
        visible_announcements = Announcement.objects.filter(
            Q(audience='all') | Q(audience=user.role)
        )
        read_announcement_ids = AnnouncementRead.objects.filter(
            user=user
        ).values_list('announcement_id', flat=True)

        unread_count = visible_announcements.exclude(id__in=read_announcement_ids).count()
        return {'unread_announcement_count': unread_count}
    return {}
