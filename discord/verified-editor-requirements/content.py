"""Content for the Verified Editor Application Requirements forum post.

    python3 ../_engine/build.py .        # regenerate this folder's NN-*.json

This is a pinned forum thread, not a plain channel message: META sets "thread_id"
so the engine PATCHes that thread's starter message (see ../_engine/README.md).
The webhook must be created on the forum channel that contains this thread.

"Want to become a Verified Editor?" is the thread's own title (forum thread names
are separate metadata a webhook can't edit), so it isn't repeated in the body.
"""

APPLY_HERE = "<#1278851988334972949>"                     # 📛│apply-here
APPLY_HERE_URL = "https://discord.com/channels/732343015711965204/1278851988334972949"

META = {
    "brand": "Video Editing Hub",
    "default_accent": "#E37D22",
    "thread_id": "1529525410935607307",
}

# num, slug, accent hex (or None -> default_accent), title, footer label, body, button
MESSAGES = [
    ("01", "requirements", "#E37D22", "# Verified Editor Application Requirements", "Verified Editor Requirements", f"""\
To apply for the Verified Editor role, make sure you meet the following requirements.

- **Server Activity:** You must have been a member for at least 2 months. Run `/cooldown` to learn more.

- **Work Examples:** Provide at least 3 examples of published client work, including screenshots of positive client feedback.

- **Quality:** Submit high-quality videos (1080p or higher). No drafts, only published work is accepted.

- **Versatility:** Show a range of editing skills across different genres (gaming, vlogs, motion graphics, etc.).

- **Payment Methods:** Provide proof you use reliable payment methods (no crypto or Bitcoin).

- **Service Description:** Describe the services you offer, including specialties, turnaround time, and pricing structure.

- **Portfolio & Contact:** Submit a professional portfolio or website. Provide an email or another contact method besides Discord DMs, plus any professional social media profiles.

- **Professionalism:** No active warnings on the server. Professional behavior and following the server rules are required.

- **Client Testimonials:** Provide at least 3 verifiable client testimonials.

- **No Cloud Links:** Don't submit Google Drive, OneDrive, or other cloud storage links. Only direct portfolio or website links are accepted.

- **Review Time:** Allow at least 1 week for the review process.

- **Reapplication:** If denied, you can reapply after 2 months. Run `/cooldown` to learn more.
[[SEP]]
**Application Process:** Go to {APPLY_HERE}, select Verified Editor Application, and submit the required materials.

**Reminder:** Incomplete applications will be rejected. Make sure all materials are up to date and professional.""",
     ("Apply Here", APPLY_HERE_URL)),
]
