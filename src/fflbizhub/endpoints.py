# fflbizhub/endpoints.py
BASE_URL = "https://app.fflbizhub.com"

ENDPOINTS = {
    # --- Authentication ---
    "auth": f"{BASE_URL}/api/auth",
    "set_ffl": f"{BASE_URL}/api/auth/me/setFFL",
    "get_user_ffls": f"{BASE_URL}/api/multiBookSearch/getUserFFLs",

    # --- Inventory / Serialization ---
    "check_duplicity": f"{BASE_URL}/api/receive/checkDuplicity",
    "is_acquired_batch": f"{BASE_URL}/api/serialize/isAcquiredBatch/",
    "acquire_batch": f"{BASE_URL}/api/serialize/acquireFirearmBatch?deparmentId=0^&branchId=0^&locationId=0",
    "bulk_correction": f"{BASE_URL}/api/bulkcorrection/getBulkCorrectionData",

    # --- Reports ---
    "get_report_data": f"{BASE_URL}/api/multiBookSearch/getReportData",

    # --- Loan Out / Check Out  ---
    "can_loan_out": f"{BASE_URL}/api/loanOut/canLoanOut/",
    "loan_out_firearm": f"{BASE_URL}/api/loanOut/loanOutFirearm/",

    # --- Loan Return / Check In ---
    "can_return_loan": f"{BASE_URL}/api/loanReturn/canReturnLoan/",
    "return_loan_firearm": f"{BASE_URL}/api/loanReturn/returnLoanFirearm/",

    # --- Ad Search (the one used in your curl examples) ---
    "ad_search": f"{BASE_URL}/api/adSearch/getDataByFilter",
}

