# -*- utf-8 -*-

from django.template import Node, Library
from django.utils.datastructures import MultiValueDict
from calendar import monthrange

register = Library()


class MakeMonthArrayNode (Node):
    
    def __init__ (self):
        self.year = None
        self.month = None
        self.data = MultiValueDict()
        self._weekday = None    # Weekday (Monday==0) for day 1 in this moth.
        self._n_days = None     # Number of days in month.
        
        
    def _n_added_days(self):
        """Number of added days at the end of the month to have a "full week"."""
        return ( 7 - (self._weekday + self._n_days)%7 ) % 7
    
    
    def __list2array__ (self, l, ncols=7):
        """Splits list l in lists of len()=cols. l must be "squareable".
        """
        return [ l[row*ncols:(row+1)*ncols] for row in range(0, len(l)/ncols) ]


    def squared (self):
        """Inserts keys and values in an array of days (month's calendar).
        
        Returns a list of weeks.
        One week, one list of days.
        One day, one list with [ <day-number> , [<data for this day>] ]
        """
        
        # Insert [None] in remaining days. IN PLACE.
        for i in range(1, self._n_days+1):
            if not self.data.has_key(i):
                self.data[i] = None
        
        # zerofill out-of-month days
        before = self._weekday * [[0,[None]]]
        after = self._n_added_days() * [[0,[None]]]
        # cat three lists and split per weeks
        return self.__list2array__ (before + self.data.lists() + after)
    
    
    
    def render(self, context):
        try:
            self.year = context['month'].year
            self.month = context['month'].month
            self._weekday, self._n_days = monthrange(self.year, self.month)
                
            for o in context['object_list']:
                self.data.appendlist (o.startdate.day, o)
                
            context['month_array'] = self.squared()
        except:
            pass
        return ''



@register.tag
def make_month_array (parser, token):
    return MakeMonthArrayNode()
