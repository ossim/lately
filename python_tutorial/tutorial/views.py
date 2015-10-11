from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import PostForm
from tutorial.outlookservice import get_my_messages, send_my_message
from tutorial.authhelper import get_signin_url, get_token_from_code, get_user_email_from_id_token
from random import randint

destination_email = ''


def home(request):
    redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
    sign_in_url = get_signin_url(redirect_uri)
    context = {'link': sign_in_url}
    return render(request, 'tutorial/index.html', context)


def gettoken(request):
    auth_code = request.GET['code']
    redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
    token = get_token_from_code(auth_code, redirect_uri)
    access_token = token['access_token']
    user_email = get_user_email_from_id_token(token['id_token'])

    # Save the token in the session
    request.session['access_token'] = access_token
    request.session['user_email'] = user_email
    return HttpResponseRedirect(reverse('tutorial:post_form_upload'))


# def mail(request):
#     access_token = request.session['access_token']
#     user_email = request.session['user_email']
#     # If there is no token in the session, redirect to home
#     if not access_token:
#         return HttpResponseRedirect(reverse('tutorial:home'))
#     else:
#         messages = get_my_messages(access_token, user_email)
#         context = {'messages': messages['value']}
#         return render(request, 'tutorial/mail.html', context)

def post_form_upload(request):
    if request.method == 'GET':
        form = PostForm()
    # else:
        # A POST request: Handle Form Upload
        # form = PostForm(request.POST) # Bind data from request.POST into a PostForm

        # If data is valid, proceeds to create a new post and redirect the user
        # if form.is_valid():
        #     content = form.cleaned_data['content']
        #     post = m.Post.objects.create(content=content,
        #                                  created_at=created_at)
        #     return HttpResponse(str(content))

    return render(request, 'tutorial/post_form_upload.html', {
        'form': form,
    })


# def get_email(request):

#     form_class = SendForm

#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         form = form_class(data=request.POST)

#         if form.is_valid():
#             destination_email = request.POST.get('dest_email', '')
#             return HttpResponse(str(destination_email))
#             # return HttpResponseRedirect(reverse('tutorial:send'))

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = SendForm()

#     return render(request, 'tutorial/mail.html', {'form': form})


def randomExcuses():
    prepositions = ["in", "by", "on", "under", "above", "within", "with", "out", "to", "around", "about"]
    verbs = ["tickling", "eating", "cauterizing", "dancing", "thoroughly examining", "kissing", "heavy petting", "praying for", "netflix and chillin'", "passing", "proselytizing", "smizing at", "hacking", "embracing", "feeing euphoric with", "enacting justice on", "castrating", "vomiting up", "feeling up"]
    nouns = ["zumba instructor", "hackathon", "computer", "electric cucumber", "goat", "furby", "severely athsmatic pug", "presidential candidate", "onesie", "artisanal cupcake", "Oculus", "GAP(tm) clothes (did I mention I love GAP?)", "startup accelerator", "buzzfeed quiz", "kidney stone", "eternal soul", "conjoined twin who was partially consumed in the womb", "copy of L. Ron Hubbards complete works", "inner demons", "missing Speaker of the House", "horse meat", "adult toy", "grandchild", "son", "horse", "lactate", "Ice Dancing partner", "foul mouth", "muscle spasms or jazz hands, I cannot tell", "surpressed dreams of shirtless lumberjacks"]
    possessive = ["my", "Donald Trump's", "Carly Fiorina's controversially fictional", "Selena Gomez's lupus-y", "my", "my", "my", "my partner's", "my mother's", "the CalHacks 2.0 administrative committee's shared"]
    string = ("Sorry for being late, I was " + verbs[randint(0, len(verbs)-1)]
        # + " " + prepositions[randint(0, len(prepositions) - 1)]
        + " " + possessive[randint(0, len(possessive)-1)]
        + " " + nouns[randint(0, len(nouns)-1)]
        # + " " + prepositions[randint(0, len(prepositions)-1)]
        # + " " + possessive[randint(0, len(possessive)-1)]
        # + " " + nouns[randint(0, len(nouns)-1)]
        + ".")
    return string


def send(request):
    if 'q' in request.GET:
        message = 'You searched for: %r' % request.GET['q']
    else:
        form = PostForm(request.POST)
        destination_email = request.POST.get('destination', '')
        access_token = request.session['access_token']
        user_email = request.session['user_email']
        email_recipients, total_recipients, email_address, email_address2, body, message, email, recipient_list = {}, {}, {}, {}, {}, {}, {}, []
        email_address['Address'] = str(destination_email)
        email_recipients['EmailAddress'] = email_address
        recipient_list.append(email_recipients)
        body['ContentType'] = 'text'
        body['Content'] = randomExcuses()
        message['Subject'] = 'Sorry that I am late!'
        message['Body'] = body
        message['ToRecipients'] = recipient_list
        email['Message'] = message
        email['SaveToSentItems'] = False
        if not access_token:
            return HttpResponseRedirect(reverse('tutorial:home'))
        else:
            messages = send_my_message(access_token, user_email, email)
            return render(request, 'tutorial/success.html')

def success(request):
    return HttpResponseRedirect(reverse('tutorial:success'))
