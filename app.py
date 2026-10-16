import os
import io
import time
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Neural Strikers — AI Kit & Content Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Dark-Mode Cybernetic Styling (CSS)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;600&display=swap');

    /* Global Background and Typography */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #0d131f 0%, #07090e 90%);
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }

    /* Headings */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 0.05em;
    }
    
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00f0ff 0%, #7000ff 50%, #ffd700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }

    .sub-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.15rem;
        color: #94a3b8;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }

    .badge-tag {
        display: inline-block;
        background: rgba(0, 240, 255, 0.12);
        border: 1px solid rgba(0, 240, 255, 0.35);
        color: #00f0ff;
        padding: 4px 12px;
        border-radius: 9999px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        margin-bottom: 0.8rem;
    }

    /* Card Containers */
    .cyber-card {
        background: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }

    .cyber-card-gold {
        border-left: 3px solid #ffd700;
    }

    .cyber-card-cyan {
        border-left: 3px solid #00f0ff;
    }

    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #00f0ff 0%, #0077ff 100%);
        color: #050b14 !important;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 0.65rem 1.5rem;
        font-size: 0.95rem;
        letter-spacing: 0.05em;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.6);
        color: #000000 !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 6px 6px 0px 0px;
        padding: 8px 16px;
        color: #94a3b8;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 240, 255, 0.15) !important;
        color: #00f0ff !important;
        border-bottom: 2px solid #00f0ff !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar: GCP Configuration
# ---------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="badge-tag">HACK2SKILL AI BUILDER CUP 2026</div>', unsafe_allow_html=True)
    st.markdown("### ⚙️ GCP Configuration")
    st.caption("Track: Media, Content & Digital Experiences")

    default_project = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    gcp_project_id = st.text_input(
        "GCP Project ID",
        value=default_project,
        placeholder="e.g. neural-strikers-2026",
        help="Enter your active Google Cloud Project ID with Vertex AI API enabled."
    )

    gcp_region = st.text_input(
        "GCP Region",
        value="us-central1",
        help="Vertex AI region (us-central1 recommended for Gemini 1.5 Pro & Imagen 3)."
    )

    st.markdown("---")
    st.markdown("### 🤖 Vertex AI Models")
    gemini_model_name = st.selectbox(
        "Content Engine",
        ["gemini-1.5-pro", "gemini-1.5-flash"],
        index=0,
        help="Gemini 1.5 Pro powers kit storytelling, lore, and social media generation."
    )

    imagen_model_name = st.selectbox(
        "Visuals Engine",
        ["imagen-3.0-generate-001", "imagen-3.0-fast-generate-001", "imagegeneration@006"],
        index=0,
        help="Imagen 3 generates photorealistic 3D athletic kit mockups."
    )

    st.markdown("---")
    demo_mode = st.toggle(
        "🧪 Demo Simulation Mode",
        value=False if gcp_project_id else True,
        help="Enable this to preview the full app layout and content workflow even before GCP credentials are fully authenticated."
    )

    with st.expander("🔑 GCP Authentication Guide"):
        st.markdown("""
        **1. Authenticate locally with Google Cloud:**
        ```bash
        gcloud auth application-default login
        gcloud config set project YOUR_PROJECT_ID
        ```
        **2. Enable Vertex AI API:**
        ```bash
        gcloud services enable aiplatform.googleapis.com
        ```
        """)

