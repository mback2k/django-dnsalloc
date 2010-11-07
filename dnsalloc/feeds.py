from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from dnsalloc.models import Service, Result
from django.shortcuts import get_object_or_404

class ResultFeed(Feed):
    def get_object(self, request, id):
        return get_object_or_404(Service, id=id)

    def title(self, obj):
        return 'DNS Allocator - Status Feed: %s' % obj.hostname

    def description(self, obj):
        return 'Shows the latest IP update results from DNS-O-Matic'

    def link(self, obj):
        return reverse('dnsalloc.views.show_item', kwargs={'id': obj.id})

    def items(self, obj):
        return obj.results

    def item_link(self, item):
        return '%s#%d' % (reverse('dnsalloc.views.show_item', kwargs={'id': item.service_id}), item.id)

    def item_pubdate(self, item):
        return item.crdate
