from rest_framework import serializers
from .models import Cow, Scan,Prediction


class CowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cow
        fields = ["id", "cow_id", "created_at"]
        read_only_fields = ["id", "created_at"]
class ScanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scan
        fields = [
            "id",
            "cow",
            "scan_number",
            "day",
            "conductivity_raw_mScm",
            "temperature_C",
            "conductivity_temp_adjusted_mScm",
            "milk_pH",
            "somatic_cell_count",
            "milk_yield_L",
            "clotting",

            "as7343_F1",
            "as7343_F2",
            "as7343_FZ",
            "as7343_F3",
            "as7343_F4",
            "as7343_F5",
            "as7343_FY",
            "as7343_FXL",
            "as7343_F6",
            "as7343_F7",
            "as7343_F8",
            "as7343_NIR",
            "as7343_VIS",
            "as7343_FD",

            "timestamp",
        ]

        read_only_fields = [
            "id",
            "timestamp",
        ]

    def validate_scan_number(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Scan number must be greater than 0."
            )

        return value

    def validate_day(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Day must be greater than 0."
            )

        return value

    def validate(self, data):
        cow = data.get("cow")
        scan_number = data.get("scan_number")

        # Prevent duplicate scan numbers for the same cow
        if cow and scan_number:
            existing_scan = Scan.objects.filter(
                cow=cow,
                scan_number=scan_number
            )

            # When updating an existing scan, exclude itself
            if self.instance:
                existing_scan = existing_scan.exclude(
                    pk=self.instance.pk
                )

            if existing_scan.exists():
                raise serializers.ValidationError(
                    {
                        "scan_number":
                        "This cow already has a scan with this scan number."
                    }
                )

        return data


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = [
            "id",
            "scan",
            "risk_score",
            "risk_label",
            "model_version",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
class CowScanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = [
            "day",
            "conductivity_raw_mScm",
            "temperature_C",
            "conductivity_temp_adjusted_mScm",
            "milk_pH",
            "somatic_cell_count",
            "milk_yield_L",
            "clotting",

            "as7343_F1",
            "as7343_F2",
            "as7343_FZ",
            "as7343_F3",
            "as7343_F4",
            "as7343_F5",
            "as7343_FY",
            "as7343_FXL",
            "as7343_F6",
            "as7343_F7",
            "as7343_F8",
            "as7343_NIR",
            "as7343_VIS",
            "as7343_FD",
        ]