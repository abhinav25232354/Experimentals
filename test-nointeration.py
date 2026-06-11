import os
import re

folder = "C:/Users/Abhin/Music/Emmersive Collection"

# ── Noise patterns to strip ────────────────────────────────────────────────

# Channel / source tags (case-insensitive)
SOURCE_TAGS = [
    r"OSA Official HD Video", r"OSA Worldwide", r"OSA Islamic",
    r"official HD video", r"Official Audio Song", r"Official Complete Version",
    r"official version", r"Official Music Video", r"Official 4K Video",
    r"complete full version", r"complete official full version",
    r"Complete Original Version", r"Complete Original Recording",
    r"complete version", r"Full Version", r"Full Qawwali",
    r"High Quality Version", r"HQ Quality", r"HD",
    r"NusratSahib\.Com", r"AmanDeep Music", r"Dhanak TV USA",
    r"EMIPakistanSpiritual", r"@EMIPakistanSpiritual",
    r"@RohailHyattMusic", r"Aljilani Production", r"Hi-Tech Music",
    r"Nupur Audio", r"Musical Maestros", r"Qawali network",
    r"Virsa Heritage Revived?", r"Virsa Heritage R",
    r"Lok Virsa", r"LOK VIRSA",
    r"Coke Studio (Pakistan|Season \d+)",
    r"Coke Studio Season \d+",
    r"Nfak Shayari", r"NFAK Lines",
    r"Lyrics (in Description|&? ?Translation)?",
    r"Lyric(al)? Video", r"Lyrics Video",
    r"with [Ll]yrics",
    r"By Visaal", r"zb writes", r"alifayn9075",
    r"mushiicreations", r"T2 BhaI 🎧",
    r"Haqiqat حقیقت",
    r"Sacha Koreja", r"SSQ",
    r"DJ2016",
]

# Descriptive noise words / phrases
NOISE_PHRASES = [
    r"Live (At|In|At Buena Park California \d+|Concert|Full|Full Concert|TV Recording|Meri Pasand PTV|Sargam Performance in UK)?",
    r"Live (At|In)[^|,\[\(]*",
    r"Rare (Version|Kalam|Lines|Show|Recording|Live Recording)?",
    r"RARE( VERSION)?",
    r"Super Rare (Naat)?",
    r"Very (Rare|Beautiful and Rare)",
    r"Very Rare",
    r"Beautiful and Rare",
    r"Unreleased",
    r"Unseen Recording",
    r"Private Mehfil",
    r"PRIVATE MEHFIL",
    r"Original( Rare)?",
    r"ORIGINAL",
    r"Clear Audio",
    r"CLEAR AUDIO",
    r"Clean Audio",
    r"Short Clip",
    r"Shorter version",
    r"Full Song",
    r"Full Video( Song)?",
    r"Full Video",
    r"Full Concert",
    r"Full (?:Rare )?Qawwali",
    r"Hajj Special Nasheed \d+",
    r"Best of Ghazals",
    r"Best Qawwali",
    r"BEST QAWWALI",
    r"Popular Qawwali",
    r"Popular Songs",
    r"Superhit Hindi Song",
    r"Romantic classics",
    r"Old Hindi Song",
    r"Classic Song",
    r"Bollywood Classic Songs",
    r"Classical",
    r"CLASSICAL",
    r"Death Anniversary[^|,\[\(]*",
    r"26th Death Anniversary[^|,\[\(]*",
    r"Tribute By[^|,\[\(]*",
    r"\d+ LIVE PERFORMANCE",
    r"Live \d+",
    r"ᴴᴰ",
    r"🙇🏼‍♂️🎵🕊️❤️‍🩹",
    r"💕",
    r"✨",
    r"🙏",
    r"❤",
    r"#\w+",                   # hashtags
    r"V\d+\s*$",               # version tags at end: V1, V2
    r"\(V \d+\)",
    r"V\.\d+",
    r"vol(ume)?\s*\d+",
    r"Volume \d+",
    r"part\s*\d+",
    r"\(part\d+\)",
    r"128k",
    r"320",
    r"1080p", r"720p", r"480p",
    r"\(1\)$",                 # duplicate suffix
    r"\.wmv$",                 # wrong extension leftover
]

