# src/dto/library_dto.py
from dataclasses import dataclass

@dataclass
class BookResponseDTO:
    """Об'єкт передачі даних (DTO) для безпечного виводу інформації про книгу"""
    id: int
    title: str
    author: str
    status: str