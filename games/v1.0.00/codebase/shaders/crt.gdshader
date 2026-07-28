## CRT shader — post-processing for retro look.
## Apply to a ColorRect covering the viewport with material set to this shader.
shader_type canvas_item;

uniform float scanline_strength : hint_range(0.0, 1.0) = 0.3;
uniform float scanline_count : hint_range(100.0, 800.0) = 240.0;
uniform float curvature : hint_range(0.0, 1.0) = 0.1;
uniform float chromatic_aberration : hint_range(0.0, 5.0) = 1.0;
uniform float vignette_strength : hint_range(0.0, 1.0) = 0.3;
uniform float brightness : hint_range(0.8, 1.2) = 1.0;

void fragment() {
    vec2 uv = SCREEN_UV;
    
    // Barrel distortion (curvature)
    vec2 centered = uv - 0.5;
    float dist = dot(centered, centered);
    uv = uv + centered * dist * curvature;
    
    // Chromatic aberration
    vec2 ca_offset = centered * chromatic_aberration * 0.001;
    float r = texture(SCREEN_TEXTURE, uv + ca_offset).r;
    float g = texture(SCREEN_TEXTURE, uv).g;
    float b = texture(SCREEN_TEXTURE, uv - ca_offset).b;
    
    vec3 color = vec3(r, g, b) * brightness;
    
    // Scanlines
    float scanline = sin(uv.y * scanline_count * 3.14159) * 0.5 + 0.5;
    color *= 1.0 - scanline_strength * scanline;
    
    // Vignette
    float vig = 1.0 - dot(centered, centered) * vignette_strength * 4.0;
    color *= clamp(vig, 0.0, 1.0);
    
    COLOR = vec4(color, 1.0);
}