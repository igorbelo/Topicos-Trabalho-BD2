from varzeapro import settings

def tmp_media(request):
    return {
        'MEDIA_TMP_DIR': settings.MEDIA_TMP_DIR,
        'MEDIA_TMP_URL': settings.MEDIA_TMP_URL
    }
