from django.shortcuts import render, get_object_or_404, redirect
from .forms import TweetForm, UserRegisterationForm
from .models import Tweet
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from django.core.mail import send_mail
from django.conf import settings



def tweetList(request):
    tweets = Tweet.objects.all().select_related('user').order_by('-created_at')
    query = request.GET.get('q', '').strip()

    if query:
        tweets = tweets.filter(text__icontains=query)  # Fixed typo
    
    return render(request, 'tweetList.html', {'tweets': tweets, 'query': query})  # Fixed dictionary


@login_required
def tweetCreate(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False) # form.save() here converts the data into Tweet model object.
            tweet.user = request.user
            tweet.save()
            return redirect('tweetList')
    else:
        form = TweetForm()  # Empty form for GET request.
    
    return render(request, 'tweetForm.html', {'form': form})


@login_required
def tweetEdit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweetList')
    else: 
        form = TweetForm(instance=tweet)

    return render(request, 'tweetForm.html', {'form': form})


@login_required
def tweetDelete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == "POST":
        tweet.delete()
        return redirect("tweetList")

    return render(request, "tweetConfirmDelete.html", {"tweet": tweet})


def register(request):
    if request.method=='POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweetList')

    else:
        form = UserRegisterationForm()

    return render(request, 'registration/register.html', {'form': form})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Check if all fields are filled
        if not name or not email or not message:
            messages.error(request, "All fields are required. Please fill out your name, email, and message.")
            return render(request, 'contact.html')

        # Send email if all fields are filled
        subject = f"Message from {name}"
        message_content = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        recipient_list = [settings.EMAIL_HOST_USER]  # Your email address

        send_mail(subject, message_content, email, recipient_list)

        messages.success(request, "Message sent successfully!")
        return render(request, 'contact.html')

    return render(request, 'contact.html')