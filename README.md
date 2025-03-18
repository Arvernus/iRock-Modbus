# iRock Modbus Registers 1.1.0

All provided fields will be accessible in the Holding Registers. Each field can be split into multiple registers depending on its length. Fields that are not supported by all hardware will additionally write to a coil to indicate whether this function is supported.

## Overview

| |Register|Type|Hardware Supported Register|
|-|-|-|-|
|Manufacturer ID|0|uint16|None|
|Modbus Version|1|char[16]|None|
|Hardware Name|9|char[16]|None|
|Hardware Version|17|char[8]|None|
|Serial Number|21|char[12]|None|
|Software Version|27|char[16]|None|
|Number of Cells|35|uint16|None|
|Battery Voltage|36|float32|None|
|Battery Current|38|float32|0|
|SOC|40|float32|1|
|Capacity|42|float32|None|
|Remaining Capacity|44|float32|2|
|Max Charge Current|46|float32|None|
|Max Discharge Current|48|float32|None|
|Max Cell Voltage|50|float32|None|
|Min Cell Voltage|52|float32|None|
|Temperature Sensor 1|54|float32|3|
|Temperature Sensor 2|56|float32|4|
|Temperature Sensor 3|58|float32|5|
|Temperature Sensor 4|60|float32|6|
|MOSFET Temperature|62|float32|7|
|Feedback Shunt Current|64|float32|8|
|Low Voltage Alarm|66|bool|None|
|High Voltage Alarm|67|bool|None|
|Low Cell Voltage|68|bool|None|
|High Cell Voltage|69|bool|None|
|Low SOC|70|bool|9|
|High Charge Current|71|bool|10|
|High Discharge Current|72|bool|11|
|Cell Voltage 1|73|float32|None|
|Cell Balance Status 1|75|bool|None|
|Cell Voltage 2|76|float32|None|
|Cell Balance Status 2|78|bool|None|
|Cell Voltage 3|79|float32|None|
|Cell Balance Status 3|81|bool|None|
|...| | | |

## Supported Data Types

In this documentation, we support a fixed set of data types. Each type has a defined bit width, and **all types can also be defined as arrays**.  
Arrays are declared using the notation `Type[N]`, where `N` is the number of elements. For example, `char[10]` represents an array of 10 characters, with each character occupying 8 bits.

### Data Types Overview

- **int8 / uint8**  
  8-bit signed and unsigned integers.  

- **int16 / uint16**  
  16-bit signed and unsigned integers.  

- **int32 / uint32**  
  32-bit signed and unsigned integers.  

- **float32**  
  32-bit floating point number (commonly referred to as `float`).  

- **float64**  
  64-bit floating point number (similar to `double` in many languages).  

- **bool**  
  Boolean value. Although theoretically 1 bit is enough, in practice, a full byte (8 bits) is often used.  

- **char**  
  8-bit character.  

> **Note:**  
> All the data types listed above can be used as arrays. For example, `int16[5]` is interpreted as an array with 5 elements of type `int16`. The total bit size is calculated by multiplying the bit size of the base type by the number of elements.

## Register Allocation

All registers are fixed at 16 bits in length. This means that regardless of the bit width of a data type, the allocation in registers is as follows:

- If a data type occupies less than 16 bits (e.g., a single `char` of 8 bits), it will still use one full 16-bit register. 
- Consequently, `char[1]` and `char[2]` both fit within one register since 1 or 2 characters at 8 bits each do not exceed 16 bits.
- When the total bit size of a data element (or array element) exceeds 16 bits, additional registers are allocated. For example, `char[3]` (24 bits) will require 2 registers, since one register can only hold 16 bits.
- For all data types, the number of registers used is determined by dividing the total required bit size by 16 and rounding up to the next whole number.
## Hardware Support Register

All fields provided via Modbus, regardless of their function and type, are holding registers. These are 16-bit read-write registers.

The hardware support registers are the only values written to the coil, which are 1-bit read-write registers. Each register indicates whether a specific function is supported on the hardware.

Functions without a defined hardware support register are supported by all hardware.

> **Note:** Currently, changes written to both holding registers and coils are not evaluated and will be overwritten.

## Fields

### Manufacturer ID

| Register | Type           | Size |
|-|-|-|
|0| `uint16` | 1 |

Unique identifier of the manufacturer.

### Modbus Version

| Register | Type           | Size |
|-|-|-|
|1| `char[16]` | 8 |

Modbus protocol version, as a string in semantic versioning format. This field may not change between versions of the protocol.

### Hardware Name

| Register | Type           | Size |
|-|-|-|
|9| `char[16]` | 8 |

Name of the iRock hardware. Options include: `iRock 200`, `iRock 300`, `iRock 400`, `iRock 212` or `iRock 424`.

### Hardware Version

| Register | Type           | Size |
|-|-|-|
|17| `char[8]` | 4 |

Version identifier of the hardware, as a string in float format.

### Serial Number

| Register | Type           | Size |
|-|-|-|
|21| `char[12]` | 6 |

Unique serial number of the iRock control board.

### Software Version

| Register | Type           | Size |
|-|-|-|
|27| `char[16]` | 8 |

Software version currently installed, as a string in semantic versioning format.

### Number of Cells

| Register | Type           | Size |
|-|-|-|
|35| `uint16` | 1 |

