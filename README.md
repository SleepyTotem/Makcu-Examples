# MAKCU Controller Utility

## Features
- Real-time button state monitoring
- Auto COM port detection (CH343 devices)
- 4Mbps serial communication
- Advanced mouse movement controls:
  - Instant movement
  - Bézier curves
  - Circular patterns

## Menu Options
| Key | Command                | Description                          |
|-----|------------------------|--------------------------------------|
| 1   | Show button status     | Display current button states        |
| 2   | Move mouse in circle   | 5-second circular pattern            |
| 3   | Test bezier curve      | Demonstrate curved mouse movement    |
| q   | Quit                   | Exit program                         |

## Mouse Control Syntax
```
km.move(x, y)  # Instant movement
km.move(x, y, segments)  # Auto-bézier
km.move(x, y, segments, ctrl_x, ctrl_y)  # Manual bézier
```

## Button Mapping
| Bit | Button               |
|-----|----------------------|
| 0   | Left Mouse           |
| 1   | Right Mouse          |
| 2   | Middle Mouse         |
| 3   | Side Button 4        |
| 4   | Side Button 5        |

## Configuration
Set fallback COM port in `makcu_controller.py`:
```
fallback_com_port = "COM1"  # Change if needed
```

## Troubleshooting
**Device not found?**
1. Install [CH343 driver](https://github.com/SleepyTotem/Makcu-Examples/releases/tag/Driver)
2. Check COM port in Device Manager
3. Update `fallback_com_port`


## License
This project is licensed under the terms of the [GNU General Public License v3.0 or later](https://www.gnu.org/licenses/gpl-3.0.html).

**You may:**
- Use freely  
- Modify and redistribute  
- Use for personal and commercial projects  

**You may not:**
- Sell this software directly without compliance with the GPL  

**Attribution required**
