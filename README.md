# fflbizhub-client

A thin Python client for **Orchid FFL BizHub**.  
This library provides authenticated access to common endpoints and utilities for working with Orchid’s eBound Book and related FFL software modules.

## Features

- **Authentication & Session Management**
  - `FFLBizHubAuth` to obtain and cache tokens
  - Auto-refresh support
- **Endpoint Mapping**
  - Centralized `ENDPOINTS` dictionary with commonly used API routes
- **Ad Search**
  - `ad_search_page_stream` for robust, paginated `/api/adSearch/getDataByFilter` queries
- **Modular Design**
  - Ready to expand across every module of Orchid’s FFL Suite (Serialize, Receive, Transfers, Reports, etc.)

---

## Installation (Development)

```bash
git clone https://github.com/your-org/fflbizhub-client.git
cd fflbizhub-client
pip install -e .
```

---

## Usage

```python
from fflbizhub.auth import FFLBizHubAuth
from fflbizhub.endpoints import ENDPOINTS
from fflbizhub.search import ad_search_page_stream

# Authenticate
auth = FFLBizHubAuth("username", "password")
token = auth.get_token()

# Example: Run Ad Search
params = {
    "pageSize": 50,
    "currentPage": 1,
    "filters": {"serialNumber": "12345"}
}

for page in ad_search_page_stream(auth, params):
    print(page)
```

---

## Endpoints Supported

```python
BASE_URL = "https://app.fflbizhub.com"

ENDPOINTS = {
    # Authentication
    "auth": f"{BASE_URL}/api/auth",
    "set_ffl": f"{BASE_URL}/api/auth/me/setFFL",
    "get_user_ffls": f"{BASE_URL}/api/multiBookSearch/getUserFFLs",

    # Inventory / Serialization
    "check_duplicity": f"{BASE_URL}/api/receive/checkDuplicity",
    "is_acquired_batch": f"{BASE_URL}/api/serialize/isAcquiredBatch/",
    "acquire_batch": f"{BASE_URL}/api/serialize/acquireFirearmBatch?deparmentId=0&branchId=0&locationId=0",
    "bulk_correction": f"{BASE_URL}/api/bulkcorrection/getBulkCorrectionData",

    # Reports
    "get_report_data": f"{BASE_URL}/api/multiBookSearch/getReportData",

    # Loan / Return
    "can_loan_out": f"{BASE_URL}/api/loanOut/canLoanOut/",
    "loan_out_firearm": f"{BASE_URL}/api/loanOut/loanOutFirearm/",
    "can_return_loan": f"{BASE_URL}/api/loanReturn/canReturnLoan/",
    "return_loan_firearm": f"{BASE_URL}/api/loanReturn/returnLoanFirearm/",

    # Ad Search
    "ad_search": f"{BASE_URL}/api/adSearch/getDataByFilter",
}
```

---

## Roadmap

Planned modules to cover the **entire Orchid eBound Book ecosystem**:

- ✅ Authentication & Session Management  
- ✅ Ad Search & Pagination  
- ⬜ Serialization (Serialize, Receive, Transfers, Exempt Transfer, Assemble/Disassemble)  
- ⬜ Reporting APIs (Operating, Retail, Special, FFL Reports)  
- ⬜ Loan/Return & Special Transactions (Assign, Return, Theft/Loss, Destroy, Correct)  
- ⬜ FFL Management (Bound Book switching, Masters, Uploads, Validation)  
- ⬜ Retail Transactions & 4473 eStorage integration  

---

## References

- [Orchid Advisors](https://orchidadvisors.com/)  
- [FFL BizHub Portal](https://app.fflbizhub.com/portal/ead)
