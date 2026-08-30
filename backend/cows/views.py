from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cow, Scan, Prediction
from .serializers import (
    CowSerializer,
    ScanSerializer,
    PredictionSerializer,
    CowScanCreateSerializer,
)


class CowViewSet(viewsets.ModelViewSet):
    queryset = Cow.objects.all()
    serializer_class = CowSerializer
    lookup_field = "cow_id"

    def get_serializer_class(self):
        # POST /api/cows/<cow_id>/scans/
        if self.action == "scans" and self.request.method == "POST":
            return CowScanCreateSerializer

        # GET /api/cows/<cow_id>/scans/
        if self.action == "scans" and self.request.method == "GET":
            return ScanSerializer

        return CowSerializer

    @action(detail=True, methods=["get", "post"])
    def scans(self, request, cow_id=None):
        cow = self.get_object()

        # --------------------------------
        # GET → Get all scans for this cow
        # --------------------------------
        if request.method == "GET":
            scans = cow.scans.all().order_by("day", "scan_number")

            serializer = ScanSerializer(
                scans,
                many=True
            )

            return Response({
                "cow_id": cow.cow_id,
                "total_scans": scans.count(),
                "scans": serializer.data
            })

        # --------------------------------
        # POST → Create a new scan
        # --------------------------------

        # Find the latest scan
        last_scan = cow.scans.order_by(
            "-scan_number"
        ).first()

        # Automatically calculate next scan number
        next_scan_number = (
            last_scan.scan_number + 1
            if last_scan
            else 1
        )

        # Validate incoming scan data
        serializer = CowScanCreateSerializer(
            data=request.data
        )

        if serializer.is_valid():

            # Create scan and automatically attach it
            # to the selected cow
            scan = Scan.objects.create(
                cow=cow,
                scan_number=next_scan_number,
                **serializer.validated_data
            )

            return Response(
                ScanSerializer(scan).data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )

    @action(detail=True, methods=["get"])
    def history(self, request, cow_id=None):
        cow = self.get_object()

        scans = cow.scans.all().order_by(
            "day",
            "scan_number"
        )

        history = []

        for scan in scans:
            history.append({
                "scan_number": scan.scan_number,
                "day": scan.day,
                "temperature_C": scan.temperature_C,
                "milk_pH": scan.milk_pH,
                "somatic_cell_count": scan.somatic_cell_count,
                "milk_yield_L": scan.milk_yield_L,
                "conductivity_raw_mScm": (
                    scan.conductivity_raw_mScm
                ),
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
                    "message": (
                        "No prediction available "
                        "for this scan yet."
                    )
                },
                status=404
            )

        serializer = PredictionSerializer(
            prediction
        )

        return Response(serializer.data)