# Artist/performer credit tags to remove (keep the title clean)
CREDIT_TAGS = [
    r"Ustad Nusrat Fateh Ali Khan",
    r"Ustaad Nusrat Fateh Ali Khan",
    r"USTAD NUSRAT FATEH ALI KHAN",
    r"Nusrat Fateh Ali Khan Qawwal",
    r"Nusrat Fateh Ali Khan",
    r"NUSRAT FATEH ALI KHAN",
    r"Nusrat Fatheh Ali Khan",
    r"Nusrat Fateh ALi Qawwal",
    r"Nusrat Fateh Ali",
    r"Nusrat saab",
    r"Nusrat Sahib",
    r"Ustad Bahauddin Qawwal",
    r"Ustad Bahauddin Khan Qawwal",
    r"Rahat Fateh Ali Khan",
    r"Farid Ayaz & Abu Muhammad",
    r"Farid Ayaz",
    r"Maulvi Haider Hassan Vehranwale Qawwal",
    r"Maulvi Haider Hassan Vehranwale",
    r"Maulvi Haider Hassan",
    r"Maulvi Ahmed Hassan",
    r"Molvi Ahmed Hassan",
    r"Tuqeer Ali Khan",
    r"Bahauddin Qawwal",
    r"Chishti Sabri Qawwal",
    r"Chishti Sabri",
    r"Jagjit Singh",
    r"Siza Roy",
    r"Syeda Areeba Fatima",
    r"Lori Carson",
    r"Michael Brook",
    r"Mohsin Abbas Haider",
    r"Zeb Bangash",
    r"Zeb & Haniya",
    r"Gippy Grewal",
    r"Sonu Nigam",
    r"Shankar Ehsaan Loy",
    r"Happy Raikoti",
    r"Noor Jehan",
    r"Ghulam Ali",
    r"Javed Akhtar",
    r"Mohammad Rafi",
    r"Mohammed Rafi",
    r"Lata Mangeshkar",
    r"Kishore Kumar",
    r"Madhubala",
    r"Arijit Singh",
    r"Atif Aslam",
    r"Rajeev Shukla",
    r"Hans Raj Hans",
    r"Gaudi",
    r"Farrukh Fateh Ali Khan Sahab",
    r"Teri re main to charanan laagi Peer Nizamuddin",
]

# Poet / Kalam credits (strip the "Kalam: ..." part)
POET_CREDITS = [
    r"Kalam(?:e|[\s\-]+e)?[\s\-]+(?:Iqbal|Ghalib|Hazrat Ameer Khusro|Ameer Khusrau|Amir Khusrau|Amir Khusro|Khusrau|Rumi|Maulana Jami|Maulana Jaami|Maulvi[^\|,\[\(]{1,40})",
    r"Kalam[:\s]+[A-Z][a-zA-Z\s\(\)\.]+(?=[\|\-,\[\(]|$)",
    r"Allama Iqbal (Poetry|Special)",
    r"Allama Iqbal",
    r"Mirza Ghalib",
    r"Hazrat Ameer Khusro",
    r"Amir Khusrau",
    r"Amir Khusro",
    r"Hazrat Amir Khusro",
    r"Maulana Jami",
    r"Maulana Jaami",
    r"Khawaja Ghulam Fareed[^|,\[\(]*",
    r"Bu Ali (Shah )?Qalandar",
    r"Hazrat Khawaja Naqeeb Ullah Shah",
    r"Kalam Hazrat Amir Khusro",
    r"Kalam:[^\|,\[\(]+",
]

# ── Separator characters (full-width and special) ─────────────────────────
SEPARATORS = r"[｜⧸＂＂：\|]"


