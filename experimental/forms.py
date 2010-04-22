from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(max_length=200)

class ElectionCycle(forms.Form):    
    ELECTION_CYCLES = [('1990', '1990'), ('1991', '1991'), ('1992', '1992'),
                       ('1993', '1993'), ('1994', '1994'), ('1995', '1995'),
                       ('1996', '1996'), ('1997', '1997'), ('1998', '1998'),
                       ('1999', '1999'), ('2000', '2000'), ('2001', '2001'),
                       ('2002', '2002'), ('2003', '2003'), ('2004', '2004'),
                       ('2005', '2005'), ('2006', '2006'), ('2007', '2007'),
                       ('2008', '2008'), ('2009', '2009'), ('2010', '2010'),
                       ]
    ELECTION_CYCLES.reverse()
    cycle = forms.ChoiceField(choices=ELECTION_CYCLES, initial='2010')
