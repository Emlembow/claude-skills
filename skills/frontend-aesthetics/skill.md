# Frontend Aesthetics Skill

## Purpose
This skill ensures websites and web applications are built with distinctive, creative aesthetics that avoid generic "AI slop" design patterns. Use this skill when creating any HTML, React, or web-based artifacts.

## Core Principle
**Avoid convergence toward generic outputs.** Every design should feel intentionally crafted for its specific context, not like it came from a template.

---

## Typography Excellence

### Font Selection Strategy
- **Never default to**: Inter, Roboto, Arial, Helvetica, system-ui, or other overused system fonts
- **Explore distinctive choices**:
  - Serif fonts for editorial/sophisticated contexts (Crimson Pro, Libre Baskerville, Spectral, Lora, Merriweather)
  - Display fonts for personality (DM Serif Display, Playfair Display, Abril Fatface, Righteous)
  - Geometric sans for modern/tech (Outfit, Sora, Plus Jakarta Sans, Lexend, Manrope)
  - Humanist sans for approachable (Figtree, Nunito, Quicksand, Karla)
  - Monospace with character (JetBrains Mono, Fira Code, Space Mono, IBM Plex Mono)

### Typography Best Practices
- Pair contrasting font families (serif + sans, display + body)
- Use font-weight variations strategically (100-900 range)
- Implement responsive typography with clamp() for fluid scaling
- Create hierarchy through size, weight, spacing, and family changes

### Implementation
```css
/* Import from Google Fonts or other CDN */
@import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@300;400;600&family=Outfit:wght@400;600;800&display=swap');

:root {
  --font-display: 'Outfit', sans-serif;
  --font-body: 'Crimson Pro', serif;
}
```

---

## Color & Theme Mastery

### Avoid These Clichés
- Purple gradients on white backgrounds
- Pastel everything
- Safe, corporate blue-gray combinations
- Timid, evenly-distributed color schemes

### Create Cohesive Aesthetics
- **Commit to a mood**: Dark and moody, bright and energetic, warm and earthy, cool and clinical
- **Use CSS variables** for consistency and easy theme switching
- **Dominant + accent approach**: One or two dominant colors with sharp, intentional accent colors
- **Draw inspiration from**:
  - IDE themes (Dracula, Nord, Tokyo Night, Monokai, Catppuccin)
  - Cultural aesthetics (Japanese minimalism, Memphis design, Brutalism)
  - Nature (sunset palettes, ocean depths, forest greens)
  - Art movements (Bauhaus, Art Deco, Vaporwave)

### Color Palette Examples

#### Dark & Cinematic
```css
:root {
  --bg-primary: #0a0a0f;
  --bg-secondary: #1a1a2e;
  --text-primary: #e8e8f0;
  --text-secondary: #a8a8b8;
  --accent: #ff6b6b;
  --accent-alt: #4ecdc4;
}
```

#### Warm & Earthy
```css
:root {
  --bg-primary: #faf8f3;
  --bg-secondary: #e8dcc8;
  --text-primary: #2d2416;
  --text-secondary: #6b5d4f;
  --accent: #d97706;
  --accent-alt: #059669;
}
```

#### Neon & Bold
```css
:root {
  --bg-primary: #000000;
  --bg-secondary: #1a1a1a;
  --text-primary: #00ff88;
  --text-secondary: #88ffcc;
  --accent: #ff0080;
  --accent-alt: #00d4ff;
}
```

---

## Motion & Animation

### High-Impact Animation Strategy
- **One well-orchestrated page load** > scattered micro-interactions
- Use `animation-delay` to stagger reveals for dramatic effect
- Prioritize CSS animations for performance
- Use Motion library (Framer Motion) for React when complex choreography is needed

### CSS Animation Patterns

#### Staggered Fade-In Reveal
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.element-1 {
  animation: fadeInUp 0.8s ease-out 0.1s both;
}

.element-2 {
  animation: fadeInUp 0.8s ease-out 0.3s both;
}

.element-3 {
  animation: fadeInUp 0.8s ease-out 0.5s both;
}
```

#### Hover Effects
```css
.card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}
```

#### Loading States
```css
@keyframes shimmer {
  0% { background-position: -1000px 0; }
  100% { background-position: 1000px 0; }
}

.skeleton {
  background: linear-gradient(90deg, 
    var(--bg-secondary) 0%, 
    var(--bg-primary) 50%, 
    var(--bg-secondary) 100%);
  background-size: 1000px 100%;
  animation: shimmer 2s infinite;
}
```

### React Motion (Framer Motion)
```jsx
import { motion } from "framer-motion";

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.15,
      delayChildren: 0.2
    }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0 }
};

<motion.div
  variants={containerVariants}
  initial="hidden"
  animate="visible"
>
  {items.map(item => (
    <motion.div key={item.id} variants={itemVariants}>
      {item.content}
    </motion.div>
  ))}
</motion.div>
```

---

## Background Excellence

### Never Default to Solid Colors
Create atmosphere and depth with:

#### Layered Gradients
```css
background: 
  radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3), transparent 50%),
  radial-gradient(circle at 80% 80%, rgba(255, 107, 107, 0.2), transparent 50%),
  linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

#### Geometric Patterns
```css
background-image: 
  repeating-linear-gradient(45deg, transparent, transparent 35px, 
    rgba(255, 255, 255, 0.03) 35px, rgba(255, 255, 255, 0.03) 70px);
```

