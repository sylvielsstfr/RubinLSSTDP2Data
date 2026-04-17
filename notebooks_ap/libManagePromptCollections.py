from astropy.time import Time

# --- Constantes globales ---
DATE_THRESHOLD = Time("2026-02-14 00:00:00", format="iso")

PRE_PROMPT_COLLECTIONS = [
    "u/sullii/DM-54088/2025-09-01_2026-01-30/diffim",
    "u/sullii/DM-54088/2025-09-01_2026-01-30/association",
    "u/sullii/DM-54088-test/2025-09-01_2026-01-30/association",
]

POST_PROMPT_COLLECTIONS = [
    "LSSTCam/prompt/output-2026-02-16/ApPipe/pipelines-ba6eb50-config-8f017ea",
    "LSSTCam/prompt/output-2026-02-18/ApPipe/pipelines-ba6eb50-config-8f017ea",
    "LSSTCam/prompt/output-2026-02-19/ApPipe/pipelines-ba6eb50-config-8f017ea",
    "LSSTCam/prompt/output-2026-02-22/ApPipe/pipelines-b5640f0-config-8f017ea",
    "LSSTCam/prompt/output-2026-02-23/ApPipe/pipelines-b5640f0-config-8f017ea",
    "LSSTCam/prompt/output-2026-02-24/ApPipe/pipelines-294fa0b-config-8f017ea",
    "LSSTCam/prompt/output-2026-02-25/ApPipe/pipelines-294fa0b-config-8f017ea",
    "LSSTCam/prompt/output-2026-02-26/ApPipe/pipelines-294fa0b-config-8f017ea",
    "LSSTCam/prompt/output-2026-02-27/ApPipe/pipelines-3c98fdd-config-8f017ea",
    "LSSTCam/prompt/output-2026-02-28/ApPipe/pipelines-3c98fdd-config-8f017ea",
    "LSSTCam/prompt/output-2026-03-01/ApPipe/pipelines-3c98fdd-config-8f017ea",
    "LSSTCam/prompt/output-2026-03-02/ApPipe/pipelines-3c98fdd-config-8f017ea",
    "LSSTCam/prompt/output-2026-03-03/ApPipe/pipelines-3c98fdd-config-8f017ea",
    "LSSTCam/prompt/output-2026-03-05/ApPipe/pipelines-5b4c026-config-8f017ea",
    "LSSTCam/prompt/output-2026-03-06/ApPipe/pipelines-5b4c026-config-8f017ea",
    "LSSTCam/prompt/output-2026-03-07/ApPipe/pipelines-5b4c026-config-8f017ea",
    "LSSTCam/prompt/output-2026-03-08/ApPipe/pipelines-5b4c026-config-8f017ea",
    "LSSTCam/prompt/output-2026-03-09/ApPipe/pipelines-5b4c026-config-8f017ea",
    "LSSTCam/prompt/output-2026-03-09/ApPipe/pipelines-5b4c026-config-8f017ea",
    "LSSTCam/prompt/output-2026-04-04/ApPipe/pipelines-6d8eadb-config-8f017ea",
    "LSSTCam/prompt/output-2026-04-05/ApPipe/pipelines-6d8eadb-config-8f017ea",
    "LSSTCam/prompt/output-2026-04-06/ApPipe/pipelines-6d8eadb-config-8f017ea",
    "LSSTCam/prompt/output-2026-04-07/ApPipe/pipelines-6d8eadb-config-8f017ea",
    "LSSTCam/prompt/output-2026-04-08/ApPipe/pipelines-6d8eadb-config-8f017ea",
]


def extract_date_to_iso(entier_int64):
    """
    Extract a date (YYYYMMDD) from an integer and return an astropy Time object.

    Parameters
    ----------
    entier_int64 : int or np.int64
        Integer encoding a date in the form YYYYMMDD (optionally followed by extra digits).

    Returns
    -------
    astropy.time.Time
        Time object corresponding to the extracted date (UTC, ISO format).
    """
    # Convert input to string
    s = str(entier_int64)

    # Basic validation: must contain at least YYYYMMDD
    if len(s) < 8:
        raise ValueError("Input must contain at least 8 digits (YYYYMMDD)")

    # Extract year, month, and day
    y, m, d = s[:4], s[4:6], s[6:8]

    # Build ISO date string
    date_iso = f"{y}-{m}-{d}"

    # Convert to astropy Time object (UTC scale)
    return Time(date_iso, format="iso", scale="utc")


def get_collections(visit) -> list[str]:
    """
    Return the appropriate Butler collections for a given visit.

    Selection logic:
    - Before DATE_THRESHOLD → pre-prompt (DM-54088 campaign)
    - After DATE_THRESHOLD  → prompt-processing outputs (ApPipe)

    Parameters
    ----------
    visit : object
        Visit identifier (must be compatible with `extract_date_to_iso`).

    Returns
    -------
    list of str
        Ordered list of Butler collections to query.
    """
    visit_date = extract_date_to_iso(visit)

    if visit_date < DATE_THRESHOLD:
        return PRE_PROMPT_COLLECTIONS

    return POST_PROMPT_COLLECTIONS
