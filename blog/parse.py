'''
 handle the parsing of search expressions.
'''

from django.db.models import Q

# TODO: also handle OR
def parseSearchExpression(expression):
    '''
    Given of an input of a search string containing the boolean
    operators AND and OR, returns a q object for the equivalent
    search.
    '''

    # this is the easiest way to access the polymorphic operators | and &
    def qOr(q1,q2): return q1 | q2
    def qAnd(q1,q2): return q1 & q2

    expression = expression.upper()
    orClauses = expression.split(' OR ')
    if not orClauses: return Q()
    innerQs = []
    for orClause in orClauses:
        words = [ word for word in orClause.split() if word not in ['AND'] ]
        if words:
            titleAndContentQs = [
                Q(content__icontains=word) | \
                Q(title__icontains=word)
                for word in words]
            innerQ = reduce(qAnd, titleAndContentQs)
        else:
            innerQ = Q()
        innerQs.append(innerQ)
    return reduce(qOr, innerQs)



