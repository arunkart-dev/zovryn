# apps/records/pagination.py

from rest_framework.pagination import PageNumberPagination

class RecordPagination(PageNumberPagination):
    page_size = 5        # 5 records per page
    page_size_query_param = 'page_size'  # allow client to change page size
    max_page_size = 50