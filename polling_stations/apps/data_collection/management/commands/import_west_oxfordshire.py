from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000181"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "100120970053":
            rec["postcode"] = "GL7 3JH"

        if uprn == "200002436593":
            rec["postcode"] = "OX29 9UH"

        if record.addressline1.strip() == "Horseshoe Island":
            return None

        if uprn in [
            "10024175480",  # OX182SX -> OX182SU : Flat The Swan Hotel, Radcot, Bampton, Oxon
            "10033228325",  # OX183HA -> OX182HA : The Horseshoe, Bridge Street, Bampton, Oxon
            "10002188547",  # OX183HW -> OX182HW : The Orchard, Weald Street, Weald, Bampton, Oxon
            "100121317690",  # OX75YZ -> OX75QE : Taylor Hill Farm, Hirrons Lane, Little Rollright, Chipping Norton
        ]:
            rec["accept_suggestion"] = True

        return rec
