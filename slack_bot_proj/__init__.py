from __future__ import absolute_import, unicode_literals
from slack_bot_proj.celery import app as celery_app


__all__ = ['celery_app']