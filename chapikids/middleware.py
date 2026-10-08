"""
Middleware para agregar headers de seguridad adicionales.
"""


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Headers de seguridad
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Content Security Policy básico, SOLO para el sitio público.
        #
        # El panel de /admin/ se queda sin CSP a propósito: usa scripts y
        # estilos propios de Django que no están en esta lista, y aplicarles
        # esta política deja al administrador afuera de su propio panel. Es el
        # mismo motivo por el que Django se salta CSP en /admin/.
        if not request.path.startswith('/admin/'):
            csp = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' "
                "https://www.googletagmanager.com; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com; "
                "img-src 'self' data: https:; "
                "connect-src 'self'; "
                "frame-ancestors 'none';"
            )
            response['Content-Security-Policy'] = csp

        return response