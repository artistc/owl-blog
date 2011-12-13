import django.forms as forms
from models import Comment, Article, Tag
import re


class CommentForm(forms.Form):
    user_name = forms.CharField( max_length=12 )
    article_slug = forms.CharField( widget=forms.HiddenInput() )
    captcha = forms.CharField( max_length=20 )
    content = forms.CharField( max_length=800, widget=forms.widgets.Textarea )

    def clean_article_slug(self):
        try:
            article = Article.objects.get( slug=self.cleaned_data['article_slug'] )
            self.cleaned_data['article'] = article
        except Article.DoesNotExist:
            raise forms.ValidationError('The comment is not linked to a valid article.')

    def clean_user_name(self):
        name = self.cleaned_data['user_name']
        if 'oran' in name or 'oren' in name or 'looney' in name or 'loony' in name:
            raise forms.ValidationError('This field may not be similar to "Oran Looney."')
        return name

    def clean_captcha(self):
        expectedCaptcha = 'iamnotabot'
        normalizedCaptcha = self.cleaned_data['captcha'].replace(' ','').replace('.', '').lower()
        if normalizedCaptcha != expectedCaptcha:
            raise forms.ValidationError('This field must match the image')
        else:
            return self.cleaned_data['captcha']

    def save(self):
        if not self.is_valid(): return None
        data = self.cleaned_data
        new_comment = Comment(
            user_name=data['user_name'],
            article=data['article'],
            content=data['content'] )
        new_comment.save()

class SearchForm( forms.Form ):
    keyword = forms.CharField( max_length=50 )
    
    # dynamically define all the "include tag" fields
    for tag in Tag.objects.values('slug','title'):
        slug = tag['slug'].replace('-','_')
        locals()['include_' + slug] = \
            forms.BooleanField(label=tag['title'], initial=True)
    del slug

    def __init__( self, data=False, includeAllTags=False ):
        '''
        optionally pre-select all the tags.  This enables us to
        bind to data coming from simple forms with just the keyword.
        '''

        # construct a new dict for each form to handle the default case
        if not data:
            forms.Form.__init__( self )

        else:
            if includeAllTags:
                data = data.copy()
                # To avoid the catch-22 of looping over the fields before
                # the form has been initialed, we instantiate a seperate
                # SearchForm and loop over its fields, which are identical.
                searchFormExemplar = SearchForm()
                for field in searchFormExemplar:
                    if 'include' in field.name:
                        data[ field.name ] = True

            forms.Form.__init__( self, data )
                    

    def include_fields(self):
        ''' Returns a list of just the dynamically generated include boolean
        fields. This can be used from a template as:
        {% for field in form.include_fields %}
          {{field.label}} {{field}} <br/>
        {% endfor %}
        '''
        alphabetical_list = [
            (field.name,field)
            for field in self
            if 'include' in field.name ]
	alphabetical_list.sort()
        return ([ field for name, field in alphabetical_list ])
       
    


