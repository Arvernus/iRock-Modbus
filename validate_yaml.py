#!/usr/bin/env python3
import sys
import yaml
import re
import jsonschema
import math
from semantic_version import Version
from enum import Enum
from typing import Union, Dict, List, Tuple, Any

class Result(Enum):
    OK = "OK"
    ERROR = "ERROR"
class BaseType(Enum):
    INT8 = "int8"
    UINT8 = "uint8"
    CHAR = "char"
    INT16 = "int16"
    UINT16 = "uint16"
    INT32 = "int32"
    UINT32 = "uint32"
    INT64 = "int64"
    UINT64 = "uint64"
    FLOAT32 = "float32"
    FLOAT64 = "float64"
    BOOL = "bool"
class ValueType:
    """
    Represents a data type (including optional array dimensions) and
    provides methods to compute the total number of bits and required 16-bit registers.
    
    Supported base types and their bit widths:
      - int8, uint8, char: 8 bits
      - int16, uint16: 16 bits
      - int32, uint32, float32: 32 bits
      - float64: 64 bits
      - bool: 8 bits (in practice)
      
    Array declarations are allowed in the form Type[N] (or multi-dimensional like Type[N][M]).
    """
    # Mapping of base types to bit sizes
    bit_size_map = {
        BaseType.INT8: 8,
        BaseType.UINT8: 8,
        BaseType.CHAR: 8,
        BaseType.INT16: 16,
        BaseType.UINT16: 16,
        BaseType.INT32: 32,
        BaseType.UINT32: 32,
        BaseType.INT64: 64,
        BaseType.UINT64: 64,
        BaseType.FLOAT32: 32,
        BaseType.FLOAT64: 64,
        BaseType.BOOL: 1,
    }
    
    def __init__(self, base_type: BaseType, dimension: int = 1):
        """
        Initializes a DataType with the given base type and dimension.
        
        :param base_type: The BaseType enum value.
        :param dimension: The number of elements (default is 1).
        """
        if dimension < 1:
            raise ValueError("Dimension must be at least 1")
        self.base_type: BaseType = base_type
        self.dimension: int = dimension

    def total_bits(self) -> int:
        """Calculates the total number of bits required for this data type."""
        return self.bit_size_map[self.base_type] * self.dimension

    def registers_required(self) -> int:
        """Calculates the number of 16-bit registers required (rounded up)."""
        return math.ceil(self.total_bits() / 16)
    
    def __str__(self) -> str:
        """
        Converts the ValueType to its string representation.
        If dimension is 1, returns just the base type (e.g. "char").
        Otherwise returns base type with array notation (e.g. "char[10]").
        """
        if self.dimension == 1:
            return self.base_type.value
        else:
            return f"{self.base_type.value}[{self.dimension}]"
    
    @classmethod
    def from_str(cls, type_str: str) -> Tuple[BaseType, int]:
        """
        Creates a ValueType instance from its string representation.
        
        Supported formats:
          - "char"         -> ValueType(BaseType.CHAR, 1)
          - "char[10]"     -> ValueType(BaseType.CHAR, 10)
        
        :param type_str: The type string.
        :return: A ValueType instance.
        """
        pattern = r'^(int8|uint8|char|int16|uint16|int32|uint32|float32|float64|bool)(?:\[(\d+)\])?$'
        match = re.match(pattern, type_str)
        if not match:
            raise ValueError(f"Invalid type string: {type_str}")
        base_type_str = match.group(1)
        dimension_str = match.group(2)
        dimension = int(dimension_str) if dimension_str else 1
        return cls(BaseType(base_type_str), dimension)
class Register:
    def __init__(self, name: str, value_type: ValueType, address: int, unit: str = None, hardware_support_register: int = None, description: str = ""):
        self.name: str = name
        self.address: int = address
        self.value_type: ValueType = value_type
        self.unit: str = unit
        self.hardware_support_register: int = hardware_support_register
        self.description: str = description
class Coil:
    def __init__(self, parent_address: int, address: int):
        self.parent_address: int = parent_address
        self.address: int = address