# ---------------------------------------------------------
# Vertex AI Backend Helpers
# ---------------------------------------------------------
def generate_kit_story_and_social(project_id: str, location: str, team_name: str, design_prompt: str, model_name: str):
    """Generates kit reveal narrative, team lore, and social captions using Gemini 1.5 Pro on Vertex AI."""
    import vertexai
    from vertexai.generative_models import GenerativeModel, GenerationConfig

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)

    prompt = f"""
You are the Executive Brand Director & Sports Marketing Lead for the elite sports franchise '{team_name}'.
The team is officially revealing their 2026 championship athletic kit based on this theme:
"{design_prompt}"

Produce a complete, electrifying launch package in clean, engaging Markdown format with the following three distinct sections:

## 1. 📖 Dynamic Kit Reveal Story
Write a cinematic, high-energy press release and narrative unveiling this new jersey. Detail the visual aesthetics, cybernetic and aerodynamic materials, color symbolism, and how wearing this kit strikes fear into opponents.

## 2. 🛡️ Team Backstory & Ethos
Describe the origin story of '{team_name}', their relentless competitive philosophy, battle motto, and the digital/neural spirit that powers their championship pursuit.

## 3. 📱 Ready-to-Use Social Media Captions
Provide three distinct, engagement-optimized social media posts ready for copy-pasting:
- **Instagram / TikTok**: Hook-driven, visual, hype-building, emoji-rich with call-to-action.
- **X (formerly Twitter)**: Fast, punchy announcement celebrating the kit reveal.
- **LinkedIn / Sports Industry**: Thoughtful, visionary post emphasizing innovation, digital athletic design, and creative culture.

MANDATORY HASHTAG REQUIREMENT:
Every single social media post MUST include these mandatory hashtags:
#PromptYourJersey #AIBuilderCup #Hack2Skill #{team_name.replace(' ', '')} #NeuralStrikers
"""

    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            temperature=0.7,
            max_output_tokens=2500,
        )
    )
    return response.text


def generate_kit_image(project_id: str, location: str, team_name: str, design_prompt: str, model_name: str):
    """Generates a high-resolution 3D athletic kit image using Imagen 3 on Vertex AI."""
    import vertexai
    try:
        from vertexai.preview.vision_models import ImageGenerationModel
    except ImportError:
        from vertexai.vision_models import ImageGenerationModel

    vertexai.init(project=project_id, location=location)
    model = ImageGenerationModel.from_pretrained(model_name)

    # Highly structured prompt optimized for Imagen 3 sportswear product renders
    image_prompt = (
        f"A cinematic high-resolution 3D product render of a futuristic sports jersey kit for the team '{team_name}'. "
        f"Theme and style: {design_prompt}. "
        f"Displayed on an athletic invisible mannequin against a dark minimalist studio backdrop. "
        f"Intricate breathable fabric mesh texture, high-tech moisture-wicking material, glowing cybernetic neon trim, "
        f"sharp aerodynamic lines, modern athletic crest on the chest. "
        f"Dramatic dual rim lighting, ultra-sharp 8k studio photography, sportswear design showcase."
    )

    result = model.generate_images(
        prompt=image_prompt,
        number_of_images=1,
        aspect_ratio="1:1",
        safety_filter_level="block_some",
        person_generation="allow_adult"
    )

    first_image = result[0]
    if hasattr(first_image, "_pil_image") and first_image._pil_image is not None:
        return first_image._pil_image
    elif hasattr(first_image, "_image_bytes"):
        return Image.open(io.BytesIO(first_image._image_bytes))
    else:
        # Fallback to saving to a buffer if custom object
        buffer = io.BytesIO()
        first_image.save(buffer)
        buffer.seek(0)
        return Image.open(buffer)


