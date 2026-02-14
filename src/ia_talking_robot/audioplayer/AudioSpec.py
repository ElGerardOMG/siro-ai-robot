from dataclasses import dataclass
from typing import Optional, Protocol
from enum import Enum
import numpy as np


class AudioSpec(Protocol):
    pass


@dataclass
class WavFileSpec:
    path: str
    sample_rate: Optional[int] = None
    channels: Optional[int] = None
    sample_width: Optional[int] = None  # bytes (2=16-bit)

@dataclass
class Mp3FileSpec:
    path: str
    target_sample_rate: Optional[int] = None
    target_channels: Optional[int] = None
    target_sample_width: Optional[int] = None

@dataclass
class WavBytesSpec:
    data: bytes

@dataclass
class NumpyArraySpec:
    data: np.ndarray
    sample_rate: int
    channels: int = 1
    sample_width: int = 2          # bytes objetivo (2 = 16-bit PCM)
    normalize: bool = True 
    
