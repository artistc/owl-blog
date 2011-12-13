from models import Article, Tag, Comment
from django.template import Context, loader
from django import forms
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect, QueryDict
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from forms import CommentForm, SearchForm
from parse import parseSearchExpression

def articleOrNone(articleFactory):
    try:
        return articleFactory()
    except:
        return None

### primary View functions


def home(request):
    'home page; most recent articles'

    if request.user.is_authenticated():
        latest_article = Article.objects.latest()
    else:
        latest_article = Article.objects.filter(published=True).latest()

    return render_to_response('blog/home.html',
        context_instance=Context(locals()) )


def infinite(request):
    'load additional article content for the infinite scroll feature.'
    index = int(request.GET['index'])
    try:
        article = Article.objects.filter(published=True).order_by('-date_time_added')[index]
    except IndexError:
        article = None
 
    return render_to_response('blog/home_article.html', locals())


def archive(request):
    'list of all article by date'
    articles = Article.objects.filter(published=True).order_by('-date_time_added')
    return render_to_response('blog/archive.html',
        context_instance=Context(locals()) )


def tag(request, slug):
    'list of all articles in a tag'
    try:
        tag = Tag.objects.get(slug=slug)
    except Tag.DoesNotExist:
        raise Http404
    articles = tag.articles.all().filter(published=True)
    return render_to_response('blog/tag.html',
        context_instance=Context(locals()) )


def tags(request):
    'list of all available tags'
    tags = Tag.objects.order_by('slug')
    #articles = tag.articles.all() I can do this in the template
    return render_to_response('blog/tags.html',
        context_instance=Context(locals()) )


def article(request,slug):
    'full content of an article plus comments'
    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        raise Http404
    
    # populate useful variables
    comments = article.comment_set.order_by('-date_time_added')[0:99] # just in case things get out of hand...
    comment_form = CommentForm()
    
    template = loader.get_template('blog/article.html')
    context = Context( locals() )
    html = template.render(context)
    return HttpResponse(html)


def leave_comment(request, slug):
    'stand-alone comment form, shown mostly after validation fails.'
    article=get_object_or_404(Article, slug=slug)

    # instantiate a form
    if request.method == 'POST':
        data = request.POST.copy()
        data['article_slug'] = slug
        comment_form = CommentForm(data)
        if comment_form.is_valid():
            comment_form.save()
            return HttpResponseRedirect('/%s/#comments' % slug)
    else:
        comment_form = CommentForm()

    return render_to_response(
        'blog/leave_comment.html',
        Context(dict(comment_form=comment_form, article=article)) )
    


def search( request ):
    'A simple form for full text searches in the contents of all articles.'
    
    # find the search criteria
    if request.method == 'GET' and 'keyword' in request.GET:
        keyword = request.GET.get('keyword','')
        includeAllTags = ( 'alltags' in request.GET )
        leftBlank = not keyword
        
        search_form = SearchForm(request.GET, includeAllTags )
    else:
        keyword = ''
        leftBlank = False

        search_form = SearchForm()

    # find the search results
    if keyword:
        keywordQ = parseSearchExpression(keyword)

        # optionally filter by tags
        # todo: fix edge case where no tags are selected
        tagQ = Q()
        if not includeAllTags:
            for name,value in request.GET.iteritems():
                if 'include_' in name and value:
                    tagSlug = name[len('include_'):].replace('_','-')
                    tagQ = tagQ | Q(tag__slug=tagSlug)

        searchQ = keywordQ & tagQ
        results = Article.objects.filter(searchQ).distinct()
        
    else:
        results = Article.objects.none()
    
    return render_to_response(
        'blog/search.html',
        Context(dict(
            request=request,
            search_form=search_form,
            results=results,
            keyword=keyword,
            left_blank=leftBlank)) )



### Error Pages

def error(request,code):
    ' intentionally cause errors, for testing. '
    if code == '500':
        x = 1/0  # any uncaught error causes a 500
    # 404 is the default because if they pass an unknown code, that's
    # a page not found error, isn't it?
    raise Http404

def server_error(request, template_name='500.html'):
    ' also sends an e-mail to the admins. '
    try:
        from django.core.mail import send_mail
        from django.conf import settings  # settings is not a module.
        for admin, email in settings.ADMINS:
            send_mail('500 Error in Blog app at oranlooney.com',
                      'Hi %s,\n\n   The site is broken.  Go fix it!\n' % admin,
                      'oranlooney@olooney.com',
                      [email])
        sent_email = True
    except:
        sent_email = False

    t = loader.get_template(template_name)
    return http.HttpResponseServerError(t.render(Context( dict(sent_email=sent_email) )))
