from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .ml.prediction import predict_risk
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
            scans = cow.scans.all().order_by(
        "day",
        "scan_number"
    )
            history = []
            for scan in scans:
                prediction = getattr(scan, "prediction", None)

                scan_data = ScanSerializer(scan).data

                if prediction:
                    scan_data["prediction"] = {
                "risk_score": prediction.risk_score,
                "risk_label": prediction.risk_label,
                "clinical_probability": prediction.clinical_probability,
                "healthy_probability": prediction.healthy_probability,
                "subclinical_probability": prediction.subclinical_probability,
                "model_version": prediction.model_version,
            }
                else:
                    scan_data["prediction"] = None

                history.append(scan_data)

            return Response({
        "cow_id": cow.cow_id,
        "total_scans": scans.count(),
        "scans": history
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

            # --------------------------------
            # Prepare data for ML prediction
            # --------------------------------

            prediction_data = {
                "conductivity_raw_mScm":
                    scan.conductivity_raw_mScm,

                "temperature_C":
                    scan.temperature_C,

                "conductivity_temp_adjusted_mScm":
                    scan.conductivity_temp_adjusted_mScm,

                "as7343_F1":
                    scan.as7343_F1,

                "as7343_F2":
                    scan.as7343_F2,

                "as7343_FZ":
                    scan.as7343_FZ,

                "as7343_F3":
                    scan.as7343_F3,

                "as7343_F4":
                    scan.as7343_F4,

                "as7343_F5":
                    scan.as7343_F5,

                "as7343_FY":
                    scan.as7343_FY,

                "as7343_FXL":
                    scan.as7343_FXL,

                "as7343_F6":
                    scan.as7343_F6,

                "as7343_F7":
                    scan.as7343_F7,

                "as7343_F8":
                    scan.as7343_F8,

                "as7343_NIR":
                    scan.as7343_NIR,

                "as7343_VIS":
                    scan.as7343_VIS,

                "as7343_FD":
                    scan.as7343_FD,

                "conductivity_deviation":
                    scan.conductivity_temp_adjusted_mScm - 4.689,
            }
            # --------------------------------
            # Run ML prediction
            # --------------------------------

            ml_result = predict_risk(
                prediction_data
            )

            risk_label = ml_result["risk_label"]
            probabilities = ml_result["probabilities"]

            # --------------------------------
            # Calculate risk score
            # --------------------------------

            risk_score = max(probabilities.values()) * 100

            # --------------------------------
            # Save prediction
            # --------------------------------

            prediction = Prediction.objects.create(
                scan=scan,
                risk_score=risk_score,
                risk_label=risk_label,

                clinical_probability=probabilities.get(
                    "Clinical",
                    0.0
                ),

                healthy_probability=probabilities.get(
                    "Healthy",
                    0.0
                ),

                subclinical_probability=probabilities.get(
                    "Subclinical",
                    0.0
                ),

                model_version="GauCare-v1",
            )

            # --------------------------------
            # Return scan + prediction
            # --------------------------------

            return Response(
                {
                    "scan": ScanSerializer(
                        scan
                    ).data,

                    "prediction": PredictionSerializer(
                        prediction
                    ).data,
                },
                status=201
            )

        # --------------------------------
        # Validation error
        # --------------------------------

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
                "somatic_cell_count":
                    scan.somatic_cell_count,
                "milk_yield_L":
                    scan.milk_yield_L,
                "conductivity_raw_mScm":
                    scan.conductivity_raw_mScm,
                "conductivity_temp_adjusted_mScm":
                    scan.conductivity_temp_adjusted_mScm,
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

        return Response(
            serializer.data
        )