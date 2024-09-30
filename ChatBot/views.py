# chatbot/views.py
from django.shortcuts import render
from django.http import JsonResponse
import openai
from .api import OPENAI_API_KEY

# Load OpenAI API key from environment
openai.api_key = OPENAI_API_KEY

# Function to get chatbot response using OpenAI's GPT-3.5 API
def chatbot_response(user_input):
    try:
        # Make a request to the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use "gpt-4" if available and if your subscription allows it
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ],
            max_tokens=150,
            temperature=0.7,
        )
        
        # Extract the response from the API
        response_text = response['choices'][0]['message']['content'].strip()
        return response_text
    except Exception as e:
        # Handle any exceptions
        return "Sorry, I couldn't process your request at the moment."

# View to render the chat page
def chat_view(request):
    return render(request, 'chatbot/chat.html')

# View to handle AJAX request for chatbot response
def get_response(request):
    user_message = request.GET.get('user_message')
    response = chatbot_response(user_message)
    return JsonResponse({'response': response})
