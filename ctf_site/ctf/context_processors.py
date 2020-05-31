from django.conf import settings


# Code from the internet
def constants(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'TITLE': settings.TITLE}
