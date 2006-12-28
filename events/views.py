from django.views.generic.date_based import archive_month
from django.http import HttpResponseRedirect
from djapps.events.models import EventCategory
from datetime import date, timedelta
from time import strptime

### Utility functions.

def _make_categories_list (request):
    
    # ['', 'events', '2006', '12', ....]
    categ_url = request.path.split('/')
    
    # Insert one link to every category.
    categories_links = [ {
        'name': ec.name, 
        'url': '/'.join( categ_url[:4] + ['%s', ''] ) % ec.permalink, 
    } for ec in EventCategory.objects.all() ]
    # Prepend a link for "no-category".
    categories_links.insert(0, {
        'name': 'all',
        'url': '/'.join( categ_url[:4]+[''] ),
    } )
    
    return categories_links




def _month_nav_urls (request):
    
    month_url = request.path.split('/')
    year = month_url[2]
    month = month_url[3]
    # Mask year and month on the url.
    month_url[2] = '%s'
    month_url[3] = '%s'
    
    # Previous-next month tricky maths.
    date_tuple = strptime( year+month, '%Y%m')[:3]
    first_day = date(*date_tuple).replace(day=1)
    if first_day.month == 12:
        last_day = first_day.replace(year=first_day.year + 1, month=1)
    else:
        last_day = first_day.replace(month=first_day.month + 1)

    prev_next = [None, None]     # previous month, next month
    prev_next[0] = first_day - timedelta(days=1)
    prev_next[1] = last_day + timedelta(days=1)
    
    # Giving format. Months must be 2-chars-wide.
    prev_next_str = [ ( str(d.year), str(d.month).rjust(2,'0') )  for d in prev_next ]
    prev_next_url = [ '/'.join(month_url) % tpl for tpl in prev_next_str ]
    
    return prev_next_url



### Custom views #######################################################################

def custom_archive_month (request, year, month, queryset, date_field, **kwargs):
    
    # Local list for calculated info. Will be added to 'extra_context'.
    context = {}
    
    if kwargs.has_key('category'):
        # Handling categories: preserve in context and filter objects.
        categ = kwargs.pop('category')
        context['category'] = categ
        queryset = queryset.filter(category__name=categ)
    else:
        context['category'] = None
    
    if kwargs.has_key('tags'):
        # Handling tags: preserve in context and filter objects.
        tags = kwargs.pop('tags')
        context['tags'] = tags
        queryset = queryset.filter (tags__value=tags)
    else:
        context['tags'] = None
    
    context['previous_month_url'], context['next_month_url'] = _month_nav_urls (request)
    context['categories_list'] = _make_categories_list(request)
    
    # Insert 'context' in 'extra_context'.
    if kwargs.has_key('extra_context'):
        kwargs['extra_context'].update(context)
    else:
        kwargs['extra_context'] = context

    # Finaly use the good old generic view.
    return archive_month(request, year, month, queryset, date_field, **kwargs)



def redirect_month (request, *args, **kwargs):
    url = request.path.split('/')
    url.insert(2, date.today().strftime('%Y'))
    url.insert(3, date.today().strftime('%m'))
    return HttpResponseRedirect ('/'.join(url))