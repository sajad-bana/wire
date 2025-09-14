# apps/wire/pagination.py

from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    """
    Custom pagination class to allow the client to set the page size.
    """
    # The default number of items to return per page.
    page_size = 10
    
    page_size_query_param = 'page_size'
    
    # The maximum page size that can be requested.
    max_page_size = 100
