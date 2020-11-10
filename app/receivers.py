from django.contrib.auth.signals import user_logger_in, user_logged_out, user_login_failed
from django.dispatch import receiver

import logging

logger = logging.getLogger()


@receiver(user_logger_in)
def handle_login(sender, request, user, **kwargs):
    logger.info("logged_in", user.username)


@receiver(user_logged_out)
def handle_logout(sender, request, user, **kwargs):
    logger.info("logged_out", user.username)


@receiver(user_login_failed)
def handle_login_failed(sender, request, user, **kwargs):
    logger.info("logged_failed: ", user.username)
