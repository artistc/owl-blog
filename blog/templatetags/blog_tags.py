from django import template
from django.template import Variable
from django.template import VariableDoesNotExist
from django.utils.safestring import mark_safe
from django.utils import html
from django.utils.functional import allow_lazy

register = template.Library()

def stub(modelObject, postfix='stub'):
    'renders a model object by looking for a template named'
    '%(modelName)s_stub.html somewhere in the templates directory.'
    'none of the template context will be aviable, but modelObject'
    'will be available as the (lowercase) object name.'
    'fails quietly.'
    
    # figure out the template name from the object name
    try:
        modelName = modelObject._meta.object_name
        appLabel = modelObject._meta.app_label
    except AttributeError:
        return str(modelObject)
    templateName = '%s/%s_%s.html' % (appLabel, modelName.lower(), postfix)

    # load the template
    try:
        stubTemplate = template.loader.get_template(templateName)
    except template.TemplateDoesNotExist:
        return str(modelObject) + "(couldn't find %)" % templateName

    # render the template and mark it safe
    return stubTemplate.render(
        template.Context({modelName.lower():modelObject})
    )

register.filter('stub',stub)

def stripMarkup( string ):
	return html.strip_tags( html.strip_entities( string ) )
register.filter('stripmarkup', stripMarkup)


def error_list(items,css_class='error'):
    if len(items) == 0: return ''
    if css_class:
        class_attribute = 'class="%s" ' % css_class
    else:
        class_attribute = ''

    return mark_safe(
        u'<small %s>[' % class_attribute + \
            '<br/>'.join([html.escape(unicode(i)) for i in items]) + \
        u']</small><br/>' )

register.filter('error_list',error_list)