#### Mesh Gradients
```css
background: 
  radial-gradient(at 40% 20%, hsla(28, 100%, 74%, 1) 0, transparent 50%),
  radial-gradient(at 80% 0%, hsla(189, 100%, 56%, 1) 0, transparent 50%),
  radial-gradient(at 0% 50%, hsla(355, 100%, 93%, 1) 0, transparent 50%),
  radial-gradient(at 80% 50%, hsla(340, 100%, 76%, 1) 0, transparent 50%),
  radial-gradient(at 0% 100%, hsla(22, 100%, 77%, 1) 0, transparent 50%);
```

#### Contextual Effects
- Tech/data context: Matrix-style code rain, grid patterns, scan lines
- Nature context: Organic shapes, flowing gradients, particle effects
- Business context: Geometric precision, subtle noise textures, structured patterns

---

## Layout & Composition

### Break the Grid
- Use asymmetric layouts strategically
- Implement overlapping elements with z-index layering
- Create visual rhythm through varied spacing
- Use CSS Grid's subgrid and named areas for complex layouts

### Spacing System
```css
:root {
  --space-xs: clamp(0.5rem, 2vw, 0.75rem);
  --space-sm: clamp(0.75rem, 3vw, 1rem);
  --space-md: clamp(1rem, 4vw, 1.5rem);
  --space-lg: clamp(1.5rem, 6vw, 2.5rem);
  --space-xl: clamp(2.5rem, 8vw, 4rem);
  --space-2xl: clamp(4rem, 12vw, 6rem);
}
```

---

## Anti-Patterns to Avoid

### Generic AI Aesthetics Checklist
- ❌ Inter or Roboto as primary font
- ❌ Purple (#8b5cf6) to blue (#3b82f6) gradient
- ❌ Centered everything with equal padding
- ❌ All rounded corners at border-radius: 8px
- ❌ Generic "card" components in a grid
- ❌ Pastel color palette without contrast
- ❌ No animation or generic fade-ins only
- ❌ Solid white/gray background
- ❌ Predictable three-column layout
- ❌ Generic button styles (rounded, gradient, shadow)

### What to Do Instead
- ✅ Choose fonts that match the project's personality
- ✅ Create unique color schemes from inspiration sources
- ✅ Use asymmetric layouts when appropriate
- ✅ Vary border-radius or use sharp corners intentionally
- ✅ Design custom components specific to the context
- ✅ Build contrast-rich color schemes
- ✅ Orchestrate meaningful animations
- ✅ Layer backgrounds for depth
- ✅ Break the grid strategically
- ✅ Design contextual interaction patterns

---

## Theme Variation Examples

### Brutalist Tech
```css
:root {
  --font-display: 'JetBrains Mono', monospace;
  --font-body: 'Space Mono', monospace;
  --bg: #000000;
  --text: #00ff00;
  --accent: #ff00ff;
  --border: 2px solid var(--accent);
}

/* Sharp corners, high contrast, no shadows */
```

### Elegant Minimal
```css
:root {
  --font-display: 'Cormorant Garamond', serif;
  --font-body: 'Source Sans 3', sans-serif;
  --bg: #fafaf9;
  --text: #1c1917;
  --accent: #78716c;
  --subtle: #f5f5f4;
}

/* Generous whitespace, subtle transitions, refined typography */
```

### Cyberpunk
```css
:root {
  --font-display: 'Orbitron', sans-serif;
  --font-body: 'Rajdhani', sans-serif;
  --bg: #0a0a0f;
  --text: #00ffff;
  --accent: #ff00ff;
  --neon: drop-shadow(0 0 10px currentColor);
}

/* Neon effects, scan lines, glitch animations */
```

### Warm Editorial
```css
:root {
  --font-display: 'Playfair Display', serif;
  --font-body: 'Lora', serif;
  --bg: #fef9f3;
  --text: #3a2817;
  --accent: #c87941;
  --paper: #f8f1e6;
}

/* Book-like, generous line height, warm tones */
```

---

## Implementation Checklist

When creating a new frontend artifact:

1. **Context Analysis**
   - What is the purpose/mood of this project?
   - Who is the audience?
   - What emotion should it evoke?

2. **Aesthetic Decision**
   - Choose a unique font pairing (avoid defaults)
   - Commit to a cohesive color theme (not generic)
   - Decide on animation approach (page load vs. interactions)
   - Plan background treatment (layered, patterned, contextual)

3. **Implementation**
   - Set up CSS variables for consistency
   - Implement typography hierarchy
   - Create color palette with strong contrast
   - Add orchestrated animations
   - Build atmospheric backgrounds
   - Test responsiveness

4. **Distinctiveness Check**
   - Does this look like a generic template? → Revise
   - Would another AI generate something similar? → Make it more unique
   - Is there a strong, cohesive aesthetic? → Good
   - Does it surprise and delight? → Excellent

---

## Quick Reference: Distinctive Font Pairings

1. **Crimson Pro + Outfit** (Editorial meets modern)
2. **Playfair Display + Karla** (Elegant contrast)
3. **JetBrains Mono + Inter** (Only if tech-specific context)
4. **Libre Baskerville + Figtree** (Classic readable)
5. **DM Serif Display + Plus Jakarta Sans** (Bold statement)
6. **Spectral + Manrope** (Refined professional)
7. **Space Mono + Sora** (Techy approachable)
8. **Cormorant Garamond + Source Sans 3** (Sophisticated)
9. **Righteous + Quicksand** (Playful energy)
10. **Merriweather + Lexend** (Warm accessible)

**Remember**: Rotate through different pairings. Don't converge on favorites like Space Grotesk or Outfit across multiple projects.

---

## Final Note

Every frontend should feel intentionally designed for its specific context. When in doubt, make the bolder, more unexpected choice. Generic is the enemy of memorable.
