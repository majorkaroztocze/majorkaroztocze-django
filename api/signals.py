from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import KayakReservation, CabinReservation, CampingReservation

ADMIN_EMAIL = settings.ADMIN_NOTIFICATION_EMAIL

def send_dual_email(subject, message, client_email):
    # Do właściciela
    send_mail(subject, message, None, [ADMIN_EMAIL])
    # Do klienta
    if client_email:
        send_mail(f"Potwierdzenie: {subject}", f"Dziękujemy za rezerwację!\n\n{message}", None, [client_email])

@receiver(post_save, sender=KayakReservation)
def notify_kayak_reservation(sender, instance, created, **kwargs):
    if created:
        message = (
            f"Rezerwacja kajaków na {instance.start_date} o {instance.start_time}.\n"
            f"Klient: {instance.user_name}\n"
            f"2-os: {instance.kayak_double_quantity}, "
            f"1-os: {instance.kayak_single_quantity}, "
            f"Dostawki: {instance.kayak_extra_child_quantity}, "
            f"Worki: {instance.waterproof_bag_quantity}\n"
            f"Trasa: {instance.kayak_route}\n\n"

            "Cieszymy się, że wybraliście nas na miejsce swojego wypoczynku.\n"
            "Jeśli chcielibyście uzyskać więcej informacji dotyczących spływu kajakowego, noclegu w domku "
            "lub pobytu na polu namiotowym – serdecznie zapraszamy do kontaktu.\n"
            "Z przyjemnością odpowiemy na wszystkie pytania!\n\n"

            "Gdyby zaszła potrzeba zmiany terminu, godziny, liczby uczestników lub jakichkolwiek innych "
            "szczegółów rezerwacji – dajcie nam znać.\n"
            "Jesteśmy elastyczni i postaramy się dopasować do Waszych planów.\n\n"

            "W przypadku rezygnacji z rezerwacji również prosimy o informację – dzięki temu inne osoby "
            "będą mogły skorzystać z wolnego terminu.\n\n"

            "📞 Kontakt:\n"
            "email: majorkaroztocze@gmail.com\n"
            "tel: +48 883 025 743\n\n"

            "Do zobaczenia!\n\n"
            "⚠️ Nie odpowiadaj na ten email."f"Rezerwacja kajaków na {instance.start_date} o {instance.start_time}.\n"
            f"Klient: {instance.user_name}\n"
            f"2-os: {instance.kayak_double_quantity}, "
            f"1-os: {instance.kayak_single_quantity}, "
            f"Dostawki: {instance.kayak_extra_child_quantity}, "
            f"Worki: {instance.waterproof_bag_quantity}\n"
            f"Trasa: {instance.kayak_route}\n\n"

            "Cieszymy się, że wybraliście nas na miejsce swojego wypoczynku.\n"
            "Jeśli chcielibyście uzyskać więcej informacji dotyczących spływu kajakowego, noclegu w domku "
            "lub pobytu na polu namiotowym – serdecznie zapraszamy do kontaktu.\n"
            "Z przyjemnością odpowiemy na wszystkie pytania!\n\n"

            "Gdyby zaszła potrzeba zmiany terminu, godziny, liczby uczestników lub jakichkolwiek innych "
            "szczegółów rezerwacji – dajcie nam znać.\n"
            "Jesteśmy elastyczni i postaramy się dopasować do Waszych planów.\n\n"

            "W przypadku rezygnacji z rezerwacji również prosimy o informację – dzięki temu inne osoby "
            "będą mogły skorzystać z wolnego terminu.\n\n"

            "📞 Kontakt:\n"
            "email: majorkaroztocze@gmail.com\n"
            "tel: +48 883 025 743\n\n"

            "Do zobaczenia!\n\n"
            "⚠️ Nie odpowiadaj na ten email."
        )
        send_dual_email("Nowa rezerwacja kajaków", message, instance.email)

@receiver(post_save, sender=CabinReservation)
def notify_cabin_reservation(sender, instance, created, **kwargs):
    if created:
        message = (
            f"Domek: {instance.cabin.name}\n"
            f"Rezerwacja od {instance.start_date} do {instance.end_date}\n"
            f"Klient: {instance.user_name}\n"
            f"E-mail: {instance.email}\n\n"

            "Cieszymy się, że wybraliście nas na miejsce swojego wypoczynku.\n"
            "Jeśli chcielibyście uzyskać więcej informacji dotyczących spływu kajakowego, noclegu w domku "
            "lub pobytu na polu namiotowym – serdecznie zapraszamy do kontaktu.\n"
            "Z przyjemnością odpowiemy na wszystkie pytania!\n\n"

            "Gdyby zaszła potrzeba zmiany terminu, godziny, liczby uczestników lub jakichkolwiek innych "
            "szczegółów rezerwacji – dajcie nam znać.\n"
            "Jesteśmy elastyczni i postaramy się dopasować do Waszych planów.\n\n"

            "W przypadku rezygnacji z rezerwacji również prosimy o informację – dzięki temu inne osoby "
            "będą mogły skorzystać z wolnego terminu.\n\n"

            "📞 Kontakt:\n"
            "email: majorkaroztocze@gmail.com\n"
            "tel: +48 883 025 743\n\n"

            "Do zobaczenia!\n\n"
            "⚠️ Nie odpowiadaj na ten email."
        )
        send_dual_email("Nowa rezerwacja domku", message, instance.email)

@receiver(post_save, sender=CampingReservation)
def notify_camping_reservation(sender, instance, created, **kwargs):
    if created:
        message = (
            f"Rezerwacja pola namiotowego od {instance.start_date} do {instance.end_date}\n"
            f"Dorośli: {instance.adults}, Dzieci: {instance.children}\n"
            f"Klient: {instance.user_name}\n"
            f"E-mail: {instance.email}\n\n"

            "Cieszymy się, że wybraliście nas na miejsce swojego wypoczynku.\n"
            "Jeśli chcielibyście uzyskać więcej informacji dotyczących spływu kajakowego, noclegu w domku "
            "lub pobytu na polu namiotowym – serdecznie zapraszamy do kontaktu.\n"
            "Z przyjemnością odpowiemy na wszystkie pytania!\n\n"

            "Gdyby zaszła potrzeba zmiany terminu, godziny, liczby uczestników lub jakichkolwiek innych "
            "szczegółów rezerwacji – dajcie nam znać.\n"
            "Jesteśmy elastyczni i postaramy się dopasować do Waszych planów.\n\n"

            "W przypadku rezygnacji z rezerwacji również prosimy o informację – dzięki temu inne osoby "
            "będą mogły skorzystać z wolnego terminu.\n\n"

            "📞 Kontakt:\n"
            "email: majorkaroztocze@gmail.com\n"
            "tel: +48 883 025 743\n\n"

            "Do zobaczenia!\n\n"
            "⚠️ Nie odpowiadaj na ten email."
        )
        send_dual_email("Nowa rezerwacja pola namiotowego", message, instance.email)
