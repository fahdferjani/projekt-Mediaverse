from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from core.models import Resource , BorrowTransaction
from .serializers import BorrowTransactionSerializer
from datetime import date, timedelta



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def borrow_resource(request, resource_id):
    """
    API endpoint for borrowing a resource.

    Parameters:
        request (HttpRequest): The HTTP request object containing metadata and user information.
        resource_id (int): The ID of the resource to be borrowed.

    Returns:
        JsonResponse: A JSON response indicating the result of the borrowing operation.

    Raises:
        Http404: If the specified resource does not exist.

    Permissions:
        - User must be authenticated.
        - User must have permission to borrow resources.

    Usage:
        The API should be called with a POST request including the resource ID to be borrowed.
    """

    # Retrieve the specified resource
    resource = get_object_or_404(Resource, id=resource_id)

    # Check if the resource is available for borrowing
    if not resource.is_available():
        return Response({'detail': 'Resource is not available for borrowing.'}, status=status.HTTP_400_BAD_REQUEST)

    # Get the authenticated user
    user = request.user
    borrow_date = date.today()

    # Calculate the due date as 2 weeks from now
    due_date = borrow_date + timedelta(days=14)

    # Borrow the resource for the user
    resource.borrow(user, borrow_date, due_date)

    # Return a success response
    return Response({'detail': 'Resource borrowed successfully'}, status=status.HTTP_200_OK)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def extend_due_date(request, transaction_id):
    """
    API endpoint for extending the due date of a borrow transaction.

    Parameters:
        request (HttpRequest): The HTTP request object containing metadata and user information.
        transaction_id (int): The ID of the borrow transaction to extend.

    Returns:
        Response: The HTTP response indicating the result of the operation.

    Raises:
        BorrowTransaction.DoesNotExist: If the specified borrow transaction does not exist.
        ValidationError: If there is a validation error when extending the due date.

    Notes:
        - This endpoint requires authentication using a token.
        - Only authenticated users can extend the due date of their own borrow transactions.

    Usage:
        The API should be called with a POST request including the transaction ID to be extended.
    """

    try:
        # Retrieve the specified borrow transaction
        transaction = BorrowTransaction.objects.get(id=transaction_id, user=request.user, returned=False)

        # Calculate the new due date by adding 14 days to the current due date
        new_due_date = transaction.due_date + timedelta(days=14)

        # Extend the due date of the borrow transaction
        transaction.extend_due_date(new_due_date)

        # Return a success response
        return Response(status=status.HTTP_200_OK)

    except BorrowTransaction.DoesNotExist:
        return Response({'detail': 'Borrow transaction not found.'}, status=status.HTTP_404_NOT_FOUND)

    except ValidationError as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def return_resource(request, transaction_id):
    """
    API endpoint for returning a borrowed resource.

    Parameters:
        request (HttpRequest): The HTTP request object containing metadata and user information.
        transaction_id (int): The ID of the borrow transaction for returning the resource.

    Returns:
        Response: The HTTP response indicating the result of the operation.

    Raises:
        BorrowTransaction.DoesNotExist: If the specified borrow transaction does not exist.

    Notes:
        - This endpoint requires authentication using a token.
        - Only authenticated users can return their own borrowed resources.

    Usage:
        The API should be called with a POST request including the transaction ID for returning the resource.
    """

    transaction = get_object_or_404(BorrowTransaction, id=transaction_id, user=request.user, returned=False)

    if transaction.returned:
        return Response({'detail': 'Resource is already marked as returned.'}, status=status.HTTP_400_BAD_REQUEST)

    transaction.return_resource()
    transaction.resource.is_available_to_borrow = True
    transaction.resource.save()

    return Response({'detail': 'Resource returned successfully.'}, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_actual_borrowed_resources(request):
    """
    API endpoint for retrieving the list of currently borrowed resources by the authenticated user.

    Parameters:
        request (HttpRequest): The HTTP request object containing metadata and user information.

    Returns:
        Response: The HTTP response containing the list of borrowed resources.

    Usage:
        The API should be called with a GET request to retrieve the borrowed resources.

    Notes:
        - This endpoint requires authentication using a token.
        - Only authenticated users can access their own list of borrowed resources.
    """

    user = request.user
    transactions = BorrowTransaction.objects.filter(user=user, returned=False)
    serializer = BorrowTransactionSerializer(transactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_previous_borrowed_resources(request):
    """
    API endpoint for retrieving the list of previously borrowed resources by the authenticated user.

    Parameters:
        request (HttpRequest): The HTTP request object containing metadata and user information.

    Returns:
        Response: The HTTP response containing the list of previously borrowed resources.

    Usage:
        The API should be called with a GET request to retrieve the previously borrowed resources.

    Notes:
        - This endpoint requires authentication using a token.
        - Only authenticated users can access their own list of previously borrowed resources.
    """

    user = request.user
    transactions = BorrowTransaction.objects.filter(user=user, returned=True)
    serializer = BorrowTransactionSerializer(transactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
