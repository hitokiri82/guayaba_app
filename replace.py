#!/usr/bin/python
# -*- coding: utf-8 -*-
x = """
Esta acción no se puede deshacer<br>
<form action="#" onreset="popToggle()" method="post">
    {% csrf_token %}
    <input type="hidden" name="event_id" value="{{event.id}}">
    <input type="submit" value="Confirmar" name="confirm_remove">
    <input type="reset" value="Cancelar">
</form>
"""
y = [('&', '&amp;'), ('<', '&lt;'), ('"', '&quot;'), ('>', '&gt;')]

def processThis(str,lst):
    for find, replace in lst:
        str = str.replace(find, replace)

    return str.replace('\n','')

print processThis(x,y)