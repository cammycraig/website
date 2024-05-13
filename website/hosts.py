from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'gearstore', 'gearstore_app.urls', name='gearstore'),
    host(r'portfolio', 'portfolio_app.urls', name='portfolio'),
)