import csv
import os

from django.core.management.base import BaseCommand
from django.db import transaction

from cows.models import Cow, Scan


class Command(BaseCommand):
    help = "Import MastiSense train and test CSV datasets into PostgreSQL"

    def handle(self, *args, **options):

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__))
                )
            )
        )

        dataset_dir = os.path.join(base_dir, "dataset")
        files = [
    "mastisense_balanced_train (1).csv",
    "mastisense_test (1).csv",
]

    
        total_cows_created = 0
        total_scans_created = 0
        total_scans_skipped = 0

        with transaction.atomic():

            for filename in files:

                file_path = os.path.join(dataset_dir, filename)

                if not os.path.exists(file_path):
                    self.stdout.write(
                        self.style.ERROR(
                            f"File not found: {file_path}"
                        )
                    )
                    return

                self.stdout.write(
                    f"\nImporting {filename}..."
                )

                with open(
                    file_path,
                    "r",
                    newline="",
                    encoding="utf-8"
                ) as csvfile:

                    reader = csv.DictReader(csvfile)

                    for row in reader:

                        cow_id = row["cow_id"].strip()

                        # Create cow if it does not already exist
                        cow, created = Cow.objects.get_or_create(
                            cow_id=cow_id
                        )

                        if created:
                            total_cows_created += 1

                        # Prevent duplicate scans
                        scan_exists = Scan.objects.filter(
                            cow=cow,
                            scan_number=int(row["scan_number"])
                        ).exists()

                        if scan_exists:
                            total_scans_skipped += 1
                            continue

                        Scan.objects.create(
                            cow=cow,
                            scan_number=int(row["scan_number"]),
                            day=int(row["day"]),

                            conductivity_raw_mScm=float(
                                row["conductivity_raw_mScm"]
                            ),

                            temperature_C=float(
                                row["temperature_C"]
                            ),

                            conductivity_temp_adjusted_mScm=float(
                                row["conductivity_temp_adjusted_mScm"]
                            ),

                            milk_pH=float(
                                row["milk_pH"]
                            ),

                            somatic_cell_count=float(
                                row["somatic_cell_count"]
                            ),

                            milk_yield_L=float(
                                row["milk_yield_L"]
                            ),

                            clotting=row["clotting"].strip().lower()
                            in ["1", "true", "yes"],

                            as7343_F1=float(row["as7343_F1"]),
                            as7343_F2=float(row["as7343_F2"]),
                            as7343_FZ=float(row["as7343_FZ"]),
                            as7343_F3=float(row["as7343_F3"]),
                            as7343_F4=float(row["as7343_F4"]),
                            as7343_F5=float(row["as7343_F5"]),
                            as7343_FY=float(row["as7343_FY"]),
                            as7343_FXL=float(row["as7343_FXL"]),
                            as7343_F6=float(row["as7343_F6"]),
                            as7343_F7=float(row["as7343_F7"]),
                            as7343_F8=float(row["as7343_F8"]),
                            as7343_NIR=float(row["as7343_NIR"]),
                            as7343_VIS=float(row["as7343_VIS"]),
                            as7343_FD=float(row["as7343_FD"]),
                        )

                        total_scans_created += 1

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Dataset import completed successfully!"
            )
        )

        self.stdout.write(
            f"Cows created: {total_cows_created}"
        )

        self.stdout.write(
            f"Scans created: {total_scans_created}"
        )

        self.stdout.write(
            f"Duplicate scans skipped: {total_scans_skipped}"
        )