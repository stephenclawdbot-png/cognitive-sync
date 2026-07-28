# ViewportFrame - Complete Roblox GUI Tutorial

> **Source:** [BrawlDev - Viewport Frame Tutorial #16 (2025)](https://www.youtube.com/watch?v=51hHMXf8z5c)  
> **Duration:** 24:41  
> **Channel:** BrawlDev (167K subscribers)  
> **Documented:** 2026-02-09

---

## Table of Contents

1. [What is a ViewportFrame?](#what-is-a-viewportframe)
2. [Basic Setup](#basic-setup)
3. [Camera System](#camera-system)
4. [Rendering 3D Objects](#rendering-3d-objects)
5. [Making Objects Spin](#making-objects-spin)
6. [WorldModel for Physics & Animations](#worldmodel-for-physics--animations)
7. [Playing Animations](#playing-animations)
8. [Interactive Hover System](#interactive-hover-system)
9. [SurfaceGui Integration](#surfacegui-integration)
10. [ViewportFrame Properties](#viewportframe-properties)
11. [Complete Code Examples](#complete-code-examples)
12. [Common Pitfalls](#common-pitfalls)

---

## What is a ViewportFrame?

A **ViewportFrame** is a unique type of GUI frame in Roblox that displays **3D objects in a 2D space**. Unlike regular frames that only show 2D content, ViewportFrames can render full 3D models, parts, and even animated characters.

### Use Cases
- **Shop display systems** — Show 3D previews of items for sale
- **Mini-map systems** — Render a top-down 3D view of the game world
- **Character customization** — Display player avatars in menus
- **Inventory systems** — Show 3D items instead of flat icons
- **Equipment previews** — Let players see gear before equipping
- **Trophy/Achievement displays** — Showcase 3D collectibles

---

## Basic Setup

### Step 1: Create the GUI Structure

```
StarterGui
└── ScreenGui
    └── ViewportFrame
```

1. Go to **StarterGui** in Explorer
2. Click the **+** button → Insert **ScreenGui**
3. Inside ScreenGui, click **+** → Insert **ViewportFrame**

### Step 2: Configure Size (Use Scale, Not Offset!)

ViewportFrames should use **Scale** instead of **Offset** for responsive sizing:

```
Size: {0.2, 0}, {0.2, 0}
     (ScaleX, OffsetX), (ScaleY, OffsetY)
```

This makes the ViewportFrame 20% of the screen width and height.

### Step 3: Position the Frame

Move/resize the ViewportFrame to your desired location (e.g., corner of screen for a mini-map).

---

## Camera System

### The Default Camera Problem

By default, ViewportFrames use a camera positioned at the **world origin (0, 0, 0)**. This often results in objects appearing incorrectly positioned or not visible at all.

### Solution: Create a Custom Camera

```lua
local viewportFrame = script.Parent

-- Create a new camera for this ViewportFrame
local viewportCam = Instance.new("Camera")

-- Position the camera (adjust Z value to zoom in/out)
-- Negative Z = closer to objects, Positive Z = farther away
viewportCam.CFrame = CFrame.new(0, 0, -10)

-- Assign the camera to the ViewportFrame
viewportFrame.CurrentCamera = viewportCam
```

### Camera Positioning Guide

| Z Value | Effect |
|---------|--------|
| `-5` | Very close (zoomed in) |
| `-10` | Medium distance |
| `5` | Far away (zoomed out) |
| `10` | Very far |

### ⚠️ Important: Studio Camera vs Game Camera

**Do NOT use `workspace.CurrentCamera`** for ViewportFrames!

- The **Studio camera** and **in-game camera** are different
- When you hit Play, Roblox creates a copy of the Studio camera
- This copy doesn't update, so your ViewportFrame appears frozen
- Always create a **dedicated camera** for each ViewportFrame

---

## Rendering 3D Objects

### How to Add Objects to ViewportFrame

Simply **drag and drop** any 3D object (Part, Model, MeshPart, etc.) **directly into the ViewportFrame** in the Explorer.

```
ViewportFrame
├── Camera
├── Part          ← Rendered in the viewport
└── Model         ← Also rendered
```

### What Gets Rendered

- ✅ Parts (all types)
- ✅ MeshParts
- ✅ Models
- ✅ Characters (with some setup)
- ✅ Unions
- ❌ Terrain (not supported)
- ❌ Beams, Trails (limited support)

---

## Making Objects Spin

A common effect is having objects rotate continuously in the ViewportFrame:

```lua
local viewportFrame = script.Parent
local part = viewportFrame.Part  -- Reference to the part inside

-- Create and assign camera
local viewportCam = Instance.new("Camera")
viewportCam.CFrame = CFrame.new(0, 0, -10)
viewportFrame.CurrentCamera = viewportCam

-- Spin the part continuously
while true do
    task.wait()  -- Wait one frame
    
    -- Rotate 1 degree on the Y axis each frame
    part.CFrame *= CFrame.Angles(0, math.rad(1), 0)
end
```

### Rotation Axis Reference

```lua
CFrame.Angles(X, Y, Z)
-- X = Pitch (tilt forward/backward)
-- Y = Yaw (spin left/right) ← Most common for displays
-- Z = Roll (tilt sideways)
```

---

## WorldModel for Physics & Animations

### The Problem

By default, ViewportFrames **do NOT run physics or animations**. If you put a character inside, it will appear frozen with no idle animation.

### The Solution: WorldModel

Wrap your models inside a **WorldModel** to enable physics:

```
ViewportFrame
├── Camera
└── WorldModel        ← Physics container
    └── Character     ← Now animations work!
```

### Setup Steps

1. Inside ViewportFrame, click **+** → Insert **WorldModel**
2. Drag your character/model **into the WorldModel**
3. Now physics and animations will work!

```lua
-- Structure in code:
local viewportFrame = script.Parent
local worldModel = viewportFrame.WorldModel
local character = worldModel.Character
```

---

## Playing Animations

Once your character is inside a WorldModel, you can play animations:

### Getting a Character into ViewportFrame

1. Hit **Play** in Studio
2. In Explorer, go to `Workspace` → Find your character
3. **Right-click** → **Copy**
4. Hit **Stop**
5. **Right-click** on Workspace → **Paste Into**
6. Drag the character into `ViewportFrame.WorldModel`

### Animation Script

Create a **LocalScript** inside the character:

```lua
-- DanceScript (LocalScript inside Character)

local animation = script.Animation  -- Animation object as child
local humanoid = script.Parent:WaitForChild("Humanoid")
local animator = humanoid:WaitForChild("Animator")

-- Load and play the animation
local loadedAnimation = animator:LoadAnimation(animation)
loadedAnimation:Play()
```

### Finding Animation IDs

1. Select your character's **Animate** script
2. Look for animation folders (idle, walk, dance, etc.)
3. Each contains Animation objects with IDs you can copy

---

## Interactive Hover System

This creates a shop-display-style effect where:
- **Mouse enters** → Character zooms in and starts rotating
- **Mouse leaves** → Rotation stops, character returns to default position

### Full Implementation

```lua
-- LocalScript inside ViewportFrame

local TweenService = game:GetService("TweenService")
local RunService = game:GetService("RunService")

local viewportFrame = script.Parent
local character = viewportFrame.WorldModel.Character

-- State tracking
local mouseEntered = false
local rotationConnection = nil

-- Default position (adjust based on your character's position)
-- The 180 degree rotation faces the character toward the camera
local defaultCFrame = CFrame.new(0, 0, 0) * CFrame.Angles(0, math.rad(180), 0)

-- Camera setup
local viewportCam = Instance.new("Camera")
viewportCam.CFrame = CFrame.new(0, 0, 6)  -- Adjust distance as needed
viewportFrame.CurrentCamera = viewportCam

-- Tween for zooming IN (moves character toward camera)
local tweenIn = TweenService:Create(
    character.PrimaryPart,
    TweenInfo.new(0.25),  -- Duration: 0.25 seconds
    {CFrame = defaultCFrame + defaultCFrame.LookVector}  -- Move 1 stud forward
)

-- Tween for zooming OUT (returns to default position)
local tweenOut = TweenService:Create(
    character.PrimaryPart,
    TweenInfo.new(0.25),
    {CFrame = defaultCFrame}
)

-- Mouse enters the ViewportFrame
viewportFrame.MouseEnter:Connect(function()
    if not mouseEntered then
        mouseEntered = true
        tweenIn:Play()
        
        -- Start rotating after zoom completes
        tweenIn.Completed:Connect(function()
            if mouseEntered then
                rotationConnection = RunService.RenderStepped:Connect(function()
                    -- Rotate 1 degree per frame on Y axis
                    character.PrimaryPart.CFrame *= CFrame.Angles(0, math.rad(1), 0)
                end)
            end
        end)
    end
end)

-- Mouse leaves the ViewportFrame
viewportFrame.MouseLeave:Connect(function()
    if mouseEntered then
        mouseEntered = false
        
        -- Stop the rotation
        if rotationConnection then
            rotationConnection:Disconnect()
            rotationConnection = nil
        end
        
        -- Zoom back out
        tweenOut:Play()
    end
end)
```

### Key Concepts Explained

| Concept | Purpose |
|---------|---------|
| `mouseEntered` | Debounce to prevent multiple triggers |
| `rotationConnection` | Store the RenderStepped connection so we can disconnect it |
| `defaultCFrame` | Remember the starting position to return to |
| `LookVector` | Direction the character faces; adding it moves forward |
| `RenderStepped` | Runs every frame for smooth rotation (LocalScript only) |

---

## SurfaceGui Integration

You can display ViewportFrames on **3D surfaces** (walls, parts) using SurfaceGui:

### Setup

```
Workspace
└── Part (the display surface)

StarterGui
└── ScreenGui
    └── SurfaceGui
        ├── Adornee: [set to the Part]
        └── ViewportFrame
            └── (your 3D content)
```

### Steps

1. Create a Part in Workspace (this is your "screen")
2. In StarterGui → ScreenGui, insert a **SurfaceGui**
3. Select SurfaceGui → Set **Adornee** property to your Part
4. Insert ViewportFrame inside SurfaceGui
5. Add your 3D content to the ViewportFrame

Now the ViewportFrame renders on the surface of the Part!

---

## ViewportFrame Properties

### Lighting Properties

| Property | Type | Description |
|----------|------|-------------|
| `Ambient` | Color3 | Ambient light color in the viewport |
| `LightColor` | Color3 | Color of the directional light |
| `LightDirection` | Vector3 | Direction the light comes from |

### Camera Properties

| Property | Type | Description |
|----------|------|-------------|
| `CurrentCamera` | Camera | The camera used to render the viewport |

### Example: Custom Lighting

```lua
local viewportFrame = script.Parent

-- Warm ambient lighting
viewportFrame.Ambient = Color3.fromRGB(50, 40, 30)

-- Bright white main light
viewportFrame.LightColor = Color3.fromRGB(255, 255, 255)

-- Light coming from above-front
viewportFrame.LightDirection = Vector3.new(-1, -1, -1)
```

---

## Complete Code Examples

### Example 1: Simple Spinning Part Display

```lua
-- LocalScript in ViewportFrame
local viewportFrame = script.Parent

-- Create a part to display
local part = Instance.new("Part")
part.Size = Vector3.new(4, 4, 4)
part.Color = Color3.fromRGB(255, 100, 100)
part.CFrame = CFrame.new(0, 0, 0)
part.Parent = viewportFrame

-- Create and set up camera
local camera = Instance.new("Camera")
camera.CFrame = CFrame.new(0, 2, -10) * CFrame.Angles(math.rad(-10), 0, 0)
camera.Parent = viewportFrame
viewportFrame.CurrentCamera = camera

-- Spin the part
while true do
    task.wait()
    part.CFrame *= CFrame.Angles(0, math.rad(1), 0)
end
```

### Example 2: Character Preview with Animation

```lua
-- LocalScript in ViewportFrame
-- Assumes character is already in ViewportFrame.WorldModel

local viewportFrame = script.Parent
local worldModel = viewportFrame.WorldModel
local character = worldModel:FindFirstChild("Character")

-- Set up camera
local camera = Instance.new("Camera")
camera.CFrame = CFrame.new(0, 2, 6)
camera.Parent = viewportFrame
viewportFrame.CurrentCamera = camera

-- Position character
if character and character.PrimaryPart then
    character:SetPrimaryPartCFrame(
        CFrame.new(0, 0, 0) * CFrame.Angles(0, math.rad(180), 0)
    )
end

-- Optional: Load and play animation
local humanoid = character:FindFirstChild("Humanoid")
if humanoid then
    local animator = humanoid:FindFirstChildOfClass("Animator")
    if animator then
        -- Create animation (replace with your animation ID)
        local animation = Instance.new("Animation")
        animation.AnimationId = "rbxassetid://507771019"  -- Wave animation
        
        local animTrack = animator:LoadAnimation(animation)
        animTrack:Play()
    end
end
```

### Example 3: Mini-Map System (Conceptual)

```lua
-- LocalScript for a top-down mini-map
local viewportFrame = script.Parent
local worldModel = Instance.new("WorldModel")
worldModel.Parent = viewportFrame

-- Create camera looking straight down
local camera = Instance.new("Camera")
camera.CFrame = CFrame.new(0, 100, 0) * CFrame.Angles(math.rad(-90), 0, 0)
camera.Parent = viewportFrame
viewportFrame.CurrentCamera = camera

-- Clone relevant parts from workspace into the viewport
-- (buildings, terrain features, etc.)
local function updateMiniMap()
    -- Clear old content
    for _, child in worldModel:GetChildren() do
        child:Destroy()
    end
    
    -- Clone important landmarks
    for _, landmark in workspace.Landmarks:GetChildren() do
        local clone = landmark:Clone()
        clone.Parent = worldModel
    end
end

-- Update periodically
while true do
    updateMiniMap()
    task.wait(1)
end
```

---

## Common Pitfalls

### 1. Objects Not Visible
**Problem:** Put a part in ViewportFrame but can't see it.  
**Solution:** 
- Create a custom camera
- Position the camera to look at your object
- Adjust camera Z position (try -5 to -20)

### 2. Character Has No Animation
**Problem:** Character appears frozen, no idle animation.  
**Solution:** 
- Put character inside a **WorldModel**
- WorldModel enables physics for its children

### 3. Camera Works in Studio, Not in Game
**Problem:** ViewportFrame looks correct in Studio but freezes when you play.  
**Solution:** 
- Don't use `workspace.CurrentCamera` as your ViewportFrame camera
- Create a new `Instance.new("Camera")` specifically for the viewport

### 4. Rotation Is Jerky
**Problem:** Object rotation looks stuttery.  
**Solution:**
- Use `RunService.RenderStepped` for LocalScripts
- Use `RunService.Heartbeat` for server Scripts
- Make sure you're using `task.wait()` not `wait()`

### 5. Object Positioned Weirdly
**Problem:** Object appears at strange angle or position.  
**Solution:**
- Reset object's CFrame: `object.CFrame = CFrame.new(0, 0, 0)`
- Adjust camera position to frame the object nicely
- For characters: rotate 180° on Y axis to face camera

---

## Performance Considerations

- ViewportFrames **re-render every frame** — use sparingly
- Complex models with many parts = more GPU load
- Consider **Level of Detail (LOD)** — simpler models for viewports
- Limit the number of ViewportFrames visible at once
- Disable ViewportFrames when not visible (set `Visible = false`)

---

## Quick Reference

```lua
-- MINIMUM VIABLE VIEWPORTFRAME

local vpf = script.Parent  -- ViewportFrame

-- 1. Add something to display
local part = Instance.new("Part")
part.Parent = vpf

-- 2. Create camera
local cam = Instance.new("Camera")
cam.CFrame = CFrame.new(0, 0, -10)
cam.Parent = vpf
vpf.CurrentCamera = cam

-- Done! Part now visible in viewport
```

---

## Related Tutorials

From BrawlDev's GUI Tutorial Series:
- #3: TextButton
- #4: Scale vs Offset (UDim2)
- #5: TextBox
- #16: **ViewportFrame** (this tutorial)

---

*Documentation generated from YouTube transcript via `youtube-transcript-api`*
