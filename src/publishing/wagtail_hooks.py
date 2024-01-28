from django.utils.html import format_html
from django.templatetags.static import static
from wagtail import hooks
from wagtail.snippets.models import register_snippet

from .models import Author
from wagtail.snippets.views.snippets import SnippetViewSet

class AuthorViewSet(SnippetViewSet):
    model = Author
    icon = "user"
    add_to_admin_menu = True



@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static('css/custom.css'))


register_snippet(AuthorViewSet)