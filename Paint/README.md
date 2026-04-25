
Paint

Description:
This is a simple drawing application built with Pygame.
It allows the user to draw, create shapes, erase, and choose colors.

Features:
- Brush tool (free drawing)
- Eraser tool
- Filled rectangle
- Filled circle
- Color selection (red, green, blue)
- Simple UI with buttons

Controls:
- Mouse click on buttons → select tool or color
- Mouse click on canvas → start drawing
- Mouse movement → draw with brush or eraser
- Mouse release → finish rectangle or circle

How it works:
- Drawing happens on a separate surface called "canvas"
- Canvas stores all drawings
- Canvas is displayed on the screen every frame
- Screen updates using pygame.display.flip()
