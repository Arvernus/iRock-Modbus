# iRock Modbus Registers 2.0.0

All provided fields will be accessible in the Holding Registers. Each field can be split into multiple registers depending on its length. Fields that are not supported by all hardware will additionally write to a coil to indicate whether this function is supported.

## Table of Contents

- [Versioning](#versioning)
- [Overview](#overview)
- [Supported Data Types](#supported-data-types)
- [Register Allocation](#register-allocation)
- [Hardware Support Register](#hardware-support-register)
- [Fields](#fields)
  - [Cells](#cells)

## Versioning

This table version is "2.0.0". Future changes to the table will follow semantic versioning:

- Patch version (0.0.x): Compatible changes, such as adding new fields or minor adjustments that do not affect existing registers.
- Minor version (0.x.0): Changes that may alter values but keep the same position and length, such as updating default values or improving data types.
- Major version (x.0.0): Comprehensive changes that may alter the position of fields, remove deprecated fields, or introduce breaking changes that require client updates.

## Overview

| |Register|Type|[Hardware Supported Register](#hardware-support-register)|
|-|-|-|-|
|[Manufacturer ID](#manufacturer-id)|0|uint16|None|
|[Modbus Version](#modbus-version)|1|char[16]|None|
|[Hardware Name](#hardware-name)|9|char[16]|None|
|[Hardware Version](#hardware-version)|17|char[16]|None|
|[Serial Number](#serial-number)|25|char[8]|None|
|[Software Version](#software-version)|29|char[16]|None|
|[Number of Cells](#number-of-cells)|37|uint16|None|
|[Battery Voltage](#battery-voltage)|38|float32|None|
|[Battery Current](#battery-current)|40|float32|0|
|[SOC](#soc)|42|float32|1|
|[Capacity](#capacity)|44|float32|None|
|[Remaining Capacity](#remaining-capacity)|46|float32|2|
|[Max Charge Current](#max-charge-current)|48|float32|None|
|[Max Discharge Current](#max-discharge-current)|50|float32|None|
|[Max Cell Voltage](#max-cell-voltage)|52|float32|None|
|[Min Cell Voltage](#min-cell-voltage)|54|float32|None|
|[Temperature Sensor 1](#temperature-sensor-1)|56|float32|3|
|[Temperature Sensor 2](#temperature-sensor-2)|58|float32|4|
|[Temperature Sensor 3](#temperature-sensor-3)|60|float32|5|
|[Temperature Sensor 4](#temperature-sensor-4)|62|float32|6|
|[MOSFET Temperature](#mosfet-temperature)|64|float32|7|
|[Feedback Shunt Current](#feedback-shunt-current)|66|float32|8|
|[Charge FET](#charge-fet)|68|bool|9|
|[Discharge FET](#discharge-fet)|69|bool|10|
|[Allow Charge](#allow-charge)|70|bool|11|
|[Allow Discharge](#allow-discharge)|71|bool|12|
|[Low Voltage Alarm](#low-voltage-alarm)|72|uint8|None|
|[High Voltage Alarm](#high-voltage-alarm)|73|uint8|None|
|[Low Cell Voltage Alarm](#low-cell-voltage-alarm)|74|uint8|None|
|[High Cell Voltage Alarm](#high-cell-voltage-alarm)|75|uint8|None|
|[Low SOC Alarm](#low-soc-alarm)|76|uint8|13|
|[High Charge Current Alarm](#high-charge-current-alarm)|77|uint8|14|
|[High Discharge Current Alarm](#high-discharge-current-alarm)|78|uint8|15|
|[Temperature Alarm](#temperature-alarm)|79|uint8|16|
|[Cell Voltage 1](#cell-voltage-1)|80|float32|None|
|[Cell Balance Status 1](#cell-balance-status-1)|82|bool|None|
|[Cell Voltage 2](#cell-voltage-2)|83|float32|None|
|[Cell Balance Status 2](#cell-balance-status-2)|85|bool|None|
|[Cell Voltage 3](#cell-voltage-3)|86|float32|None|
|[Cell Balance Status 3](#cell-balance-status-3)|88|bool|None|
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

- **int64 / uint64**  
  64-bit signed and unsigned integers.  

- **float32**  
  32-bit floating point number (commonly referred to as `float`).  

- **float64**  
  64-bit floating point number (similar to `double` in many languages).  

- **bool**  
  Boolean value, represented as 1 bit.  `true` is represented as `1`, and `false` is represented as `0`.  

- **char**  
  8-bit character. See the ASCII table for character representation.  

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
|17| `char[16]` | 8 |

Version identifier of the hardware, as a string in semantic versioning format.

### Serial Number

| Register | Type           | Size |
|-|-|-|
|25| `char[8]` | 4 |

Unique serial number of the iRock control board.

### Software Version

| Register | Type           | Size |
|-|-|-|
|29| `char[16]` | 8 |

Software version currently installed, as a string in semantic versioning format.

### Number of Cells

| Register | Type           | Size |
|-|-|-|
|37| `uint16` | 1 |

Number of battery cells in the system. May be any number between 2 and 24.

### Battery Voltage [V]

| Register | Type           | Size |
|-|-|-|
|38| `float32` | 2 |

Total voltage of the battery pack.

### Battery Current [A]

| Register | Type           | Size |
|-|-|-|
|40| `float32` | 2 |

Current flowing in or out of the battery. Positive values indicate charging, negative values indicate discharging.
iRock may set coil 0 to true if function is supported.

### SOC [%]

| Register | Type           | Size |
|-|-|-|
|42| `float32` | 2 |

State of Charge (SOC) of the battery.
iRock may set coil 1 to true if function is supported.

### Capacity [Ah]

| Register | Type           | Size |
|-|-|-|
|44| `float32` | 2 |

Total capacity of the battery pack.

### Remaining Capacity [Ah]

| Register | Type           | Size |
|-|-|-|
|46| `float32` | 2 |

Remaining available capacity in the battery pack.
iRock may set coil 2 to true if function is supported.

### Max Charge Current [A]

| Register | Type           | Size |
|-|-|-|
|48| `float32` | 2 |

Maximum current the battery can accept.

### Max Discharge Current [A]

| Register | Type           | Size |
|-|-|-|
|50| `float32` | 2 |

Maximum current the battery can deliver.

### Max Cell Voltage [V]

| Register | Type           | Size |
|-|-|-|
|52| `float32` | 2 |

Maximum voltage recorded for any single cell.

### Min Cell Voltage [V]

| Register | Type           | Size |
|-|-|-|
|54| `float32` | 2 |

Minimum voltage recorded for any single cell.

### Temperature Sensor 1 [°C]

| Register | Type           | Size |
|-|-|-|
|56| `float32` | 2 |

Temperature reading from sensor 1.
iRock may set coil 3 to true if function is supported.

### Temperature Sensor 2 [°C]

| Register | Type           | Size |
|-|-|-|
|58| `float32` | 2 |

Temperature reading from sensor 2.
iRock may set coil 4 to true if function is supported.

### Temperature Sensor 3 [°C]

| Register | Type           | Size |
|-|-|-|
|60| `float32` | 2 |

Temperature reading from sensor 3.
iRock may set coil 5 to true if function is supported.

### Temperature Sensor 4 [°C]

| Register | Type           | Size |
|-|-|-|
|62| `float32` | 2 |

Temperature reading from sensor 4.
iRock may set coil 6 to true if function is supported.

### MOSFET Temperature [°C]

| Register | Type           | Size |
|-|-|-|
|64| `float32` | 2 |

MOSFET temperature sensor reading.
iRock may set coil 7 to true if function is supported.

### Feedback Shunt Current [A]

| Register | Type           | Size |
|-|-|-|
|66| `float32` | 2 |

Current flowing through the feedback shunt. The feedback shunt messures the current of all ballancers in sum.
iRock may set coil 8 to true if function is supported.

### Charge FET

| Register | Type           | Size |
|-|-|-|
|68| `bool` | 1 |

Boolean indicating if the charge FET is active. `true` indicates active, `false` indicates inactive.
iRock may set coil 9 to true if function is supported.

### Discharge FET

| Register | Type           | Size |
|-|-|-|
|69| `bool` | 1 |

Boolean indicating if the discharge FET is active. `true` indicates active, `false` indicates inactive.
iRock may set coil 10 to true if function is supported.

### Allow Charge

| Register | Type           | Size |
|-|-|-|
|70| `bool` | 1 |

Boolean indicating if charging is allowed. `true` indicates allowed, `false` indicates disallowed.
iRock may set coil 11 to true if function is supported.

### Allow Discharge

| Register | Type           | Size |
|-|-|-|
|71| `bool` | 1 |

Boolean indicating if discharging is allowed. `true` indicates allowed, `false` indicates disallowed.
iRock may set coil 12 to true if function is supported.

### Low Voltage Alarm

| Register | Type           | Size |
|-|-|-|
|72| `uint8` | 1 |

Alarm Status for low battery voltage. No Alarm may be `0`, Warnings may be `1` and Alarms may be `2`.

### High Voltage Alarm

| Register | Type           | Size |
|-|-|-|
|73| `uint8` | 1 |

Alarm Status for high battery voltage. No Alarm may be `0`, Warnings may be `1` and Alarms may be `2`.

### Low Cell Voltage Alarm

| Register | Type           | Size |
|-|-|-|
|74| `uint8` | 1 |

Alarm Status for low cell voltage. No Alarm may be `0`, Warnings may be `1` and Alarms may be `2`.

### High Cell Voltage Alarm

| Register | Type           | Size |
|-|-|-|
|75| `uint8` | 1 |

Alarm Status for high cell voltage. No Alarm may be `0`, Warnings may be `1` and Alarms may be `2`.

### Low SOC Alarm

| Register | Type           | Size |
|-|-|-|
|76| `uint8` | 1 |

Alarm Status for low SOC. No Alarm may be `0`, Warnings may be `1` and Alarms may be `2`.
iRock may set coil 13 to true if function is supported.

### High Charge Current Alarm

| Register | Type           | Size |
|-|-|-|
|77| `uint8` | 1 |

Alarm Status for high charge current. No Alarm may be `0`, Warnings may be `1` and Alarms may be `2`.
iRock may set coil 14 to true if function is supported.

### High Discharge Current Alarm

| Register | Type           | Size |
|-|-|-|
|78| `uint8` | 1 |

Alarm Status for high discharge current. No Alarm may be `0`, Warnings may be `1` and Alarms may be `2`.
iRock may set coil 15 to true if function is supported.

### Temperature Alarm

| Register | Type           | Size |
|-|-|-|
|79| `uint8` | 1 |

Alarm Status for high temperature. No Alarm may be `0`, Warnings may be `1` and Alarms may be `2`.
iRock may set coil 16 to true if function is supported.

### Cells

The cell fields repeat as many times as there are cells in the corresponding iRock. Cell numbering starts with 1. The starting address for cell 1 is 80, and the starting address for each subsequent cell is the next available free address. So a Cell Register is calculated as follows:

$$Starting Address + Offset + \left(Last Cell Offset + Last Cell Size\right) * \left( Cell Number -1 \right)$$
$$=80 + Offset + \left(2 + 1\right) * \left( Cell Number -1 \right)$$
$$=80 + Offset + 3 * \left( Cell Number -1 \right)$$

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
