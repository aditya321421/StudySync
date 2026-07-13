import streamlit as st
import streamlit.components.v1 as components

def render_galaxy_component(
    height=600,
    density=1.5,
    glow_intensity=0.5,
    saturation=0.8,
    hue_shift=240,
    star_speed=0.5,
    mouse_repulsion=True,
    repulsion_strength=2.0,
    twinkle_intensity=0.3,
    rotation_speed=0.1,
    transparent=True
):
    """
    Compiles and renders the React Bits WebGL Galaxy Component natively within Streamlit.
    """
    
    # Raw Shaders passed securely to the WebGL context pipeline
    vertex_shader = """
    attribute vec2 uv;
    attribute vec2 position;
    varying vec2 vUv;
    void main() {
        vUv = uv;
        gl_Position = vec4(position, 0, 1);
    }
    """
    
    fragment_shader = """
    precision highp float;
    uniform float uTime;
    uniform vec3 uResolution;
    uniform vec2 uFocal;
    uniform vec2 uRotation;
    uniform float uStarSpeed;
    uniform float uDensity;
    uniform float uHueShift;
    uniform float uSpeed;
    uniform vec2 uMouse;
    uniform float uGlowIntensity;
    uniform float uSaturation;
    uniform bool uMouseRepulsion;
    uniform float uTwinkleIntensity;
    uniform float uRotationSpeed;
    uniform float uRepulsionStrength;
    uniform float uMouseActiveFactor;
    uniform float uAutoCenterRepulsion;
    uniform bool uTransparent;

    varying vec2 vUv;

    #define NUM_LAYER 4.0
    #define STAR_COLOR_CUTOFF 0.2
    #define MAT45 mat2(0.7071, -0.7071, 0.7071, 0.7071)
    #define PERIOD 3.0

    float Hash21(vec2 p) {
        p = fract(p * vec2(123.34, 456.21));
        p += dot(p, p + 45.32);
        return fract(p.x * p.y);
    }

    float tri(float x) { return abs(fract(x) * 2.0 - 1.0); }
    float tris(float x) {
        float t = fract(x);
        return 1.0 - smoothstep(0.0, 1.0, abs(2.0 * t - 1.0));
    }
    float trisn(float x) {
        float t = fract(x);
        return 2.0 * (1.0 - smoothstep(0.0, 1.0, abs(2.0 * t - 1.0))) - 1.0;
    }

    vec3 hsv2rgb(vec3 c) {
        vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
        vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
        return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
    }

    float Star(vec2 uv, float flare) {
        float d = length(uv);
        float m = (0.05 * uGlowIntensity) / d;
        float rays = smoothstep(0.0, 1.0, 1.0 - abs(uv.x * uv.y * 1000.0));
        m += rays * flare * uGlowIntensity;
        uv *= MAT45;
        rays = smoothstep(0.0, 1.0, 1.0 - abs(uv.x * uv.y * 1000.0));
        m += rays * 0.3 * flare * uGlowIntensity;
        m *= smoothstep(1.0, 0.2, d);
        return m;
    }

    vec3 StarLayer(vec2 uv) {
        vec3 col = vec3(0.0);
        vec2 gv = fract(uv) - 0.5; 
        vec2 id = floor(uv);

        for (int y = -1; y <= 1; y++) {
            for (int x = -1; x <= 1; x++) {
                vec2 offset = vec2(float(x), float(y));
                vec2 si = id + vec2(float(x), float(y));
                float seed = Hash21(si);
                float size = fract(seed * 345.32);
                float glossLocal = tri(uStarSpeed / (PERIOD * seed + 1.0));
                float flareSize = smoothstep(0.9, 1.0, size) * glossLocal;

                float red = smoothstep(STAR_COLOR_CUTOFF, 1.0, Hash21(si + 1.0)) + STAR_COLOR_CUTOFF;
                float blu = smoothstep(STAR_COLOR_CUTOFF, 1.0, Hash21(si + 3.0)) + STAR_COLOR_CUTOFF;
                float grn = min(red, blu) * seed;
                vec3 base = vec3(red, grn, blu);
                
                float hue = atan(base.g - base.r, base.b - base.r) / (2.0 * 3.14159) + 0.5;
                hue = fract(hue + uHueShift / 360.0);
                float sat = length(base - vec3(dot(base, vec3(0.299, 0.587, 0.114)))) * uSaturation;
                float val = max(max(base.r, base.g), base.b);
                base = hsv2rgb(vec3(hue, sat, val));

                vec2 pad = vec2(tris(seed * 34.0 + uTime * uSpeed / 10.0), tris(seed * 38.0 + uTime * uSpeed / 30.0)) - 0.5;
                float star = Star(gv - offset - pad, flareSize);
                vec3 color = base;

                float twinkle = trisn(uTime * uSpeed + seed * 6.2831) * 0.5 + 1.0;
                twinkle = mix(1.0, twinkle, uTwinkleIntensity);
                star *= twinkle;
                col += star * size * color;
            }
        }
        return col;
    }

    void main() {
        vec2 focalPx = uFocal * uResolution.xy;
        vec2 uv = (vUv * uResolution.xy - focalPx) / uResolution.y;
        
        if (uMouseRepulsion) {
            vec2 mousePosUV = (uMouse * uResolution.xy - focalPx) / uResolution.y;
            float mouseDist = length(uv - mousePosUV);
            vec2 repulsion = normalize(uv - mousePosUV) * (uRepulsionStrength / (mouseDist + 0.1));
            uv += repulsion * 0.05 * uMouseActiveFactor;
        }

        float autoRotAngle = uTime * uRotationSpeed;
        mat2 autoRot = mat2(cos(autoRotAngle), -sin(autoRotAngle), sin(autoRotAngle), cos(autoRotAngle));
        uv = autoRot * uv;
        uv = mat2(uRotation.x, -uRotation.y, uRotation.y, uRotation.x) * uv;

        vec3 col = vec3(0.0);
        for (float i = 0.0; i < 1.0; i += 1.0 / NUM_LAYER) {
            float depth = fract(i + uStarSpeed * uSpeed);
            float scale = mix(20.0 * uDensity, 0.5 * uDensity, depth);
            float fade = depth * smoothstep(1.0, 0.9, depth);
            col += StarLayer(uv * scale + i * 453.32) * fade;
        }

        if (uTransparent) {
            float alpha = length(col);
            alpha = smoothstep(0.0, 0.3, alpha);
            gl_FragColor = vec4(col, min(alpha, 1.0));
        } else {
            gl_FragColor = vec4(col, 1.0);
        }
    }
    """

    # HTML Shell embedding OGL from CDN and running the translated loop
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            html, body {{ margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: transparent; }}
            #galaxy-container {{ width: 100%; height: 100%; position: relative; }}
        </style>
    </head>
    <body>
        <div id="galaxy-container"></div>
        
        <script type="module">
            import {{ Renderer, Program, Mesh, Color, Triangle }} from 'https://cdn.jsdelivr.net/npm/ogl@0.0.116/dist/ogl.mjs';

            const vertexShader = `{vertex_shader}`;
            const fragmentShader = `{fragment_shader}`;

            const config = {{
                density: {density},
                glowIntensity: {glow_intensity},
                saturation: {saturation},
                hueShift: {hue_shift},
                starSpeed: {star_speed},
                mouseRepulsion: {str(mouse_repulsion).lower()},
                repulsionStrength: {repulsion_strength},
                twinkleIntensity: {twinkle_intensity},
                rotationSpeed: {rotation_speed},
                transparent: {str(transparent).lower()}
            }};

            const ctn = document.getElementById('galaxy-container');
            const targetMousePos = {{ x: 0.5, y: 0.5 }};
            const smoothMousePos = {{ x: 0.5, y: 0.5 }};
            let targetMouseActive = 0.0;
            let smoothMouseActive = 0.0;

            const renderer = new Renderer({{ alpha: config.transparent, premultipliedAlpha: false }});
            const gl = renderer.gl;

            if (config.transparent) {{
                gl.enable(gl.BLEND);
                gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
                gl.clearColor(0, 0, 0, 0);
            }} else {{
                gl.clearColor(0, 0, 0, 1);
            }}

            let program;

            function resize() {{
                renderer.setSize(ctn.offsetWidth, ctn.offsetHeight);
                if (program) {{
                    program.uniforms.uResolution.value = new Color(gl.canvas.width, gl.canvas.height, gl.canvas.width / gl.canvas.height);
                }}
            }
            window.addEventListener('resize', resize, false);

            const geometry = new Triangle(gl);
            program = new Program(gl, {{
                vertex: vertexShader,
                fragment: fragmentShader,
                uniforms: {{"
                    uTime: {{ value: 0 }},
                    uResolution: {{ value: new Color(gl.canvas.width, gl.canvas.height, gl.canvas.width / gl.canvas.height) }},
                    uFocal: {{ value: new Float32Array([0.5, 0.5]) }},
                    uRotation: {{ value: new Float32Array([1.0, 0.0]) }},
                    uStarSpeed: {{ value: config.starSpeed }},
                    uDensity: {{ value: config.density }},
                    uHueShift: {{ value: config.hueShift }},
                    uSpeed: {{ value: 1.0 }},
                    uMouse: {{ value: new Float32Array([0.5, 0.5]) }},
                    uGlowIntensity: {{ value: config.glowIntensity }},
                    uSaturation: {{ value: config.saturation }},
                    uMouseRepulsion: {{ value: config.mouseRepulsion }},
                    uTwinkleIntensity: {{ value: config.twinkleIntensity }},
                    uRotationSpeed: {{ value: config.rotationSpeed }},
                    uRepulsionStrength: {{ value: config.repulsionStrength }},
                    uMouseActiveFactor: {{ value: 0.0 }},
                    uAutoCenterRepulsion: {{ value: 0.0 }},
                    uTransparent: {{ value: config.transparent }}
                "}}
            }});

            resize();
            const mesh = new Mesh(gl, {{ geometry, program }});
            ctn.appendChild(gl.canvas);

            function update(t) {{
                requestAnimationFrame(update);
                program.uniforms.uTime.value = t * 0.001;
                program.uniforms.uStarSpeed.value = (t * 0.001 * config.starSpeed) / 10.0;

                const lerpFactor = 0.05;
                smoothMousePos.x += (targetMousePos.x - smoothMousePos.x) * lerpFactor;
                smoothMousePos.y += (targetMousePos.y - smoothMousePos.y) * lerpFactor;
                smoothMouseActive += (targetMouseActive - smoothMouseActive) * lerpFactor;

                program.uniforms.uMouse.value[0] = smoothMousePos.x;
                program.uniforms.uMouse.value[1] = smoothMousePos.y;
                program.uniforms.uMouseActiveFactor.value = smoothMouseActive;

                renderer.render({{ scene: mesh }});
            }
            requestAnimationFrame(update);

            // Bounded coordinate listeners tracking local iframe vectors cleanly
            ctn.addEventListener('mousemove', (e) => {{
                const rect = ctn.getBoundingClientRect();
                targetMousePos.x = (e.clientX - rect.left) / rect.width;
                targetMousePos.y = 1.0 - (e.clientY - rect.top) / rect.height;
                targetMouseActive = 1.0;
            }});

            ctn.addEventListener('mouseleave', () => {{
                targetMouseActive = 0.0;
            }});
        </script>
    </body>
    </html>
    """
    
    return components.html(html_code, height=height, scrolling=False)

# ==========================================
#  EXECUTION LAYER
# ==========================================
st.set_page_config(layout="wide")
st.title("⚡ Study Sync Terminal Showcase")
st.write("Hover over the section wrapper below to interact with the real-time WebGL engine.")

# Render your component using your custom properties
render_galaxy_component(
    height=600,
    mouseRepulsion=True,
    density=1.5,
    glow_intensity=0.6,
    saturation=0.9,
    hue_shift=240,
    star_speed=0.6
)