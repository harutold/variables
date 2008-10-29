#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import template
from variables.models import *

register = template.Library()

@register.tag(name="variable")
def variable(parser, token):
    tokens = token.contents.split()
    if len(tokens) != 2:
        raise template.TemplateSyntaxError(u"'%r' tag requires 1 argument." % tokens[0])
    
    return VariableNode(tokens[1])

class VariableNode(template.Node):
    def __init__(self, name):
        self.name = name

    def render(self, context):
        try:
            var = Variable.objects.get(name=self.name)
        except Variable.DoesNotExist:
            raise Exception(u"""
                            Переменная с названием «%s» не определена.
                            Пожалуйста, заполните её значение через административный интерфейс.""" % self.name)
        
        return var.value
