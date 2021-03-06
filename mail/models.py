#-*- coding: utf-8 -*-
from django.db import models
from django.core.mail import send_mass_mail
from django.template import Template, Context
from django.conf import settings

class EmailTemplate(models.Model):
    class Meta:
        verbose_name=u'Шаблон письма'
        verbose_name_plural=u'Шаблоны писем'
    key   = models.CharField(max_length=250, verbose_name=u'Ключ', unique=True, db_index=True)
    title = models.CharField(max_length=250, verbose_name=u'Название')
    subj  = models.CharField(max_length=250, verbose_name=u'Тема письма')
    body  = models.TextField(verbose_name=u'Тело письма')

    def send(self, receivers, sender=None, data={}):
	c = Context(data)
	subject = Template(self.subj).render(c)
	body = Template(self.body).render(c)
	if sender is None:
	    sender = settings.EMAIL_FROM
	for receiver in receivers:
	    kwargs['receiver'] = receiver
	    EmailQueue.objects.create(
		from_field=sender, to_field=receiver, subject=subject, body=body
	    )

    @staticmethod
    def get(key):
	return EmailTemplate.objects.get(key=key)

class EmailQueue(models.Model):
    class Meta:
	verbose_name=u'Очередь email'
	verbose_name_plural=u'Очередь email'
    from_field  = models.CharField(max_length=250)
    to_field    = models.TextField()
    subject     = models.CharField(max_length=250)
    body        = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    sent_at     = models.DateTimeField(blank=True, null=True)