def generate_demo_kit_image(team_name: str, design_prompt: str) -> Image.Image:
    """Generates a stylized placeholder 3D kit graphic when running in Demo Mode."""
    img = Image.new("RGB", (800, 800), color=(11, 15, 25))
    draw = ImageDraw.Draw(img)

    # Background gradient / tech grid
    for y in range(0, 800, 20):
        draw.line([(0, y), (800, y)], fill=(18, 26, 44), width=1)
    for x in range(0, 800, 20):
        draw.line([(x, 0), (x, 800)], fill=(18, 26, 44), width=1)

    # Stylized Jersey Silhouette
    jersey_coords = [
        (260, 200), (350, 160), (450, 160), (540, 200),
        (660, 280), (600, 360), (530, 310), (540, 680),
        (260, 680), (270, 310), (200, 360), (140, 280)
    ]
    draw.polygon(jersey_coords, fill=(15, 23, 42), outline=(0, 240, 255), width=4)

    # Cybernetic accent lines
    draw.line([(320, 220), (400, 660)], fill=(255, 215, 0), width=3)
    draw.line([(480, 220), (400, 660)], fill=(255, 215, 0), width=3)
    draw.line([(280, 380), (520, 380)], fill=(0, 240, 255), width=2)
    draw.line([(280, 500), (520, 500)], fill=(0, 240, 255), width=2)

    # Central Badge
    badge_coords = [(360, 280), (440, 280), (440, 340), (400, 370), (360, 340)]
    draw.polygon(badge_coords, fill=(0, 240, 255), outline=(255, 215, 0), width=3)

    # Text overlay
    draw.text((400, 320), "NS", fill=(10, 15, 30), anchor="mm")
    draw.text((400, 440), team_name.upper(), fill=(255, 255, 255), anchor="mm")
    draw.text((400, 720), "[ DEMO MODE — LIVE IMAGEN 3 CONNECTS VIA GCP ]", fill=(0, 240, 255), anchor="mm")
    draw.text((400, 750), f"Prompt: {design_prompt[:50]}...", fill=(148, 163, 184), anchor="mm")
    return img


def generate_demo_kit_content(team_name: str, design_prompt: str) -> str:
    """Provides high-quality sample storytelling and social copy for Demo Mode."""
    clean_tag = team_name.replace(" ", "")
    return f"""
## 1. 📖 Dynamic Kit Reveal Story
**The Cybernetic Era Commences:** Today, **{team_name}** unveils their 2026 championship battle armor, engineered under the theme *"{design_prompt}"*.

Crafted at the intersection of generative artificial intelligence and high-performance athletic engineering, this kit features ultra-lightweight carbon-poly microfibers woven with conductive electroluminescent threads. Pulsing neon cybernetic accents trace the bio-kinetic pathways of the human body, turning every sprint, cut, and strike into a flash of electric power. The shimmering gold trim serves as an enduring tribute to championship ambition, ensuring the team commands the arena the moment they emerge from the tunnel.

## 2. 🛡️ Team Backstory & Ethos
Founded as an elite collective of digital-age competitors, **{team_name}** was born from a singular vision: to bridge human athleticism with algorithmic precision. 

Their battle philosophy, *"Strike with Intelligence, Prevail through Relentless Will"*, permeates every practice, tactic, and match. {team_name} does not merely react to the tempo of the game—they compute, adapt, and conquer.

## 3. 📱 Ready-to-Use Social Media Captions

### 📸 Instagram / TikTok
⚡ **THE 2026 ARMOR HAS ARRIVED.** ⚡  
Meet the official kit for **{team_name}**. Built with dynamic cybernetic conduits and forged in gold for the new competitive era. 

Drop a 🔥 in the comments if you're ready to see us take the field!  
🔗 Link in bio to customize your gear.  

#PromptYourJersey #AIBuilderCup #Hack2Skill #{clean_tag} #NeuralStrikers

---

### 🐦 X (formerly Twitter)
Engineered for champions. Powered by AI. 🦾⚡  

Introducing the official 2026 kit for **{team_name}**:  
✨ Cybernetic neon patterns  
🏆 24K gold victory accents  
🌪️ Aerodynamic ultra-light weave  

The future belongs to those who strike first.  
#PromptYourJersey #AIBuilderCup #Hack2Skill #{clean_tag} #NeuralStrikers

---

### 💼 LinkedIn / Digital Media Hub
We are proud to unveil the 2026 official kit and digital brand identity for **{team_name}**, created for the **Hack2skill AI Builder Cup 2026** (Media, Content & Digital Experiences Track).

Using Google Cloud Vertex AI (Gemini 1.5 Pro and Imagen 3), we synthesized high-fashion sportswear design with computational brand lore in seconds. This marks a new milestone in how sports franchises will ideate, prototype, and market merchandise.

#PromptYourJersey #AIBuilderCup #Hack2Skill #{clean_tag} #NeuralStrikers #VertexAI #GenerativeAI
"""

