from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from frontend_app.models import Group, UserGroup
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import BibleVerse
import json
import re

from .models import Comment, Highlight
from django.views.decorators.http import require_POST
from django.http import JsonResponse

@login_required
def fetch_group_data(request):
    try:
        user_group = UserGroup.objects.get(user=request.user)
        group = user_group.group
    except UserGroup.DoesNotExist:
        return JsonResponse({'error': 'User is not assigned to any group.'}, status=400)

    # Fetch all highlights/comments for this group
    highlights = Highlight.objects.filter(group=group)
    comments = Comment.objects.filter(group=group)

    # Serialize the data
    data = {
        'highlights': [
            {
                'verse_id': h.verse.id,
                'book': h.verse.book,
                'chapter': h.verse.chapter,
                'verse_number': h.verse.verse,
                'text': h.verse.text,
                'color': h.color,
                'user': h.user.username,
            }
            for h in highlights
        ],
        'comments': [
            {
                'verse_id': c.verse.id,
                'text': c.text,
                'user': c.user.username,
                'created_at': c.created_at.isoformat(),
            }
            for c in comments
        ],
    }

    return JsonResponse(data)

@login_required
def group_verses(request):
    # Get the user's group
    user_group = UserGroup.objects.get(user=request.user)
    group = user_group.group

    # Fetch all verses
    verses = BibleVerse.objects.all()

    # Get highlights and comments for the group
    highlights = Highlight.objects.filter(group=group)
    comments = Comment.objects.filter(group=group)

    return render(request, 'group_verses.html', {
        'verses': verses,
        'highlights': highlights,
        'comments': comments
    })

@login_required
@require_POST
def post_comment(request):
    verse_id = request.POST['verse_id']
    text = request.POST['text']
    verse = get_object_or_404(BibleVerse, id=verse_id)
    
    # Get the user's group via the UserGroup model
    user_group = UserGroup.objects.get(user=request.user)
    group = user_group.group

    # Create the comment and associate it with the user's group
    comment = Comment.objects.create(
        user=request.user, 
        verse=verse, 
        text=text, 
        group=group
    )

    return JsonResponse({
        'message': 'Comment posted',
        'username': request.user.username,
        'text': comment.text
    })

@login_required
@require_POST
def add_highlight(request):
    verse_id = request.POST['verse_id']
    color = request.POST['color']
    verse = get_object_or_404(BibleVerse, id=verse_id)
    
    user_group = UserGroup.objects.get(user=request.user)
    group = user_group.group

    highlight, created = Highlight.objects.update_or_create(
    verse=verse,
    user=request.user,
    group=group,
    defaults={
        'color': color,
        'text': verse.text,
        'book': BOOK_NAMES.get(verse.book, "Unknown"),
        'chapter': verse.chapter,
        'verse_number': verse.verse
    })


    return JsonResponse({'message': 'Verse highlighted'})


@login_required
def save_highlight(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_group = UserGroup.objects.get(user=request.user)
        Highlight.objects.create(
            user=request.user,
            group=user_group.group,
            book=data["book"],
            chapter=data["chapter"],
            verse=data["verse"],
            text=data["text"],
            comment=data.get("comment", "")
        )
        return JsonResponse({"status": "ok"})

def index(request):
    return render(request, 'index.html')

def sign_in_success(request):
    return render(request, 'sign-in-success.html')

def bible_view(request):
    book_name_param = request.GET.get('book_name')
    chapter = int(request.GET.get('chapter', 1))

    # Convert name to book ID
    book = 1  # Default
    book_name = "Genesis"  # Default

    if book_name_param:
        # Normalize user input
        book_name_param = book_name_param.strip().lower()
        for k, v in BOOK_NAMES.items():
            if v.lower() == book_name_param:
                book = k
                book_name = v
                break
    else:
        book = int(request.GET.get('book', 1))
        book_name = BOOK_NAMES.get(book, 'Unknown Book')

    verses = BibleVerse.objects.filter(book=book, chapter=chapter)

    user_group = UserGroup.objects.get(user=request.user)
    group = user_group.group
    
    group_users = User.objects.filter(usergroup__group=group)
    
    highlights = Highlight.objects.filter(
        verse__in=verses,
        user__in=group_users
    )

    comments = Comment.objects.filter(
        verse__in=verses,
        user__in=group_users
    )

    return render(request, "bible_view.html", {
        "book_names": BOOK_NAMES,
        "book_name": book_name,
        "chapter": chapter,
        "verses": verses,
        "highlights": highlights,
        "comments": comments,
    })

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        subject = 'Activate Your Account'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        message = render_to_string('email_verification.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': uid,
            'token': token,
        })
        send_mail(subject, message, 'BibleProjectPython@gmail.com', [email])

        return HttpResponse("<h1>Go to your email to get your account verified...</h1>\
                            <p><a href='/'>Return to home page</a></p>")
    
    return render(request, 'register_form.html') 

