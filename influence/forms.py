from django.core.context_processors import request
from django import forms


DEFAULT_ELECTION_CYCLES = [('1990', '1990'), 
                           ('1992', '1992'),
                           ('1994', '1994'), 
                           ('1996', '1996'), 
                           ('1998', '1998'),
                           ('2000', '2000'), 
                           ('2002', '2002'), 
                           ('2004', '2004'),
                           ('2006', '2006'), 
                           ('2008', '2008'), 
                           ('2010', '2010'),
                           (-1, 'Lifetime')]

class SearchForm(forms.Form):
    query = forms.CharField(max_length=200, initial='SEARCH')

class ElectionCycle(forms.Form):    
    ELECTION_CYCLES = DEFAULT_ELECTION_CYCLES

    ELECTION_CYCLES.reverse()
    cycle = forms.ChoiceField(choices=ELECTION_CYCLES, initial='Lifetime')

    def __init__(self, cycles=None, *args, **kwargs):       
        # call to super() must go before customizing the cycle field
        super(ElectionCycle, self).__init__(*args, **kwargs)
        if cycles:
            cycles.sort()
            # -1 will always be the smallest number, so take the
            # second smallest to get the first real year.
            #career = "All: %s - %s" % (cycles[1], cycles[-1])
            self.fields['cycle'].choices = [(cycle, "%d - %s" % (int(cycle)-1, cycle)) 
                                            for cycle in cycles if cycle != "-1"] + [(-1, "All Cycles")]
