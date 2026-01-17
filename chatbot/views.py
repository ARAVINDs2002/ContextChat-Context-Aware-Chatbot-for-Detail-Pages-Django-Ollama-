from django.shortcuts import render
from django.http import JsonResponse
import json
from .context import get_house_context
from .logic import detect_intent, validate_data
from .ai import generate_response
from .models import House

def index(request):
    houses = House.objects.all()
    return render(request, 'chatbot/index.html', {'houses': houses})

def chat_view(request, house_id):
    # 1. Load context
    context = get_house_context(house_id)
    if not context:
        return render(request, 'chatbot/404.html', status=404)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question = data.get('question', '')
            
            # 2. Detect Intent
            intent = detect_intent(question)

            # 3. Validate Data (Manual Logic)
            is_valid, relevant_data, manual_response = validate_data(context, intent)

            if not is_valid:
                # 4. Manual Fallback
                return JsonResponse({"response": manual_response})
            else:
                # 5. Call AI
                response = generate_response(context['house'], relevant_data, question)
                return JsonResponse({"response": response})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # Render the chat interface
    return render(request, 'chatbot/chat.html', {'house': context['house']})