def activate(request, uid, token):
    try:
        uid = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Your account has been activated! You can now log in.')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required
def groups_home(request):
    return render(request, 'groups_home.html')

@login_required
def create_group(request):
    if UserGroup.objects.filter(user=request.user).exists():  # Check if the user is already in a group
        messages.warning(request, "You're already in a group!")
        return redirect('groups-home')
    
    if request.method == "POST":
        group_name = request.POST.get('name')
        
        group, created = Group.objects.get_or_create(name=group_name)
        
        UserGroup.objects.create(user=request.user, group=group)  # Ensure group is a Group instance
        
        return redirect('group_detail', group_id=group.id)
    
    return render(request, 'create_group.html')

def join_group_page(request):
    groups = Group.objects.all()
    return render(request, 'join_group.html', {'groups': groups})

@login_required
def join_group(request, group_id):
    if UserGroup.objects.filter(user=request.user).exists():  # Check if the user is already in a group
        return redirect('already_in_group')  # Redirect if already in a group
    
    group = Group.objects.get(id=group_id)
    UserGroup.objects.create(user=request.user, group=group)
    
    return redirect('group_detail', group_id=group.id)

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    members = UserGroup.objects.filter(group=group)
    return render(request, 'group_detail.html', {'group': group, 'members': members})

@login_required
def leave_group(request):
    try:
        user_group = UserGroup.objects.get(user=request.user)
        user_group.delete()
        # Optional: message or redirect after successful leave
        return redirect('index')  # or wherever you'd like
    except UserGroup.DoesNotExist:
        # Handle the case where the user isn't in a group
        # Optional: show a message or redirect somewhere else
        return redirect('index')  # same as above or a custom "not in group" page


BOOK_NAMES = {
    1: 'Genesis',
    2: 'Exodus',
    3: 'Leviticus',
    4: 'Numbers',
    5: 'Deuteronomy',
    6: 'Joshua',
    7: 'Judges',
    8: 'Ruth',
    9: '1 Samuel',
    10: '2 Samuel',
    11: '1 Kings',
    12: '2 Kings',
    13: '1 Chronicles',
    14: '2 Chronicles',
    15: 'Ezra',
    16: 'Nehemiah',
    17: 'Esther',
    18: 'Job',
    19: 'Psalms',
    20: 'Proverbs',
    21: 'Ecclesiastes',
    22: 'Song of Solomon',
    23: 'Isaiah',
    24: 'Jeremiah',
    25: 'Lamentations',
    26: 'Ezekiel',
    27: 'Daniel',
    28: 'Hosea',
    29: 'Joel',
    30: 'Amos',
    31: 'Obadiah',
    32: 'Jonah',
    33: 'Micah',
    34: 'Nahum',
    35: 'Habakkuk',
    36: 'Zephaniah',
    37: 'Haggai',
    38: 'Zechariah',
    39: 'Malachi',
    40: 'Matthew',
    41: 'Mark',
    42: 'Luke',
    43: 'John',
    44: 'Acts',
    45: 'Romans',
    46: '1 Corinthians',
    47: '2 Corinthians',
    48: 'Galatians',
    49: 'Ephesians',
    50: 'Philippians',
    51: 'Colossians',
    52: '1 Thessalonians',
    53: '2 Thessalonians',
    54: '1 Timothy',
    55: '2 Timothy',
    56: 'Titus',
    57: 'Philemon',
    58: 'Hebrews',
    59: 'James',
    60: '1 Peter',
    61: '2 Peter',
    62: '1 John',
    63: '2 John',
    64: '3 John',
    65: 'Jude',
    66: 'Revelation',
}

def get_book_name(book_id):
    # Return the book name by its ID
    return BOOK_NAMES.get(book_id, "Invalid book ID")

def search_book(query):
    # Check if query is a number or a name
    if query.isdigit():
        book_id = int(query)
        book_name = get_book_name(book_id)
    else:
        book_name = query.capitalize()
        # Try to find the corresponding book ID for the name
        book_id = next((id for id, name in BOOK_NAMES.items() if name == book_name), None)

    return book_name, book_id

# Use this dictionary in your context
