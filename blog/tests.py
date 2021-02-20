from django.test import TestCase

# Create your tests here.
import markdown
s = "## hell-world"
print(markdown.markdown(s))
s2 = "$$f_(x)$$"
body = markdown.markdown(s2,
                              extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite',
                                          'markdown.extensions.tables', 'markdown.extensions.toc', 'mdx_math'],
                              extension_configs={
                                  'mdx_math': {'enable_dollar_delimiter': True}
                              }
                              )
print(markdown.markdown(body))