def clean_name(raw):
    name = raw

    # Remove numbered prefix: "101 - ", "NA - "
    name = re.sub(r"^\d+\s*-\s*", "", name)
    name = re.sub(r"^NA\s*-\s*", "", name, flags=re.IGNORECASE)

    # Remove file extension
    name = re.sub(r"\.(webm|mp3|m4a|wmv)$", "", name, flags=re.IGNORECASE)

    # Replace full-width / special separators with " - "
    name = re.sub(SEPARATORS, " - ", name)

    # Remove hashtags early
    name = re.sub(r"#\w+", "", name)

    # Strip source tags
    for tag in SOURCE_TAGS:
        name = re.sub(tag, "", name, flags=re.IGNORECASE)

    # Strip poet / kalam credits
    for tag in POET_CREDITS:
        name = re.sub(tag, "", name, flags=re.IGNORECASE)

    # Strip artist credit tags
    for tag in CREDIT_TAGS:
        name = re.sub(tag, "", name, flags=re.IGNORECASE)

    # Strip noise phrases
    for phrase in NOISE_PHRASES:
        name = re.sub(phrase, "", name, flags=re.IGNORECASE)

    # Remove bracketed noise: [Live At ...], [OKARA 1986], [ORIGINAL RECORDING], etc.
    name = re.sub(r"\[[^\]]{0,60}\]", "", name)

    # Remove parenthetical noise that is purely descriptive / year / location
    name = re.sub(r"\(\s*(?:19|20)\d{2}\s*\)", "", name)           # (1975), (2021)
    name = re.sub(r"\(\s*(?:Remastered|Remix|Live[^)]{0,40}|Incomplete Version|Original[^)]{0,40}|Unseen[^)]{0,40}|Clear[^)]{0,40}|Full[^)]{0,40})\s*\)", "", name, flags=re.IGNORECASE)

    # Remove remaining separators at start/end of segments
    name = re.sub(r"\s*-\s*-\s*", " - ", name)   # double dash
    name = re.sub(r"^\s*[-–—,\s]+", "", name)
    name = re.sub(r"[-–—,\s]+$", "", name)

    # Collapse multiple spaces / dashes
    name = re.sub(r"\s{2,}", " ", name)
    name = re.sub(r"\s*-\s*$", "", name)
    name = re.sub(r"^\s*-\s*", "", name)

    # Title-case (preserve existing caps for Urdu romanisation)
    words = name.strip().split()
    # Only title-case if mostly lowercase (avoid ALL CAPS blasting)
    if name == name.upper() and len(name) > 3:
        name = name.title()

    name = name.strip(" -–—,.")

    return name if name else raw  # fallback to raw if we wiped everything


def safe_filename(name, ext):
    """Remove chars illegal in filenames."""
    name = re.sub(r'[\\/:*?"<>|]', "", name)
    name = name.strip(". ")
    return f"{name}{ext}"


def get_unique_path(folder, filename):
    """If target path already exists, append _2, _3, etc."""
    base, ext = os.path.splitext(filename)
    candidate = filename
    counter = 2
    while os.path.exists(os.path.join(folder, candidate)):
        candidate = f"{base}_{counter}{ext}"
        counter += 1
    return candidate


# ── Main ──────────────────────────────────────────────────────────────────

files = sorted(os.listdir(folder))
renamed, skipped, unchanged = 0, 0, 0

print(f"Found {len(files)} files in '{folder}'\n")

for original in files:
    ext = os.path.splitext(original)[1].lower()

    # Only process audio/video files
    if ext not in (".mp3", ".webm", ".m4a", ".wmv", ".flac", ".ogg"):
        print(f"  SKIP  {original}")
        skipped += 1
        continue

    clean = clean_name(original)
    new_filename = safe_filename(clean, ext)
    new_filename = get_unique_path(folder, new_filename)

    old_path = os.path.join(folder, original)
    new_path = os.path.join(folder, new_filename)

    if original == new_filename:
        unchanged += 1
        continue

    os.rename(old_path, new_path)
    print(f"  ✔  {original}")
    print(f"     → {new_filename}\n")
    renamed += 1

print(f"\n{'─'*60}")
print(f"  Renamed  : {renamed}")
print(f"  Unchanged: {unchanged}")
print(f"  Skipped  : {skipped}")
print(f"{'─'*60}")