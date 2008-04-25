# -*- coding: utf-8 -*-

from django.db import models, connection
from django.utils.translation import gettext_lazy as _
from tagging.fields import TagField


markup_help = {
    'markdown': _('''<div class="markup_help"><pre>
[un link][1]    *italica*    **negreta**    Titol     - un punt d'una llista
                                            -----     - segon punt
[1]: http://www.un.link.com                            - llista indentada
</pre>(<a href="http://daringfireball.net/projects/markdown/basics">Markdown syntax)</a></div>'''),
    'textile':  _('''<div class="markup_help">
    Use <a href="http://daringfireball.net/projects/markdown/basics">Textile</a> Syntax</div>'''),
    'docutils': _('''
    <div class="markup_help"><pre>
`un link`_    *italica*    **negreta**    Titol     - un punt d'una llista
                                          -----     - segon punt
.. _`un link`: http://www.google.com                 - llista indentada
</pre>(<a href="http://docutils.sourceforge.net/docs/user/rst/quickstart.html">reST syntax</a>: documentation).
    </div>'''),
}


class EventCategory (models.Model):
    """Single-level category system with ordering, color and icon.
    """
    
    def priority_default (increment=10):
        """Returns next suitable value for 'priority' field."""
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(priority) FROM events_eventcategory ;")
        row = cursor.fetchone()
        try:
            return row[0] + increment
        except:
            return increment
    
    
    name = models.CharField (_('name'), max_length=200, )
    
    easyname = models.SlugField (_('easyname'),
        prepopulate_from = ('name',),
        unique = True,
        help_text = _('Easy-to-link name (good, if short, twice good).')
    )
    priority = models.PositiveIntegerField (_('priority'),
        unique = True,
        help_text = _('Categories will be sorted by this field.'),
        default = priority_default,
    )
    color = models.CharField (_('color'),
        max_length = 10,
        default = '#000000',
        # Farbtastic colorpicker looks for this div.
        help_text = _('''<div id="picker"></div>'''),
    )
    icon = models.ImageField (_('icon'),
        upload_to = 'events/category',
        blank = True,
        height_field = 'icon_height', width_field = 'icon_width',
        help_text = _('Optional icon for the category.'),
    )
    # bug#1537  : height and width aren't refreshed on re-save
    icon_height = models.IntegerField(_('icon height'), blank = True, null=True,)
    icon_width = models.IntegerField(_('icon width'), blank = True, null=True, )



    class Meta:
        verbose_name = _('event category')
        verbose_name_plural = _('event categories')
        ordering = ('priority',)
    
    class Admin:
        fields = (
            (None, {'fields': ('name', 'color',)}),
            (_('Advanced'), {'fields': ('easyname', 'priority', 'icon',), 'classes': 'collapse'})
            )
        list_display = ('name', 'priority',)
    
    def __unicode__ (self):
        return self.name



class Event (models.Model):
    
    startdate = models.DateTimeField (_('start day and hour'), )
    abstract = models.CharField (_('abstract'), max_length=200,
        help_text = _('Short text describing the event.'),
    )
    body = models.TextField (_('body'),
        blank = True,
        help_text = markup_help['markdown'],
    )

    easyname = models.SlugField (_('easyname'),
        prepopulate_from = ('abstract',),
        unique = True,
        help_text = _('Easy-to-link name (good, if short, twice good).'),
    )
    category = models.ForeignKey (EventCategory,
        verbose_name=_('category'),
    )
    tags = TagField()


    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
    
    class Admin:
        date_hierarchy = 'startdate'
        list_display = ('abstract', 'startdate',)
        list_filter = ('category',)
        search_fields = ('abstract',)

        
    def __unicode__ (self):
        return self.abstract
    
    def get_absolute_url (self):
        pass