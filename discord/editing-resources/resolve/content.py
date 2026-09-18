"""DaVinci Resolve resources for the Editing Resources V2 forum thread."""

META = {"brand": "Video Editing Hub", "default_accent": "#1F8B4C"}

# num, slug, accent (or None), title, footer label, body, optional URL button
META["navigation"] = [('Learn a skill', 'learn-by-task'), ('Creator tutorials', 'creator-tutorials'), ('Assets and tools', 'assets-tools'), ('Video tools', 'video-tools'), ('Workflow tools', 'workflow-tools'), ('Delivery tools', 'delivery-tools'), ('General resources', '@general')]

MESSAGES = [
    ("01", "start-here", None, "# DaVinci Resolve Resources", "DaVinci Resolve · Start Here", """\
Start with the official course, then choose the part of Resolve you need for the project in front of you. You do not need every tool listed below to make an edit.

[[SEP]]
**New to Resolve?** Open the **[official training page](https://www.blackmagicdesign.com/products/davinciresolve/training)** and choose the beginner guide with its lesson files. Work through a real project, then explore the Edit, Color, Fairlight, and Fusion training for your next skill.

Use the official material to learn the page you are working in; use the directories below when you want another explanation or a specific tool."""),
    ("02", "learn-by-task", None, "# Learn a Skill", "DaVinci Resolve · Learn by Task", """\
**Start with the current training catalog**

- **[Official Resolve training](https://www.blackmagicdesign.com/products/davinciresolve/training)** — Follow the Edit lessons for a project-based route through a rough cut, trims, effects, and delivery.

**Older fundamentals:** The videos below were recorded in Resolve 17. Editing concepts still help, but menus and controls may differ.

- **[Editing lesson](https://youtu.be/fYlwId_z_yU?si=uYIJ4tZqaZrZ5NCZ)** — Blackmagic Design's *DaVinci Resolve 17 Edit Training: Introduction to Editing Part 1*.
[[SEP]]
**Color and look development**

- **[Color grading lesson](https://youtu.be/OrEcXbET1Y4?si=c_2nRVx3L_xRtwNV)** — Blackmagic Design's *DaVinci Resolve 17 Color Training: Introduction to Color*.
- **[Mixing Light](https://mixinglight.com/)** — Color-grading articles and training; check the site for current access options.
[[SEP]]
**Motion graphics and VFX**

- **[Fusion lesson](https://youtu.be/mJf1-Ilgis8?si=FXxewUtiQm_rXZpG)** — Blackmagic Design's *DaVinci Resolve 17 Fusion Training: Introduction to Fusion*.
- **[Blackmagic Fusion Tutorials](https://www.youtube.com/c/BlackmagicFusionTutorials/)** — An archive of Fusion 8/9 tutorials; expect an older interface.
[[SEP]]
**Dialogue, sound, and mix**

- **[Fairlight lesson](https://youtu.be/5lceOriiwu8?si=aQf_53SoJcd0TJJp)** — Blackmagic Design's *DaVinci Resolve 17 Fairlight Training: Introduction to Audio*."""),
    ("03", "creator-tutorials", None, "# More Creator Tutorials", "DaVinci Resolve · Creator Tutorials", """\
Browse a channel, then search within it for the task and Resolve version you need. Individual uploads and current focus change over time.

**Color and Fusion**

- **[Learn Color Grading](https://www.youtube.com/c/LearnColorGrading/)** — Tutorials focused on color grading.
- **[Blackmagic Fusion Tutorials](https://www.youtube.com/c/BlackmagicFusionTutorials/)** — Older Fusion 8/9 tutorials.
[[SEP]]
**More creator tutorials**

- **[JayAreTV](https://www.youtube.com/c/JayAreTV/)**
- **[Casey Faris](https://www.youtube.com/user/CaseyFaris777/)**
- **[Patrick Stirling](https://www.youtube.com/c/PatrickStirling/)**
- **[Jamie Fenn](https://www.youtube.com/c/JamieFenn/)**
- **[MrAlexTech](https://www.youtube.com/c/MrAlexTech/)**
- **[VFXstudy](https://www.youtube.com/c/VFXstudy/)**
- **[Darren Mostyn](https://www.youtube.com/c/DarrenMostyn/)**
- **[Jay Lippman](https://www.youtube.com/c/JayLippman/)**
- **[Jason Yadlovski](https://www.youtube.com/c/JasonYadlovski/)**
- **[Creative Video Tips](https://www.youtube.com/c/CreativeVideoTips/)**
- **[Lazy Artist](https://www.youtube.com/c/VideoArtGR/)**
- **[Molin Guides](https://www.youtube.com/c/MolinGuides/)**
- **[Lowepost](https://www.youtube.com/channel/UC-NcqjEMr_ybHfK0pKN9m0g/)**
- **[Branden Arc](https://www.youtube.com/c/BrandenArc/)**
[[SEP]]
**Older tutorial archives**
Useful for techniques and fundamentals; follow current documentation when controls differ.

- **[Billy Rybka](https://www.youtube.com/c/BillyRybka/)**
- **[Core and Blue](https://www.youtube.com/c/CoreandBlue/)**
- **[Nathan Carter](https://www.youtube.com/c/NathanCarterVids/)**
- **[MiesnerMedia](https://www.youtube.com/c/Miesnermedia/)**
- **[The Modern Filmmaker](https://www.youtube.com/c/TheModernFilmmaker/)**
- **[Darren Frenette](https://www.youtube.com/channel/UCOwXdxE3HLAJVM4WG48_7OQ/)**
- **[Aram K](https://www.youtube.com/c/AramK/)**"""),
    ("04", "assets-tools", None, "# Assets & Community Tools", "DaVinci Resolve · Assets & Tools", """\
- **[MotionVFX free Resolve items](https://www.motionvfx.com/store/davinci-resolve?free=true)** — Free. Filtered MotionVFX catalog for its no-cost DaVinci Resolve items.
- **[Reactor](https://www.steakunderwater.com/wesuckless/viewtopic.php?f=32&t=3067)** — Free. Community package manager for finding Fusion tools and macros.
- **[Motion Array free Resolve templates](https://motionarray.com/davinci-resolve-templates/free/)** — Free. Motion Array's free collection for DaVinci Resolve templates.
- **[MrAlexTech free stuff](https://www.mralextech.net/free-stuff)** — Creator's directory of free resources.
- **[Baldavenger](https://github.com/baldavenger/)** — Source repositories for community Resolve and color tools.
[[SEP]]
Read the publisher's install notes, supported Resolve version, and license for the exact item. A template or plugin listing is not a promise that it fits every system or project."""),
    ("05", "video-tools", None, "# Video, Color & Effects Tools", "DaVinci Resolve · Video Tools", """\
These optional tools cover image, color, restoration, titles, and effects. Check the exact product’s Resolve version, operating system, and Free/Studio requirements: a publisher’s full catalog may not support Resolve.

- **[Boris FX](https://borisfx.com/)** — Browse its visual-effects and plug-in catalog.
- **[CineMatch](https://www.cinematch.com/)** — A camera-matching product now presented through FilmConvert.
- **[Colourlab for Resolve](https://colourlab.ai/colourlab-ai-for-davinci-resolve/)** — Tools for color correction, grading, and look creation.
- **[Dehancer](https://www.dehancer.com/)** — Film-emulation tools for color work.
- **[Digital Anarchy Beauty Box for Resolve](https://digitalanarchy.com/downloads/davinci-resolve-ofx-beauty-box-video/)** — Skin-retouching effects. For flicker removal, see **[Flicker Free for Resolve](https://digitalanarchy.com/downloads/davinci-resolve-ofx-flicker-free/)**.
- **[FilmConvert](https://www.filmconvert.com/)** — Film-look and grain products.
- **[Filmworkz OFX](https://filmworkz.com/ofx/)** — Post-production restoration and finishing tools.
- **[Livegrain](https://www.livegrain.com/)** — Film-grain plug-in tools.
- **[Maxon Red Giant compatibility](https://support.maxon.net/hc/en-us/articles/23987275556764-Red-Giant-Compatibility)** — Check Resolve support for the specific effect before buying.
- **[Neat Video](https://www.neatvideo.com/)** — Video noise-reduction tools.
- **[NewBlue](https://newbluefx.com/)** — Titling and visual-effects tools.
- **[PixelTools](https://pixeltoolspost.com/)** — DCTL tools and PowerGrade presets.
- **[RevisionFX for Resolve](https://revisionfx.com/products/for/resolve/)** — Resolve-specific effects product page.
- **[Textuler](https://textuler.io/features)** — Text and chat-bubble creation tools.
- **[VideoVillage](https://videovillage.co/)** — Grain, diffusion, and LUT-building tools."""),
    ("06", "workflow-tools", None, "# Workflow & Integration Tools", "DaVinci Resolve · Workflow Tools", """\
**Work together**

- **[Blackmagic Cloud collaboration](https://www.blackmagicdesign.com/products/davinciresolve/collaboration)** — Learn about shared projects, proxy workflows, and Presentations for review. Cloud services have their own plans and requirements.

**Transcription**

- **[Simon Says Resolve extension](https://www.simonsays.ai/blackmagic-davinci-resolve-extension)** — Bring Simon Says transcript work into Resolve.
- **[StoryToolkitAI](https://github.com/octimot/StoryToolkitAI)** — Transcript and translation tools. Its Resolve API integration requires Studio 18 or later; standalone transcript work is separate. Read the **[installation guide](https://github.com/octimot/StoryToolkitAI/blob/main/INSTALLATION.md)**.
[[SEP]]
**Older integration announcements**
These describe historical workflows, not current compatibility guarantees. Check current publisher support before planning a team setup.

- **[EditShare Flow Panel](https://editshare.com/editshares-flow-panel-for-davinci-resolve-studio-creates-gateway-to-wider-media-ecosystem-and-remote-proxy-editing/)** — An integration announcement covering media management and proxy editing.
- **[Primestream Xchange](https://primestream.com/news/press-release/xchange-mam-pam-and-davinci-resolve-17-now-integrated/)** — An integration announcement for media management in Resolve 17.
- **[ShareBrowser](https://www.studionetworksolutions.com/sns-unveils-sharebrowser-workflow-integration-plugin-for-davinci-resolve/)** — An integration announcement for collaborative media management."""),
    ("08", "delivery-tools", None, "# Delivery & Encoding Tools", "DaVinci Resolve · Delivery Tools", """\
- **[MainConcept Blackmagic plug-ins](https://www.mainconcept.com/blackmagic-plugins)** — Delivery and codec plug-ins for Blackmagic workflows.
- **[Voukoder Pro](https://www.voukoder.org/documentation/)** — Optional paid export and encoding tool. Its Resolve integration requires **DaVinci Resolve Studio**; the older Voukoder Classic is discontinued."""),
]
