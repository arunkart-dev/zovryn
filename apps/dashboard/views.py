from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from apps.roles.permissions import IsAnalystOrAdmin
from .services import get_category_totals, get_monthly_analytics, get_user_totals


@api_view(['GET'])
@permission_classes([IsAnalystOrAdmin])   # viewer gets 403; analyst + admin allowed
def dashboard_analytics(request):
    """
    GET /dashboard/analytics/

    Access:
      viewer  → 403 Forbidden
      analyst → allowed
      admin   → allowed
    """
    user = request.user

    totals           = get_user_totals(user)
    category_income  = list(get_category_totals(user, 'income'))
    category_expense = list(get_category_totals(user, 'expense'))
    monthly          = list(get_monthly_analytics(user))

    paginator = PageNumberPagination()
    paginator.page_size = 5

    category_income_paginated  = paginator.paginate_queryset(category_income, request)
    category_expense_paginated = paginator.paginate_queryset(category_expense, request)
    monthly_paginated          = paginator.paginate_queryset(monthly, request)

    return Response({
        "totals":           totals,
        "category_income":  paginator.get_paginated_response(category_income_paginated).data,
        "category_expense": paginator.get_paginated_response(category_expense_paginated).data,
        "monthly":          paginator.get_paginated_response(monthly_paginated).data,
    })