from mcur import settings

def basic(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'SKIOG_VERSION': settings.SKIOG_VERSION}