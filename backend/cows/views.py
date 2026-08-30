from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cow, Scan, Prediction
from .serializers import CowSerializer, ScanSerializer, PredictionSerializer


class CowViewSet(viewsets.ModelViewSet):
    queryset = Cow.objects.all()
    serializer_class = CowSerializer
    lookup_field = "cow_id"

    @action(detail=True, methods=["get"])
    def scans(self, request, cow_id=None):
        cow = self.get_object()

        scans = cow.scans.all().order_by("day", "scan_number")

        serializer = ScanSerializer(scans, many=True)

        return Response({
            "cow_id": cow.cow_id,
            "total_scans": scans.count(),
            "scans": serializer.data
        })
    @action(detail=True, methods=["get"])
    def history(self, request, cow_id=None):
        cow = self.get_object()

        scans = cow.scans.all().order_by("day", "scan_number")

        history = []

        for scan in scans:
            history.append({
                "scan_number": scan.scan_number,
                "day": scan.day,
                "temperature_C": scan.temperature_C,
                "milk_pH": scan.milk_pH,
                "somatic_cell_count": scan.somatic_cell_count,
                "milk_yield_L": scan.milk_yield_L,
                "conductivity_raw_mScm": scan.conductivity_raw_mScm,
                "conductivity_temp_adjusted_mScm": (
                    scan.conductivity_temp_adjusted_mScm
                ),
                "clotting": scan.clotting,
                "timestamp": scan.timestamp,
            })

        return Response({
            "cow_id": cow.cow_id,
            "total_scans": len(history),
            "history": history,
        })
class ScanViewSet(viewsets.ModelViewSet):
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer

    @action(detail=True, methods=["get"])
    def prediction(self, request, pk=None):
        scan = self.get_object()

        try:
            prediction = scan.prediction
        except Prediction.DoesNotExist:
            return Response(
                {
                    "message": "No prediction available for this scan yet."
                },
                status=404
            )

        serializer = PredictionSerializer(prediction)

        return Response(serializer.data)