# ---------------------------------------------------------
# Main Application Header
# ---------------------------------------------------------
st.markdown('<div class="badge-tag">⚡ HACK2SKILL AI BUILDER CUP 2026 • MEDIA & DIGITAL EXPERIENCES</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Neural Strikers — AI Kit & Content Hub</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Generate Photorealistic 3D Athletic Kits with Imagen 3 & Campaign Lore with Gemini 1.5 Pro</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Input Section
# ---------------------------------------------------------
with st.container():
    st.markdown('<div class="cyber-card cyber-card-cyan">', unsafe_allow_html=True)
    st.markdown("#### 🎨 Design Your Team's Next-Gen Kit")
    
    col_input_1, col_input_2 = st.columns([1, 2])
    
    with col_input_1:
        team_name = st.text_input(
            "Team Name",
            value="Neural Strikers",
            placeholder="e.g. Neural Strikers, Cyber Vipers, Quantum FC",
            help="The official franchise or team name displayed on the kit and in media releases."
        )
        kit_type = st.selectbox(
            "Kit Type",
            ["Home Championship Kit", "Away Stealth Kit", "Third Cybernetic Edition", "Goalkeeper Special Edition"],
            index=0
        )

    with col_input_2:
        design_prompt = st.text_area(
            "Design Theme / Prompt",
            value="Neon cybernetic patterns with gold accents",
            height=110,
            placeholder="Describe colors, motifs, textures, lighting, and aerodynamic style...",
            help="Describe the visual aesthetic, patterns, and spirit of your sports jersey."
        )

    generate_btn = st.button("🚀 Generate Kit & Media", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Generation Execution & State Management
# ---------------------------------------------------------
if "generated_data" not in st.session_state:
    st.session_state.generated_data = None

if generate_btn:
    if not team_name.strip():
        st.error("Please enter a valid Team Name.")
    elif not design_prompt.strip():
        st.error("Please provide a Design Theme / Prompt.")
    else:
        # Check GCP configuration if not in demo mode
        if not demo_mode and not gcp_project_id.strip():
            st.error("⚠️ GCP Project ID is required for Vertex AI. Enter your Project ID in the sidebar or switch on 'Demo Simulation Mode'.")
        else:
            with st.spinner("⚡ Synthesizing 3D Athletic Kit with Imagen 3 & crafting campaign lore with Gemini 1.5 Pro..."):
                start_time = time.time()
                generated_image = None
                generated_content = ""
                error_occurred = False

                if demo_mode:
                    time.sleep(1.2)  # Realistic simulation feel
                    generated_image = generate_demo_kit_image(team_name, design_prompt)
                    generated_content = generate_demo_kit_content(team_name, design_prompt)
                else:
                    # Live Vertex AI Execution
                    try:
                        # 1. Generate text story and social copy via Gemini 1.5 Pro
                        generated_content = generate_kit_story_and_social(
                            project_id=gcp_project_id.strip(),
                            location=gcp_region.strip(),
                            team_name=team_name.strip(),
                            design_prompt=f"{kit_type}: {design_prompt.strip()}",
                            model_name=gemini_model_name
                        )
                    except Exception as e:
                        st.error(f"❌ Error during Gemini 1.5 Pro generation: {str(e)}")
                        error_occurred = True

                    try:
                        # 2. Generate 3D Kit Image via Imagen 3
                        full_img_prompt = f"{kit_type} with {design_prompt.strip()}"
                        generated_image = generate_kit_image(
                            project_id=gcp_project_id.strip(),
                            location=gcp_region.strip(),
                            team_name=team_name.strip(),
                            design_prompt=full_img_prompt,
                            model_name=imagen_model_name
                        )
                    except Exception as e:
                        st.error(f"❌ Error during Imagen 3 image generation: {str(e)}")
                        st.info("Tip: Ensure Vertex AI API is enabled and your GCP credentials have `Vertex AI User` permissions. You can also test with 'Demo Simulation Mode' in the sidebar.")
                        error_occurred = True

                duration = time.time() - start_time
                if not error_occurred or generated_image or generated_content:
                    st.session_state.generated_data = {
                        "team_name": team_name,
                        "kit_type": kit_type,
                        "design_prompt": design_prompt,
                        "image": generated_image,
                        "content": generated_content,
                        "is_demo": demo_mode,
                        "duration": round(duration, 2)
                    }
                    st.success(f"✨ Kit & Media successfully generated in {round(duration, 2)}s!")

# ---------------------------------------------------------
# Side-by-Side Results Display
# ---------------------------------------------------------
if st.session_state.generated_data:
    data = st.session_state.generated_data

    st.markdown("---")
    st.markdown(f"### 🏆 Official Kit Reveal: **{data['team_name']}** ({data['kit_type']})")

    col_image, col_content = st.columns([1, 1], gap="large")

    # LEFT COLUMN: 3D Athletic Kit Reveal (Imagen 3)
    with col_image:
        st.markdown('<div class="cyber-card cyber-card-cyan">', unsafe_allow_html=True)
        st.markdown("#### 🎽 3D Athletic Kit Render")
        st.caption("Generated with Vertex AI **Imagen 3** (High-Resolution Studio Render)")

        if data["image"] is not None:
            st.image(data["image"], use_container_width=True, caption=f"{data['team_name']} — {data['kit_type']}")

            # Image download button
            buf = io.BytesIO()
            data["image"].save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="📥 Download High-Res Kit (PNG)",
                data=byte_im,
                file_name=f"{data['team_name'].lower().replace(' ', '_')}_kit_render.png",
                mime="image/png",
                use_container_width=True
            )
        else:
            st.warning("Kit image could not be loaded. Please re-run generation.")

        st.markdown("""
        **Specifications:**
        - **Engine:** Google Vertex AI Imagen 3 (`imagen-3.0-generate-001`)
        - **Render Mode:** 3D Athletic Studio Lighting (1:1 Aspect Ratio)
        - **Theme Vector:** Neon cybernetic accents, aerodynamic fabric weave
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # RIGHT COLUMN: Content Hub & Social Media (Gemini 1.5 Pro)
    with col_content:
        st.markdown('<div class="cyber-card cyber-card-gold">', unsafe_allow_html=True)
        st.markdown("#### 📣 Launch & Social Media Studio")
        st.caption("Generated with Vertex AI **Gemini 1.5 Pro**")

        tab_full, tab_social, tab_prompt = st.tabs(["🚀 Complete Media Kit", "📱 Social Media Captions", "⚡ Prompt Inspector"])

        with tab_full:
            st.markdown(data["content"])

        with tab_social:
            st.markdown("##### Ready-to-Post Campaign Copy")
            st.info("💡 Official Campaign Hashtags are automatically included: `#PromptYourJersey` `#AIBuilderCup` `#Hack2Skill`")
            
            # Extract or display social section directly
            st.markdown("""
            Copy and publish directly to amplify the kit reveal:
            """)
            st.code(
f"""⚡ THE NEW ARMOR HAS ARRIVED: {data['team_name'].upper()} 2026!
Engineered with {data['design_prompt']}.

#PromptYourJersey #AIBuilderCup #Hack2Skill #{data['team_name'].replace(' ', '')} #NeuralStrikers""",
                language="text"
            )

        with tab_prompt:
            st.markdown("##### Prompt Engineering Diagnostics")
            st.markdown(f"**Team Name:** `{data['team_name']}`")
            st.markdown(f"**Kit Variant:** `{data['kit_type']}`")
            st.markdown(f"**Design Prompt:** `{data['design_prompt']}`")
            st.markdown(f"**Execution Mode:** `{'Demo Simulation' if data['is_demo'] else 'Live Vertex AI'}`")
            st.markdown(f"**Generation Latency:** `{data['duration']} seconds`")

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 1rem 0;">'
    '⚡ Built for <strong>Hack2skill AI Builder Cup 2026</strong> | Track: <em>Media, Content & Digital Experiences</em><br>'
    'Powered by <strong>Google Cloud Vertex AI</strong> (Gemini 1.5 Pro & Imagen 3) + <strong>Streamlit</strong>'
    '</div>',
    unsafe_allow_html=True
)
