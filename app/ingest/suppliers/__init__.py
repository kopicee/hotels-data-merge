from app.ingest.suppliers import \
    supplier_5ebbea002e000054009f3ffc, \
    supplier_5ebbea102e000029009f3fff, \
    supplier_5ebbea1f2e00002b009f4000
    

def get_extractors():
    return [
        supplier_5ebbea002e000054009f3ffc.extract,
        supplier_5ebbea102e000029009f3fff.extract,
        supplier_5ebbea1f2e00002b009f4000.extract,
    ]
