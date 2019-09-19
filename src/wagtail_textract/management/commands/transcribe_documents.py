from django.core.management.base import BaseCommand
from wagtail.documents.models import get_document_model
from wagtail_textract.handlers import async_transcribe_document


class Command(BaseCommand):
    """Extract text from all Documents."""
    help = 'Extract text from Documents'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('-s', '--slice', type=str, help="Transcribe a subset of documents using Python's basic slicing syntax")
        parser.add_argument('-d', '--dry-run', action='store_true', dest='dry_run', help="Show what actions will be undertaken with a given transcribe command and its associated parameters")
                       
    def handle(self, *args, **options):
        """Extract text from all Documents."""
        ctr = 1
        slice_ctr = 0
        if options['slice']:
            slices = [x for x in options['slice'].split(':') if x]
            if len(slices) == 2:
                docs = get_document_model().objects.all().order_by('title')[int(slices[0]):int(slices[1])]
                slice_ctr = int(slices[0])
            elif options['slice'].startswith(':') and len(slices) == 1:
                docs = get_document_model().objects.all().order_by('title')[:int(slices[0])]
            elif options['slice'].endswith(':') and len(slices) == 1:
                docs = get_document_model().objects.all().order_by('title')[int(slices[0]):]
                slice_ctr = int(slices[0])
            else:
                docs = get_document_model().objects.all().order_by('title')
        else:
            docs = get_document_model().objects.all().order_by('title')

        if options['dry_run']:
            self.stdout.write("\n{:,} documents will be transcribed\n\n".format( docs.count()))
        else:
            self.stdout.write("\nStarting Transcription of {:,} documents\n\n".format( docs.count()))
        for document in docs:
            if options['verbosity'] >= 1:
                print("{:,} (-s {}:{}) - {}".format(ctr, slice_ctr, slice_ctr + 1, document))
            if not options['dry_run']:
                async_transcribe_document(document, options)
            ctr += 1
            slice_ctr += 1
        if not options['dry_run']:
            self.stdout.write("\n{:,} documents being processed asynchonously\n\n--- AWAITING COMPLETION ---\n\n".format( docs.count()))
        else:
            self.stdout.write("")
