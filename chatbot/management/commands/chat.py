from django.core.management.base import BaseCommand
from chatbot.context import get_house_context
from chatbot.logic import detect_intent, validate_data
from chatbot.ai import generate_response

class Command(BaseCommand):
    help = 'Chat about a specific house'

    def add_arguments(self, parser):
        parser.add_argument('house_id', type=int, help='ID of the house')
        parser.add_argument('question', type=str, help='The question to ask')

    def handle(self, *args, **options):
        house_id = options['house_id']
        question = options['question']

        # 1. Load context
        context = get_house_context(house_id)
        if not context:
            self.stdout.write("House not found.")
            return

        # 2. Detect Intent
        intent = detect_intent(question)

        # 3. Validate Data (Manual Logic)
        is_valid, relevant_data, manual_response = validate_data(context, intent)

        if not is_valid:
            # 4. Manual Fallback
            self.stdout.write(manual_response)
        else:
            # 5. Call AI
            # Pass only house info and relevant data slice
            response = generate_response(context['house'], relevant_data, question)
            self.stdout.write(response)
