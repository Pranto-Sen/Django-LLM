from django.core.management.base import BaseCommand
from django.db import connections
from myapp.models import PropertySummary
import ollama
from concurrent.futures import ThreadPoolExecutor, as_completed

class Command(BaseCommand):
    help = (
        'Rewrites the Title and Description fields of the MyApp_property table, '
        'generates summaries, and stores them in a separate summary table.'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = "phi3"
        self.max_workers = 5  # Adjust based on your system's capabilities

    def get_ollama_response(self, prompt):
        try:
            response = ollama.generate(model=self.model, prompt=prompt)
            return response.get('response', '').strip() if response else None
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"API error: {e}"))
            return None

    def truncate_text(self, text, max_length):
        if len(text) > max_length:
            return text[:max_length].rsplit(' ', 1)[0]
        return text

    def generate_title(self, current_title, max_length):
        prompt = (
            f"Please rewrite the property title below to make it more unique and appealing. "
            f"The new title should be distinct, creative, and within {max_length} characters:\n\n"
            f"Current Title: {current_title}"
        )
        new_title = self.get_ollama_response(prompt)
        return self.truncate_text(new_title, max_length) if new_title else None

    def generate_description(self, title, max_length):
        prompt = (
            f"Rewrite the property description below based on the given title. "
            f"Ensure the description is detailed, unique, and exactly {max_length} characters long:\n\n"
            f"Title: {title}\n"
        )
        new_description = self.get_ollama_response(prompt)
        return self.truncate_text(new_description, max_length) if new_description else None

    def generate_summary(self, title, description):
        prompt = (
            f"Please generate a concise summary based on the following property details. "
            f"Ensure the summary captures the key points and provides a clear overview of the property.\n\n"
            f"Title: {title}\n"
            f"Instructions:\n"
            f"- The summary should be brief yet informative.\n"
            f"- Focus on highlighting the main features and unique aspects of the property.\n"
            f"- Avoid including unnecessary details or repetition.\n"
            f"- Aim for a summary length of approximately 1-2 sentences.\n"
        )   
        return self.get_ollama_response(prompt)

    def process_property(self, property_data):
        id, title, description = property_data
        max_title_length = 80
        max_description_length = 230

        new_title = self.generate_title(title, max_title_length)
        if not new_title:
            return id, None, None, None

        new_description = self.generate_description(new_title, max_description_length)
        if not new_description:
            return id, None, None, None

        summary_text = self.generate_summary(new_title, new_description)
        if not summary_text:
            return id, None, None, None

        return id, new_title, new_description, summary_text

    def handle(self, *args, **options):
        with connections['default'].cursor() as cursor:
            cursor.execute('SELECT id, title, description FROM "myapp_property"')
            properties = cursor.fetchall()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_property = {executor.submit(self.process_property, prop): prop for prop in properties}
            
            for future in as_completed(future_to_property):
                id, new_title, new_description, summary_text = future.result()
                
                if new_title and new_description and summary_text:
                    with connections['default'].cursor() as cursor:
                        cursor.execute(
                            '''
                            UPDATE "myapp_property"
                            SET title = %s, description = %s
                            WHERE id = %s
                            ''',
                            [new_title, new_description, id]
                        )

                    PropertySummary.objects.update_or_create(
                        property_id=id,
                        defaults={'summary': summary_text}
                    )

                    self.stdout.write(self.style.SUCCESS(f'Successfully updated and summarized property {id}'))
                else:
                    self.stdout.write(self.style.WARNING(f"Skipping property {id} due to processing failure"))

        self.stdout.write(self.style.SUCCESS('All properties have been processed'))

# python manage.py rewrite_properties

# all okkkk
# from django.core.management.base import BaseCommand
# from django.db import connections
# from myapp.models import PropertySummary
# import ollama

# class Command(BaseCommand):
#     help = (
#         'Rewrites the Title and Description fields of the MyApp_property table, '
#         'generates summaries, and stores them in a separate summary table.'
#     )

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # self.model = "gemma2:2b"  # Change to "phi3" if needed
#         self.model = "phi3"
#     def get_ollama_response(self, prompt):
#         try:
#             response = ollama.generate(model=self.model, prompt=prompt)
#             return response.get('response', '').strip() if response else None
#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f"API error: {e}"))
#             return None

#     def truncate_text(self, text, max_length):
#         if len(text) > max_length:
#             return text[:max_length].rsplit(' ', 1)[0]
#         return text

#     def generate_title(self, current_title, max_length):
#         prompt = (
#             f"Please rewrite the property title below to make it more unique and appealing. "
#             f"The new title should be distinct, creative, and within {max_length} characters:\n\n"
#             f"Current Title: {current_title}"
#         )
#         new_title = self.get_ollama_response(prompt)
#         return self.truncate_text(new_title, max_length) if new_title else None

#     def generate_description(self, title, max_length):
#         prompt = (
#             f"Rewrite the property description below based on the given title. "
#             f"Ensure the description is detailed, unique, and exactly {max_length} characters long:\n\n"
#             f"Title: {title}\n"
#         )
#         new_description = self.get_ollama_response(prompt)
#         return self.truncate_text(new_description, max_length) if new_description else None

#     def generate_summary(self, title, description):
       
#         prompt = (
#             f"Please generate a concise summary based on the following property details. "
#             f"Ensure the summary captures the key points and provides a clear overview of the property.\n\n"
#             f"Title: {title}\n"
#             f"Instructions:\n"
#             f"- The summary should be brief yet informative.\n"
#             f"- Focus on highlighting the main features and unique aspects of the property.\n"
#             f"- Avoid including unnecessary details or repetition.\n"
#             f"- Aim for a summary length of approximately 1-2 sentences.\n"
#         )   
#         return self.get_ollama_response(prompt)

#     def handle(self, *args, **options):
#         max_title_length = 80
#         max_description_length = 230

#         with connections['default'].cursor() as cursor:
#             cursor.execute('SELECT id, title, description FROM "myapp_property"')
#             properties = cursor.fetchall()

#             for id, title, description in properties:
#                 new_title = self.generate_title(title, max_title_length)
#                 if not new_title:
#                     self.stdout.write(self.style.WARNING(f"Skipping property {id} due to title generation failure"))
#                     continue

#                 new_description = self.generate_description(new_title, max_description_length)
#                 if not new_description:
#                     self.stdout.write(self.style.WARNING(f"Skipping property {id} due to description generation failure"))
#                     continue

#                 cursor.execute(
#                     '''
#                     UPDATE "myapp_property"
#                     SET title = %s, description = %s
#                     WHERE id = %s
#                     ''',
#                     [new_title, new_description, id]
#                 )

#                 summary_text = self.generate_summary(new_title, new_description)
#                 if not summary_text:
#                     self.stdout.write(self.style.WARNING(f"Skipping summary creation for property {id}"))
#                     continue

#                 PropertySummary.objects.update_or_create(
#                     property_id=id,
#                     defaults={'summary': summary_text}
#                 )

#                 self.stdout.write(self.style.SUCCESS(f'Successfully updated and summarized property {id}'))

#         self.stdout.write(self.style.SUCCESS('All properties have been processed'))

