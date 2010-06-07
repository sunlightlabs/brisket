from influence.forms import SearchForm

def custom_context(request):
    return {'search_form': SearchForm()}
    
