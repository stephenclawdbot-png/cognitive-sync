# 🎨 BUNDLE SHOP UI — COMPLETE BREAKDOWN
**Game:** [UPD] Knockout! by braxworks
**Analyzed:** 2026-02-08

---

## **Design Style Name: "Soft Bento UI" / "Kawaii Card UI"**
This is a mix of:
- **Bento Box Layout** — modular cards/panels
- **Soft UI (Neumorphism-lite)** — rounded corners, soft shadows
- **Kawaii/Cartoon aesthetic** — playful colors, chunky elements

---

## 📐 **LAYOUT STRUCTURE**

```
┌─────────────────────────────────────────────────────────┐
│ [Title]                    [Timer/Progress]        [X]  │  ← HEADER BAR
├─────────────────────────────────────────────────────────┤
│                                          ┌────────────┐ │
│                                          │ Item List  │ │
│     ┌─────────┐    ┌─────────┐          │ - Skin     │ │
│     │ 3D Pet  │    │ Player  │          │ - Title    │ │  ← PREVIEW STAGE
│     │ Preview │    │ Preview │          │ - Arrow    │ │
│     └─────────┘    └─────────┘          │ - Dance    │ │
│                                          ├────────────┤ │
│                                          │ [BUY Ⓡ99] │ │
│                                          └────────────┘ │
├─────────────────────────────────────────────────────────┤
│ ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│ │ Bundle 1 │  │ Bundle 2 │  │ Bundle 3 │  ...          │  ← CAROUSEL
│ └──────────┘  └──────────┘  └──────────┘               │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 **COLOR PALETTE**

| Element | Color | Hex (approx) |
|---------|-------|--------------|
| Background | Light cyan/ice blue | `#E8F4F8` |
| Header text | White + black stroke | `#FFFFFF` |
| Timer badge | Coral/salmon | `#FF6B6B` |
| Buy button | Bright green | `#7ED321` |
| Close button | Red/orange gradient | `#FF4444` → `#FF6600` |
| Card borders | Varies by theme | — |
| Item list bg | Dark blue/navy | `#1A2744` |

---

## 🔤 **TYPOGRAPHY**

- **Title font:** Bold, rounded sans-serif with **black outline/stroke** (2-3px)
- **Body text:** Clean sans-serif, white on dark backgrounds
- **Labels:** ALL CAPS for categories (SKIN, TITLE, ARROW)
- **Numbers:** Bold, slightly condensed

**Font style:** Looks like **Fredoka One** or **Luckiest Guy** for titles

---

## 📦 **COMPONENT BREAKDOWN**

### 1. **Header Bar**
- Left: Title with drop shadow
- Center/Right: Status indicator (timer OR progress)
- Far Right: Big X close button
- **Height:** ~60-80px

### 2. **Preview Stage**
- 3D rendered scene (not flat image)
- Metal/industrial platform floor
- Character + Pet side by side
- Floating title above character
- **Ambient lighting:** soft, slightly blue tint

### 3. **Item List Panel**
- Dark navy background (`#1A2744`)
- Rounded corners (~12px)
- Scrollable vertically
- Each row: `[Thumbnail] [Name] [Type]`
- Some items have action buttons (👁 View)

### 4. **Buy Button**
- Bright green (`#7ED321`)
- Robux icon + price
- Full-width within panel
- Rounded corners (~8px)
- Slight shadow

### 5. **Bundle Carousel (Bottom)**
- Horizontal scroll
- Cards are ~200x150px
- Selected card has **colored border glow**
- Each card has:
  - Background image/gradient
  - Timer overlay (top-left)
  - Bundle name (bottom)
  - Theme-specific styling

---

## ✨ **SPECIAL EFFECTS**

| Effect | Where Used |
|--------|------------|
| **Drop shadows** | All floating panels |
| **Border glow** | Selected items |
| **Gradient backgrounds** | Bundle cards |
| **Hazard stripes** | Milestone/grind items |
| **Countdown timers** | Limited items |
| **Progress bars** | Milestone unlocks |

---

## 🎯 **BUNDLE CARD THEMES**

| Bundle | Background | Border | Vibe |
|--------|------------|--------|------|
| Napguin | Night sky, stars, moon | Cyan | Sleepy/cozy |
| Broguin | Orange fire/flames | Orange | Cool/street |
| Drillguin | B&W industrial, static | ⚠️ Yellow hazard | Grind/hardcore |

---

## 🏷️ **UNLOCK TYPE PATTERNS**

| Unlock Type | Header Indicator | Border Style |
|-------------|-----------------|--------------|
| Time-limited | ⏱️ Countdown timer | Standard |
| Milestone | 📊 Progress (0/1000) | ⚠️ Hazard stripes |

---

## 💰 **PRICING TIERS**

| Bundle | Price | Includes |
|--------|-------|----------|
| Napguin | Ⓡ 99 | Basic 4-item set |
| Broguin | Ⓡ 299 | Mid-tier |
| Drillguin | Ⓡ 799 | Premium + Animation Pack |

---

## 📦 **BUNDLE CONTENTS PATTERN**

Each bundle typically includes:
- **Skin** — Penguin appearance
- **Title** — Floating name tag above player
- **Arrow** — Knockout indicator cosmetic
- **Dance** — Emote/animation
- **Animation Pack** (premium only) — Full animation set with preview button

---

## 💡 **HOW TO RECREATE IN ROBLOX STUDIO**

### GUI Structure:
1. **ScreenGui** with CanvasGroup for main container
2. **UICorner** on everything (CornerRadius = 12-16)
3. **UIStroke** for text outlines
4. **UIGradient** for button/card backgrounds
5. **ViewportFrame** for 3D previews
6. **ScrollingFrame** for item list
7. **TweenService** for selection animations

### Key Properties:
```lua
-- Rounded corners
local corner = Instance.new("UICorner")
corner.CornerRadius = UDim.new(0, 12)
corner.Parent = frame

-- Text stroke
textLabel.TextStrokeTransparency = 0
textLabel.TextStrokeColor3 = Color3.new(0, 0, 0)

-- Buy button gradient
local gradient = Instance.new("UIGradient")
gradient.Color = ColorSequence.new({
    ColorSequenceKeypoint.new(0, Color3.fromRGB(126, 211, 33)),
    ColorSequenceKeypoint.new(1, Color3.fromRGB(100, 180, 25))
})
gradient.Rotation = 90
gradient.Parent = buyButton

-- Selection glow (using UIStroke)
local stroke = Instance.new("UIStroke")
stroke.Color = Color3.fromRGB(0, 200, 255)
stroke.Thickness = 3
stroke.Transparency = 0
stroke.Parent = selectedCard
```

### ViewportFrame for 3D Preview:
```lua
local viewport = Instance.new("ViewportFrame")
viewport.Size = UDim2.new(0.5, 0, 0.7, 0)
viewport.BackgroundTransparency = 1

-- Add camera
local camera = Instance.new("Camera")
camera.CFrame = CFrame.new(Vector3.new(0, 2, 5), Vector3.new(0, 1, 0))
viewport.CurrentCamera = camera

-- Clone and add model
local previewModel = penguinModel:Clone()
previewModel.Parent = viewport
```

---

## 🎬 **ANIMATIONS TO IMPLEMENT**

1. **Card selection** — Scale up + border glow tween
2. **Panel open** — Slide in from right or fade + scale
3. **Buy button hover** — Slight scale + brightness
4. **Item list scroll** — Smooth momentum scrolling
5. **Timer countdown** — Number tick animation
6. **3D preview** — Idle animation loop on character/pet

---

*Notes compiled by Max ⚡*