Number of battery cells in the system. May be any number between 2 and 24.

### Battery Voltage [V]

| Register | Type           | Size |
|-|-|-|
|36| `float32` | 2 |

Total voltage of the battery pack.

### Battery Current [A]

| Register | Type           | Size |
|-|-|-|
|38| `float32` | 2 |

Current flowing in or out of the battery. Positive values indicate charging, negative values indicate discharging.
iRock may set coil 0 to true if function is supported.

### SOC [%]

| Register | Type           | Size |
|-|-|-|
|40| `float32` | 2 |

State of Charge (SOC) of the battery.
iRock may set coil 1 to true if function is supported.

### Capacity [Ah]

| Register | Type           | Size |
|-|-|-|
|42| `float32` | 2 |

Total capacity of the battery pack.

### Remaining Capacity [Ah]

| Register | Type           | Size |
|-|-|-|
|44| `float32` | 2 |

Remaining available capacity in the battery pack.
iRock may set coil 2 to true if function is supported.

### Max Charge Current [A]

| Register | Type           | Size |
|-|-|-|
|46| `float32` | 2 |

Maximum current the battery can accept.

### Max Discharge Current [A]

| Register | Type           | Size |
|-|-|-|
|48| `float32` | 2 |

Maximum current the battery can deliver.

### Max Cell Voltage [V]

| Register | Type           | Size |
|-|-|-|
|50| `float32` | 2 |

Maximum voltage recorded for any single cell.

### Min Cell Voltage [V]

| Register | Type           | Size |
|-|-|-|
|52| `float32` | 2 |

Minimum voltage recorded for any single cell.

### Temperature Sensor 1 [°C]

| Register | Type           | Size |
|-|-|-|
|54| `float32` | 2 |

Temperature reading from sensor 1.
iRock may set coil 3 to true if function is supported.

### Temperature Sensor 2 [°C]

| Register | Type           | Size |
|-|-|-|
|56| `float32` | 2 |

Temperature reading from sensor 2.
iRock may set coil 4 to true if function is supported.

### Temperature Sensor 3 [°C]

| Register | Type           | Size |
|-|-|-|
|58| `float32` | 2 |

Temperature reading from sensor 3.
iRock may set coil 5 to true if function is supported.

### Temperature Sensor 4 [°C]

| Register | Type           | Size |
|-|-|-|
|60| `float32` | 2 |

Temperature reading from sensor 4.
iRock may set coil 6 to true if function is supported.

### MOSFET Temperature [°C]

| Register | Type           | Size |
|-|-|-|
|62| `float32` | 2 |

MOSFET temperature sensor reading.
iRock may set coil 7 to true if function is supported.

### Feedback Shunt Current [A]

| Register | Type           | Size |
|-|-|-|
|64| `float32` | 2 |

Current flowing through the feedback shunt. The feedback shunt messures the current of all ballancers in sum.
iRock may set coil 8 to true if function is supported.

### Low Voltage Alarm

| Register | Type           | Size |
|-|-|-|
|66| `bool` | 1 |

Indicates if a low voltage alarm is active. `true` indicates active, `false` indicates inactive.

### High Voltage Alarm

| Register | Type           | Size |
|-|-|-|
|67| `bool` | 1 |

Indicates if a high voltage alarm is active. `true` indicates active, `false` indicates inactive.

### Low Cell Voltage

| Register | Type           | Size |
|-|-|-|
|68| `bool` | 1 |

Indicates if a low cell voltage alarm is active. `true` indicates active, `false` indicates inactive.

### High Cell Voltage

| Register | Type           | Size |
|-|-|-|
|69| `bool` | 1 |

Indicates if a high cell voltage alarm is active. `true` indicates active, `false` indicates inactive.

### Low SOC

| Register | Type           | Size |
|-|-|-|
|70| `bool` | 1 |

Indicates if a low state of charge alarm is active. `true` indicates active, `false` indicates inactive.
iRock may set coil 9 to true if function is supported.

### High Charge Current

| Register | Type           | Size |
|-|-|-|
|71| `bool` | 1 |

Indicates if a high charge current alarm is active. `true` indicates active, `false` indicates inactive.
iRock may set coil 10 to true if function is supported.

### High Discharge Current

| Register | Type           | Size |
|-|-|-|
|72| `bool` | 1 |

Indicates if a high discharge current alarm is active. `true` indicates active, `false` indicates inactive.
iRock may set coil 11 to true if function is supported.

### Cells

The cell fields repeat as many times as there are cells in the corresponding iRock. The starting address for cell 1 is 73, and the starting address for each subsequent cell is the next available free address. So a Cell Register is calculated as follows:

$$Starting Address + Offset + \left(Last Cell Offset + Last Cell Size\right) * \left( Cell Number -1 \right)=73 + Offset + \left(2 + 1\right) * \left( Cell Number -1 \right)$$

#### Cell Voltage [V]

| Offset | Type           | Size |
|-|-|-|
|0|`float32`|2|

Voltage of cell.

#### Cell Balance Status

| Offset | Type           | Size |
|-|-|-|
|2|`bool`|1|

Boolean indicating if the cells balancer is active. `true` indicates active, `false` indicates inactive.

_This documentation was automatically generated from the YAML configuration file._
