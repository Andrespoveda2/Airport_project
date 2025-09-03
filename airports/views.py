from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests


# Vista para renderizar la página principal
def airport_distance_views(request):
    return render(request, "airport_distance.html")


@csrf_exempt
def calculate_distance(request):
    if request.method == "POST":
        try:
            aeropuerto_origen = (
                request.POST.get("aeropuerto_origen", "").strip().upper()
            )
            aeropuerto_destino = (
                request.POST.get("aeropuerto_destino", "").strip().upper()
            )

            # Validaciones
            if not aeropuerto_origen or not aeropuerto_destino:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Ambos códigos de aeropuerto son requeridos.",
                    },
                    status=400,
                )

            if len(aeropuerto_origen) != 3 or len(aeropuerto_destino) != 3:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Los códigos IATA deben tener exactamente 3 letras.",
                    },
                    status=400,
                )

            if aeropuerto_origen == aeropuerto_destino:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "El origen y destino no pueden ser iguales.",
                    },
                    status=400,
                )

            # Petición a la API
            base_url = "https://airportgap.com/api/airports/distance"
            data = {"from": aeropuerto_origen, "to": aeropuerto_destino}
            response = requests.post(base_url, json=data)

            if response.status_code == 200:
                datos = response.json()
                atributos = datos.get("data", {}).get("attributes", {})

                info = {
                    "origen": {
                        "nombre": atributos.get("from_airport", {}).get("name"),
                        "ciudad": atributos.get("from_airport", {}).get("city"),
                        "iata": atributos.get("from_airport", {}).get("iata"),
                        "pais": atributos.get("from_airport", {}).get("country"),
                        "codigo": aeropuerto_origen,
                    },
                    "destino": {
                        "nombre": atributos.get("to_airport", {}).get("name"),
                        "ciudad": atributos.get("to_airport", {}).get("city"),
                        "iata": atributos.get("to_airport", {}).get("iata"),
                        "pais": atributos.get("to_airport", {}).get("country"),
                        "codigo": aeropuerto_destino,
                    },
                    "distancia_km": atributos.get("kilometers"),
                    "distancia_millas": atributos.get("miles"),
                    "distancia_nauticas": atributos.get("nautical_miles"),
                }

                return JsonResponse({"success": True, "data": info})
            elif response.status_code == 422:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Datos de entrada no válidos.",
                    },
                    status=422,
                )

            else:
                return JsonResponse(
                    {
                        "success": False,
                        "error": f"Error en la API (status {response.status_code}).",
                    },
                    status=response.status_code,
                )
        except requests.exceptions.Timeout:
            return JsonResponse(
                {
                    "success": False,
                    "error": "La solicitud ha excedido el tiempo de espera.",
                },
                status=408,
            )
        except requests.exceptions.ConnectionError:
            return JsonResponse(
                {"success": False, "error": "Error de conexión."}, status=503
            )

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Método no permitido."}, status=405)
