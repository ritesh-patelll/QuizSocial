from django_brotli.middleware import BrotliMiddleware as OriginalBrotliMiddleware


class BrotliMiddleware(OriginalBrotliMiddleware):
    FONT_EXTENSIONS = (
        '.otf',
        '.ttf',
        '.woff',
        '.woff2',
    )

    def process_response(self, request, response):
        # If the URL ends with a font file extension, skip compression
        if request.path.endswith(self.FONT_EXTENSIONS):
            return response

        return super().process_response(request, response)