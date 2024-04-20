from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Theater, Showtime, Ticket, Reservation
from movies import serializers
from .serializers import (
    MovieSerializer,
    TheaterSerializer,
    ShowtimeSerializer,
    ReservationSerializer,
    TicketSerializer,
    RegisterSerializer,
    UserLoginSerializer,
)
from datetime import timezone
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from .validations import validate_username, validate_password
from django.contrib.auth import login, logout
from rest_framework.views import APIView


class MovieListCreateView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class TheaterListCreateView(generics.ListCreateAPIView):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer


class TheaterRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer


class ShowtimeListCreateView(generics.ListCreateAPIView):
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer


class ShowtimeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer
    
    permission_classes = []
    authentication_classes = (TokenAuthentication,)

    # Implement validation checks for showtime date and time
    def perform_update(self, serializer):
        if serializer.validated_data['date_and_time'] <= timezone.now():
            raise serializers.ValidationError(
                "Showtime date and time must be in the future.")
        serializer.save()

    def perform_create(self, serializer):
        if serializer.validated_data['date_and_time'] <= timezone.now():
            raise serializers.ValidationError(
                "Showtime date and time must be in the future.")
        serializer.save()


class AvailableSeatsView(generics.RetrieveAPIView):
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer

    def get(self, request, *args, **kwargs):
        return Response({"available_seats": Showtime.available_seats})


class ReserveSeatsView(generics.UpdateAPIView):
    queryset = Showtime.objects.all()
    permission_classes = []
    authentication_classes = (TokenAuthentication,)
    serializer_class = ReservationSerializer

    # Implement validation checks for available seats
    def perform_update(self, serializer, instance=None):
        requested_seats = self.request.data.get('requested_seats')
        if requested_seats is None:
            return Response({"message": "Number of requested seats is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Split requested seats into a list
        requested_seats_list = requested_seats.split(',')
        # Assuming seats are stored as comma-separated string
        available_seats_list = instance.seats.split(',')

        # Check for invalid seat numbers or duplicates
        invalid_seats = set(requested_seats_list) - set(available_seats_list)
        if invalid_seats:
            return Response({"message": f"Invalid seat(s): {', '.join(invalid_seats)}"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check for enough available seats
        if len(requested_seats_list) > len(available_seats_list):
            return Response({"message": "Not enough available seats."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update available seats in Showtime
        # Intersection of requested and available seats
        reserved_seats = set(requested_seats_list) & set(available_seats_list)
        remaining_seats = [
            seat for seat in available_seats_list if seat not in reserved_seats]
        instance.seats = ','.join(remaining_seats)
        instance.save()

        if requested_seats > instance.available_seats:
            raise serializers.ValidationError("Not enough available seats.")

        # Create a Reservation object
        reservation = Reservation(
            seats=','.join(requested_seats_list),
            show=instance,
            user=self.request.user
        )

        reservation.save()
        return Response({"message": "Seats reserved successfully."},
                        status=status.HTTP_201_CREATED)


class PurchaseTicketsView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def post(self, request, *args, **kwargs):
        # Assuming reservation ID and seat type are sent in the request body
        reservation_id = request.data.get('reservation_id')
        seat_type = request.data.get('seat_type')

        if not reservation_id:
            return Response({"message": "Reservation ID is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the reservation object from the database
            reservation = Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            return Response({"message": "Reservation not found."},
                            status=status.HTTP_404_NOT_FOUND)

        # Define mapping of seat types to ticket prices
        seat_type_prices = {
            'RECLINER': 300.00,
            'PRIME': 200.00,
            'CLASSIC': 100.00,
        }

        # Check if the provided seat type is valid
        if seat_type not in seat_type_prices:
            return Response({"message": "Invalid seat type."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the ticket price based on the seat type
        ticket_price = seat_type_prices[seat_type]

        # Create ticket object based on the reservation and seat type
        ticket_data = {
            'reservation': reservation,
            'price': ticket_price,
        }
        ticket_serializer = self.get_serializer(data=ticket_data)
        ticket_serializer.is_valid(raise_exception=True)
        ticket_serializer.save()
        return Response({"message": "Tickets purchased successfully."}, 
                        status=status.HTTP_201_CREATED)


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        data = request.data
        assert validate_username(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            return Response({"success": "Successfully Logged In"}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    def post(self, request):
        logout(request)
        return Response({"success": "Successfully logged out."}, status=status.HTTP_200_OK)
