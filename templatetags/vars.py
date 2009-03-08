#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import template
from django.template import resolve_variable
from variables.models import *

register = template.Library()

class VariableTemplateError(template.TemplateSyntaxError):
    def __unicode__(self):
        return self.message

@register.tag(name="variable")
def variable(parser, token):
    tokens = token.contents.split()
    if len(tokens) < 2:
        raise template.TemplateSyntaxError(u"'%r' tag requires at least 1 argument." % tokens[0])
    
    return VariableNode(tokens[1:])

@register.tag(name="variable_silent")
def variable_silent(parser, token):
    u""" Пытается найти переменную в модели. Если оной нет - возвращает пустую строку. """
    tokens = token.contents.split()
    if len(tokens) < 2:
        raise template.TemplateSyntaxError(u"'%r' tag requires at least 1 argument." % tokens[0])
    
    return SilentVariableNode(tokens[1:])

class VariableNode(template.Node):
    def __init__(self, names):
        self.names = names

    def render(self, context):
        try:
            name = u''.join([unicode(resolve_variable(x, context)) for x in self.names])
            var = Variable.objects.get(name=name)
        except Variable.DoesNotExist:
            raise VariableTemplateError(u"""
                            Переменная с названием «%s» не определена.
                            Пожалуйста, заполните её значение через административный интерфейс.""" % name)
        
        return var.value

class SilentVariableNode(template.Node):
    def __init__(self, names):
        self.names = names

    def render(self, context):
        try:
            name = u''.join([unicode(resolve_variable(x, context)) for x in self.names])
            value = Variable.objects.get(name=name).value
        except Variable.DoesNotExist:
            value = ""
        
        return value