from datetime import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import phonenumbers
from phonenumbers import geocoder, carrier, is_valid_number, number_type, PhoneNumberType


def index(request):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render(request, 'example/index.html', {'current_time': current_time})


class PhoneInfoView(APIView):
    def get(self, request):
        phone_number = request.query_params.get('phone_number')
        if not phone_number:
            return Response({"error": "Phone number is required"}, status=400)
        return self.process_phone_number(phone_number)

    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({"error": "Phone number is required"}, status=400)
        return self.process_phone_number(phone_number)

    def process_phone_number(self, phone_number):
        try:
            print(f"Processing phone number: {phone_number}")  # Débogage
            # Nettoyer le numéro
            phone_number = phone_number.strip().replace(" ", "").replace("-", "")
            print(f"Cleaned phone number: {phone_number}")  # Débogage

            # Parser le numéro
            parsed_number = None
            if not phone_number.startswith("+"):
                parsed_number = phonenumbers.parse(f"+{phone_number}", None)
            else:
                parsed_number = phonenumbers.parse(phone_number, None)
            print(f"Parsed number: {parsed_number}")  # Débogage

            # Vérifier si le parsing a réussi
            if parsed_number is None:
                raise ValueError("Failed to parse phone number")

            location = geocoder.description_for_number(parsed_number, "fr")
            service_provider = carrier.name_for_number(parsed_number, "fr")
            num_type = number_type(parsed_number)

            type_names = {
                PhoneNumberType.FIXED_LINE: "FIXED_LINE",
                PhoneNumberType.MOBILE: "MOBILE",
                PhoneNumberType.FIXED_LINE_OR_MOBILE: "FIXED_LINE_OR_MOBILE",
                PhoneNumberType.TOLL_FREE: "TOLL_FREE",
                PhoneNumberType.PREMIUM_RATE: "PREMIUM_RATE",
                PhoneNumberType.SHARED_COST: "SHARED_COST",
                PhoneNumberType.VOIP: "VOIP",
                PhoneNumberType.PERSONAL_NUMBER: "PERSONAL_NUMBER",
                PhoneNumberType.PAGER: "PAGER",
                PhoneNumberType.UAN: "UAN",
                PhoneNumberType.VOICEMAIL: "VOICEMAIL",
                PhoneNumberType.UNKNOWN: "UNKNOWN",
            }

            response_data = {
                "phone_number": phone_number,
                "country_code": parsed_number.country_code,
                "national_number": parsed_number.national_number,
                "location": location,
                "service_provider": service_provider,
                "is_valid_number": is_valid_number(parsed_number),
                "number_type": type_names.get(num_type, "UNKNOWN")
            }
            return Response(response_data, status=200)

        except phonenumbers.NumberParseException as e:
            return Response({"error": f"Invalid phone number: {str(e)}"}, status=400)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=500)
