from django import CharField, Textarea

class TextField(CharField):
    widget = Textarea(attrs={'cols': '85'})
   
