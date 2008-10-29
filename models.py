#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models

class Variable(models.Model):
    name = models.CharField(u'Имя',max_length=100, unique=True)
    type = models.SmallIntegerField(u'Тип', choices=(
        (1, 'строка'),
        (2, 'текст'),
        (3, 'целое число'),
        (4, 'дробное число'),
    ))
    desc = models.CharField(u'Описание', help_text=u"используется только в админке", max_length=255, blank=True, null=True)
    string = models.CharField(u'Строковое значение', max_length=255, blank=True, null=True)
    text = models.TextField(u'Текстовое значение', blank=True, null=True)
    num = models.FloatField(u'Числовое значение', blank=True, null=True)
    
    def set_value(self, new_val):
        if self.type == 1:
            self.string = new_val
        if self.type == 2:
            self.text = new_val
        if self.type == 3:
            self.num = int(new_val)
        if self.type == 4:
            self.num = new_val

    def get_value(self):
        if self.type == 1:
            return self.string
        if self.type == 2:
            return self.text
        if self.type == 3:
            return int(self.num)
        if self.type == 4:
            return self.num
    value = property(get_value, set_value)
    #value.verbose_name = u"Значение"
    #value.allow_tags = True
    
    class Meta:
        ordering = ['name']
        verbose_name = u'Переменная'
        verbose_name_plural = u'Переменные'
    def __unicode__(self):
        return self.name

def var(name):
    return Variable.objects.get(name=name).value
