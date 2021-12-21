from django.contrib.auth import get_user_model
from django.db.models import signals
from django.dispatch import receiver

from profiles.models import Profile


user_model = get_user_model()


@receiver(signals.post_save, sender=user_model, dispatch_uid='user_pre_save')
def profile_create_signal(sender, instance, created, **kwargs):
    """Сигнал создания пустого профайла для пользователя
    в случае, если он не был по какой-то причине создан.
    """
    try:
        if not created or instance.profile:
            return
    except Exception:
        Profile.objects.create(user=instance)
