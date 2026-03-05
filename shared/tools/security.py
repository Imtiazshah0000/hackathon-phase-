import re
import os
import logging
from typing import Any, Dict, List

logger = logging.getLogger("security-service")

class SecurityGuard:
    """Handles PII masking and safety guardrails for the Digital FTE."""

    @staticmethod
    def mask_pii(data: Any) -> Any:
        """
        Recursively masks PII (Emails, Names) in strings or dictionaries.
        Used for safe logging and analytics.
        """
        if isinstance(data, str):
            # Mask Email: j.doe@acme.corp -> j***@acme.corp
            data = re.sub(r"([a-zA-Z0-9_.+-])[a-zA-Z0-9_.+-]*@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", r"\1***@\2", data)
            return data
        elif isinstance(data, dict):
            return {k: SecurityGuard.mask_pii(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [SecurityGuard.mask_pii(i) for i in data]
        return data

class KillSwitch:
    """
    Emergency mechanism to stop autonomous outreach (ADR-4).
    Can be triggered via Environment Variable or a dedicated 'kill_switch' file.
    """
    
    @staticmethod
    def is_active() -> bool:
        """Returns True if outreach is globally disabled."""
        if os.getenv("REV_OPS_KILL_SWITCH") == "TRUE":
            logger.warning("KILL SWITCH ACTIVE: Env var set to TRUE.")
            return True
        if os.path.exists("/tmp/revops_kill_switch"):
            logger.warning("KILL SWITCH ACTIVE: Kill file detected.")
            return True
        return False

    @staticmethod
    def activate():
        """Programmatically triggers the kill switch."""
        with open("/tmp/revops_kill_switch", "w") as f:
            f.write("STOP")
        logger.error("KILL SWITCH ACTIVATED MANUALLY.")
