import urllib, re
from django.template.defaultfilters import urlencode

def get_direct_link(name, namespace, ext_id, cycle=None):
    """ Return a (label, url) pair for a namespace and name. """
    without_cycle_links = {
        'urn:crp:recipient':      ("OpenSecrets.org",    "http://www.opensecrets.org/usearch/index.php?q={0}".format(urlencode(name))),
        'urn:crp:organization':   ("OpenSecrets.org",    "http://www.opensecrets.org/usearch/index.php?q={0}".format(urlencode(name))),
        'urn:nimsp:organization': ("FollowTheMoney.org", "http://www.followthemoney.org/database/topcontributor.phtml?u={0}".format(ext_id)),
        'urn:nimsp:recipient':    ("FollowTheMoney.org", "http://www.followthemoney.org/database/uniquecandidate.phtml?uc={0}".format(ext_id)),
    }

    with_cycle_links = without_cycle_links.copy()
    with_cycle_links.update({
        'urn:nimsp:organization': ("FollowTheMoney.org", "http://www.followthemoney.org/database/topcontributor.phtml?u={0}&y={1}".format(ext_id, cycle)),
    })

    return with_cycle_links.get(namespace, None) if cycle else without_cycle_links.get(namespace, None)


def get_links(standardized_name, namespaces_and_ids, cycle):
    """ Return a list of (label, url) pairs. Expects as an argument the structure returned by api.entity_metadata(). """

    links = []
    for pair in namespaces_and_ids:
        link = get_direct_link(standardized_name, pair['namespace'], pair['id'], cycle)
        if link:
            links.append({'text': link[0], 'url': link[1]})

    return links

