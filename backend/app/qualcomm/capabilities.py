"""Safe hardware and system capability detection module."""

import os
import platform
import sys
from typing import List
from app.qualcomm.schemas import SystemCapabilitiesSpec


def detect_system_capabilities() -> SystemCapabilitiesSpec:
    """
    Safely detect system hardware capabilities without spawning shell processes.
    Truthfully identifies non-Snapdragon development machines vs ARM64 Snapdragon hosts.
    """
    os_name = f"{platform.system()} {platform.release()}"
    processor = platform.processor() or platform.machine() or "Unknown Processor"
    architecture = platform.architecture()[0]

    # Check processor string and architecture for Qualcomm/Snapdragon ARM64 indicators
    proc_upper = processor.upper()
    mach_upper = platform.machine().upper()

    is_arm64 = "ARM64" in proc_upper or "AARCH64" in proc_upper or "ARM64" in mach_upper
    has_qualcomm_indicator = "SNAPDRAGON" in proc_upper or "QUALCOMM" in proc_upper

    # On a standard x86_64 Windows PC (Intel/AMD), is_snapdragon_hardware is False
    is_snapdragon = is_arm64 and has_qualcomm_indicator

    compute_units: List[str] = ["CPU"]
    if is_snapdragon:
        compute_units.extend(["NPU", "GPU"])

    return SystemCapabilitiesSpec(
        os_name=os_name,
        processor=processor,
        architecture=architecture,
        is_snapdragon_hardware=is_snapdragon,
        available_compute_units=compute_units
    )