class RegisterList:
    def __init__(self):
        self.general_registers: List[Register] = []
        self.cell_registers: List[Register] = []
        self.coils: List[Coil] = []
        self.cell_start_address: int = None
        self.version: Version = None
    def add_register(self, name: str, value_type: ValueType, address: Union[str, int] = None, unit: str = None, hardware_support_register: Union[str, int] = None, description: str = "") -> Result:
        if address == "auto":
            address = self.next_address()
        if hardware_support_register == "auto":
            hardware_support_register = self.next_coil()
        self.general_registers.append(Register(name, value_type, address, unit, hardware_support_register, description))
        self.general_registers.sort(key=lambda x: x.address)
        if hardware_support_register is not None:
            self.coils.append(Coil(address, hardware_support_register))
            self.coils.sort(key=lambda x: x.address)
        return Result.OK
    def next_address(self) -> int:
        if self.general_registers:
            return self.general_registers[-1].address + self.general_registers[-1].value_type.registers_required()
        return 0
    def next_coil(self) -> int:
        if self.coils:
            return self.coils[-1].address + 1
        return 0
    def next_cell_address(self) -> int:
        if self.cell_registers:
            return self.cell_registers[-1].address + self.cell_registers[-1].value_type.registers_required()
        return 0
    def add_cell_registers(self, name: str, value_type: ValueType, offset: Union[str, int], unit: str = None, hardware_support_register: int = None, description: str = "") -> Result:
        if offset == "auto":
            offset = self.next_cell_address()
        if hardware_support_register == "auto":
            hardware_support_register = self.next_coil()
        self.cell_registers.append(Register(name, value_type, offset, unit, hardware_support_register, description))
        self.cell_registers.sort(key=lambda x: x.address)
        if hardware_support_register is not None:
            self.coils.append(Coil(offset, hardware_support_register))
            self.coils.sort(key=lambda x: x.address)
        return Result.OK
    def set_cell_start_address(self, address: Union[int, str]) -> Result:
        if address == "auto":
            address = self.next_address()
        if isinstance(address, int):
            self.cell_start_address = address
            return Result.OK
        return Result.ERROR
    def get_all_registers(self, number_of_cells: int = 2) -> List[Register]:
        if self.cell_start_address is None:
            self.cell_start_address = self.next_address()
        all_registers = []
        all_registers.extend(self.general_registers)
        last_cell_offset = 0
        last_cell_size = 0
        for reg in self.cell_registers:
            if reg.address > last_cell_offset:
                last_cell_offset = reg.address
                last_cell_size = reg.value_type.registers_required()
        total_size = last_cell_offset + last_cell_size
        for i in range(1, number_of_cells + 1):
            for reg in self.cell_registers:
                all_registers.append(Register(reg.name + f" {i}", reg.value_type, reg.address + self.cell_start_address + (i - 1) * total_size, reg.unit, reg.hardware_support_register))
        return all_registers
    def validate_address_overlaps(self, number_of_cells: int = 49) -> Result:
        test_registers = self.get_all_registers(number_of_cells)
        for i in range(1, len(test_registers)):
            prev = test_registers[i - 1]
            current = test_registers[i]
            if current.address < prev.address + prev.value_type.registers_required():
                print( f"Adressüberlappung: Register '{prev.name}' (Bereich {prev.address}–{prev.address + prev.value_type.registers_required()}) und Register '{current.name}' (Bereich {current.address}–{current.address + current.value_type.registers_required()})")
                return Result.ERROR
        for i in range(1, len(self.coils)):
            prev = self.coils[i - 1]
            current = self.coils[i]
            if current.address < prev.address:
                print(f"Adressüberlappung: Coil '{prev.parent_address}' (Bereich {prev.address}) und Coil '{current.parent_address}' (Bereich {current.address})")
                return Result.ERROR
        return Result.OK
    def register_to_dict(self) -> Dict[Version, Union[str, Dict[str, Dict[str, Any]]]]:
        """
        Konvertiert die RegisterList in ein Dictionary-Format.
        
        :return: Ein Dictionary mit den allgemeinen Registern und Zellregistern.
        """
        def register_details(register: Register) -> Dict[str, Union[Any]]:
            return {
                "name": register.name,
                "address": register.address,
                "array_size": register.value_type.dimension,
                "type": register.value_type.base_type.value,
                "description": register.description,
                "unit": register.unit,
                "hardware_support_register": register.hardware_support_register
            }
        
        registers_dict = {
            reg.name: register_details(reg) for reg in self.general_registers
        }
        
        return {
            "version": self.version,
            "register": registers_dict
        }

def load_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def validate_schema(data, schema):
    try:
        jsonschema.validate(instance=data, schema=schema)
        print("Schema-Validierung erfolgreich!")
    except jsonschema.ValidationError as e:
        print("Schema-Validierungsfehler:")
        print(e)
        sys.exit(1)

def generate_registers(data) -> RegisterList:
    """
    Erzeugt aus den Daten die Listen mit Register- und Coil-Tupeln,
    jeweils als (Name, Startadresse, Endadresse), und sortiert diese.
    """
    registers = RegisterList()
    registers.version = Version(data.get("version"))

    # Allgemeine Register
    general_regs = data.get("general", {}).get("registers", {})
    next_coil = 0
    for key, reg in general_regs.items():
        name: str = reg.get("name", key)
        addr = reg.get("address", "auto")
        vt: ValueType = ValueType.from_str(reg.get("ValueType"))
        unit: str = reg.get("unit")
        coil = reg.get("hardware_support_register")
        description: str = reg.get("description", "")
        registers.add_register(name, vt, addr, unit, coil, description)

    # Zellen-Register
    cells_regs = data.get("cells", {}).get("registers", {})
    registers.set_cell_start_address(data.get("cells", {}).get("address", "auto"))
    for key, reg in cells_regs.items():
        name: str = reg.get("name", key)
        offset = reg.get("offset", "auto")
        vt: ValueType = ValueType.from_str(reg.get("ValueType"))
        unit: str = reg.get("unit")
        coil = reg.get("hardware_support_register")
        description: str = reg.get("description", "")
        registers.add_cell_registers(name, vt, offset, unit, coil, description)
    return registers

def main():
    if len(sys.argv) != 3:
        print("Usage: python validate_jsonschema.py <schema.json> <data.yaml>")
        sys.exit(1)
    schema_file = sys.argv[1]
    data_file = sys.argv[2]
    
    try:
        schema = load_yaml(schema_file)
    except Exception as e:
        print("Fehler beim Laden des Schema-Files:", e)
        sys.exit(1)
    
    try:
        data = load_yaml(data_file)
    except Exception as e:
        print("Fehler beim Laden der Daten-Datei:", e)
        sys.exit(1)
    
    # JSON-Schema-Validierung
    validate_schema(data, schema)
    
    overall_errors = False
    # Custom-Check: Adressüberlappungen
    registers = generate_registers(data)
    
    if registers.validate_address_overlaps() == Result.ERROR:
        overall_errors = True
    
    if overall_errors:
        print("Es sind Validierungsfehler aufgetreten.")
        sys.exit(1)
    else:
        print("Alle Validierungen erfolgreich.")

if __name__ == "__main__":
    main()
