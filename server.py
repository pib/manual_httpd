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
    print '\n\n%s %s' % (environ['REQUEST_METHOD'], path)
    print request_headers(environ), '\n'

    remote = environ.get('REMOTE_HOST', 'somebody')
    inp = get_input('%s wants %s\n>>> ' % (remote, path))
    while inp and inp != '\n':
        yield inp
        inp = '\n' + get_input('... ')
    print ''


def manual_handler(environ, start_response):
    response = server_prompt(environ)

    if environ['REQUEST_METHOD'] == 'HEAD':
        length = ''.join(response)
        start_response('200 OK', [('Content-Length', length)])
        return []
    start_response('200 OK', [])
    return response


def run():
    httpd = make_server('', 8000, manual_handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print ' Bye!'


if __name__ == '__main__':
    run()
