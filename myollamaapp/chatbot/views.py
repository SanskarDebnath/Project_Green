from django.shortcuts import render

# Create your views here.
import ollama
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def ask_ollama(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_input = data.get("question", "")

        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": user_input}])

        return JsonResponse({"response": response["message"]["content"]})

    return JsonResponse({"error": "Invalid request"}, status=400)

from django.shortcuts import render

def chatbot_ui(request):
    return render(request, "index.html")
