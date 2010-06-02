

link_templates = {'urn:crp:individual': None,
                   'urn:crp:organization':
                        {'label': "OpenSecrets.org",
                         'main': "http://www.opensecrets.org/orgs/summary.php?id=%s",
                         'cycle': "http://www.opensecrets.org/orgs/toprecips.php?id=%s&cycle=%s"},
                   'urn:crp:recipient': 
                        {'label': 'OpenSecrets.org',
                         'main': "http://www.opensecrets.org/politicians/summary.php?cid=%s", 
                         'cycle': "http://www.opensecrets.org/politicians/summary.php?cid=%s&cycle=%s"},
                   'urn:nimsp:individual': None,
                   'urn:nimsp:organization': 
                        {'label': "FollowTheMoney.org",
                         'main': "http://www.followthemoney.org/database/topcontributor.phtml?u=%s", 
                         'cycle':"http://www.followthemoney.org/database/topcontributor.phtml?u=%s&y=%s"},
                   'urn:nimsp:recipient': 
                        {'label': "FollowTheMoney.org",
                         'main': "http://www.followthemoney.org/database/uniquecandidate.phtml?uc=%s",}}


def get_direct_link(namespace, id, cycle=None):
    template = link_templates[namespace]
    if not template:
        return None
 
    if cycle and 'cycle' in template:
        return (template['label'], template['cycle'] % (id, cycle))
    else:
        return (template['label'], template['main'] % id)
    
    
def get_links(entity_info, cycle=None):
    """ Return a list of (label, url) pairs. Expects as an argument the structure returned by api.entity_metadata(). """
    
    links = []
    for (namespace, id) in [(ext['namespace'], ext['id']) for ext in entity_info['external_ids']]:
        link = get_direct_link(namespace, id, cycle)
        if link:
            links.append(link)
            
    return links

