"""Scene-pack resources for the Editing Resources forum thread."""

META = {
    "brand": "Video Editing Hub",
    "default_accent": "#E37D22",
}

META["navigation"] = [('Practice editing', 'practice-footage'), ('VFX and color practice', 'vfx-color-practice'), ('Stock footage / B-roll', 'stock-footage'), ('Anime', 'anime'), ('Film and TV', 'film-tv'), ('Automotive', 'automotive'), ('Sports', 'sports'), ('General resources', '@general')]

MESSAGES = [
    ("01", "index", None, "# Scene packs and clip sources", "Scene Packs", """\
Choose raw practice footage to build an edit from scratch, or browse scene packs and visual references by footage type. Some packs already have slow motion, interpolation, or color applied. Check the terms and rights for each clip before using it in a published project.

"""),
    ("03", "anime", None, "# Anime", "Scene Packs", """\
- **[AnimeClips](https://animeclips.online/)** — Anime clips with original-frame-rate MP4 and processed Twixtor options; choose the version that suits your edit.
- **[RingWitDaHoodie Twixtor](https://www.youtube.com/channel/UC8_TCk7q8Tuy5LNWwgtiI6g)** — Processed anime clips and Twixtor edits.
- **[RingWitDaClips](https://ringwitdaclips.com/)** — Anime clips, including no-subtitle and interpolated variants."""),
    ("04", "film-tv", None, "# Film and TV", "Scene Packs", """\
- **[Ronin](https://www.youtube.com/@roninfx7)** — A YouTube source for film and TV clips.
- **[RoninFX Twixtors](https://www.roninfxtwixtors.com/)** — Scene collections with 24 fps and processed 60 fps variants, plus car and sports clips.
- **[Clips & Talks](https://www.youtube.com/@clipsandtalks)** — Scene packs, including some with color grading already applied."""),
    ("05", "automotive", None, "# Automotive", "Scene Packs", """\
- **[The Pro Video](https://www.youtube.com/@theprovideo)** — Finished cinematic automotive films for inspiration and studying pacing, framing, and sound. This is not a raw-footage pack directory."""),
    ("06", "sports", None, "# Sports", "Scene Packs", """\
- **[ItzK4RAX](https://www.youtube.com/@KaraxAep)** — Football scene packs and finished sports edits; some clips already include color or enhancement processing."""),
    ("07", "practice-footage", None, "# Practice Editing", "Scene Packs · Practice Footage", """**Want footage you can actually build a scene from?**

- **[CineStudy: EDIT THIS exercises](https://cinestudy.org/)** — Editing exercises with source footage. Pick a project, read its brief, and try your own cut.
- **[CineStudy raw-footage archive](https://cinestudy.org/tag/free-raw-footage/)** — Browse more practice material.
- **[EditStock](https://editstock.com/)** — **Paid** film footage for practicing storytelling and cutting scenes from multiple takes. Choose a project suited to your skill level.

Try making two versions of the same scene with different pacing or story emphasis. Follow the project’s instructions and terms when sharing your result."""),
    ("08", "vfx-color-practice", None, "# VFX & Color Practice", "Scene Packs · VFX & Color", """**Practice a specific post-production skill**

- **[ActionVFX practice footage](https://www.actionvfx.com/practicefootage)** — **Free** footage for practicing visual effects, compositing, and tracking.
- **[Blackmagic camera originals](https://www.blackmagicdesign.com/nl/products/blackmagiccinemacamera/gallery)** — Download original camera files to practice color correction and grading. Choose the camera-original download rather than the graded preview.

Try matching two shots, separating a subject from its background, or adding an effect that follows the camera movement. Camera-original files can be large; start with one clip."""),
    ("09", "stock-footage", None, "# Stock Footage / B-roll", "Scene Packs · Stock Footage", """**Need extra shots for a montage, a story, or a practice project?**

- **[Pexels videos](https://www.pexels.com/videos/)** — **Free** stock footage for B-roll, travel edits, and montages. See the **[Pexels license](https://www.pexels.com/license/)** for usage terms.
- **[Mixkit stock footage](https://mixkit.co/free-stock-video/)** — **Free downloads** across a range of subjects and styles. Check each clip’s license: the **Free License** allows commercial projects, while the **Restricted License** covers non-commercial use.

Look for shots that belong together: similar lighting, movement, and framing can make footage from different sources feel like one sequence."""),
]
