#!/usr/bin/env python3
import argparse
import yaml
from validate_yaml import ValueType, load_yaml, generate_registers # Import from your existing script

def generate_markdown(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        registers = generate_registers(data)
        f.write("# iRock Modbus Registers")
        if data.get("version"):
            f.write(f" {data.get("version")}")
        f.write("\n\nAll provided fields will be accessible in the Holding Registers. Each field can be split into multiple registers depending on its length. Fields that are not supported by all hardware will additionally write to a coil to indicate whether this function is supported.\n\n")
        
        f.write("## Overview\n\n")
        f.write("| |Register|Type|Hardware Supported Register|\n|-|-|-|-|\n")
        for reg in registers.get_all_registers(3):
            f.write(f"|{reg.name}|{reg.address}|{reg.value_type}|{reg.hardware_support_register}|\n")
        f.write("|...| | | |\n\n")
        f.write("## Supported Data Types\n\n")
        f.write("In this documentation, we support a fixed set of data types. Each type has a defined bit width, and **all types can also be defined as arrays**.  \n")
        f.write("Arrays are declared using the notation `Type[N]`, where `N` is the number of elements. For example, `char[10]` represents an array of 10 characters, with each character occupying 8 bits.\n\n")
        
        f.write("### Data Types Overview\n\n")
        
        f.write("- **int8 / uint8**  \n")
        f.write("  8-bit signed and unsigned integers.  \n\n")
        
        f.write("- **int16 / uint16**  \n")
        f.write("  16-bit signed and unsigned integers.  \n\n")
                    
        f.write("- **int32 / uint32**  \n")
        f.write("  32-bit signed and unsigned integers.  \n\n")
        
        f.write("- **float32**  \n")
        f.write("  32-bit floating point number (commonly referred to as `float`).  \n\n")
        
        f.write("- **float64**  \n")
        f.write("  64-bit floating point number (similar to `double` in many languages).  \n\n")
        
        f.write("- **bool**  \n")
        f.write("  Boolean value. Although theoretically 1 bit is enough, in practice, a full byte (8 bits) is often used.  \n\n")
        
        f.write("- **char**  \n")
        f.write("  8-bit character.  \n\n")
        
        f.write("> **Note:**  \n")
        f.write("> All the data types listed above can be used as arrays. For example, `int16[5]` is interpreted as an array with 5 elements of type `int16`. The total bit size is calculated by multiplying the bit size of the base type by the number of elements.\n\n")
        
        f.write("## Register Allocation\n\n")
        f.write("All registers are fixed at 16 bits in length. This means that regardless of the bit width of a data type, the allocation in registers is as follows:\n\n")
        f.write("- If a data type occupies less than 16 bits (e.g., a single `char` of 8 bits), it will still use one full 16-bit register. \n")
        f.write("- Consequently, `char[1]` and `char[2]` both fit within one register since 1 or 2 characters at 8 bits each do not exceed 16 bits.\n")
        f.write("- When the total bit size of a data element (or array element) exceeds 16 bits, additional registers are allocated. For example, `char[3]` (24 bits) will require 2 registers, since one register can only hold 16 bits.\n")
        f.write("- For all data types, the number of registers used is determined by dividing the total required bit size by 16 and rounding up to the next whole number.\n")
        f.write("## Fields\n\n")
        for reg in registers.general_registers:
            f.write(f"### {reg.name}")
            if reg.unit is not None:
                f.write(f" [{reg.unit}]\n\n")
            else:
                f.write("\n\n")
            vt = reg.value_type
            reg_count = reg.value_type.registers_required()
            f.write(f"| Register | Type           | Size |\n|-|-|-|\n|{reg.address}| `{vt}` | {reg_count} |\n\n")
            f.write(f"{reg.description}\n")
            if reg.hardware_support_register is not None:
                f.write(f"iRock may set coil {reg.hardware_support_register} to true if function is supported.\n")
            f.write("\n")
        
        f.write("### Cells\n\n")
        last_cell_offset = 0
        last_cell_size = 0
        for reg in registers.cell_registers:
            if reg.address > last_cell_offset:
                last_cell_offset = reg.address
                last_cell_size = reg.value_type.registers_required()
        total_size = last_cell_offset + last_cell_size
        f.write(f"The cell fields repeat as many times as there are cells in the corresponding iRock. The starting address for cell 1 is {registers.cell_start_address}, and the starting address for each subsequent cell is the next available free address. So a Cell Register is calculated as follows:\n\n")
        f.write(f"$$Starting Address + Offset + \\left(Last Cell Offset + Last Cell Size\\right) * \\left( Cell Number -1 \\right)={registers.cell_start_address} + Offset + \\left({last_cell_offset} + {last_cell_size}\\right) * \\left( Cell Number -1 \\right)$$\n\n")
        
        for reg in registers.cell_registers:
            f.write(f"#### {reg.name}")
            if reg.unit is not None:
                f.write(f" [{reg.unit}]\n\n")
            else:
                f.write("\n\n")
            vt = reg.value_type
            reg_count = vt.registers_required()
            f.write(f"| Offset | Type           | Size |\n|-|-|-|\n|{reg.address}|`{vt}`|{reg_count}|\n\n")
            f.write(f"{reg.description}\n")
            if reg.hardware_support_register is not None:
                f.write(f"iRock may set coil {reg.hardware_support_register} to true if function is supported.\n")
            f.write("\n")
        
        f.write("_This documentation was automatically generated from the YAML configuration file._\n")
    print(f"Documentation generated in '{output_file}'.")

def main():
    parser = argparse.ArgumentParser(description="Generate documentation from YAML configuration file.")
    parser.add_argument("yaml_file", help="Path to the YAML configuration file")
    parser.add_argument("--output", "-o", default="documentation.md", help="Output Markdown file (default: documentation.md)")
    args = parser.parse_args()
    
    data = load_yaml(args.yaml_file)
    generate_markdown(data, args.output)

if __name__ == "__main__":
    main()
