# chatbot/views.py
from django.shortcuts import render
from django.http import JsonResponse
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load the pre-trained model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
chat_history = []

def chatbot_response(user_input):
    global chat_history
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # Append new user input to the chat history
    if len(chat_history) > 0:
        bot_input_ids = torch.cat([chat_history, new_input_ids], dim=-1)
    else:
        bot_input_ids = new_input_ids

    # Generate a response
    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_p=0.95,
        top_k=50
    )

    # Update chat history
    chat_history = chat_history_ids

    # Decode the response
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response

# View to render the chat page
def chat_view(request):
    return render(request, 'chatbot/chat.html')

# View to handle AJAX request for chatbot response
def get_response(request):
    user_message = request.GET.get('user_message')
    response = chatbot_response(user_message)
    return JsonResponse({'response': response})
