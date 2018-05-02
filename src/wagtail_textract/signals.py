from django.dispatch import Signal

document_saved = Signal(providing_args=['instance'])
