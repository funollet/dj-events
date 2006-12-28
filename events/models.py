# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext_lazy as _
from djapps.misc.markup import markup_help, parse_markup
from djapps.tags.models import Tag
from djapps.tags import fields



class EventCategory (models.Model):
    """Single-level category system with ordering, color and icon.
    """
    name = models.CharField (_('name'), maxlength=200, )
    
    permalink = models.SlugField (_('permalink'),
        prepopulate_from = ('name',),
        unique = True,
        help_text = _('Easy-to-link name (good, if short, twice good).')
    )
    priority = models.PositiveIntegerField (_('priority'),
        unique = True,
        help_text = _('Categories will be sorted by this field.')
    )
    color = models.CharField (_('color'),
        maxlength = 10,
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
            (None, {'fields': (('name', 'priority',), 'color',)}),
            (_('Advanced'), {'fields': ('permalink', 'icon',), 'classes': 'collapse'})
            )
        list_display = ('name', 'priority',)
        #js = ('/js/jquery.pack.js', '/js/farbtastic.js', '/js/colorpicker.js',)
    
    def __str__ (self):
        return self.name



class Event (models.Model):
    
    startdate = models.DateTimeField (_('start day and hour'), )
    abstract = models.CharField (_('abstract'), maxlength=200,
        help_text = _('Short text describing the event.'),
    )
    body = models.TextField (_('body_html'), editable=False,)
    body_markup = models.TextField (_('body'), 
        blank = True,
        help_text = markup_help['docutils'],
    )

    permalink = models.SlugField (_('permalink'),
        prepopulate_from = ('abstract',),
        unique = True,
        help_text = _('Easy-to-link name (good, if short, twice good).'),
    )
    category = models.ForeignKey (EventCategory,
        verbose_name=_('category'),
    )
    tags = fields.TagsField(Tag,
        blank = True,
    )


    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
    
    class Admin:
        date_hierarchy = 'startdate'
        list_display = ('abstract', 'startdate',)
        list_filter = ('category',)
        search_fields = ('abstract',)

        
    def __str__ (self):
        return self.abstract
    
    def get_absolute_url (self):
        pass

    def save (self):
        parse_markup (self)
        super(Event, self).save()
