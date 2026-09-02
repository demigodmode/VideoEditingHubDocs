"""Content for the server Rules channel. Edit here; publish with the engine.

    python3 ../_engine/build.py .        # regenerate this folder's NN-*.json

6 containers: sections are merged in pairs (all rule numbers unchanged). The glossary
uses [[JUMP:slug]] tokens that the engine resolves to jump links at publish time, so it
posts last. @mention is the VEH bot (DM it to open a native-modmail ticket); channel
link is post-free-ad. Each rule is a > blockquote for readability.
"""

MODMAIL = "<@1255909585785720882>"      # VEH bot — DM to open a ticket (native modmail)
FREE_AD = "<#1138844785558433802>"      # 🆓│post-free-ad

META = {
    "brand": "Video Editing Hub",
    "default_accent": "#5865F2",
}

# num, slug, accent hex (or None -> default_accent), title, footer label, body
MESSAGES = [
    ("01", "conduct-communication", "#5865F2", "# 1. General Conduct", "General Conduct & Language", f"""\
> **1.1 Respectful behavior.** Treat every member with respect. Harassment, bullying, or discrimination of any kind isn't tolerated.

> **1.2 No scamming.** Don't scam anyone out of their work or commissions. Scammers are banned and added to the scammer list. (Instant ban, see 8.5.)

> **1.3 No exploits.** Don't use or promote glitches, hacks, or bugs.

> **1.4 Follow Discord's TOS.** Everyone must comply with Discord's Terms of Service, including the 13+ minimum age.

> **1.5 Be respectful to staff.** Don't argue with staff. If you feel you were treated unfairly or need clarification on a mod action, DM {MODMAIL} to open a ticket and a different staff member will look into it.

> **1.6 No impersonation.** Don't impersonate staff or other members, whether through your name, avatar, or claiming to be someone you're not.
[[SEP]]
# 2. Language & Communication

> **2.1 Respectful communication.** Hate speech is banned: slurs, insults, or imagery that targets or demeans someone based on race, ethnicity, nationality, religion, sex, gender identity or expression, sexual orientation, disability, or any other protected characteristic. This applies in every channel, and to every part of your presence here: your username, nickname, avatar, banner, bio, status, and any media you share. (Slurs are an instant ban, see 8.1 and 8.2.)

> **2.2 Swearing.** Allowed, as long as it isn't aimed at someone as an insult.

> **2.3 No inflammatory topics.** No debates about racism, sexuality, religion, politics, and the like.

> **2.4 English only.** For moderation, keep it to English. Non-English messages will be removed."""),

    ("02", "posting-content", "#5865F2", "# 3. Spamming & Advertising", "Posting & Content", f"""\
> **3.1 No spamming.** No flooding chat with messages, GIFs, or emojis.

> **3.2 No excessive pinging.** Don't spam pings. (Mass-pinging `@everyone` or `@here` is an instant ban, see 8.3.)

> **3.3 No DM advertising.** Don't advertise in members' DMs. (Instant ban, see 8.7.)

> **3.4 No unapproved links.** No referral links or Discord server invites.

> **3.5 No selling.** No selling accounts, courses, photos, followers, presets, and the like. This includes giving away your own free assets.

> **3.6 No agency posts.** No agency advertisements. (See 8.8 on middle-manning.)
[[SEP]]
# 4. Content Restrictions

> **4.1 No adult content.** Don't share 18+ material.

> **4.2 No pirated or cracked software.** No sharing or discussing pirated or cracked software. (Instant ban, see 8.6.)

> **4.3 No copyright violations.** Don't stream copyrighted music, movies, or TV without permission. (Applies in voice too, see 6.4.)

> **4.4 Keep your profile SFW.** Your avatar, banner, and profile must be safe for work."""),

    ("03", "channels-voice", "#5865F2", "# 5. Channel Usage", "Channels & Voice", f"""\
> **5.1 Stay on topic.** Keep messages in the right channel. Repeated misposting after a warning can lead to a mute or ban.

> **5.2 No competition posts.** Only with prior approval from the owner.

> **5.3 Editors in the free-ad channel.** Editors shouldn't ask for payment from clients who posted in {FREE_AD}.

> **5.4 Post duration.** Client posts older than 7 days are locked, closed, and may be deleted.
[[SEP]]
# 6. Voice Chat

> **6.1 No channel surfing.** Don't hop between channels repeatedly.

> **6.2 Keep noise appropriate.** No annoying, loud, or high-pitched noises.

> **6.3 Minimize background noise.** Use push-to-talk if you need to.

> **6.4 No streaming copyrighted material.** No music, movies, or TV without permission (same as 4.3, for voice)."""),

    ("04", "reporting-moderation", "#5865F2", "# 7. Reporting & Moderation", "Reporting & Moderation", f"""\
> **7.1 Report properly.** Don't call people out in chat. DM {MODMAIL} to open a ticket and report them.

> **7.2 No unofficial bots.** Don't invite unofficial bots.

> **7.3 Warnings and infractions.** After two warnings, any further infraction is a ban.

> **7.4 How enforcement works.** Most rules (sections 1 to 7) follow the two-warning system in 7.3. The offenses in section 8 skip warnings and are immediate bans. Staff have the final say, and these rules can change over time."""),

    ("05", "instant-bans", "#E74C3C", "# 8. Instant-Ban Offenses", "Instant-Ban Offenses", """\
These skip warnings and go straight to a ban.

> **8.1 Racial slurs.** Any derogatory term aimed at someone's race or ethnicity. No context or excuse applies.

> **8.2 Transphobic / homophobic slurs.** Targeting someone's gender identity or sexual orientation with slurs, even as a joke.

> **8.3 Tagging `@everyone` or `@here`.** Mass tagging disrupts the server and spams members.

> **8.4 Spamming ads / repeated misposting after warnings.** Posting ads or irrelevant links, or misusing channels after being told to stop, whether intentional or careless. (Escalation of 3.1, 3.4, and 5.1.)

> **8.5 Scamming.** Any attempt to defraud, steal from, trick, or misrepresent services to members. Includes phishing, fake giveaways, and financial scams.

> **8.6 Cracked software (incl. watermark-removal questions).** Sharing or discussing pirated software or cracked plugins, or asking how to remove watermarks.

> **8.7 DM advertising.** Unsolicited promo in DMs counts as harassment and spam. Banned without warning.

> **8.8 Outsourcing / outreaching / middle-manning.** Hiring another editor to do your work, finding clients or editors on someone else's behalf, or acting as a go-between.

> **8.9 Scam links (drop-ship, gift cards, etc.).** Any suspicious link, such as drop-ship scams, fake gift-card sites, or malware URLs, even if shared unintentionally.

> **8.10 Discrimination.** No excluding or blocking a member over religion or ethnicity. The only valid reasons to decline a request are region restrictions or language limits.

> **8.11 Compromised accounts.** Any account we reasonably suspect is hacked, such as one posting scam links, phishing, or acting out of character, gets an instant ban. Appeals are considered only after the account is secured and ownership verified.

> **8.12 Ban evasion.** Rejoining on an alt to dodge a mute or ban.

> **8.13 Doxxing.** Sharing someone's private or personal information without their consent.

> **8.14 Threats & harm.** Credible threats of violence, or encouraging self-harm or suicide."""),

    ("06", "glossary", "#5865F2", "# Rules Glossary", "Rules Glossary", """\
Jump to a section:

- [1. General Conduct]([[JUMP:conduct-communication]])
- [2. Language & Communication]([[JUMP:conduct-communication]])
- [3. Spamming & Advertising]([[JUMP:posting-content]])
- [4. Content Restrictions]([[JUMP:posting-content]])
- [5. Channel Usage]([[JUMP:channels-voice]])
- [6. Voice Chat]([[JUMP:channels-voice]])
- [7. Reporting & Moderation]([[JUMP:reporting-moderation]])
- [8. Instant-Ban Offenses]([[JUMP:instant-bans]])"""),
]
