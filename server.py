import readline
from wsgiref.simple_server import make_server


def request_path(environ):
    url = environ['PATH_INFO']
    if environ['QUERY_STRING']:
        return '%s?%s' % (url, environ['QUERY_STRING'])
    return url


def request_headers(environ):
    headers = []
    for name, val in environ.iteritems():
        if name.startswith('HTTP_'):
            name = '-'.join([part.capitalize()
                             for part in name[5:].split('_')])
            headers.append('%s: %s' % (name, val))
    return '\n'.join(headers)


def get_input(prompt):
    try:
        return raw_input(prompt)
    except EOFError:
        return ''


def server_prompt(environ):
    path = request_path(environ)
    method = environ['REQUEST_METHOD']
    print '\n\n%s %s' % (method, path)
    print request_headers(environ), '\n'

    content_length = int(environ['CONTENT_LENGTH'] or 0)
    if content_length:
        print '---   %s body    ---' % method
        print environ['wsgi.input'].read(content_length)
        print '---end of %s body---' % method

    remote = environ.get('REMOTE_HOST', 'somebody')
    inp = get_input('%s wants %s\n>>> ' % (remote, path))
    while inp and inp != '\n':
        yield inp
        inp = '\n' + get_input('... ')
    print ''


def manual_handler(environ, start_response):
    response = server_prompt(environ)

    start_response('200 OK', [])
    return list(response)


def run():
    httpd = make_server('', 8000, manual_handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print ' Bye!'


if __name__ == '__main__':
    run()
