"""Hardware driver abstractions and mock drivers.

Provide lightweight, testable interfaces so real hardware drivers can be plugged in later.
"""
from typing import Protocol, Any, Dict

class HardwareDriver(Protocol):
    def connect(self) -> None: ...
    def read(self) -> Dict[str, Any]: ...
    def disconnect(self) -> None: ...

class MockDriver:
    def __init__(self, name: str = "mock-driver"):
        self.name = name
        self.connected = False

    def connect(self) -> None:
        self.connected = True

    def read(self) -> Dict[str, Any]:
        if not self.connected:
            raise RuntimeError("Driver not connected")
        # deterministic mock read
        return {"driver": self.name, "measurement": 0.0}

    def disconnect(self) -> None:
        self.connected = False
