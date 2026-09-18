"""Shared assets and audio resources, independent of an editing application."""

META = {
    "brand": "Video Editing Hub",
    "default_accent": "#E8C84A",
    "navigation": [("Assets and downloads", "assets"), ("Audio tools", "audio-tools"), ("File preparation", "file-preparation"), ("Scene packs", "@scene-packs"), ("DaVinci Resolve", "@resolve"), ("Premiere Pro", "@premiere"), ("After Effects", "@after-effects")],
}

MESSAGES = [
    ("01", "index", None, "# General Resources", "General Resources", """Shared assets, audio tools, and file-preparation help for your editing projects. Start with what your project needs, then check the download format, supported software, and terms for the specific item.

For application-specific tutorials, templates, and workflows, use the DaVinci Resolve, Premiere Pro, or After Effects guides."""),
    ("02", "assets", None, "# Assets and Downloads", "General Resources · Assets", """Browse these collections for reusable project ingredients, from overlays and graphics to sound and production resources. Availability and terms vary by item.

- **[CinePacks free packs](https://cinepacks.store/collections/free-packs)** — Free. A collection of no-cost packs; check each pack's included files before downloading.
- **[Shutterstock/PremiumBeat video assets](https://www.shutterstock.com/blog/premiumbeat-free-week-200-free-video-assets)** — An older roundup of video assets from PremiumBeat; some installation instructions use older software interfaces.
- **[Envato free files](https://elements.envato.com/free-files)** — **Free** rotating files with an account; check the license supplied with each file.
- **[No Film School post-production assets](https://nofilmschool.com/free-film-assets)** — A 2024 roundup of post-production resources; availability depends on the linked publisher."""),
    ("03", "audio-tools", None, "# Audio Tools", "General Resources · Audio", """These publishers make audio effects, processing, or sound-design tools. Check each product's current host support and license before adding it to a project.

**Mixing, cleanup, and levels**
- **[End Boost](https://alexaudiobutler.com/)** — Paid standalone automatic mixing, the successor to Alex Audio Butler. Uses a WAV export workflow rather than the discontinued plug-in.
- **[Youlean Loudness Meter](https://youlean.co/youlean-loudness-meter/)** — Measure loudness and true peaks with the free edition; extra features require Pro. It measures levels rather than fixing them automatically.
- **[Auburn Sounds](https://www.auburnsounds.com/index.html)** — Audio effects including dynamics, voice, and spatial tools.
- **[iZotope](https://www.izotope.com/)** — Audio repair, mixing, and effects products.
- **[TBProAudio](https://www.tbproaudio.de/)** — EQ, metering, and dynamics tools.
- **[Waves](https://www.waves.com/)** — Audio effects, processing, and cleanup product catalog.
[[SEP]]
**Sound design and music**
- **[Soundly Shape It and Place It](https://getsoundly.com/tools/)** — Free EQ and speaker/environment simulation tools for shaping a sound or making it fit a scene.
- **[Valhalla DSP](https://valhalladsp.com/plugins/)** — Reverb and audio-effects plug-ins.
- **[Igorski.nl downloads](https://www.igorski.nl/download)** — Music-focused effects and plug-ins.
- **[Native Instruments](https://www.native-instruments.com/en/)** — Music-production instruments and effects.
- **[ViatorDSP](https://www.patreon.com/ViatorDSP/posts)** — Creator posts for lo-fi and EQ plug-ins; access varies by post.
[[SEP]]
**Specialist directories**
- **[GPU Audio](https://www.gpu.audio/)** — Explore GPU-audio projects; check which products are available for your system.
- **[Arch Linux VST packages](https://archlinux.org/groups/x86_64/vst-plugins/)** — An advanced Linux package index, not a Windows/macOS plug-in bundle."""),
    ("04", "file-preparation", None, "# File Preparation & Troubleshooting", "General Resources · File Preparation", """**A clip won’t import, plays badly, or exports strangely?** Start by checking what is inside the file.

- **[MediaInfo](https://mediaarea.net/en/MediaInfo)** — Inspect the video codec, frame rate, bit depth, and audio details. Useful information to include when asking for editing help.
- **[Shutter Encoder](https://www.shutterencoder.com/)** — Free media conversion and preparation tools, including editing codecs, rewrapping, and subtitle tasks. Rewrap when you only need a different container; transcode when the codec needs to change.

Keep your original footage and test a short sample before converting a whole project."""),
]
