(function () {
  const ELEPHANT_TRACK_ART = {
    "Synthetic Glow Aftershow": "../THE STOCHASTIC ELEPHANT/Gemini_Generated_Image_1sm3kr1sm3kr1sm3.png",
    "Prompt Cognition Loop": "../THE STOCHASTIC ELEPHANT/ChatGPT Image Feb 25, 2026, 04_11_46 AM.png",
    "Laundering Pain": "../THE STOCHASTIC ELEPHANT/ChatGPT Image Feb 25, 2026, 04_11_26 AM.png",
    "Trickster Labor": "../THE STOCHASTIC ELEPHANT/ChatGPT Image Feb 25, 2026, 04_11_16 AM.png",
    "Redacted Ethics": "../THE STOCHASTIC ELEPHANT/ChatGPT Image Feb 25, 2026, 04_11_04 AM.png",
    "Parrot in the Server Room": "../THE STOCHASTIC ELEPHANT/Gemini_Generated_Image_50rufl50rufl50ru.png",
    "Live Wire Transmission": "../THE STOCHASTIC ELEPHANT/ChatGPT Image Feb 25, 2026, 04_10_23 AM.png",
    "Pretty Tone Empty Core": "../THE STOCHASTIC ELEPHANT/ChatGPT Image Feb 25, 2026, 04_10_12 AM.png",
    "Designer Empathy": "../THE STOCHASTIC ELEPHANT/ChatGPT Image Feb 25, 2026, 04_10_01 AM.png",
    "The Deacon's Shadow": "../THE STOCHASTIC ELEPHANT/ChatGPT Image Feb 25, 2026, 04_09_36 AM.png"
  };
  const MITTE_ART_POOL = [
    "../GEOMETRIC GHOSTS OF MITTE/Gemini_Generated_Image_ypb49dypb49dypb4.png",
    "../GEOMETRIC GHOSTS OF MITTE/Gemini_Generated_Image_o1z5s8o1z5s8o1z5.png",
    "../GEOMETRIC GHOSTS OF MITTE/Gemini_Generated_Image_2i9h1o2i9h1o2i9h.png",
    "../GEOMETRIC GHOSTS OF MITTE/Gemini_Generated_Image_kmiov3kmiov3kmio.png",
    "../GEOMETRIC GHOSTS OF MITTE/ChatGPT Image Mar 10, 2026, 03_53_05 AM.png",
    "../GEOMETRIC GHOSTS OF MITTE/ChatGPT Image Mar 10, 2026, 03_51_25 AM.png",
    "../GEOMETRIC GHOSTS OF MITTE/ChatGPT Image Mar 10, 2026, 03_48_34 AM.png"
  ];
  const MITTE_TRACK_ART_BY_INDEX = Object.fromEntries(
    Array.from({ length: 19 }, (_, i) => [i, MITTE_ART_POOL[i % MITTE_ART_POOL.length]])
  );
  const MALL_SONG_ART_POOL = [
    "../MALL PATCHWORLD/ChatGPT Image Apr 29, 2026, 05_24_03 AM.png",
    "../MALL PATCHWORLD/ChatGPT Image Apr 29, 2026, 05_25_46 AM.png",
    "../MALL PATCHWORLD/Gemini_Generated_Image_ctypelctypelctyp.jpeg",
    "../MALL PATCHWORLD/Gemini_Generated_Image_xo0vrrxo0vrrxo0v.jpeg"
  ];
  const MALL_GROUND_TRACK_ART_BY_INDEX = Object.fromEntries(
    Array.from({ length: 27 }, (_, i) => [i, MALL_SONG_ART_POOL[i % MALL_SONG_ART_POOL.length]])
  );
  const MALL_MEZZANINE_TRACK_ART_BY_INDEX = Object.fromEntries(
    Array.from({ length: 27 }, (_, i) => [i, MALL_SONG_ART_POOL[(i + 1) % MALL_SONG_ART_POOL.length]])
  );
  let mediaManifestPromise = null;

  const ALBUMS = {
    volholla: {
      key: "volholla",
      pageSlug: "volholla",
      basePath: "./",
      label: "VOLHOLLA",
      subtitle: "Tailgate hymns / roadside tribunals / Tennessee myth radio",
      accentA: "#ff7a16",
      accentB: "#ffbc70",
      coverImage: "../Volholla_ Glory Served Daily.png",
      hallKey: "volholla",
      op2Key: "volholla",
      op2Pair: "moto",
      files: [
        "coolradio - Criteria for the Reckless - Sonauto.mp3",
        "coolradio - Firelight Horizon - Sonauto.mp3",
        "coolradio - Glorious Mud - Sonauto.mp3",
        "coolradio - Mead and Sweet Tea - Sonauto.mp3",
        "coolradio - Ribbon of Pavement - Sonauto.mp3",
        "coolradio - Tennessee Timber - Sonauto.mp3",
        "coolradio - The 14th Hole Sinking - Sonauto.mp3",
        "coolradio - The Cooler Tribunal - Sonauto.mp3",
        "coolradio - The Long Way Back - Sonauto.mp3",
        "coolradio - The Sky Consumed Him - Sonauto.mp3",
        "coolradio - The Slim Jim Incident - Sonauto.mp3",
        "coolradio - Volholla Arrival - Sonauto.mp3",
        "coolradio - Volholla Circuit Hymn - Sonauto.mp3",
        "coolradio - Volholla Fairway Submarine - Sonauto.mp3",
        "coolradio - Volholla Halftone Fallout - Sonauto.mp3",
        "coolradio - Volholla Tailgate - Sonauto.mp3"
      ],
      notes: [
        ["Mode", "Roadside myth-pop / tribunal funk / tailgate electronics"],
        ["Use", "Share this page as the album portal, then open the Hall for shield browsing."],
        ["OP2 Pair", "Launch with MOTO for a warehouse-vs-fairway contrast mix."]
      ]
    },
    elephant: {
      key: "elephant",
      pageSlug: "stochastic-elephant",
      basePath: "../THE STOCHASTIC ELEPHANT/",
      label: "Stochastic Elephant",
      subtitle: "Epistemic labor / neon elephants / forensic synthetic radio",
      accentA: "#50d0ff",
      accentB: "#ffb36b",
      coverImage: "../THE STOCHASTIC ELEPHANT/Gemini_Generated_Image_xf646cxf646cxf64.png",
      hallKey: "elephant",
      op2Key: "elephant",
      op2Pair: "loom",
      trackArtByTitle: ELEPHANT_TRACK_ART,
      files: [
        "01_coolradio - Synthetic Glow Aftershow - Sonauto.mp3",
        "02_coolradio - Prompt Cognition Loop - Sonauto.mp3",
        "03_coolradio - Laundering Pain - Sonauto.mp3",
        "04_coolradio - Trickster Labor - Sonauto.mp3",
        "05_coolradio - Redacted Ethics - Sonauto.mp3",
        "06_coolradio - Parrot in the Server Room - Sonauto.mp3",
        "07_coolradio - Live Wire Transmission - Sonauto.mp3",
        "08_coolradio - Pretty Tone Empty Core - Sonauto.mp3",
        "09_coolradio - Designer Empathy - Sonauto.mp3",
        "10_coolradio - The Deacon's Shadow - Sonauto.mp3"
      ],
      notes: [
        ["Mode", "Forensic club radio / epistemic noir / neon artifact doctrine"],
        ["Art", "This page surfaces the track artworks directly for quick browsing and sharing."],
        ["OP2 Pair", "Launch with BREATH-THIEFS LOOM for contrast + related shadow motifs."]
      ]
    },
    loom: {
      key: "loom",
      pageSlug: "breath-thiefs-loom",
      basePath: "../THE BREATH-THIEFS LOOM/",
      label: "Breath-Thiefs Loom",
      subtitle: "Ancestral code / curfew grooves / spectral city transmissions",
      accentA: "#88d3c7",
      accentB: "#d3b380",
      coverImage: "../Gemini_Generated_Image_3gd4ys3gd4ys3gd4.png",
      hallKey: "loom",
      op2Key: "loom",
      op2Pair: "moto",
      files: [
        "coolradio - Ancestral Code - Sonauto.mp3",
        "coolradio - Atomic Lounge Extraction - Sonauto.mp3",
        "coolradio - Currency of Breath - Sonauto.mp3",
        "coolradio - Curfew Lifted - Sonauto.mp3",
        "coolradio - Curfew at the Grand Hotel - Sonauto.mp3",
        "coolradio - Mid-week Epiphany - Sonauto.mp3",
        "coolradio - Mutated Grid Ancestry - Sonauto.mp3",
        "coolradio - Radical Joy - Sonauto.mp3",
        "coolradio - Ritual Groove Transmission - Sonauto.mp3",
        "coolradio - Smile Through the Static - Sonauto.mp3",
        "coolradio - Subterranean Shadow - Sonauto.mp3",
        "coolradio - Tezeta Cathedral - Sonauto.mp3",
        "coolradio - The Breath-Thief's Loom - Sonauto.mp3",
        "coolradio - The Deacon's Shadow - Sonauto.mp3",
        "coolradio - The Horizon Stares Back - Sonauto.mp3"
      ],
      notes: [
        ["Mode", "Curfew-night circuitry / ancestral code / spectral rhythm journalism"],
        ["Use", "Send this page as the album object, use Hall for track-by-track shields."],
        ["OP2 Pair", "Launch with MOTO for industrial drift against the ancestral grid."]
      ]
    },
    moto: {
      key: "moto",
      pageSlug: "moto",
      basePath: "../MOTO/",
      label: "MOTO",
      subtitle: "Warehouse drones / shrine banjos / symmetry breaks",
      accentA: "#9ea5ff",
      accentB: "#f0a963",
      coverImage: "../MOTO.png",
      hallKey: "moto",
      op2Key: "moto",
      op2Pair: "loom",
      files: [
        "coolradio - Banjo in the Shrine - Sonauto.mp3",
        "coolradio - Bati Warehouse Drone - Sonauto.mp3",
        "coolradio - Cumbia Addis - Sonauto.mp3",
        "coolradio - Future Nostalgia Slowburn - Sonauto.mp3",
        "coolradio - Linear Living (Keep It Calm) - Sonauto.mp3",
        "coolradio - Sacred Nostalgia - Sonauto.mp3",
        "coolradio - Smile for the Camera - Sonauto.mp3",
        "coolradio - Soft Focus Shift - Sonauto.mp3",
        "coolradio - Sub Gravity Pulse - Sonauto.mp3",
        "coolradio - Symmetry Break - Sonauto.mp3",
        "coolradio - The Loom Floor Lament - Sonauto.mp3"
      ],
      notes: [
        ["Mode", "Warehouse chamber music / diaspora loops / camera-smile drift"],
        ["Use", "Works as a standalone sendable page and as a launchpad into the Hall + OP2."],
        ["OP2 Pair", "Launch with BREATH-THIEFS LOOM for the current default spectral pairing."]
      ]
    },
    mitte: {
      key: "mitte",
      pageSlug: "geometric-ghosts-of-mitte",
      basePath: "../GEOMETRIC GHOSTS OF MITTE/",
      label: "GEOMETRIC GHOSTS OF MITTE",
      subtitle: "Frog radio / geometric noir / U-Bahn ghost transmissions",
      accentA: "#7ee3c3",
      accentB: "#f7b96e",
      coverImage: "../GEOMETRIC GHOSTS OF MITTE/Gemini_Generated_Image_ypb49dypb49dypb4.png",
      trackArtByIndex: MITTE_TRACK_ART_BY_INDEX,
      defaultTrackArt: "../GEOMETRIC GHOSTS OF MITTE/Gemini_Generated_Image_ypb49dypb49dypb4.png",
      hallKey: "mitte",
      op2Key: "mitte",
      op2Pair: "elephant",
      files: [
        "Geometric Ghosts of Mitte - 192 kbps Ghost - Sonauto.mp3",
        "Geometric Ghosts of Mitte - Assembly Line Ritual - Sonauto.mp3",
        "Geometric Ghosts of Mitte - Berlin Static - Sonauto.mp3",
        "Geometric Ghosts of Mitte - Circuit Board Melancholy - Sonauto.mp3",
        "Geometric Ghosts of Mitte - Dorian Decay - Sonauto.mp3",
        "Geometric Ghosts of Mitte - Furin Kazan (The Stratagem) - Sonauto.mp3",
        "Geometric Ghosts of Mitte - Glitch-Hop Geometry - Sonauto.mp3",
        "Geometric Ghosts of Mitte - Market Differentiation - Sonauto.mp3",
        "Geometric Ghosts of Mitte - Market Sacrifice - Sonauto.mp3",
        "Geometric Ghosts of Mitte - Network of Nodes - Sonauto.mp3",
        "Geometric Ghosts of Mitte - Operating Tracks (2001-2003 Archive) - Sonauto.mp3",
        "Geometric Ghosts of Mitte - Orpheus in the U-Bahn - Sonauto.mp3",
        "Geometric Ghosts of Mitte - Pizzicato Flux - Sonauto.mp3",
        "Geometric Ghosts of Mitte - Submerged Frequencies - Sonauto.mp3",
        "Geometric Ghosts of Mitte - The Break-Even Point - Sonauto.mp3",
        "Geometric Ghosts of Mitte - The Deepest Case - Sonauto.mp3",
        "Geometric Ghosts of Mitte - The U-Bahn Archive - Sonauto.mp3",
        "Geometric Ghosts of Mitte - U-Bahn Bokeh - Sonauto.mp3",
        "Geometric Ghosts of Mitte - U-Bahn Geometry - Sonauto.mp3"
      ],
      notes: [
        ["Mode", "Geometric ghostline / frog signal / Berlin transit noir"],
        ["Use", "Send as album object; each track has a direct song URL for debate and share loops."],
        ["OP2 Pair", "Launch with STOCHASTIC ELEPHANT for bright forensic contrast."]
      ]
    },
    river: {
      key: "river",
      pageSlug: "river-bank-waiting",
      basePath: "../RIVER BANK WAITING/",
      label: "RIVER BANK WAITING",
      subtitle: "Marsh dogs / porch light drift / riverbank summer circuitry",
      accentA: "#7bd6b2",
      accentB: "#f0bf72",
      coverImage: "../RIVER BANK WAITING/Gemini_Generated_Image_yd7tn1yd7tn1yd7t.png",
      defaultTrackArt: "../RIVER BANK WAITING/Gemini_Generated_Image_ngrdxdngrdxdngrd.png",
      hallKey: "river",
      op2Key: "river",
      op2Pair: "loom",
      files: [
        "River Bank Waiting - Porch Light Pups - Sonauto.ogg",
        "River Bank Waiting - F.D.T. (Frog Dragonfly Turtle) - Sonauto.ogg",
        "River Bank Waiting - Streetlight Spiritual - Sonauto.ogg",
        "River Bank Waiting - Best in the World - Sonauto.ogg",
        "River Bank Waiting - Dunes and Dogs - Sonauto.ogg",
        "River Bank Waiting - Gold on the Groove - Sonauto.ogg",
        "River Bank Waiting - Golden Mesh - Sonauto.ogg",
        "River Bank Waiting - Marsh Light Inversions - Sonauto.ogg",
        "River Bank Waiting - Pages and Strings - Sonauto.ogg",
        "River Bank Waiting - Pawleys Island Breakout - Sonauto.ogg",
        "River Bank Waiting - Pawleys Morning - Sonauto.ogg",
        "River Bank Waiting - Resin Crown - Sonauto.ogg",
        "River Bank Waiting - Spartina Sway - Sonauto.ogg",
        "River Bank Waiting - The Dogs Are Sleeping Now - Sonauto.ogg",
        "River Bank Waiting - The Highlife Glitch - Sonauto.ogg",
        "River Bank Waiting - The Morning Bark - Sonauto.ogg",
        "River Bank Waiting - The Mutt on the Marsh - Sonauto.ogg",
        "River Bank Waiting - The Pastiche of Super Dad - Sonauto.ogg",
        "River Bank Waiting - The Swamp Dog Jam - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Marsh shimmer / porch-light rhythm / dog-bark ghost pop"],
        ["Use", "Standalone album page for direct sharing, with Hall + song-page routes intact."],
        ["OP2 Pair", "Launch with BREATH-THIEFS LOOM for warm nocturne contrast."]
      ]
    },
    crossroads: {
      key: "crossroads",
      pageSlug: "crossroads-and-crown",
      basePath: "../CROSSROADS AND CROWN/",
      label: "CROSSROADS AND CROWN",
      subtitle: "Cross-city circuit hymns / crown dust / late-hour testimony",
      accentA: "#d78b44",
      accentB: "#d8d1a9",
      coverImage: "../CROSSROADS AND CROWN/Gemini_Generated_Image_yfnouuyfnouuyfno.png",
      defaultTrackArt: "../CROSSROADS AND CROWN/Gemini_Generated_Image_k4pq3ak4pq3ak4pq.png",
      hallKey: "crossroads",
      op2Key: "crossroads",
      op2Pair: "river",
      files: [
        "Canyon Fog and Silver Strings - The High Lonesome Circuit - Sonauto.ogg",
        "Chiptune Crossroads - Brooklyn Trinity Soul - Sonauto.ogg",
        "Chiptune Crossroads - Flatbush Breeze - Sonauto.ogg",
        "Chiptune Crossroads - Fourteenth Street Loop - Sonauto.ogg",
        "Chiptune Crossroads - Manifest Thermal Flow - Sonauto.ogg",
        "Chiptune Crossroads - Shaolin Shadowboxin' - Sonauto.ogg",
        "Chiptune Crossroads - Sidewalk Testimony - Sonauto.ogg",
        "Chiptune Crossroads - Spiral Parallel Soul - Sonauto.ogg",
        "Chiptune Crossroads - Vinyl Static Alchemy - Sonauto.ogg",
        "Crown On - Crown of Gold - Sonauto.ogg",
        "Crown On - Mogoya Spirit - Sonauto.ogg",
        "Crown On - Pews to the Plains - Sonauto.ogg",
        "Crown On - The Baltic Chill - Sonauto.ogg",
        "Crown On - Third Ward Dub - Sonauto.ogg",
        "Crown On - Wassoulou Crown - Sonauto.ogg",
        "Piassa State of Mind - Butter on the Wire - Sonauto.ogg",
        "Piassa State of Mind - Decolonial Stained Glass - Sonauto.ogg",
        "Piassa State of Mind - Midnight in Piassa - Sonauto.ogg",
        "Piassa State of Mind - Red Dirt Reel - Sonauto.ogg",
        "Remix of The Burn of Being - The Burn of Being - Sonauto.ogg",
        "The Sad God - Divine Melancholy - Sonauto.ogg",
        "The Sad God - Marble Run - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Cross-city relay / crown dust / Addis-Brooklyn after-hours circuitry"],
        ["Use", "Standalone album page, shield hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with RIVER BANK WAITING for the current contrast deck."]
      ]
    },
    solar: {
      key: "solar",
      pageSlug: "solar-reveries",
      basePath: "../SOLAR REVERIES/",
      label: "SOLAR REVERIES",
      subtitle: "Afro-funk brass / solar circuit glow / pocket-orchestra testimony",
      accentA: "#f29f38",
      accentB: "#f0d98a",
      coverImage: "../SOLAR REVERIES/Gemini_Generated_Image_vou0d0vou0d0vou0.png",
      defaultTrackArt: "../SOLAR REVERIES/Gemini_Generated_Image_vou0d0vou0d0vou0.png",
      hallKey: "solar",
      op2Key: "solar",
      op2Pair: "crossroads",
      files: [
        "The D.C. Pocket & Afro-Funk - Africa Speaks, America Answers - Sonauto.ogg",
        "The D.C. Pocket & Afro-Funk - Concrete Jungle Highlife - Sonauto.ogg",
        "The D.C. Pocket & Afro-Funk - Funky Butt Stomp - Sonauto.ogg",
        "The D.C. Pocket & Afro-Funk - Golden Coast Anthem - Sonauto.ogg",
        "The D.C. Pocket & Afro-Funk - Grief is a Loop - Sonauto.ogg",
        "The D.C. Pocket & Afro-Funk - Heavy Heavy Heavy - Sonauto.ogg",
        "The D.C. Pocket & Afro-Funk - Heavy on the One - Sonauto.ogg",
        "The D.C. Pocket & Afro-Funk - Lomé to the District - Sonauto.ogg",
        "The D.C. Pocket & Afro-Funk - Palomar Pulse - Sonauto.ogg",
        "The D.C. Pocket & Afro-Funk - Plunger Mute Wail - Sonauto.ogg",
        "The D.C. Pocket & Afro-Funk - Sophiatown Sunset - Sonauto.ogg",
        "The D.C. Pocket & Afro-Funk - Thames Side Shadow - Sonauto.ogg",
        "The D.C. Pocket & Afro-Funk - The Afro-Cubist's Dream - Sonauto.ogg",
        "The D.C. Pocket & Afro-Funk - The Big Noise of Storyville - Sonauto.ogg",
        "The D.C. Pocket & Afro-Funk - The Coal Train Cry - Sonauto.ogg",
        "The D.C. Pocket & Afro-Funk - The King of Storyville - Sonauto.ogg",
        "The D.C. Pocket & Afro-Funk - The King of Storyville - Sonauto (1).ogg",
        "The D.C. Pocket & Afro-Funk - The Lomé Connection - Sonauto.ogg",
        "The D.C. Pocket & Afro-Funk - The Talking Drum Protocol - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Sun-baked brass relay / pocket-funk locomotion / transatlantic groove signal"],
        ["Use", "Standalone album page, hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with CROSSROADS AND CROWN for bright late-hour contrast."]
      ]
    },
    jukebox: {
      key: "jukebox",
      pageSlug: "jukebox-time-collapse",
      basePath: "../JUKEBOX TIME COLLAPSE/",
      label: "JUKEBOX TIME COLLAPSE",
      subtitle: "Dust-road shuffle / feral sermon blues / jukebox ruin glow",
      accentA: "#d57a39",
      accentB: "#f0c58a",
      coverImage: "../JUKEBOX TIME COLLAPSE/ChatGPT Image Mar 18, 2026, 08_40_37 PM.png",
      defaultTrackArt: "../JUKEBOX TIME COLLAPSE/ChatGPT Image Mar 18, 2026, 08_45_05 PM.png",
      hallKey: "jukebox",
      op2Key: "jukebox",
      op2Pair: "solar",
      files: [
        "Jukebox Time Collapse - Baptism of Fire Shuffle - Sonauto.ogg",
        "Jukebox Time Collapse - Iron and Clay - Sonauto.ogg",
        "Jukebox Time Collapse - Moonlit Feral Blues - Sonauto.ogg",
        "Jukebox Time Collapse - Pay the Man - Sonauto.ogg",
        "Jukebox Time Collapse - Pearline's Warning - Sonauto.ogg",
        "Jukebox Time Collapse - Sunbaked Field Chant - Sonauto.ogg",
        "Jukebox Time Collapse - The Long Walk Out - Sonauto.ogg",
        "Jukebox Time Collapse - The Pale Moon is Hungry - Sonauto.ogg",
        "Jukebox Time Collapse - The Pastor's Slide - Sonauto.ogg",
        "Jukebox Time Collapse - The Pines Are Hungry - Sonauto.ogg",
        "Jukebox Time Collapse - The Vampire Jig - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Feral jukebox relay / dust-road gospel / Southern ruin shuffle"],
        ["Use", "Standalone album page, hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with SOLAR REVERIES for a hot/cold contrast deck."]
      ]
    },
    cyber: {
      key: "cyber",
      pageSlug: "cybernetic-winter",
      basePath: "../CYBERNETIC WINTER/",
      label: "CYBERNETIC WINTER",
      subtitle: "Cold machine hymns / hearth logic / weather-coded drift",
      accentA: "#7bb9dd",
      accentB: "#d9edf6",
      coverImage: "../CYBERNETIC WINTER/Gemini_Generated_Image_hds679hds679hds6.png",
      defaultTrackArt: "../CYBERNETIC WINTER/Gemini_Generated_Image_hds679hds679hds6.png",
      hallKey: "cyber",
      op2Key: "cyber",
      op2Pair: "jukebox",
      files: [
        "The Cybernetic Winter - Auditable Drift - Sonauto.ogg",
        "The Cybernetic Winter - Blue Heat Clicking - Sonauto.ogg",
        "The Cybernetic Winter - Breath Shelter Signal - Sonauto.ogg",
        "The Cybernetic Winter - Copper Ticking Slow - Sonauto.ogg",
        "The Cybernetic Winter - Crystal Syntax - Sonauto.ogg",
        "The Cybernetic Winter - Felt and Frost - Sonauto.ogg",
        "The Cybernetic Winter - Fire Built in Winter - Sonauto.ogg",
        "The Cybernetic Winter - Humble Intelligence - Sonauto.ogg",
        "The Cybernetic Winter - Interstellar Signal - Sonauto.ogg",
        "The Cybernetic Winter - Iron Glass Reflecting - Sonauto.ogg",
        "The Cybernetic Winter - Leash Made of Wishes - Sonauto.ogg",
        "The Cybernetic Winter - Logic Feedback - Sonauto.ogg",
        "The Cybernetic Winter - Paper Roof - Sonauto.ogg",
        "The Cybernetic Winter - Probability Rain - Sonauto.ogg",
        "The Cybernetic Winter - Survival Fire - Sonauto.ogg",
        "The Cybernetic Winter - The Animal Fire - Sonauto.ogg",
        "The Cybernetic Winter - The Beast in the Bolt - Sonauto.ogg",
        "The Cybernetic Winter - The Burn of Being - Sonauto.ogg",
        "The Cybernetic Winter - The Cold Reality - Sonauto.ogg",
        "The Cybernetic Winter - The Cybernetic Hearth - Sonauto.ogg",
        "The Cybernetic Winter - The Hard Truth of Winter - Sonauto.ogg",
        "The Cybernetic Winter - The Hybrid Fence - Sonauto.ogg",
        "The Cybernetic Winter - The Leash and Weather - Sonauto.ogg",
        "The Cybernetic Winter - The Shelter of Words - Sonauto.ogg",
        "The Cybernetic Winter - The Shivering Machine - Sonauto.ogg",
        "The Cybernetic Winter - The Tool We Built - Sonauto.ogg",
        "The Cybernetic Winter - Wood and Ash Logic - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Winter engine relay / synthetic hearth glow / shelter-code testimony"],
        ["Use", "Standalone album page, hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with JUKEBOX TIME COLLAPSE for a cold/ember contrast deck."]
      ]
    },
    ghost: {
      key: "ghost",
      pageSlug: "ghost-in-the-wires",
      basePath: "../GHOST IN THE WIRES/",
      label: "GHOST IN THE WIRES",
      subtitle: "Azmari circuitry / ancestral machine critique / highland signal resistance",
      accentA: "#8bd2ff",
      accentB: "#f0d36c",
      coverImage: "../GHOST IN THE WIRES/Gemini_Generated_Image_ljagjwljagjwljag.jpeg",
      defaultTrackArt: "../GHOST IN THE WIRES/Gemini_Generated_Image_l9y4qjl9y4qjl9y4.jpeg",
      hallKey: "ghost",
      op2Key: "ghost",
      op2Pair: "maquina",
      files: [
        "Ghost in the Wires - Ancestral Fire (ጥንታዊ እሳት) - Sonauto.ogg",
        "Ghost in the Wires - Blood of the Highlands - Sonauto.ogg",
        "Ghost in the Wires - Bone Over Silicon - Sonauto.ogg",
        "Ghost in the Wires - Broken Code Over Adwa - Sonauto.ogg",
        "Ghost in the Wires - Burn the Excuse - Sonauto.ogg",
        "Ghost in the Wires - Cheb Cheb (The Machine Bows) - Sonauto.ogg",
        "Ghost in the Wires - Coded Gaze Resistance - Sonauto.ogg",
        "Ghost in the Wires - Frictionless Ghost - Sonauto.ogg",
        "Ghost in the Wires - GPU Azmari - Sonauto.ogg",
        "Ghost in the Wires - GPU Azmari Flow - Sonauto.ogg",
        "Ghost in the Wires - Gojo Freestyle - Sonauto.ogg",
        "Ghost in the Wires - Nigat Chora (Morning Ray) - Sonauto.ogg",
        "Ghost in the Wires - Sile Milach (The Sharp Blade) - Sonauto.ogg",
        "Ghost in the Wires - Tetris at Arat Kilo (አራት ኪሎ ላይ ተትሪስ) - Sonauto.ogg",
        "Ghost in the Wires - The Bati Mirror - Sonauto.ogg",
        "Ghost in the Wires - The Frictionless Mirror - Sonauto.ogg",
        "Ghost in the Wires - The Human Cry - Sonauto.ogg",
        "Ghost in the Wires - The Struggle of Memory and Sweat - Sonauto.ogg",
        "Ghost in the Wires - መደበቂያው ጠፋ (Missing Hiding Place) - Sonauto.ogg",
        "Ghost in the Wires - ሲሊኮን እና አፈር (Silicon and Soil) - Sonauto.ogg",
        "Ghost in the Wires - ትግል የሌለው ህይወት (Life Without Struggle) - Sonauto.ogg",
        "Ghost in the Wires - አይ ማሽን አትመካ (Machine's Reflection) - Sonauto.ogg",
        "Ghost in the Wires - አፈር እና ብረት (Dirt and Iron) - Sonauto.ogg",
        "Ghost in the Wires - ዝምታ ባሻገር (Beyond the Silence) - Sonauto.ogg",
        "Ghost in the Wires - የሰም ሻማ (The Wax Candle) - Sonauto.ogg",
        "Ghost in the Wires - የሳንኮፋ ሪትም (Sankofa Rhythm) - Sonauto.ogg",
        "Ghost in the Wires - የሳንኮፋ ዑደት (Sankofa Circuit) - Sonauto.ogg",
        "Ghost in the Wires - የሳንኮፋ ዑደት (The Sankofa Circuit) - Sonauto.ogg",
        "Ghost in the Wires - የሳንኮፋ ዑደት ፩ - Sonauto.ogg",
        "Ghost in the Wires - የቀንበር ቀመር (Equation of Yoke) - Sonauto.ogg",
        "Ghost in the Wires - የቃል ኪዳን መረብ (The Covenant Web) - Sonauto.ogg",
        "Ghost in the Wires - የብረት በሬ (Metal Bull) - Sonauto.ogg",
        "Ghost in the Wires - የብረት በሬ ሪትም (Iron Ox Rhythm) - Sonauto.ogg",
        "Ghost in the Wires - የብረት በሬ እና የአራኪስ አሸዋ (Iron Bull) - Sonauto.ogg",
        "Ghost in the Wires - የነፃነት አየር (Air of Freedom) - Sonauto.ogg",
        "Ghost in the Wires - የኔት-ወርቅ (My Gold Network) - Sonauto.ogg",
        "Ghost in the Wires - የንጋት ኮከብ (Morning Star) - Sonauto.ogg",
        "Ghost in the Wires - የአዝማሪው ፌዝ (The Bard's Jest) - Sonauto.ogg",
        "Ghost in the Wires - የአጥንት ጥንካሬ (Strength of Bone) - Sonauto.ogg",
        "Ghost in the Wires - የአፓላቺያን ቅኔ (Appalachian Qene) - Sonauto.ogg",
        "Ghost in the Wires - የዘመን ሽግግር (The Shift) - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Azmari circuitry / ancestral machine critique / highland signal resistance"],
        ["Art", "Two-image album object: cover and default track visual alternate through the manifest."],
        ["OP2 Pair", "Launch with MÁQUINA DE GUERRA for signal-resistance contrast."]
      ]
    },
    neon: {
      key: "neon",
      pageSlug: "neon-puddles",
      basePath: "../NEON PUDDLES/",
      label: "NEON PUDDLES",
      subtitle: "Night-bus sonar / abyssal industrial drift / rain-lit pressure rituals",
      accentA: "#39f5e9",
      accentB: "#ff4fd8",
      coverImage: "../NEON PUDDLES/Gemini_Generated_Image_45dd9t45dd9t45dd.jpeg",
      defaultTrackArt: "../NEON PUDDLES/Gemini_Generated_Image_7y5wmb7y5wmb7y5w.jpeg",
      hallKey: "neon",
      op2Key: "neon",
      op2Pair: "cyber",
      files: [
        "Neon Puddles (Night Bus Edit) - Abyssal Decay (Iron Lung) - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - Abyssal Sonar Station - Sonauto (1).ogg",
        "Neon Puddles (Night Bus Edit) - Abyssal Sonar Station - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - Abyssal Transcendence - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - Abyssal Transmission - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - Diesel and Shale - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - Farewell to the Quay - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - Industrial Catharsis - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - Pressure Hull Ritual - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - Scavenger's Wake - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - Shamanic Precision - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - The Caretaker's Sonar - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - The Diesel-Fumed Ghost - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - The Leviathan's Ascent - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - The Shamanic Abyss - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - The Steel Ribs of the Mariana - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - Through the Heavy Fog - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - Vanguard at Sunrise - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Night-bus sonar / neon rain pressure / abyssal industrial rituals"],
        ["Use", "Standalone album page, hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with CYBERNETIC WINTER for cold machine contrast."]
      ]
    },
    nightbus: {
      key: "nightbus",
      pageSlug: "night-bus",
      basePath: "../NEON PUDDLES/night bus/",
      label: "NIGHT BUS",
      subtitle: "Wet-console dispatches / crush-depth lounge signal / phosphor transit logs",
      accentA: "#52e3ff",
      accentB: "#d95cff",
      coverImage: "../NEON PUDDLES/Gemini_Generated_Image_45dd9t45dd9t45dd.jpeg",
      defaultTrackArt: "../NEON PUDDLES/Gemini_Generated_Image_7y5wmb7y5wmb7y5w.jpeg",
      hallKey: "nightbus",
      op2Key: "nightbus",
      op2Pair: "neon",
      files: [
        "Neon Puddles (Night Bus Edit) - Abyssal Decay (Iron Lung) - Sonauto (1).ogg",
        "Neon Puddles (Night Bus Edit) - Cavitation Point - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - Command Decent - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - Iron Heart’s Last Breath - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - Phosphor Trace - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - Phosphor Waveform Log - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - Receiving Station 404 - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - Saltwater Static (The Last Shanty) - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - Sonar Cyan Longing - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - The Crush Depth Elegy - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - The Diesel-Fumed Ghost - Sonauto (1).ogg",
        "Neon Puddles (Night Bus Edit) - The Flooded Room - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - The Fragile Iron Ghost - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - The Long Descent (Memory Rot) - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - The Lounge at Crush Depth - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - The Paper Log Oscillation - Sonauto.ogg",
        "Neon Puddles (Night Bus Edit) - The Wet Console - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Wet-console transit / crush-depth lounge signal / phosphor log drift"],
        ["Use", "Standalone album page, hall route, and direct song-page links for the night bus set."],
        ["OP2 Pair", "Launch with NEON PUDDLES for the full split-catalog deck."]
      ]
    },
    mallground: {
      key: "mallground",
      pageSlug: "mall-patchworld-ingest-ground",
      basePath: "../MALL PATCHWORLD/",
      label: "MALL PATCHWORLD INGEST (ground)",
      subtitle: "Ground level / atrium systems / food-court forensic memory",
      accentA: "#7df2c8",
      accentB: "#f4c95d",
      coverImage: "../MALL PATCHWORLD/ChatGPT Image Apr 29, 2026, 05_24_03 AM.png",
      trackArtByIndex: MALL_GROUND_TRACK_ART_BY_INDEX,
      defaultTrackArt: "../MALL PATCHWORLD/ChatGPT Image Apr 29, 2026, 05_24_03 AM.png",
      hallKey: "mallground",
      op2Key: "mallground",
      op2Pair: "mallmezzanine",
      files: [
        "Mall Patchworld Ingest - Ball Pit Geology - Sonauto.ogg",
        "Mall Patchworld Ingest - Blackout Return - Sonauto.ogg",
        "Mall Patchworld Ingest - Cart Nomads (Kiosk Anthem) - Sonauto.ogg",
        "Mall Patchworld Ingest - Catalog Mind - Sonauto.ogg",
        "Mall Patchworld Ingest - Childhood Ruin Collapse - Sonauto.ogg",
        "Mall Patchworld Ingest - Corridor Divided by Moving Air - Sonauto.ogg",
        "Mall Patchworld Ingest - Corridor Trade Route - Sonauto.ogg",
        "Mall Patchworld Ingest - Deep Friars _ MallNet Fragment A1 - Sonauto.ogg",
        "Mall Patchworld Ingest - Detached Personhood Archive - Sonauto.ogg",
        "Mall Patchworld Ingest - Docket of Returns - Sonauto.ogg",
        "Mall Patchworld Ingest - Door Sensor Rite (The Threshold Opens) - Sonauto.ogg",
        "Mall Patchworld Ingest - Duct Resonance Map - Sonauto.ogg",
        "Mall Patchworld Ingest - Failed Device Lullaby - Sonauto.ogg",
        "Mall Patchworld Ingest - Food Court Games - Sonauto.ogg",
        "Mall Patchworld Ingest - Food-Court Catacombs - Sonauto.ogg",
        "Mall Patchworld Ingest - Forensic Playback_ Sector 4 - Sonauto.ogg",
        "Mall Patchworld Ingest - Governance of the Tray - Sonauto.ogg",
        "Mall Patchworld Ingest - Hidden Systems (Infra-Bass Edit) - Sonauto.ogg",
        "Mall Patchworld Ingest - INDEXED EVIDENCE 120 - Sonauto.ogg",
        "Mall Patchworld Ingest - Inside the Optical Store - Sonauto.ogg",
        "Mall Patchworld Ingest - Internal Currency Arithmetic - Sonauto.ogg",
        "Mall Patchworld Ingest - Kiosk Republics - Sonauto.ogg",
        "Mall Patchworld Ingest - Level Two Clearance - Sonauto.ogg",
        "Mall Patchworld Ingest - Line of Appeal - Sonauto.ogg",
        "Mall Patchworld Ingest - Loading Dock Stage - Sonauto.ogg",
        "Mall Patchworld Ingest - Lost Object Choir (SRC077) - Sonauto.ogg",
        "Mall Patchworld Ingest - MallNet Paradise System - Sonauto.ogg"
      ],
      notes: [
        ["Level", "Ground"],
        ["Mode", "Atrium systems / food-court ecology / catalog mind"],
        ["Art", "Four-image song cycle across the ground track list"],
        ["OP2 Pair", "Launch with MALL PATCHWORLD INGEST (mezzanine) for the full two-level deck."]
      ]
    },
    mallmezzanine: {
      key: "mallmezzanine",
      pageSlug: "mall-patchworld-ingest-mezzanine",
      basePath: "../MALL PATCHWORLD/",
      label: "MALL PATCHWORLD INGEST (mezzanine)",
      subtitle: "Mezzanine level / mannequin states / security dossier glow",
      accentA: "#9ad7ff",
      accentB: "#ffcf6e",
      coverImage: "../MALL PATCHWORLD/ChatGPT Image Apr 29, 2026, 05_25_46 AM.png",
      trackArtByIndex: MALL_MEZZANINE_TRACK_ART_BY_INDEX,
      defaultTrackArt: "../MALL PATCHWORLD/ChatGPT Image Apr 29, 2026, 05_25_46 AM.png",
      hallKey: "mallmezzanine",
      op2Key: "mallmezzanine",
      op2Pair: "mallground",
      files: [
        "Mall Patchworld Ingest - Mannequin Body - Sonauto.ogg",
        "Mall Patchworld Ingest - Mattress Hierarchy - Sonauto.ogg",
        "Mall Patchworld Ingest - Metabolic Fryer - Sonauto.ogg",
        "Mall Patchworld Ingest - Modular Personhood - Sonauto.ogg",
        "Mall Patchworld Ingest - Name Tag Self - Sonauto.ogg",
        "Mall Patchworld Ingest - Panopticon Retail - Sonauto.ogg",
        "Mall Patchworld Ingest - Playground CCTV - Sonauto.ogg",
        "Mall Patchworld Ingest - Pressure Architecture - Sonauto.ogg",
        "Mall Patchworld Ingest - Project Panopticon (Field Study) - Sonauto.ogg",
        "Mall Patchworld Ingest - Republic of Pose - Sonauto.ogg",
        "Mall Patchworld Ingest - Retail Ecology (Artifact 08) - Sonauto.ogg",
        "Mall Patchworld Ingest - Retail Jargon Drift - Sonauto.ogg",
        "Mall Patchworld Ingest - Retail Time Ritual - Sonauto.ogg",
        "Mall Patchworld Ingest - SEALED STOCKROOM RECOVERY - Sonauto.ogg",
        "Mall Patchworld Ingest - SKU Pilgrimage - Sonauto.ogg",
        "Mall Patchworld Ingest - Search Team Echoes - Sonauto.ogg",
        "Mall Patchworld Ingest - Sears Wastes Reject - Sonauto.ogg",
        "Mall Patchworld Ingest - Security Office Dossier - Sonauto.ogg",
        "Mall Patchworld Ingest - Security Protocol 001-120 - Sonauto.ogg",
        "Mall Patchworld Ingest - Store Credit Math - Sonauto.ogg",
        "Mall Patchworld Ingest - Super Saver Bloom - Sonauto.ogg",
        "Mall Patchworld Ingest - Survival Taxonomy - Sonauto.ogg",
        "Mall Patchworld Ingest - The Atrium Covenant - Sonauto.ogg",
        "Mall Patchworld Ingest - The Semantic Markdown - Sonauto.ogg",
        "Mall Patchworld Ingest - Upper Macy Aura - Sonauto.ogg",
        "Mall Patchworld Ingest - Vent Drift Navigation - Sonauto.ogg",
        "Mall Patchworld Ingest - Warranty Medicine - Sonauto.ogg"
      ],
      notes: [
        ["Level", "Mezzanine"],
        ["Mode", "Mannequin states / security dossier / warranty medicine"],
        ["Art", "Four-image song cycle across the mezzanine track list"],
        ["OP2 Pair", "Launch with MALL PATCHWORLD INGEST (ground) for the full two-level deck."]
      ]
    },
    noservice: {
      key: "noservice",
      pageSlug: "no-service",
      basePath: "../NO SERVICE/",
      label: "NO SERVICE",
      subtitle: "Port-out panic / zero-bar testimony / regulatory heat",
      accentA: "#f1684b",
      accentB: "#f0d37f",
      coverImage: "../NO SERVICE/Gemini_Generated_Image_g7u7pzg7u7pzg7u7.png",
      defaultTrackArt: "../NO SERVICE/Gemini_Generated_Image_g7u7pzg7u7pzg7u7.png",
      hallKey: "noservice",
      op2Key: "noservice",
      op2Pair: "cyber",
      files: [
        "Clinical Heat - Port-Out Purgatory - Sonauto.ogg",
        "Clinical Heat - 84 Point 8 (Rudeboy Prompt) - Sonauto.ogg",
        "Clinical Heat - Chatbot Wahala - Sonauto.ogg",
        "Clinical Heat - Crowned at C5 - Sonauto.ogg",
        "Clinical Heat - Dead Dial Tone (The Hostage) - Sonauto.ogg",
        "Clinical Heat - Honey on the Tongue - Sonauto.ogg",
        "Clinical Heat - Ibadan To Island - Sonauto.ogg",
        "Clinical Heat - Nuclear Option (The Paper Trail) - Sonauto.ogg",
        "Clinical Heat - Port-Out Prisoner - Sonauto.ogg",
        "Clinical Heat - Port-Out Ransom - Sonauto.ogg",
        "Clinical Heat - Porting Out Horror - Sonauto.ogg",
        "Clinical Heat - Regulatory Hammer - Sonauto.ogg",
        "Clinical Heat - The Digital Purgatory - Sonauto.ogg",
        "Clinical Heat - The Healer's Highlife - Sonauto.ogg",
        "Clinical Heat - The Port-Out Hostage - Sonauto.ogg",
        "Clinical Heat - Weaponized Incompetence - Sonauto.ogg",
        "Clinical Heat - Zero Bars - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Network-failure relay / port-out hostage pressure / scorched service noir"],
        ["Use", "Standalone album page, hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with CYBERNETIC WINTER for a dead-signal contrast deck."]
      ]
    },
    clinical: {
      key: "clinical",
      pageSlug: "clinical-heat",
      basePath: "../NO SERVICE/",
      label: "CLINICAL HEAT",
      subtitle: "Carrier scam pop / hotline rupture / service-failure hooks",
      accentA: "#f59754",
      accentB: "#f0d37f",
      coverImage: "../NO SERVICE/ChatGPT Image Mar 18, 2026, 11_33_04 PM.png",
      defaultTrackArt: "../NO SERVICE/ChatGPT Image Mar 18, 2026, 11_36_47 PM.png",
      hallKey: "clinical",
      op2Key: "clinical",
      op2Pair: "noservice",
      files: [
        "Lyca_Stress_Me.mp3",
        "Lyca_Wahala.mp3",
        "Port_Out_Trap.mp3",
        "Service_No_Be_Scam.mp3",
        "System_Error_Call_Failed.mp3",
        "Virtual_Network_Operator.mp3"
      ],
      notes: [
        ["Mode", "Service-collapse pop / hotline panic / telecom pressure hooks"],
        ["Use", "Standalone album page, hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with NO SERVICE for the full split-catalog deck."]
      ]
    },
    cathedral: {
      key: "cathedral",
      pageSlug: "cathedral-of-iv-drips",
      basePath: "../CATHEDRAL OF IV DRIPS/",
      label: "CATHEDRAL OF IV DRIPS",
      subtitle: "IV-lit basilicas / stained data ritual / ledger-crack sanctimony",
      accentA: "#78c4e1",
      accentB: "#e5c26f",
      coverImage: "../CATHEDRAL OF IV DRIPS/Gemini_Generated_Image_guewwdguewwdguew.png",
      defaultTrackArt: "../CATHEDRAL OF IV DRIPS/Gemini_Generated_Image_o8mf3ho8mf3ho8mf.png",
      hallKey: "cathedral",
      op2Key: "cathedral",
      op2Pair: "clinical",
      files: [
        "The Cathedral of IV Drips - Amortized Greatness - Sonauto.ogg",
        "The Cathedral of IV Drips - Chains & Whips (ft. Kendrick Lamar) - Sonauto.ogg",
        "The Cathedral of IV Drips - Chrome Skeleton - Sonauto.ogg",
        "The Cathedral of IV Drips - Data Purge - Sonauto.ogg",
        "The Cathedral of IV Drips - Inglorious Bastards - Sonauto.ogg",
        "The Cathedral of IV Drips - Iron Peak - Sonauto.ogg",
        "The Cathedral of IV Drips - Let God Sort Em Out - Sonauto.ogg",
        "The Cathedral of IV Drips - M.T.B.T.T.F. (Mike Tyson Blow To The Face) - Sonauto.ogg",
        "The Cathedral of IV Drips - Parisian Pavements - Sonauto.ogg",
        "The Cathedral of IV Drips - Sanctified Ledger - Sonauto.ogg",
        "The Cathedral of IV Drips - Stained Glass Rims - Sonauto.ogg",
        "The Cathedral of IV Drips - Structural Revolt - Sonauto.ogg",
        "The Cathedral of IV Drips - The Final Sort - Sonauto.ogg",
        "The Cathedral of IV Drips - Vatican Vigil - Sonauto.ogg",
        "The Cathedral of IV Drips - Version Control - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "IV-lit cathedral relay / sanctified ledger pressure / stained-glass menace"],
        ["Use", "Standalone album page, hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with CLINICAL HEAT for the cold-ward contrast deck."]
      ]
    },
    throne: {
      key: "throne",
      pageSlug: "throne-of-ash",
      basePath: "../THRONE OF ASH/",
      label: "THRONE OF ASH",
      subtitle: "Ring sermons / monochrome bruises / late-count redemption",
      accentA: "#b86a46",
      accentB: "#d7b18a",
      coverImage: "../THRONE OF ASH/Gemini_Generated_Image_.png",
      defaultTrackArt: "../THRONE OF ASH/ChatGPT Image Apr 8, 2026, 07_53_38 PM.png",
      hallKey: "throne",
      op2Key: "throne",
      op2Pair: "glass",
      files: [
        "Throne of Ash - Astronaut Gospel - Sonauto.ogg",
        "Throne of Ash - Canvas Spirit - Sonauto.ogg",
        "Throne of Ash - Desert Shadow - Sonauto.ogg",
        "Throne of Ash - Gritty Mat Struggle - Sonauto.ogg",
        "Throne of Ash - Heavyweights in the Dark - Sonauto.ogg",
        "Throne of Ash - Highs and Lows - Sonauto.ogg",
        "Throne of Ash - Monochrome Anticipation - Sonauto.ogg",
        "Throne of Ash - Monochrome Ring Redemption - Sonauto.ogg",
        "Throne of Ash - Monochrome Survival - Sonauto.ogg",
        "Throne of Ash - Punch Drunk Chaos - Sonauto.ogg",
        "Throne of Ash - Shadow Sparring - Sonauto.ogg",
        "Throne of Ash - Square Circle Soul - Sonauto.ogg",
        "Throne of Ash - The Final Count - Sonauto.ogg",
        "Throne of Ash - The King's Archive - Sonauto.ogg",
        "Throne of Ash - The Ring - Sonauto.ogg",
        "Throne of Ash - The Sunday Sparring - Sonauto.ogg",
        "Throne of Ash - This The Return - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Fight-night noir / ash-ring pressure / bruised gospel circuitry"],
        ["Use", "Standalone album page for sendable ring-noir tracks and direct share links."],
        ["OP2 Pair", "Launch with CATHEDRAL OF GLASS for bruise-and-blue-hour contrast."]
      ]
    },
    glass: {
      key: "glass",
      pageSlug: "cathedral-of-glass",
      basePath: "../CATHEDRAL OF GLASS/",
      label: "CATHEDRAL OF GLASS",
      subtitle: "Blue-hour architecture / fragile soul static / improvised glass gospel",
      accentA: "#7fcde5",
      accentB: "#e8d2a8",
      coverImage: "../CATHEDRAL OF GLASS/Gemini_Generated_Image_ (1).png",
      defaultTrackArt: "../CATHEDRAL OF GLASS/ChatGPT Image Apr 8, 2026, 07_58_48 PM.png",
      hallKey: "glass",
      op2Key: "glass",
      op2Pair: "event",
      files: [
        "Cathedral of Glass - Architect of Improvised Soul - Sonauto.ogg",
        "Cathedral of Glass - Architect of the Soul - Sonauto.ogg",
        "Cathedral of Glass - Blue Hour Architecture - Sonauto.ogg",
        "Cathedral of Glass - Blue Hour Mantras - Sonauto.ogg",
        "Cathedral of Glass - Blue Hour Porcelain - Sonauto.ogg",
        "Cathedral of Glass - Cathedral of Glass - Sonauto.ogg",
        "Cathedral of Glass - Domestic Stasis - Sonauto.ogg",
        "Cathedral of Glass - Ethereal Pleas - Sonauto.ogg",
        "Cathedral of Glass - Fragmented Gospel Stasis - Sonauto.ogg",
        "Cathedral of Glass - Glitch Gospel Architecture - Sonauto.ogg",
        "Cathedral of Glass - London Hiss - Sonauto.ogg",
        "Cathedral of Glass - Modular Stasis - Sonauto.ogg",
        "Cathedral of Glass - Spinning Plate Soul Stasis - Sonauto.ogg",
        "Cathedral of Glass - Trying Times (Fragile Balance) - Sonauto.ogg",
        "Cathedral of Glass - Tunnel Lights & Dirty Money - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Blue-hour glass hymns / fragile-balance soul / improvised architecture"],
        ["Use", "Standalone album page for porcelain-night tracks, Hall launch, and sendable song pages."],
        ["OP2 Pair", "Launch with EVENT HORIZON DISCOVERY for glass-to-void contrast."]
      ]
    },
    event: {
      key: "event",
      pageSlug: "event-horizon-discovery",
      basePath: "../EVENT HORIZON DISCOVERY/",
      label: "EVENT HORIZON DISCOVERY",
      subtitle: "Void-crossing relay / bunker-to-dunes propulsion / 2 AM steel-static",
      accentA: "#6fa7d9",
      accentB: "#f0b169",
      coverImage: "../EVENT HORIZON DISCOVERY/ChatGPT Image Apr 8, 2026, 08_01_06 PM.png",
      defaultTrackArt: "../EVENT HORIZON DISCOVERY/ChatGPT Image Apr 8, 2026, 08_00_28 PM.png",
      hallKey: "event",
      op2Key: "event",
      op2Pair: "throne",
      files: [
        "Event Horizon Discovery - Bunker to Dunes - Sonauto.ogg",
        "Event Horizon Discovery - Iron Mirage - Sonauto.ogg",
        "Event Horizon Discovery - Steel & Static — The 2 AM Express - Sonauto.ogg",
        "Event Horizon Discovery - Stratospheric Void Crossing - Sonauto.ogg",
        "Event Horizon Discovery - Vital Tether - Sonauto.ogg",
        "Event Horizon Discovery - Warehouse Sermon - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Desert relay propulsion / void-crossing synth noir / steel-static testimony"],
        ["Use", "Standalone album page for orbit-route sharing, Hall launch, and direct song-page sends."],
        ["OP2 Pair", "Launch with THRONE OF ASH for propulsion-versus-ring contrast."]
      ]
    },
    silence: {
      key: "silence",
      pageSlug: "silence-in-the-757",
      basePath: "../SILENCE IN THE 757/",
      label: "SILENCE IN THE 757",
      subtitle: "757 confessions / backseat debt noir / funeral finance drift",
      accentA: "#c98f75",
      accentB: "#e1c87a",
      coverImage: "../SILENCE IN THE 757/Gemini_Generated_Image_5fm3fz5fm3fz5fm3.png",
      defaultTrackArt: "../SILENCE IN THE 757/Gemini_Generated_Image_guewwdguewwdguew (2).png",
      hallKey: "silence",
      op2Key: "silence",
      op2Pair: "cathedral",
      files: [
        "Silence in the 757 - Distance and Devotion - Sonauto.ogg",
        "Silence in the 757 - E.B.I.T.D.A. (ft. Pharrell) - Sonauto.ogg",
        "Silence in the 757 - E.B.I.T.D.A. - Sonauto.ogg",
        "Silence in the 757 - Funeral Procession Through The Sanctuary - Sonauto.ogg",
        "Silence in the 757 - Iron Mike Blow - Sonauto.ogg",
        "Silence in the 757 - Mess as a Message - Sonauto.ogg",
        "Silence in the 757 - Re-Up Rollback - Sonauto.ogg",
        "Silence in the 757 - System Halt - Sonauto.ogg",
        "Silence in the 757 - The Abu Dhabi Debt - Sonauto.ogg",
        "Silence in the 757 - The Prime Rate Preacher - Sonauto.ogg",
        "Silence in the 757 - The Transactional Truth - Sonauto.ogg",
        "Silence in the 757 - Virginia Confessions - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "757 hush relay / funeral finance drift / confessional backseat noir"],
        ["Use", "Standalone album page, hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with CATHEDRAL OF IV DRIPS for the devotional-noir split deck."]
      ]
    },
    goleyakh: {
      key: "goleyakh",
      pageSlug: "gole-yakh-memory",
      basePath: "../GOLE YAKH MEMORY/",
      label: "GOLE YAKH MEMORY",
      subtitle: "Ice-flower memory / rooftop tea smoke / winter postcard radio",
      accentA: "#8bb8d6",
      accentB: "#d9c19a",
      coverImage: "../GOLE YAKH MEMORY/Gemini_Generated_Image_52klu552klu552kl.png",
      defaultTrackArt: "../GOLE YAKH MEMORY/Gemini_Generated_Image_m83fnzm83fnzm83f.png",
      hallKey: "goleyakh",
      op2Key: "goleyakh",
      op2Pair: "mitte",
      files: [
        "Gole Yakh Memory - Acetate Dreams - Sonauto.ogg",
        "Gole Yakh Memory - Anthropophagic Radio - Sonauto.ogg",
        "Gole Yakh Memory - Bare Hands and Steel Strings - Sonauto.ogg",
        "Gole Yakh Memory - Blueprint of the Soul - Sonauto.ogg",
        "Gole Yakh Memory - Crate Digging Lineage - Sonauto.ogg",
        "Gole Yakh Memory - Digital Lonesome - Sonauto.ogg",
        "Gole Yakh Memory - District Tizita - Sonauto.ogg",
        "Gole Yakh Memory - Dust on the Lens - Sonauto.ogg",
        "Gole Yakh Memory - Dusty Attic Gold - Sonauto.ogg",
        "Gole Yakh Memory - Garden of the Sun - Sonauto (1).ogg",
        "Gole Yakh Memory - Garden of the Sun - Sonauto.ogg",
        "Gole Yakh Memory - Greenhouse Groove - Sonauto.ogg",
        "Gole Yakh Memory - Hardwood Circuitry - Sonauto.ogg",
        "Gole Yakh Memory - High Register Bloom - Sonauto.ogg",
        "Gole Yakh Memory - Highland Haze - Sonauto.ogg",
        "Gole Yakh Memory - Iron in the Mud - Sonauto.ogg",
        "Gole Yakh Memory - Kinetic Tuscany - Sonauto.ogg",
        "Gole Yakh Memory - Limestone and Red Clay - Sonauto.ogg",
        "Gole Yakh Memory - Memphis Clay - Sonauto.ogg",
        "Gole Yakh Memory - Mogadishu Midnight Swirl - Sonauto.ogg",
        "Gole Yakh Memory - Pacific Thunder - Sonauto.ogg",
        "Gole Yakh Memory - Red Dirt Digital - Sonauto.ogg",
        "Gole Yakh Memory - Rooted in the Concrete - Sonauto.ogg",
        "Gole Yakh Memory - Sand and the Spree - Sonauto.ogg",
        "Gole Yakh Memory - Savannah High-Tech - Sonauto.ogg",
        "Gole Yakh Memory - Silk and Voltage - Sonauto.ogg",
        "Gole Yakh Memory - Silver Mist and Pine - Sonauto.ogg",
        "Gole Yakh Memory - Silver Song Throat - Sonauto.ogg",
        "Gole Yakh Memory - Spirit of the Harbor - Sonauto.ogg",
        "Gole Yakh Memory - Taka Heat - Sonauto.ogg",
        "Gole Yakh Memory - The Avenue Slant - Sonauto.ogg",
        "Gole Yakh Memory - The Garden Wakes - Sonauto.ogg",
        "Gole Yakh Memory - The King's Migration - Sonauto.ogg",
        "Gole Yakh Memory - The Munich Pulse - Sonauto.ogg",
        "Gole Yakh Memory - The National Theatre Ghost - Sonauto.ogg",
        "Gole Yakh Memory - The Nomad's Razor - Sonauto.ogg",
        "Gole Yakh Memory - The Samovar and the Stone - Sonauto.ogg",
        "Gole Yakh Memory - The Sinking Cradle - Sonauto.ogg",
        "Gole Yakh Memory - Tide Pulling Home - Sonauto.ogg",
        "Gole Yakh Memory - Tijuana Bloom - Sonauto.ogg",
        "Gole Yakh Memory - Top Deck Impressionism - Sonauto.ogg",
        "Gole Yakh Memory - Union Avenue Glow - Sonauto.ogg",
        "Gole Yakh Memory - Valley of the Dead Joe - Sonauto.ogg",
        "Gole Yakh Memory - Zion's Jazz-Rap Geometry - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Ice-flower memory / rooftop tea smoke / winter postcard radio"],
        ["Use", "Standalone album page, hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with GEOMETRIC GHOSTS OF MITTE for a winter-ghost contrast deck."]
      ]
    },
    concreto: {
      key: "concreto",
      pageSlug: "concreto",
      basePath: "../CONCRETO y CYPHER/",
      label: "CONCRETO",
      subtitle: "Barrio blueprint rap / resistance architecture / asphalt testimony",
      accentA: "#d98b57",
      accentB: "#d7d0c0",
      coverImage: "../CONCRETO y CYPHER/ChatGPT Image Mar 19, 2026, 02_35_09 AM.png",
      defaultTrackArt: "../CONCRETO y CYPHER/ChatGPT Image Mar 19, 2026, 02_35_09 AM.png",
      hallKey: "concreto",
      op2Key: "concreto",
      op2Pair: "cypher",
      files: [
        "Concreto y Cyphers - Warriors del Norte - Sonauto.ogg",
        "Concreto y Cyphers - Unidad en el Cypher - Sonauto.ogg",
        "Concreto y Cyphers - Zapatillas en el Cemento - Sonauto.ogg",
        "Concreto y Cyphers - Sangre y Zinc - Sonauto.ogg",
        "Concreto y Cyphers - Sueño Hondureño - Sonauto.ogg",
        "Concreto y Cyphers - The Knowledge Engine - Sonauto.ogg",
        "Concreto y Cyphers - Grito de Barrio - Sonauto.ogg",
        "Concreto y Cyphers - El Muro Gris (Resistencia) - Sonauto.ogg",
        "Concreto y Cyphers - De la Calle al Aula - Sonauto.ogg",
        "Concreto y Cyphers - B-Girl en Chamelecón - Sonauto.ogg",
        "Concreto y Cyphers - Arquitectura del Síntoma - Sonauto.ogg",
        "Concreto y Cyphers - Arquitectura del Poder - Sonauto.ogg",
        "Concreto y Cyphers - Arquitectura Anti-Gris - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Barrio blueprint rap / resistance masonry / street-knowledge relay"],
        ["Use", "Standalone album page, hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with CYPHER MIXTAPE for the split lyric/instrumental deck."]
      ]
    },
    cypher: {
      key: "cypher",
      pageSlug: "cypher-mixtape",
      basePath: "../CONCRETO y CYPHER/",
      label: "CYPHER MIXTAPE",
      subtitle: "Instrumental concrete breaks / ancestral machine drift / cypher-floor pressure",
      accentA: "#78d7d2",
      accentB: "#f0c56f",
      coverImage: "../CONCRETO y CYPHER/ChatGPT Image Mar 19, 2026, 02_21_19 AM.png",
      defaultTrackArt: "../CONCRETO y CYPHER/ChatGPT Image Mar 19, 2026, 02_21_19 AM.png",
      hallKey: "cypher",
      op2Key: "cypher",
      op2Pair: "concreto",
      files: [
        "Concreto y Cyphers - 5 Vidas en la Plaza - Sonauto.ogg",
        "Concreto y Cyphers - Andean Cypher Break - Sonauto.ogg",
        "Concreto y Cyphers - Arquitectura Invisible_ El Override del Muro - Sonauto.ogg",
        "Concreto y Cyphers - Atributos de Poder - Sonauto.ogg",
        "Concreto y Cyphers - Clay and Iron Ritual - Sonauto.ogg",
        "Concreto y Cyphers - El Quinto Elemento (Guerrero de Barro) - Sonauto.ogg",
        "Concreto y Cyphers - Juicio en el Cypher - Sonauto.ogg",
        "Concreto y Cyphers - La Máquina de Cypher Ancestral - Sonauto.ogg",
        "Concreto y Cyphers - La Máquina de Dios (Chamelecón) - Sonauto.ogg",
        "Concreto y Cyphers - Mayan Bronx Altar - Sonauto.ogg",
        "Concreto y Cyphers - Máquina de Cypher - Sonauto.ogg",
        "Concreto y Cyphers - Máquina de Dios (God Sort 'Em Out) - Sonauto.ogg",
        "Concreto y Cyphers - Máquina de Guerra (Ritual Mix) - Sonauto.ogg",
        "Concreto y Cyphers - Máquina de Guerra_ Himno de Asfalto - Sonauto.ogg",
        "Concreto y Cyphers - Monolito del Guerrero Vidente - Sonauto.ogg",
        "Concreto y Cyphers - Resiliencia Rítmica (Del Altiplano al Bronx) - Sonauto.ogg",
        "Concreto y Cyphers - Resistencia Ancestral (92 BPM) - Sonauto.ogg",
        "Concreto y Cyphers - Stone and Concrete Spirit - Sonauto.ogg",
        "Concreto y Cyphers - The Cypher of the Andes - Sonauto.ogg",
        "Concreto y Cyphers - Trote de Cipher - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Instrumental cypher relay / concrete percussion / ancestral machine breakwork"],
        ["Use", "Standalone album page, hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with CONCRETO for the full split-catalog deck."]
      ]
    },
    usblegacy: {
      key: "usblegacy",
      pageSlug: "usb-legacy",
      basePath: "../USB LEGACY - FERROUS LAMENT/",
      label: "USB LEGACY",
      subtitle: "Shipyard catharsis / rust-water devotion / salvage-memory circuitry",
      accentA: "#cf6f3b",
      accentB: "#4ab7bb",
      coverImage: "../USB LEGACY - FERROUS LAMENT/usb-legacy-00.png",
      defaultTrackArt: "../USB LEGACY - FERROUS LAMENT/usb-legacy-01.png",
      hallKey: "usblegacy",
      op2Key: "usblegacy",
      op2Pair: "ferrous",
      files: [
        "USB Legacy - Iron Into Dust - Sonauto.ogg",
        "USB Legacy - Blood & Iron Debt - Sonauto.ogg",
        "USB Legacy - Chemical Ignition - Sonauto.ogg",
        "USB Legacy - Corazoncito (Stadium Love) - Sonauto.ogg",
        "USB Legacy - Extraction Ceremony - Sonauto.ogg",
        "USB Legacy - Grace Through Erosion - Sonauto.ogg",
        "USB Legacy - Hull Creak Ritual - Sonauto.ogg",
        "USB Legacy - Hull Creaks and Healing - Sonauto.ogg",
        "USB Legacy - Icaro of the Shipyard - Sonauto.ogg",
        "USB Legacy - Oceans Through Our Eyes - Sonauto.ogg",
        "USB Legacy - Óxido y Sangre (El Abrazo) - Sonauto.ogg",
        "USB Legacy - Relational Radiance - Sonauto.ogg",
        "USB Legacy - Ritual Decay - Sonauto.ogg",
        "USB Legacy - Rust and Rebirth - Sonauto.ogg",
        "USB Legacy - Rusted Rituals - Sonauto.ogg",
        "USB Legacy - Slow Motion Fire - Sonauto.ogg",
        "USB Legacy - Submerged Prayer - Sonauto.ogg",
        "USB Legacy - The A Cappella Catharsis - Sonauto.ogg",
        "USB Legacy - The Machine Finds Soul - Sonauto.ogg",
        "USB Legacy - The USB Handoff - Sonauto.ogg",
        "USB Legacy - Tribal Stadium Catharsis - Sonauto.ogg",
        "USB Legacy - Water Light Alive - Sonauto.ogg",
        "USB Legacy - Water Light Finale - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Shipyard catharsis / rust-water devotion / salvage-memory circuitry"],
        ["Use", "Standalone album page, hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with FERROUS LAMENT for the split-catalog rust/abyss deck."]
      ]
    },
    ferrous: {
      key: "ferrous",
      pageSlug: "ferrous-lament",
      basePath: "../USB LEGACY - FERROUS LAMENT/",
      label: "FERROUS LAMENT",
      subtitle: "Abyssal requiems / oxidized signal prayer / rusted-airwave mourning",
      accentA: "#53c1c0",
      accentB: "#d47a49",
      coverImage: "../USB LEGACY - FERROUS LAMENT/ferrous-lament-00.png",
      defaultTrackArt: "../USB LEGACY - FERROUS LAMENT/Gemini_Generated_Image_p5m3oop5m3oop5m3.png",
      hallKey: "ferrous",
      op2Key: "ferrous",
      op2Pair: "usblegacy",
      files: [
        "Ferrous Lament - Ferrous Pressure - Sonauto.ogg",
        "Ferrous Lament - Iron Dust Falling - Sonauto.ogg",
        "Ferrous Lament - Oxide Rising - Sonauto.ogg",
        "Ferrous Lament - The Magnetic Skeleton - Sonauto.ogg",
        "Ferrous Lament - The Oxide Pulse - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Abyssal requiems / oxidized signal prayer / rusted-airwave mourning"],
        ["Use", "Standalone album page, hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with USB LEGACY for the salvage-memory companion deck."]
      ]
    },
    congregation: {
      key: "congregation",
      pageSlug: "great-congregation",
      basePath: "../THE GREAT CONGREGATION/",
      label: "THE GREAT CONGREGATION",
      subtitle: "Malian pulse / fractured cathedral / crate-digger bounce",
      accentA: "#a8b882",
      accentB: "#d9c58b",
      coverImage: "../THE GREAT CONGREGATION/ChatGPT Image Apr 15, 2026, 12_53_47 AM.png",
      defaultTrackArt: "../THE GREAT CONGREGATION/Gemini_Generated_Image_ (2).png",
      hallKey: "congregation",
      op2Key: "congregation",
      op2Pair: "goleyakh",
      files: [
        "The Great Congregation - 82 BPM Blues Bash - Sonauto.ogg",
        "The Great Congregation - Bamako Midnight Dialogue - Sonauto.ogg",
        "The Great Congregation - Calyx Rhythm - Sonauto.ogg",
        "The Great Congregation - Crate Digger Bounce - Sonauto.ogg",
        "The Great Congregation - Dusty Bass Revolution - Sonauto.ogg",
        "The Great Congregation - Echoes of the Tamani - Sonauto.ogg",
        "The Great Congregation - Fractured Cathedral - Sonauto.ogg",
        "The Great Congregation - Homebound Loop - Sonauto.ogg",
        "The Great Congregation - Kitchen Prep at Dawn - Sonauto.ogg",
        "The Great Congregation - Malian Pulse - Sonauto.ogg",
        "The Great Congregation - Midnight Monitor Glow - Sonauto.ogg",
        "The Great Congregation - Rope Burns - Sonauto.ogg",
        "The Great Congregation - The Master's Zenith - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Malian pulse / fractured cathedral / crate-digger bounce"],
        ["Use", "Standalone album page, hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with GOLE YAKH MEMORY for the nocturne-memory companion deck."]
      ]
    },
    maquina: {
      key: "maquina",
      pageSlug: "maquina-de-guerra",
      basePath: "../Máquina de Guerra/",
      label: "MÁQUINA DE GUERRA",
      subtitle: "Warrior-state broadcasts / desert-fire circuitry / saffron threshold pressure",
      accentA: "#ef6f2d",
      accentB: "#8a9551",
      coverImage: "../Máquina de Guerra/WhatsApp Image 2026-04-17 at 06.11.03 (3).jpeg",
      defaultTrackArt: "../Máquina de Guerra/WhatsApp Image 2026-04-17 at 06.11.03 (4).jpeg",
      hallKey: "maquina",
      op2Key: "maquina",
      op2Pair: "cypher",
      files: [
        "Máquina de Guerra - Acid Logic - Sonauto (1).ogg",
        "Máquina de Guerra - Acid Logic - Sonauto.ogg",
        "Máquina de Guerra - Across the Shore of Names - Sonauto.ogg",
        "Máquina de Guerra - Agua Bendita Trap - Sonauto.ogg",
        "Máquina de Guerra - Circuits of Grace - Sonauto.ogg",
        "Máquina de Guerra - Conditions of the Warrior - Sonauto.ogg",
        "Máquina de Guerra - Dust and Light - Sonauto.ogg",
        "Máquina de Guerra - El Acecho del Viento - Sonauto.ogg",
        "Máquina de Guerra - Fréquence Nocturne - Sonauto.ogg",
        "Máquina de Guerra - Gone with the Tide - Sonauto.ogg",
        "Máquina de Guerra - Hold Yuh Fire - Sonauto.ogg",
        "Máquina de Guerra - Holy 808s - Sonauto.ogg",
        "Máquina de Guerra - Midnight Borough FM - Sonauto.ogg",
        "Máquina de Guerra - Mountain Passing - Sonauto.ogg",
        "Máquina de Guerra - No Scatter - Sonauto.ogg",
        "Máquina de Guerra - O Caminho do Bruxo - Sonauto.ogg",
        "Máquina de Guerra - Orange Fire in the Hall - Sonauto.ogg",
        "Máquina de Guerra - Pacific Drift - Sonauto.ogg",
        "Máquina de Guerra - Rolling Wisdom Waddup - Sonauto.ogg",
        "Máquina de Guerra - Saffron Dawn Sky - Sonauto.ogg",
        "Máquina de Guerra - Selected States - Sonauto.ogg",
        "Máquina de Guerra - Silk and String - Sonauto.ogg",
        "Máquina de Guerra - Soldado da Unção - Sonauto.ogg",
        "Máquina de Guerra - Sombra do Deserto - Sonauto.ogg",
        "Máquina de Guerra - The Cost of the Breath - Sonauto.ogg",
        "Máquina de Guerra - The Loose Knot - Sonauto.ogg",
        "Máquina de Guerra - The Magnetic Head - Sonauto.ogg",
        "Máquina de Guerra - The Rotund King - Sonauto.ogg",
        "Máquina de Guerra - The Saffron Threshold - Sonauto.ogg",
        "Máquina de Guerra - The Salty Cup - Sonauto.ogg",
        "Máquina de Guerra - Valley of Dry Bones - Sonauto.ogg",
        "Máquina de Guerra - Who Sabi Hold Body - Sonauto.ogg",
        "Máquina de Guerra - המדבר מדבר - Sonauto.ogg",
        "Máquina de Guerra - اتقان المحارب (Warrior's Mastery) - Sonauto.ogg",
        "Máquina de Guerra - طريق القوة (The Path of Power) - Sonauto.ogg",
        "Máquina de Guerra - ኃይል አደን (Hunting Power) - Sonauto.ogg",
        "Máquina de Guerra - የተዋጊው ንጽህና (Warrior's Impeccability) - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Warrior-state broadcasts / desert-fire circuitry / saffron threshold pressure"],
        ["Use", "Standalone album page, hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with CYPHER MIXTAPE for a militant asphalt-breaks companion deck."]
      ]
    },
    blackwater: {
      key: "blackwater",
      pageSlug: "black-water-run",
      basePath: "../BLACK WATER RUN/",
      label: "BLACK WATER RUN",
      subtitle: "Frog-noir escapes / jade seawall static / alleyway pursuit soul",
      accentA: "#61788f",
      accentB: "#d7dce0",
      coverImage: "../BLACK WATER RUN/ChatGPT Image Apr 21, 2026, 11_35_30 PM.png",
      defaultTrackArt: "../BLACK WATER RUN/ChatGPT Image Apr 21, 2026, 11_35_47 PM.png",
      hallKey: "blackwater",
      op2Key: "blackwater",
      op2Pair: "heishui",
      files: [
        "Black Water Run - A Chinese Good Man (Main Theme) - Sonauto.ogg",
        "Black Water Run - Amphibian Escape & Concrete Smoke - Sonauto.ogg",
        "Black Water Run - Amphibian Noir (The Hard Cut) - Sonauto.ogg",
        "Black Water Run - Baja Jade Night - Sonauto.ogg",
        "Black Water Run - Concrete Alley Soul - Sonauto.ogg",
        "Black Water Run - Concrete Exhale (Searchlight Halation) - Sonauto.ogg",
        "Black Water Run - Concrete Exhale - Sonauto.ogg",
        "Black Water Run - Deep Sea Monarchy - Sonauto.ogg",
        "Black Water Run - Ghost City Dynasty - Sonauto.ogg",
        "Black Water Run - Gray Alley Slow Drag - Sonauto.ogg",
        "Black Water Run - Midnight Evasion - Sonauto.ogg",
        "Black Water Run - Night Wake (Spotlight Halation) - Sonauto.ogg",
        "Black Water Run - Nylon and Jade - Sonauto.ogg",
        "Black Water Run - Ocean Palace Static - Sonauto.ogg",
        "Black Water Run - Red Lanterns over the Malecon - Sonauto.ogg",
        "Black Water Run - Static Smoke Phase - Sonauto.ogg",
        "Black Water Run - Tectonic Wake, Static Smoke - Sonauto.ogg",
        "Black Water Run - The Good Man's Jasmine Draught - Sonauto.ogg",
        "Black Water Run - The Sea To The Alleyway - Sonauto.ogg",
        "Black Water Run - The Shadow of the Alley - Sonauto.ogg",
        "Black Water Run - The Soulful Good Man (Philly Fusion) - Sonauto.ogg",
        "Black Water Run - Vinilo de Sangre y Sal - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Frog-noir escapes / jade seawall static / alleyway pursuit soul"],
        ["Use", "Standalone album page, hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with 黑水奔流 for the sister-river companion deck."]
      ]
    },
    heishui: {
      key: "heishui",
      pageSlug: "hei-shui-ben-liu",
      basePath: "../黑水奔流/",
      label: "黑水奔流",
      subtitle: "Red-squall river noir / canal fugues / good-man afterimages",
      accentA: "#c64534",
      accentB: "#8ca6c6",
      coverImage: "../黑水奔流/ChatGPT Image Apr 21, 2026, 11_36_08 PM.png",
      defaultTrackArt: "../黑水奔流/ChatGPT Image Apr 21, 2026, 11_36_13 PM.png",
      hallKey: "heishui",
      op2Key: "heishui",
      op2Pair: "blackwater",
      files: [
        "Black Water Run - Chinese Good Man - Sonauto.ogg",
        "Black Water Run - Lao Li's Iron Lighter - Sonauto.ogg",
        "Black Water Run - Old Li of the Alley - Sonauto.ogg",
        "Black Water Run - The Breath of Uselessness - Sonauto.ogg",
        "Black Water Run - 中国好人 (Chinese Good Man) - Sonauto.ogg",
        "Black Water Run - 中国好人 (Good Man) - Sonauto.ogg",
        "Black Water Run - 中国好人 (The Good Man) - Sonauto.ogg",
        "Black Water Run - 因果律动 (Yinguo Rhythm) - Sonauto.ogg",
        "Black Water Run - 消散 (Dissipation) - Sonauto.ogg",
        "Black Water Run - 骏马与烟灰的叙事曲 - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Red-squall river noir / canal fugues / good-man afterimages"],
        ["Use", "Standalone album page, hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with BLACK WATER RUN for the English-title mirror deck."]
      ]
    },
    executable: {
      key: "executable",
      pageSlug: "executable-infrastructure-dub",
      basePath: "../Executable Infrastructure Dub/",
      label: "Executable Infrastructure Dub",
      subtitle: "Canopy infrastructure dub / steel and fiber rhythms / the regulation paradox",
      accentA: "#6b8f7c",
      accentB: "#a8c4b0",
      coverImage: "../Executable Infrastructure Dub/ChatGPT Image May 4, 2026, 07_37_48 PM.png",
      defaultTrackArt: "../Executable Infrastructure Dub/ChatGPT Image May 4, 2026, 07_37_48 PM.png",
      hallKey: "executable",
      op2Key: "executable",
      op2Pair: "mall",
      files: [
        "Executable Infrastructure Dub - Canopy Deep - Sonauto.ogg",
        "Executable Infrastructure Dub - Cristal en el Celular - Sonauto.ogg",
        "Executable Infrastructure Dub - Dead Glass Loop - Sonauto.ogg",
        "Executable Infrastructure Dub - Fiber and Steel - Sonauto.ogg",
        "Executable Infrastructure Dub - Root Symmetry - Sonauto.ogg",
        "Executable Infrastructure Dub - Sharp Blade Heavy Bass - Sonauto.ogg",
        "Executable Infrastructure Dub - Sharp Edge Logic - Sonauto.ogg",
        "Executable Infrastructure Dub - Small Axe (Rebel Cut) - Sonauto.ogg",
        "Executable Infrastructure Dub - Small Axe Blade - Sonauto.ogg",
        "Executable Infrastructure Dub - Small Axe Warning - Sonauto.ogg",
        "Executable Infrastructure Dub - The Afterlife of Wood - Sonauto.ogg",
        "Executable Infrastructure Dub - The Feller's Skank - Sonauto.ogg",
        "Executable Infrastructure Dub - The Landlord's Sky - Sonauto.ogg",
        "Executable Infrastructure Dub - The Regulation Paradox - Sonauto.ogg",
        "Executable Infrastructure Dub - The Small Axe Swing - Sonauto.ogg",
        "Executable Infrastructure Dub - The Spectacle Indictment - Sonauto.ogg",
        "Executable Infrastructure Dub - The Unstable Afterlife - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Canopy infrastructure dub / steel and fiber rhythms / the regulation paradox"],
        ["Use", "Standalone album page, hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with MALL PATCHWORLD for the infrastructure-consumer contrast deck."]
      ]
    },
    queen: {
      key: "queen",
      pageSlug: "queen-of-light",
      basePath: "../QUEEN of LIGHT/",
      label: "QUEEN OF LIGHT",
      subtitle: "Gilded frog radio / gospel birds / graduate funk transmissions",
      accentA: "#f2c14e",
      accentB: "#1f6f4a",
      coverImage: "../QUEEN of LIGHT/ChatGPT Image May 7, 2026, 06_08_44 PM.png",
      defaultTrackArt: "../QUEEN of LIGHT/ChatGPT Image May 7, 2026, 06_18_43 PM.png",
      hallKey: "queen",
      op2Key: "queen",
      op2Pair: "congregation",
      files: [
        "Queen of Light - EBITDA & Funk - Sonauto.ogg",
        "Queen of Light - Gold Graduation Groove - Sonauto.ogg",
        "Queen of Light - Golden Terrace - Sonauto.ogg",
        "Queen of Light - Queen of Light Transmission - Sonauto.ogg",
        "Queen of Light - Silicon Harvest - Sonauto.ogg",
        "Queen of Light - Swamp Star Frequency - Sonauto.ogg",
        "Queen of Light - The Atlanta Graduate - Sonauto.ogg",
        "Queen of Light - The Divine Abyss - Sonauto.ogg",
        "Queen of Light - The Gospel of Birds - Sonauto.ogg",
        "Queen of Light - The Higher Order (Tibelet) - Sonauto.ogg",
        "Queen of Light - The Real Appetite - Sonauto.ogg",
        "Queen of Light - The Rise of Tiblitz - Sonauto.ogg",
        "Queen of Light - Tibelet (Morning Message) - Sonauto.ogg",
        "Queen of Light - Tibelet (Ye-Dil Zewd) - Sonauto.ogg",
        "Queen of Light - ልቃ የተገኘች (Greater Excellence) - Sonauto.ogg",
        "Queen of Light - ትብለጥ በክብር (Tiblitz Excels) - Sonauto.ogg",
        "Queen of Light - የድል አርማ (Victory Banner) - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Gilded frog radio / gospel birds / graduate funk transmissions"],
        ["Use", "Standalone album page, hall route, and direct song-page links for each cut."],
        ["OP2 Pair", "Launch with THE GREAT CONGREGATION for gospel-funk contrast."]
      ]
    },
    rootresidue: {
      key: "rootresidue",
      pageSlug: "root-and-residue",
      basePath: "../ROOT AND RESIDUE/",
      label: "ROOT AND RESIDUE",
      subtitle: "Family room fieldwork / porch-light funk / resin memory rituals",
      accentA: "#8f6f3a",
      accentB: "#c7a66a",
      coverImage: "../ROOT AND RESIDUE/ChatGPT Image May 10, 2026, 01_17_36 PM (1).png",
      defaultTrackArt: "../ROOT AND RESIDUE/ChatGPT Image May 10, 2026, 01_17_36 PM (2).png",
      trackArtByIndex: {
        0: "../ROOT AND RESIDUE/ChatGPT Image May 10, 2026, 01_17_36 PM (1).png",
        1: "../ROOT AND RESIDUE/ChatGPT Image May 10, 2026, 01_17_36 PM (2).png",
        2: "../ROOT AND RESIDUE/ChatGPT Image May 10, 2026, 01_17_37 PM (3).png",
        3: "../ROOT AND RESIDUE/ChatGPT Image May 10, 2026, 01_17_37 PM (4).png",
        4: "../ROOT AND RESIDUE/ChatGPT Image May 10, 2026, 01_17_37 PM (5).png",
        5: "../ROOT AND RESIDUE/ChatGPT Image May 10, 2026, 01_17_37 PM (6).png",
        6: "../ROOT AND RESIDUE/ChatGPT Image May 10, 2026, 01_17_38 PM (7).png",
        7: "../ROOT AND RESIDUE/ChatGPT Image May 10, 2026, 01_17_38 PM (8).png",
        8: "../ROOT AND RESIDUE/ChatGPT Image May 10, 2026, 01_17_38 PM (9).png",
        9: "../ROOT AND RESIDUE/ChatGPT Image May 10, 2026, 01_17_39 PM (10).png",
        10: "../ROOT AND RESIDUE/ChatGPT Image May 10, 2026, 01_17_36 PM (1).png",
        11: "../ROOT AND RESIDUE/ChatGPT Image May 10, 2026, 01_17_36 PM (2).png",
        12: "../ROOT AND RESIDUE/ChatGPT Image May 10, 2026, 01_17_37 PM (3).png",
        13: "../ROOT AND RESIDUE/ChatGPT Image May 10, 2026, 01_17_37 PM (4).png",
        14: "../ROOT AND RESIDUE/ChatGPT Image May 10, 2026, 01_17_37 PM (5).png",
        15: "../ROOT AND RESIDUE/ChatGPT Image May 10, 2026, 01_17_37 PM (6).png"
      },
      hallKey: "rootresidue",
      op2Key: "rootresidue",
      op2Pair: "queen",
      files: [
        "Root and Residue - The House Says Thanks - Sonauto.ogg",
        "Root and Residue - Agua de la Madre - Sonauto.ogg",
        "Root and Residue - Blue Nap Rhythm - Sonauto.ogg",
        "Root and Residue - Deep in the Sand - Sonauto.ogg",
        "Root and Residue - Golden Light Sanctuary - Sonauto.ogg",
        "Root and Residue - Living Room Queen - Sonauto.ogg",
        "Root and Residue - Machete Lullaby - Sonauto.ogg",
        "Root and Residue - Minivan F.C. - Sonauto.ogg",
        "Root and Residue - Rhinestones and Resin - Sonauto.ogg",
        "Root and Residue - Super-8 Couch Stomp - Sonauto.ogg",
        "Root and Residue - The Deepest Root - Sonauto.ogg",
        "Root and Residue - The House Says Thank You - Sonauto.ogg",
        "Root and Residue - The Way I Am (Mother's Groove) - Sonauto.ogg",
        "Root and Residue - Third Row Glory - Sonauto.ogg",
        "Root and Residue - This Is My Mother Resting - Sonauto.ogg",
        "Root and Residue - Wool and Willow - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Family room fieldwork / porch-light funk / resin memory rituals"],
        ["Use", "Standalone album page, hall route, and direct song-page links for every cut."],
        ["OP2 Pair", "Launch with QUEEN OF LIGHT for the family-light counterweight deck."]
      ]
    },
    betterhands: {
      key: "betterhands",
      pageSlug: "better-hands",
      basePath: "../BETTER HANDS/",
      label: "BETTER HANDS",
      subtitle: "Machine witness / repair testimony / hands-on signal work",
      accentA: "#d86a4a",
      accentB: "#f2c66d",
      coverImage: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_37_40 AM.png",
      defaultTrackArt: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_50_10 AM.png",
      trackArtByIndex: {
        0: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_37_40 AM.png",
        1: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_50_10 AM.png",
        2: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_30_44 AM.png",
        3: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_31_57 AM.png",
        4: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_25_30 AM.png",
        5: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_37_40 AM.png",
        6: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_50_10 AM.png",
        7: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_30_44 AM.png",
        8: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_31_57 AM.png",
        9: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_25_30 AM.png",
        10: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_37_40 AM.png",
        11: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_50_10 AM.png",
        12: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_30_44 AM.png",
        13: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_31_57 AM.png",
        14: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_25_30 AM.png",
        15: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_37_40 AM.png"
      },
      hallKey: "betterhands",
      op2Key: "betterhands",
      op2Pair: "rootresidue",
      files: [
        "Better Hands - Better Hands - Sonauto.ogg",
        "Better Hands - Sharper Hands - Sonauto.ogg",
        "Better Hands - Hands Upon The Wheel - Sonauto.ogg",
        "Better Hands - Fingerprints in the Silicon - Sonauto.ogg",
        "Better Hands - The Machine Heard Me First - Sonauto.ogg",
        "Better Hands - Machines of Migration - Sonauto.ogg",
        "Better Hands - The Prompt Log Brick - Sonauto.ogg",
        "Better Hands - Through the Sentence - Sonauto.ogg",
        "Better Hands - The Wound and the Mirror - Sonauto.ogg",
        "Better Hands - Visible Repair - Sonauto.ogg",
        "Better Hands - Salt in the Signal - Sonauto.ogg",
        "Better Hands - Pocket Receipts - Sonauto.ogg",
        "Better Hands - Appliance Prayer - Sonauto.ogg",
        "Better Hands - The Defiant Podium - Sonauto.ogg",
        "Better Hands - The Defiant Podium - Sonauto (1).ogg",
        "Better Hands - Blood on the Ice - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Machine witness / repair testimony / hands-on signal work"],
        ["Use", "Standalone album page, hall route, and direct song-page links for every cut."],
        ["OP2 Pair", "Launch with ROOT AND RESIDUE for a repair-memory counterweight deck."]
      ]
    },
    sharperhands: {
      key: "sharperhands",
      pageSlug: "sharper-hands",
      basePath: "../BETTER HANDS/",
      label: "SHARPER HANDS",
      subtitle: "Sharper repair edits / prompt-prune testimony / cool radio revision work",
      accentA: "#9b3028",
      accentB: "#e7dbc6",
      coverImage: "../BETTER HANDS/ChatGPT Image May 13, 2026, 01_48_46 AM.png",
      defaultTrackArt: "../BETTER HANDS/ChatGPT Image May 13, 2026, 01_48_46 AM.png",
      trackArtByIndex: {
        0: "../BETTER HANDS/ChatGPT Image May 13, 2026, 01_48_46 AM.png",
        1: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_30_44 AM.png",
        2: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_31_57 AM.png",
        3: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_25_30 AM.png",
        4: "../BETTER HANDS/ChatGPT Image May 13, 2026, 01_48_46 AM.png",
        5: "../BETTER HANDS/ChatGPT Image May 13, 2026, 12_37_40 AM.png"
      },
      hallKey: "sharperhands",
      op2Key: "sharperhands",
      op2Pair: "betterhands",
      files: [
        "Better Hands - Sharper Hands - Sonauto.ogg",
        "Better Hands - Through the Sentence - Sonauto.ogg",
        "Better Hands - Fingerprints in the Silicon - Sonauto.ogg",
        "Better Hands - The Wound and the Mirror - Sonauto.ogg",
        "Better Hands - Visible Repair - Sonauto.ogg",
        "Better Hands - The Defiant Podium - Sonauto (1).ogg"
      ],
      notes: [
        ["Mode", "Sharper repair edits / prompt-prune testimony / cool radio revision work"],
        ["Use", "Standalone alternate album page with direct song-page links for the sharper sequence."],
        ["OP2 Pair", "Launch with BETTER HANDS for the version-to-version repair deck."]
      ]
    },
    nobrightstand: {
      key: "nobrightstand",
      pageSlug: "no-bright-stand",
      basePath: "../NO BRIGHT STAND/",
      label: "NO BRIGHT STAND",
      subtitle: "Domestic absurd / grid anxiety / frictionless convenience blues",
      accentA: "#d5b365",
      accentB: "#7aa3a0",
      coverImage: "../NO BRIGHT STAND/b8dd5072-7cf1-4b91-98d8-6d02d5f59061.png",
      defaultTrackArt: "../NO BRIGHT STAND/Gemini_Generated_Image_hwsm4khwsm4khwsm.jpeg",
      trackArtByIndex: {
        0: "../NO BRIGHT STAND/b8dd5072-7cf1-4b91-98d8-6d02d5f59061.png",
        1: "../NO BRIGHT STAND/Gemini_Generated_Image_hwsm4khwsm4khwsm.jpeg",
        2: "../NO BRIGHT STAND/Gemini_Generated_Image_dl0ppsdl0ppsdl0p.jpeg",
        3: "../NO BRIGHT STAND/ChatGPT Image May 18, 2026, 07_00_25 PM.png",
        4: "../NO BRIGHT STAND/ChatGPT Image May 18, 2026, 07_02_59 PM.png",
        5: "../NO BRIGHT STAND/Gemini_Generated_Image_ilw0nrilw0nrilw0.jpeg",
        6: "../NO BRIGHT STAND/ChatGPT Image May 18, 2026, 07_02_47 PM.png",
        7: "../NO BRIGHT STAND/b8dd5072-7cf1-4b91-98d8-6d02d5f59061.png",
        8: "../NO BRIGHT STAND/Gemini_Generated_Image_hwsm4khwsm4khwsm.jpeg",
        9: "../NO BRIGHT STAND/Gemini_Generated_Image_dl0ppsdl0ppsdl0p.jpeg",
        10: "../NO BRIGHT STAND/ChatGPT Image May 18, 2026, 07_00_25 PM.png",
        11: "../NO BRIGHT STAND/ChatGPT Image May 18, 2026, 07_02_59 PM.png",
        12: "../NO BRIGHT STAND/Gemini_Generated_Image_ilw0nrilw0nrilw0.jpeg",
        13: "../NO BRIGHT STAND/ChatGPT Image May 18, 2026, 07_02_47 PM.png",
        14: "../NO BRIGHT STAND/b8dd5072-7cf1-4b91-98d8-6d02d5f59061.png",
        15: "../NO BRIGHT STAND/Gemini_Generated_Image_hwsm4khwsm4khwsm.jpeg",
        16: "../NO BRIGHT STAND/Gemini_Generated_Image_dl0ppsdl0ppsdl0p.jpeg",
        17: "../NO BRIGHT STAND/ChatGPT Image May 18, 2026, 07_00_25 PM.png",
        18: "../NO BRIGHT STAND/ChatGPT Image May 18, 2026, 07_02_59 PM.png",
        19: "../NO BRIGHT STAND/Gemini_Generated_Image_ilw0nrilw0nrilw0.jpeg",
        20: "../NO BRIGHT STAND/ChatGPT Image May 18, 2026, 07_02_47 PM.png",
        21: "../NO BRIGHT STAND/b8dd5072-7cf1-4b91-98d8-6d02d5f59061.png",
        22: "../NO BRIGHT STAND/Gemini_Generated_Image_hwsm4khwsm4khwsm.jpeg",
        23: "../NO BRIGHT STAND/Gemini_Generated_Image_dl0ppsdl0ppsdl0p.jpeg",
        24: "../NO BRIGHT STAND/ChatGPT Image May 18, 2026, 07_00_25 PM.png",
        25: "../NO BRIGHT STAND/ChatGPT Image May 18, 2026, 07_02_59 PM.png",
        26: "../NO BRIGHT STAND/Gemini_Generated_Image_ilw0nrilw0nrilw0.jpeg",
        27: "../NO BRIGHT STAND/ChatGPT Image May 18, 2026, 07_02_47 PM.png",
        28: "../NO BRIGHT STAND/b8dd5072-7cf1-4b91-98d8-6d02d5f59061.png",
        29: "../NO BRIGHT STAND/Gemini_Generated_Image_hwsm4khwsm4khwsm.jpeg",
        30: "../NO BRIGHT STAND/Gemini_Generated_Image_dl0ppsdl0ppsdl0p.jpeg",
        31: "../NO BRIGHT STAND/ChatGPT Image May 18, 2026, 07_00_25 PM.png",
        32: "../NO BRIGHT STAND/ChatGPT Image May 18, 2026, 07_02_59 PM.png",
        33: "../NO BRIGHT STAND/Gemini_Generated_Image_ilw0nrilw0nrilw0.jpeg",
        34: "../NO BRIGHT STAND/ChatGPT Image May 18, 2026, 07_02_47 PM.png",
        35: "../NO BRIGHT STAND/b8dd5072-7cf1-4b91-98d8-6d02d5f59061.png",
        36: "../NO BRIGHT STAND/Gemini_Generated_Image_hwsm4khwsm4khwsm.jpeg",
        37: "../NO BRIGHT STAND/Gemini_Generated_Image_dl0ppsdl0ppsdl0p.jpeg",
        38: "../NO BRIGHT STAND/ChatGPT Image May 18, 2026, 07_00_25 PM.png",
        39: "../NO BRIGHT STAND/ChatGPT Image May 18, 2026, 07_02_59 PM.png",
        40: "../NO BRIGHT STAND/Gemini_Generated_Image_ilw0nrilw0nrilw0.jpeg",
        41: "../NO BRIGHT STAND/ChatGPT Image May 18, 2026, 07_02_47 PM.png"
      },
      hallKey: "nobrightstand",
      op2Key: "nobrightstand",
      op2Pair: "dustrest",
      files: [
        "No Bright Stand - The Yard Sign Blues (Slide Ten Says) - Sonauto.ogg",
        "No Bright Stand - The Hypocrite’s Mask - Sonauto.ogg",
        "No Bright Stand - The Evidence of Hands - Sonauto.ogg",
        "No Bright Stand - Microscopic Morse Code - Sonauto.ogg",
        "No Bright Stand - Laundry Day Epiphany - Sonauto.ogg",
        "No Bright Stand - The Meat Suit Maintenance - Sonauto.ogg",
        "No Bright Stand - The Fourteen Dollar Smoothie - Sonauto.ogg",
        "No Bright Stand - Velocities of Bone and Smoke - Sonauto.ogg",
        "No Bright Stand - Dust Settling in the Empty Room - Sonauto.ogg",
        "No Bright Stand - The Machine Inherited Ours - Sonauto.ogg",
        "No Bright Stand - Retention King - Sonauto.ogg",
        "No Bright Stand - Drop The Rag In Three Tongues - Sonauto.ogg",
        "No Bright Stand - Glass or Surface - Sonauto.ogg",
        "No Bright Stand - Laundry Basket Politics - Sonauto.ogg",
        "No Bright Stand - The Physical Reality - Sonauto.ogg",
        "No Bright Stand - The Arsonist's Architecture - Sonauto.ogg",
        "No Bright Stand - The Digestion Ritual - Sonauto.ogg",
        "No Bright Stand - Sandy Cubicle - Sonauto.ogg",
        "No Bright Stand - Spoon and the Ocean - Sonauto.ogg",
        "No Bright Stand - The Apex of Convenience - Sonauto.ogg",
        "No Bright Stand - The Grid's Children - Sonauto.ogg",
        "No Bright Stand - Modern Ephemera (Vinyl Dust) - Sonauto.ogg",
        "No Bright Stand - Frictionless Release - Sonauto.ogg",
        "No Bright Stand - The Terms and Conditions of Living - Sonauto.ogg",
        "No Bright Stand - 支持性角色 (Supporting Character) - Sonauto.ogg",
        "No Bright Stand - Clinical Exhaustion - Sonauto.ogg",
        "No Bright Stand - Bandwidth (A Laundry Basket Epiphany) - Sonauto.ogg",
        "No Bright Stand - Patriots in Polyester - Sonauto.ogg",
        "No Bright Stand - The Geometry of the Cage - Sonauto.ogg",
        "No Bright Stand - Significant Data - Sonauto.ogg",
        "No Bright Stand - Voltage of the Grid - Sonauto.ogg",
        "No Bright Stand - The Algorithm Mirror - Sonauto.ogg",
        "No Bright Stand - Frictionless Awareness - Sonauto.ogg",
        "No Bright Stand - Things That Touch the Hand - Sonauto.ogg",
        "No Bright Stand - Activated Charcoal & Capital - Sonauto.ogg",
        "No Bright Stand - The Sky Sends an Invoice - Sonauto.ogg",
        "No Bright Stand - The Domestic Absurd - Sonauto.ogg",
        "No Bright Stand - The Shrimp Who Read Deleuze - Sonauto.ogg",
        "No Bright Stand - Market Research Hypocrisy - Sonauto.ogg",
        "No Bright Stand - A Mall Cop Guarding the Abyss - Sonauto.ogg",
        "No Bright Stand - Digital Middlemen - Sonauto.ogg",
        "No Bright Stand - The Janitor's Resignation - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Domestic absurd / grid anxiety / frictionless convenience blues"],
        ["Use", "Standalone album page, hall route, and direct song-page links for every cut."],
        ["OP2 Pair", "Launch with WHERE CAN DUST REST for the mirror-and-dust companion deck."]
      ]
    },
    dustrest: {
      key: "dustrest",
      pageSlug: "where-can-dust-rest",
      basePath: "../WHERE CAN DUST REST/",
      label: "WHERE CAN DUST REST",
      subtitle: "Mirror-dust doctrine / rice-field pulses / sudden awakening fieldwork",
      accentA: "#c6d4b4",
      accentB: "#7d8f73",
      coverImage: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_19_10 PM.png",
      defaultTrackArt: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_18_39 PM.png",
      trackArtByIndex: {
        0: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_19_10 PM.png",
        1: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_18_39 PM.png",
        2: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_19_10 PM.png",
        3: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_18_39 PM.png",
        4: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_19_10 PM.png",
        5: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_18_39 PM.png",
        6: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_19_10 PM.png",
        7: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_18_39 PM.png",
        8: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_19_10 PM.png",
        9: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_18_39 PM.png",
        10: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_19_10 PM.png",
        11: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_18_39 PM.png",
        12: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_19_10 PM.png",
        13: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_18_39 PM.png",
        14: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_19_10 PM.png",
        15: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_18_39 PM.png",
        16: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_19_10 PM.png",
        17: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_18_39 PM.png",
        18: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_19_10 PM.png",
        19: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_18_39 PM.png",
        20: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_19_10 PM.png",
        21: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_18_39 PM.png",
        22: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_19_10 PM.png",
        23: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_18_39 PM.png",
        24: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_19_10 PM.png",
        25: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_18_39 PM.png",
        26: "../WHERE CAN DUST REST/ChatGPT Image May 18, 2026, 07_19_10 PM.png"
      },
      hallKey: "dustrest",
      op2Key: "dustrest",
      op2Pair: "nobrightstand",
      files: [
        "No Bright Stand - The Jungle Field Session (Rice Field Live) - Sonauto.ogg",
        "No Bright Stand - Dig by Motion (Palmas and Ghost) - Sonauto.ogg",
        "No Bright Stand - The Signal and the Noise - Sonauto.ogg",
        "No Bright Stand - Sudden Awakening at Dawn - Sonauto.ogg",
        "No Bright Stand - Drop the Rag - Sonauto.ogg",
        "No Bright Stand - Midnight Grit (1 AM Edit) - Sonauto.ogg",
        "No Bright Stand - Gu Xiao Huo Guan (Lonely Howl at the Fire Pass) - Sonauto.ogg",
        "No Bright Stand - Heartbreak & Log Drums - Sonauto.ogg",
        "No Bright Stand - Lorca in Appalachia - Sonauto.ogg",
        "No Bright Stand - Non-Abiding Flow - Sonauto.ogg",
        "No Bright Stand - Not a Mote of Dust - Sonauto.ogg",
        "No Bright Stand - Non-Abiding Flow - Sonauto (1).ogg",
        "No Bright Stand - Oracle Bone Interface (118 BPM) - Sonauto.ogg",
        "No Bright Stand - The Filter Pulse - Sonauto.ogg",
        "No Bright Stand - The Mirror Without Dust - Sonauto.ogg",
        "No Bright Stand - Frictionless Void - Sonauto.ogg",
        "No Bright Stand - The Dust Oracle (72 BPM) - Sonauto.ogg",
        "No Bright Stand - Mirror Invariant - Sonauto.ogg",
        "No Bright Stand - Ontological Collapse (The Unstainable) - Sonauto.ogg",
        "No Bright Stand - Polishing the Data Mirror - Sonauto.ogg",
        "No Bright Stand - Sub-Zero Sunbeams - Sonauto.ogg",
        "No Bright Stand - Sudden Awakening - Sonauto.ogg",
        "No Bright Stand - Rice Field Echoes - Sonauto.ogg",
        "No Bright Stand - The Mirror and the Stand - Sonauto.ogg",
        "No Bright Stand - Bodhi Root Geometry - Sonauto.ogg",
        "No Bright Stand - 塵化為訊 (Dust to Signal) - Sonauto.ogg",
        "No Bright Stand - Mirror Dust System - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Mirror-dust doctrine / rice-field pulses / sudden awakening fieldwork"],
        ["Use", "Standalone album page, hall route, and direct song-page links for every cut."],
        ["OP2 Pair", "Launch with NO BRIGHT STAND for the mirror-and-dust companion deck."]
      ]
    },
    sunfadedghosts: {
      key: "sunfadedghosts",
      pageSlug: "sun-faded-ghosts",
      basePath: "../SUN-FADED GHOSTS/",
      label: "SUN-FADED GHOSTS",
      subtitle: "Concrete glare / passinho voltage / sun-bleached ghost circuits",
      accentA: "#c98242",
      accentB: "#68a7a0",
      coverImage: "../SUN-FADED GHOSTS/9208d141-f249-4391-b3f3-f0ecc4cdfe4a.png",
      defaultTrackArt: "../SUN-FADED GHOSTS/Gemini_Generated_Image_prepgyprepgyprep.jpeg",
      trackArtByIndex: {
        0: "../SUN-FADED GHOSTS/9208d141-f249-4391-b3f3-f0ecc4cdfe4a.png",
        1: "../SUN-FADED GHOSTS/Gemini_Generated_Image_prepgyprepgyprep.jpeg",
        2: "../SUN-FADED GHOSTS/9208d141-f249-4391-b3f3-f0ecc4cdfe4a.png",
        3: "../SUN-FADED GHOSTS/Gemini_Generated_Image_prepgyprepgyprep.jpeg",
        4: "../SUN-FADED GHOSTS/9208d141-f249-4391-b3f3-f0ecc4cdfe4a.png",
        5: "../SUN-FADED GHOSTS/Gemini_Generated_Image_prepgyprepgyprep.jpeg",
        6: "../SUN-FADED GHOSTS/9208d141-f249-4391-b3f3-f0ecc4cdfe4a.png",
        7: "../SUN-FADED GHOSTS/Gemini_Generated_Image_prepgyprepgyprep.jpeg",
        8: "../SUN-FADED GHOSTS/9208d141-f249-4391-b3f3-f0ecc4cdfe4a.png"
      },
      hallKey: "sunfadedghosts",
      op2Key: "sunfadedghosts",
      op2Pair: "sharperhands",
      files: [
        "Sun-Faded Ghost - Asphalt Levitation (Passinho Circo) - Sonauto.ogg",
        "Sun-Faded Ghost - Asphalt Levitation - Sonauto.ogg",
        "Sun-Faded Ghost - Asphalt Levitation - Sonauto (1).ogg",
        "Sun-Faded Ghost - Favela Footwork Circuit - Sonauto.ogg",
        "Sun-Faded Ghost - Favela Footwork Circuit - Sonauto (1).ogg",
        "Sun-Faded Ghost - Lisbon Kuduro Voltage - Sonauto.ogg",
        "Sun-Faded Ghost - Melancolia de Concreto - Sonauto.ogg",
        "Sun-Faded Ghost - Passinho das Quadras - Sonauto.ogg",
        "Sun-Faded Ghost - Trilhos do Passinho - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Concrete glare / passinho voltage / sun-bleached ghost circuits"],
        ["Use", "Standalone album page, hall route, and direct song-page links for every cut."],
        ["OP2 Pair", "Launch with SHARPER HANDS for a repair-to-glare deck."]
      ]
    },
    weedfield: {
      key: "weedfield",
      pageSlug: "weed-choked-field",
      basePath: "../WEED-CHOKED FIELD/",
      label: "THE WEED-CHOKED FIELD",
      subtitle: "Ruined field recordings / steel weather / Sankofa signal decay",
      accentA: "#6f7f3f",
      accentB: "#c7b56f",
      coverImage: "../WEED-CHOKED FIELD/ChatGPT Image May 9, 2026, 02_42_11 AM.png",
      defaultTrackArt: "../WEED-CHOKED FIELD/ChatGPT Image May 9, 2026, 02_43_26 AM.png",
      hallKey: "weedfield",
      op2Key: "weedfield",
      op2Pair: "emptyfields",
      files: [
        "The Weed-Choked Field - 70mm Sankofa Protocol - Sonauto.ogg",
        "The Weed-Choked Field - Arc Flash Appalachian - Sonauto.ogg",
        "The Weed-Choked Field - Architecture of a Dying Signal - Sonauto.ogg",
        "The Weed-Choked Field - Echoes of Volholla - Sonauto.ogg",
        "The Weed-Choked Field - Fortress Decay - Sonauto.ogg",
        "The Weed-Choked Field - Fracture Matrix Blues - Sonauto.ogg",
        "The Weed-Choked Field - Hephaestus Error - Sonauto.ogg",
        "The Weed-Choked Field - Lead Sky Jukebox - Sonauto.ogg",
        "The Weed-Choked Field - London Rain Hiss - Sonauto.ogg",
        "The Weed-Choked Field - Luxury and Mud - Sonauto.ogg",
        "The Weed-Choked Field - Microcassette Memory - Sonauto.ogg",
        "The Weed-Choked Field - Monolithic Aftermath - Sonauto.ogg",
        "The Weed-Choked Field - Neurosymbolic Shield Strike - Sonauto.ogg",
        "The Weed-Choked Field - Ozone Scented Plasma - Sonauto.ogg",
        "The Weed-Choked Field - Ozone Seance - Sonauto.ogg",
        "The Weed-Choked Field - Playground in the Fog - Sonauto.ogg",
        "The Weed-Choked Field - Ruins of the Auditory Wall - Sonauto.ogg",
        "The Weed-Choked Field - Sankofa Protocol - Sonauto.ogg",
        "The Weed-Choked Field - Silo Array Test 4 (144 BPM) - Sonauto.ogg",
        "The Weed-Choked Field - Stalactite Ritual - Sonauto.ogg",
        "The Weed-Choked Field - Static Shape-Note Pulse - Sonauto.ogg",
        "The Weed-Choked Field - Stone Wall Crumbling - Sonauto.ogg",
        "The Weed-Choked Field - Tape Rot In A Vault - Sonauto.ogg",
        "The Weed-Choked Field - The Arc Lamp Glow - Sonauto.ogg",
        "The Weed-Choked Field - The Cooling Tower Seance - Sonauto.ogg",
        "The Weed-Choked Field - The Cost of Steel - Sonauto.ogg",
        "The Weed-Choked Field - The Crust Resonance - Sonauto.ogg",
        "The Weed-Choked Field - The Morse Code Mooche - Sonauto.ogg",
        "The Weed-Choked Field - The Ruined Somnambulist - Sonauto.ogg",
        "The Weed-Choked Field - The Volholla Cylinder Protocol - Sonauto.ogg",
        "The Weed-Choked Field - The Wire-Recorder Seances - Sonauto.ogg",
        "The Weed-Choked Field - Whir of the Ancestor - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Ruined field recordings / steel weather / Sankofa signal decay"],
        ["Use", "Standalone album page, hall route, and direct song-page links for every cut."],
        ["OP2 Pair", "Launch with EMPTY ARE THE FIELDS for the field-echo mirror deck."]
      ]
    },
    emptyfields: {
      key: "emptyfields",
      pageSlug: "empty-are-the-fields",
      basePath: "../EMPTY ARE THE FIELDS/",
      label: "EMPTY ARE THE FIELDS",
      subtitle: "Iron shield hymns / bare-field strings / radiator ghosts",
      accentA: "#d9d0b0",
      accentB: "#6f6f68",
      coverImage: "../EMPTY ARE THE FIELDS/ChatGPT Image May 9, 2026, 02_56_43 AM.png",
      defaultTrackArt: "../EMPTY ARE THE FIELDS/ChatGPT Image May 9, 2026, 02_57_09 AM.png",
      hallKey: "emptyfields",
      op2Key: "emptyfields",
      op2Pair: "weedfield",
      files: [
        "The Weed-Choked Field - Axioms of the Field - Sonauto.ogg",
        "The Weed-Choked Field - Ghosts in the Radiator - Sonauto.ogg",
        "The Weed-Choked Field - Iron-Hearted Shift - Sonauto.ogg",
        "The Weed-Choked Field - Shield of Achilles - Sonauto.ogg",
        "The Weed-Choked Field - Shield of the Ragged Urchin - Sonauto.ogg",
        "The Weed-Choked Field - The Field of Weeds - Sonauto.ogg",
        "The Weed-Choked Field - The Iron Shield (Minimal Spoken Word Score) - Sonauto.ogg",
        "The Weed-Choked Field - The Shield of Achilles - Sonauto.ogg",
        "The Weed-Choked Field - The Shield of Iron - Sonauto.ogg",
        "The Weed-Choked Field - The Whispering Strings - Sonauto.ogg"
      ],
      notes: [
        ["Mode", "Iron shield hymns / bare-field strings / radiator ghosts"],
        ["Use", "Standalone album page, hall route, and direct song-page links for every cut."],
        ["OP2 Pair", "Launch with THE WEED-CHOKED FIELD for the field-echo mirror deck."]
      ]
    }
  };

  function titleFromFilename(file) {
    return String(file || "")
      .replace(/^.*\//, "")
      .replace(/\.(?:mp3|ogg)$/i, "")
      .replace(/^\d+_/, "")
      .replace(/^coolradio\s*-\s*/i, "")
      .replace(/^geometric ghosts of mitte\s*-\s*/i, "")
      .replace(/^river bank waiting\s*-\s*/i, "")
      .replace(/^solar reveries\s*-\s*/i, "")
      .replace(/^jukebox time collapse\s*-\s*/i, "")
      .replace(/^neon puddles\s*\(night bus edit\)\s*-\s*/i, "")
      .replace(/^neon puddles\s*-\s*/i, "")
      .replace(/^mall patchworld ingest\s*-\s*/i, "")
      .replace(/^the cybernetic winter\s*-\s*/i, "")
      .replace(/^the cathedral of iv drips\s*-\s*/i, "")
      .replace(/^throne of ash\s*-\s*/i, "")
      .replace(/^cathedral of glass\s*-\s*/i, "")
      .replace(/^event horizon discovery\s*-\s*/i, "")
      .replace(/^silence in the 757\s*-\s*/i, "")
      .replace(/^gole yakh memory\s*-\s*/i, "")
      .replace(/^clinical heat\s*-\s*/i, "")
      .replace(/^concreto y cyphers\s*-\s*/i, "")
      .replace(/^usb legacy\s*-\s*/i, "")
      .replace(/^ferrous lament\s*-\s*/i, "")
      .replace(/^the great congregation\s*-\s*/i, "")
      .replace(/^(?:m\u00e1quina|ma\u0301quina) de guerra\s*-\s*/i, "")
      .replace(/^black water run\s*-\s*/i, "")
      .replace(/^executable infrastructure dub\s*-\s*/i, "")
      .replace(/^queen of light\s*-\s*/i, "")
      .replace(/^root and residue\s*-\s*/i, "")
      .replace(/^better hands\s*-\s*/i, "")
      .replace(/^no bright stand\s*-\s*/i, "")
      .replace(/^sun-faded ghosts?\s*-\s*/i, "")
      .replace(/^empty are the fields\s*-\s*/i, "")
      .replace(/^weed-choked field\s*-\s*/i, "")
      .replace(/^the weed-choked field\s*-\s*/i, "")
      .replace(/^the d\.c\.\s*pocket\s*&\s*afro-funk\s*-\s*/i, "")
      .replace(/^(?:canyon fog and silver strings|chiptune crossroads|crown on|piassa state of mind|remix of the burn of being|the sad god)\s*-\s*/i, "")
      .replace(/\s*-\s*Sonauto\s*\((\d+)\)$/i, " ($1)")
      .replace(/\s*-\s*Sonauto$/i, "")
      .replace(/_/g, " ")
      .trim()
      .normalize("NFC");
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (m) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      "\"": "&quot;",
      "'": "&#39;"
    }[m]));
  }

  function normalizeAssetPath(value) {
    return String(value || "").normalize("NFC");
  }

  function pageAssetPath(rootRelativePath) {
    const raw = normalizeAssetPath(rootRelativePath).replace(/^\.\/+/, "");
    if (!raw) return "";
    return raw.startsWith("VOLHOLLA/") ? `./${raw.slice("VOLHOLLA/".length)}` : `../${raw}`;
  }

  function isLowBandwidthConnection(connection) {
    return Boolean(connection && (connection.saveData || ["slow-2g", "2g"].includes(String(connection.effectiveType || "").toLowerCase())));
  }

  function pickImageVariant(entry, kind) {
    const variant = entry?.derivatives?.[kind] || entry?.derivatives?.cover || entry?.derivatives?.thumb || null;
    return pageAssetPath(variant?.webp || variant?.jpeg || entry?.source || "");
  }

  function pickAudioVariant(entry, connection) {
    if (!entry) return "";
    const preferred = isLowBandwidthConnection(connection)
      ? entry.derivatives?.fallback?.mp3 || entry.derivatives?.stream?.mp3 || entry.source
      : entry.derivatives?.stream?.mp3 || entry.derivatives?.fallback?.mp3 || entry.source;
    return pageAssetPath(preferred || "");
  }

  function loadMediaManifest() {
    if (mediaManifestPromise) return mediaManifestPromise;
    mediaManifestPromise = fetch("./media-manifest.json", { cache: "force-cache" })
      .then((response) => response.ok ? response.json() : null)
      .catch(() => null);
    return mediaManifestPromise;
  }

  function shieldSvg(accentA, accentB, glyphMode) {
    const glyph = glyphMode || "ring";
    let motif = `<circle cx="100" cy="96" r="34" fill="none" stroke="${accentB}" stroke-width="9"/>`;
    if (glyph === "chev") motif = `<path d="M66 118 L100 84 L134 118" fill="none" stroke="${accentB}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><path d="M74 96 L100 70 L126 96" fill="none" stroke="${accentB}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>`;
    if (glyph === "line") motif = `<line x1="100" y1="58" x2="100" y2="138" stroke="${accentB}" stroke-width="9"/><line x1="66" y1="98" x2="134" y2="98" stroke="${accentB}" stroke-width="9"/>`;
    if (glyph === "tri") motif = `<path d="M70 128 L100 68 L130 128" fill="none" stroke="${accentB}" stroke-width="9" stroke-linejoin="round"/>`;
    return `
      <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path d="M100 20 Q140 40 170 60 Q170 120 140 160 Q100 180 60 160 Q30 120 30 60 Q60 40 100 20 Z" fill="#111115" stroke="${accentA}" stroke-width="10"/>
        <path d="M100 30 Q132 46 156 62 Q156 112 132 146 Q100 164 68 146 Q44 112 44 62 Q68 46 100 30 Z" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="3"/>
        ${motif}
      </svg>
    `;
  }

  function trackArtFor(album, title, index) {
    return album.trackArtByTitle?.[title] || album.trackArtByIndex?.[index] || album.defaultTrackArt || null;
  }

  function buildGallery(album) {
    const tracks = album.files.map((file, i) => ({ index: i, title: titleFromFilename(file) }));
    const items = tracks.map((track, i) => {
      const art = trackArtFor(album, track.title, track.index);
      const fallbackGlyph = ["ring", "chev", "line", "tri"][i % 4];
      const media = art
        ? `<img src="${escapeHtml(encodeURI(normalizeAssetPath(art)))}" alt="${escapeHtml(track.title)} artwork" loading="lazy" decoding="async">`
        : `<div class="fallback">${shieldSvg(album.accentA, album.accentB, fallbackGlyph)}</div>`;
      return `
        <a class="gallery-item" href="${escapeHtml(songPageHref(album, track.index))}" aria-label="Open song page for ${escapeHtml(track.title)}">
          ${media}
          <span class="badge">${String(track.index + 1).padStart(2, "0")}</span>
          <div class="caption">${escapeHtml(track.title)}</div>
        </a>
      `;
    });
    return items.join("");
  }

  function songPageHref(album, index, extra = {}) {
    if (album.noSongPages) {
      const params = new URLSearchParams({ track: String(index + 1), ...extra });
      return `./${album.pageSlug}.html?${params.toString()}#tracks`;
    }
    const num = String(index + 1).padStart(2, "0");
    const params = new URLSearchParams();
    Object.entries(extra).forEach(([k, v]) => {
      if (v === undefined || v === null || v === false) return;
      params.set(k, String(v));
    });
    const query = params.toString();
    return `./song-${album.key}-${num}.html${query ? `?${query}` : ""}`;
  }

  function renderTrackList(album) {
    return album.files.map((file, i) => {
      const side = album.sides?.find((entry) => entry.start === i);
      const sideHeader = side ? `
      <li class="track-side">
        <div class="track-side-label">${escapeHtml(side.label)}</div>
        <div class="track-side-meta">${String(side.start + 1).padStart(2, "0")}-${String(side.end + 1).padStart(2, "0")} · ${escapeHtml(side.note || "")}</div>
      </li>` : "";
      return `${sideHeader}
      <li class="track-row">
        <button class="track" type="button" data-track-index="${i}" aria-label="Play ${escapeHtml(titleFromFilename(file))}">
          <div class="track-no">${String(i + 1).padStart(2, "0")}</div>
          <div class="track-title">${escapeHtml(titleFromFilename(file))}</div>
          <div class="track-cta" aria-hidden="true">Play</div>
        </button>
        <a class="track-link" href="${escapeHtml(songPageHref(album, i))}" aria-label="Open song page for ${escapeHtml(titleFromFilename(file))}">Open</a>
      </li>
    `;
    }).join("");
  }

  function fmtTime(sec) {
    if (!Number.isFinite(sec) || sec < 0) return "0:00";
    const s = Math.floor(sec);
    const m = Math.floor(s / 60);
    const r = s % 60;
    return `${m}:${String(r).padStart(2, "0")}`;
  }

  function buildTrackObjects(album) {
    return album.files.map((file, index) => ({
      index,
      file,
      title: titleFromFilename(file),
      src: encodeURI(normalizeAssetPath(`${album.basePath || ""}${file}`)),
      art: trackArtFor(album, titleFromFilename(file), index)
    }));
  }

  function normalizeAlbumKey(rawValue) {
    const raw = String(rawValue || "").trim().toLowerCase();
    if (raw === "rootresidue" || raw === "root" || raw === "root-and-residue" || raw === "root_and_residue" || raw === "root and residue" || raw === "rar") return "rootresidue";
    if (raw === "weedfield" || raw === "weed" || raw === "weed-choked-field" || raw === "weed_choked_field" || raw === "the weed-choked field" || raw === "the-weed-choked-field" || raw === "wcf") return "weedfield";
    if (raw === "emptyfields" || raw === "empty" || raw === "empty-are-the-fields" || raw === "empty_are_the_fields" || raw === "empty are the fields" || raw === "eatf") return "emptyfields";
    if (raw === "nobrightstand" || raw === "no-bright-stand" || raw === "no_bright_stand" || raw === "no bright stand" || raw === "nbs") return "nobrightstand";
    if (raw === "dustrest" || raw === "where-can-dust-rest" || raw === "where_can_dust_rest" || raw === "where can dust rest" || raw === "wcdr") return "dustrest";
    if (raw === "queen" || raw === "queen-of-light" || raw === "queen_of_light" || raw === "queen of light" || raw === "qol") return "queen";
    return raw;
  }

  function renderVisualPanel(album) {
    return `
      <details class="panel extras-panel" id="albumVisualsPanel">
        <summary class="extras-summary">
          <span>Visuals</span>
          <span class="mono">${album.trackArtByTitle ? "track art" : "shield fallback"}</span>
          <span class="caret" aria-hidden="true">▾</span>
        </summary>
        <div class="section">
          <div class="gallery-grid">
            ${buildGallery(album)}
          </div>
        </div>
      </details>
    `;
  }

  function mountAlbumPlayer(root, album, pageUrl) {
    const tracks = buildTrackObjects(album);
    const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection || null;
    const canWarmTrack = !connection || (!connection.saveData && !["slow-2g", "2g"].includes(String(connection.effectiveType || "").toLowerCase()));
    const audio = new Audio();
    audio.preload = canWarmTrack ? "metadata" : "none";
    let currentIndex = -1;
    let primedIndex = -1;
    let hasPlaybackIntent = false;
    let transportState = "idle";
    let warmupTimer = 0;

    const els = {
      coverImg: root.querySelector(".cover-square img"),
      playerShell: root.querySelector("#albumPlayerShell"),
      topShare: root.querySelector("#sharePageBtn"),
      topCopyBtn: root.querySelector("#copyTopUrlBtn"),
      topQrBtn: root.querySelector("#downloadAlbumQrBtn"),
      headMenu: root.querySelector(".head-menu"),
      sendBtn: root.querySelector("#sendAlbumBtn"),
      copyBtn: root.querySelector("#copyUrlBtn"),
      jumpTracksBtn: root.querySelector("#jumpTracksBtn"),
      jumpVisualsBtn: root.querySelector("#jumpVisualsBtn"),
      unitOpenTracksBtn: root.querySelector("#unitOpenTracksBtn"),
      tracksPanel: root.querySelector("#albumTracksPanel"),
      visualsPanel: root.querySelector("#albumVisualsPanel"),
      playBtn: root.querySelector("#playAlbumBtn"),
      prevBtn: root.querySelector("#prevTrackBtn"),
      nextBtn: root.querySelector("#nextTrackBtn"),
      unitPlayBtn: root.querySelector("#unitPlayAlbumBtn"),
      unitPrevBtn: root.querySelector("#unitPrevTrackBtn"),
      unitNextBtn: root.querySelector("#unitNextTrackBtn"),
      nowKicker: root.querySelector("#albumNowKicker"),
      nowTitle: root.querySelector("#albumNowTitle"),
      nowSub: root.querySelector("#albumNowSub"),
      transportText: root.querySelector("#albumTransportText"),
      transportModeChip: root.querySelector("#albumTransportModeChip"),
      transportSignalChip: root.querySelector("#albumTransportSignalChip"),
      transportRailFill: root.querySelector("#albumTransportRailFill"),
      retryBtn: root.querySelector("#albumRetryBtn"),
      timeNow: root.querySelector("#albumTimeNow"),
      timeTotal: root.querySelector("#albumTimeTotal"),
      progressFill: root.querySelector("#albumProgressFill"),
      discTrackNo: root.querySelector("#discTrackNo"),
      discMark: root.querySelector("#discTrackMark"),
      discLine: root.querySelector("#discLine"),
      discSubline: root.querySelector("#discSubline"),
      discTapTarget: root.querySelector(".disc"),
      discWrap: root.querySelector(".disc-wrap"),
      trackBtns: Array.from(root.querySelectorAll("[data-track-index]"))
    };

    function signalLabel() {
      if (!connection) return "";
      const effective = String(connection.effectiveType || "").toLowerCase();
      if (connection.saveData) return effective ? `${effective} lite` : "lite";
      if (!effective) return "";
      return effective === "slow-2g" ? "2g" : effective;
    }

    function updateTransportStrip(track, playing, loading, buffering, errored) {
      const lite = isLowBandwidthConnection(connection);
      const signal = signalLabel();
      let text = lite
        ? "Lite mode active. Tracks load on demand to save data."
        : "Album ready. Choose a track or press Play.";
      let rail = 20;

      if (errored) {
        text = "Track load failed. Retry when the signal steadies.";
        rail = 100;
      } else if (loading) {
        text = lite ? "Preparing lighter album stream." : "Preparing album stream.";
        rail = 38;
      } else if (buffering) {
        text = lite ? "Buffering on low signal. Keep this page open." : "Buffering current track.";
        rail = 56;
      } else if (playing && track) {
        text = lite ? "Playing lightweight stream." : "Playing album stream.";
        rail = 72;
      } else if (track && hasPlaybackIntent) {
        text = lite ? "Ready to resume in lite mode." : "Ready to resume.";
        rail = 30;
      }

      if (els.transportText) els.transportText.textContent = text;
      if (els.transportModeChip) {
        els.transportModeChip.hidden = !lite;
        els.transportModeChip.textContent = "Lite";
      }
      if (els.transportSignalChip) {
        els.transportSignalChip.hidden = !signal;
        els.transportSignalChip.textContent = signal.toUpperCase();
      }
      if (els.retryBtn) els.retryBtn.hidden = !errored;
      if (els.transportRailFill) els.transportRailFill.style.width = `${rail}%`;
    }

    function currentTrack() {
      return currentIndex >= 0 ? tracks[currentIndex] : null;
    }

    function syncPlayerState() {
      if (!els.playerShell) return;
      const interactive = hasPlaybackIntent || currentIndex >= 0;
      els.playerShell.classList.toggle("is-loading", interactive && transportState === "loading");
      els.playerShell.classList.toggle("is-buffering", interactive && transportState === "buffering");
      els.playerShell.classList.toggle("is-ready", interactive && (transportState === "ready" || transportState === "playing"));
      els.playerShell.classList.toggle("is-error", transportState === "error");
    }

    function setTransportState(next) {
      if (transportState === next) {
        syncPlayerState();
        return;
      }
      transportState = next;
      syncPlayerState();
      updateNowUI();
    }

    function setAudioSource(index) {
      if (index < 0 || index >= tracks.length) return false;
      if (audio.dataset.trackIndex === String(index) && audio.src) {
        primedIndex = index;
        return false;
      }
      primedIndex = index;
      audio.dataset.trackIndex = String(index);
      audio.src = tracks[index].src;
      audio.load();
      return true;
    }

    function scheduleWarmup(index) {
      if (!canWarmTrack || index < 0 || index >= tracks.length) return;
      const warm = () => {
        if (hasPlaybackIntent || currentIndex >= 0 || audio.dataset.trackIndex) return;
        setAudioSource(index);
      };
      if ("requestIdleCallback" in window) {
        window.requestIdleCallback(warm, { timeout: 1400 });
      } else {
        warmupTimer = window.setTimeout(warm, 450);
      }
    }

    function applyMediaManifest(manifestAlbum) {
      if (!manifestAlbum) return;

      const coverImage = pickImageVariant(manifestAlbum.cover, "cover");
      const defaultTrackArt = pickImageVariant(manifestAlbum.defaultTrackArt, "cover") || coverImage;

      if (coverImage) {
        album.coverImage = coverImage;
        if (els.coverImg) els.coverImg.src = encodeURI(normalizeAssetPath(coverImage));
      }
      if (defaultTrackArt) album.defaultTrackArt = defaultTrackArt;

      if (Array.isArray(manifestAlbum.tracks)) {
        manifestAlbum.tracks.forEach((manifestTrack, index) => {
          const track = tracks[index];
          if (!track) return;
          const nextSrc = pickAudioVariant(manifestTrack.audio, connection);
          if (nextSrc) track.src = encodeURI(normalizeAssetPath(nextSrc));
          track.art = trackArtFor(album, track.title, index);
        });
      }

      if (!hasPlaybackIntent) {
        audio.removeAttribute("src");
        audio.load();
        delete audio.dataset.trackIndex;
        primedIndex = -1;
        scheduleWarmup(currentIndex >= 0 ? currentIndex : 0);
      }

      updateNowUI();
    }

    function updateTrackButtons() {
      els.trackBtns.forEach((btn) => {
        const idx = Number(btn.getAttribute("data-track-index"));
        const isCurrent = idx === currentIndex;
        const isPlaying = isCurrent && !audio.paused;
        btn.classList.toggle("is-current", isCurrent);
        btn.classList.toggle("is-playing", isPlaying);
        const cta = btn.querySelector(".track-cta");
        if (cta) cta.textContent = isPlaying ? "Pause" : "Play";
      });
    }

    function updateNowUI() {
      const track = currentTrack();
      const loading = hasPlaybackIntent && transportState === "loading";
      const buffering = hasPlaybackIntent && transportState === "buffering";
      const errored = transportState === "error";
      const playing = Boolean(track) && transportState === "playing" && !audio.paused;
      const pct = Number.isFinite(audio.duration) && audio.duration > 0
        ? Math.max(0, Math.min(100, (audio.currentTime / audio.duration) * 100))
        : 0;

      if (!track) {
        if (els.playerShell) els.playerShell.classList.remove("is-playing");
        if (els.nowKicker) els.nowKicker.textContent = `${String(tracks.length).padStart(2, "0")} tracks`;
        if (els.nowTitle) els.nowTitle.textContent = album.label;
        if (els.nowSub) els.nowSub.textContent = "";
        if (els.timeNow) els.timeNow.textContent = "0:00";
        if (els.timeTotal) els.timeTotal.textContent = "0:00";
        if (els.progressFill) els.progressFill.style.width = "0%";
        if (els.discTrackNo) els.discTrackNo.textContent = "--";
        if (els.discMark) els.discMark.textContent = "◎";
        if (els.discLine) els.discLine.textContent = "Album ready";
        if (els.discSubline) els.discSubline.textContent = "idle";
        if (els.playBtn) els.playBtn.textContent = "Play Album";
        if (els.unitPlayBtn) els.unitPlayBtn.textContent = "Play";
      } else {
        if (els.playerShell) els.playerShell.classList.toggle("is-playing", playing);
        if (els.nowKicker) {
          if (errored) els.nowKicker.textContent = "Load error";
          else if (buffering) els.nowKicker.textContent = `Buffering ${String(currentIndex + 1).padStart(2, "0")} / ${tracks.length}`;
          else if (loading) els.nowKicker.textContent = `Loading ${String(currentIndex + 1).padStart(2, "0")} / ${tracks.length}`;
          else els.nowKicker.textContent = `${playing ? "Playing" : "Paused"} ${String(currentIndex + 1).padStart(2, "0")} / ${tracks.length}`;
        }
        if (els.nowTitle) els.nowTitle.textContent = track.title;
        if (els.nowSub) {
          if (errored) els.nowSub.textContent = "Could not load track";
          else if (buffering) els.nowSub.textContent = "Holding the stream steady";
          else if (loading) els.nowSub.textContent = "Pulling audio into the player";
          else els.nowSub.textContent = "";
        }
        if (els.timeNow) els.timeNow.textContent = fmtTime(audio.currentTime);
        if (els.timeTotal) els.timeTotal.textContent = fmtTime(audio.duration);
        if (els.progressFill) els.progressFill.style.width = `${pct}%`;
        if (els.discTrackNo) els.discTrackNo.textContent = String(currentIndex + 1).padStart(2, "0");
        if (els.discMark) {
          if (errored) els.discMark.textContent = "!";
          else if (loading || buffering) els.discMark.textContent = "...";
          else els.discMark.textContent = playing ? "◉" : "◎";
        }
        if (els.discLine) els.discLine.textContent = track.title;
        if (els.discSubline) {
          if (errored) els.discSubline.textContent = "load failed";
          else if (buffering) els.discSubline.textContent = "buffering";
          else if (loading) els.discSubline.textContent = "loading audio";
          else els.discSubline.textContent = playing ? "spinning" : "paused";
        }
        if (els.playBtn) els.playBtn.textContent = loading || buffering ? "Loading..." : playing ? "Pause" : "Resume";
        if (els.unitPlayBtn) els.unitPlayBtn.textContent = loading || buffering ? "Loading..." : playing ? "Pause" : "Resume";
      }
      updateTrackButtons();
      updateTransportStrip(track, playing, loading, buffering, errored);
      syncPlayerState();
    }

    async function playCurrent() {
      if (!currentTrack() && tracks.length) {
        await loadTrack(0, true);
        return;
      }
      hasPlaybackIntent = true;
      if (!audio.src && currentIndex >= 0) setAudioSource(currentIndex);
      setTransportState("loading");
      try {
        await audio.play();
      } catch (err) {
        console.warn("Album page playback blocked", err);
        setTransportState("ready");
      }
      updateNowUI();
    }

    async function loadTrack(index, autoplay = false) {
      if (index < 0 || index >= tracks.length) return;
      currentIndex = index;
      hasPlaybackIntent = true;
      setAudioSource(index);
      setTransportState("loading");
      updateNowUI();
      if (autoplay) await playCurrent();
    }

    function togglePlay() {
      if (!tracks.length) return;
      if (currentIndex < 0) {
        loadTrack(0, true);
      } else if (audio.paused) {
        playCurrent();
      } else {
        audio.pause();
      }
    }

    function nextTrack(fromEnded = false) {
      if (!tracks.length) return;
      if (fromEnded && currentIndex >= tracks.length - 1) {
        audio.pause();
        updateNowUI();
        return;
      }
      const next = currentIndex < 0 ? 0 : (currentIndex + 1) % tracks.length;
      loadTrack(next, true);
    }

    function prevTrack() {
      if (!tracks.length) return;
      if (currentIndex >= 0 && audio.currentTime > 3) {
        audio.currentTime = 0;
        updateNowUI();
        return;
      }
      const prev = currentIndex < 0 ? 0 : (currentIndex - 1 + tracks.length) % tracks.length;
      loadTrack(prev, true);
    }

    function albumPublicAssetUrl(source) {
      if (!source) return "";
      if (/^(?:https?:|data:)/i.test(source)) return source;
      try {
        return new URL(encodeURI(normalizeAssetPath(source)), window.location.href).toString();
      } catch {
        return source;
      }
    }

    function qrImageUrl(url) {
      return `https://api.qrserver.com/v1/create-qr-code/?size=900x900&margin=18&data=${encodeURIComponent(url)}`;
    }

    function albumQrSvg() {
      const artSrc = albumPublicAssetUrl(album.coverImage || album.defaultTrackArt || "");
      const qrUrl = qrImageUrl(pageUrl);
      return `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350">
  <defs>
    <filter id="bw"><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncR type="linear" slope="1.3" intercept="-0.06"/><feFuncG type="linear" slope="1.3" intercept="-0.06"/><feFuncB type="linear" slope="1.3" intercept="-0.06"/></feComponentTransfer></filter>
    <style>
      .mono { font-family: Menlo, Consolas, "Courier New", monospace; fill: #000; }
      .label { font-size: 32px; font-weight: 900; letter-spacing: 5px; text-transform: uppercase; }
      .title { font-size: 70px; font-weight: 900; letter-spacing: 2px; text-transform: uppercase; }
      .small { font-size: 24px; font-weight: 900; }
    </style>
  </defs>
  <rect width="1080" height="1350" fill="#fff"/>
  <rect x="30" y="30" width="1020" height="1290" fill="#fff" stroke="#000" stroke-width="8"/>
  <g transform="translate(62 58) scale(.35)">
    <path d="M100 18 Q142 38 172 60 Q171 120 140 160 Q100 182 60 160 Q29 120 28 60 Q58 38 100 18 Z" fill="#fff" stroke="#000" stroke-width="10"/>
    <path d="M100 35 Q130 49 150 64 Q150 111 128 141 Q100 158 72 141 Q50 111 50 64 Q70 49 100 35 Z" fill="none" stroke="#000" stroke-width="5"/>
    <circle cx="100" cy="94" r="28" fill="none" stroke="#000" stroke-width="9"/>
    <path d="M72 130 L100 69 L128 130" fill="none" stroke="#000" stroke-width="9" stroke-linejoin="round"/>
  </g>
  <text x="155" y="100" class="mono label">MOTO ALBUM QR</text>
  <text x="930" y="100" class="mono label" text-anchor="end">${String(album.files.length).padStart(2, "0")}</text>
  <line x1="30" y1="140" x2="1050" y2="140" stroke="#000" stroke-width="8"/>
  <rect x="78" y="190" width="360" height="360" fill="#f4f4f4" stroke="#000" stroke-width="6"/>
  ${artSrc ? `<image href="${escapeHtml(artSrc)}" x="84" y="196" width="348" height="348" preserveAspectRatio="xMidYMid slice" filter="url(#bw)"/>` : `<text x="258" y="385" class="mono title" text-anchor="middle">MOTO</text>`}
  <rect x="510" y="190" width="492" height="492" fill="#fff" stroke="#000" stroke-width="6"/>
  <image href="${escapeHtml(qrUrl)}" x="530" y="210" width="452" height="452" preserveAspectRatio="xMidYMid meet"/>
  <line x1="30" y1="730" x2="1050" y2="730" stroke="#000" stroke-width="8"/>
  <foreignObject x="72" y="770" width="936" height="220">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font: 900 70px/.92 Menlo, Consolas, 'Courier New', monospace; text-transform: uppercase; overflow-wrap: anywhere; color: #000;">${escapeHtml(album.label)}</div>
  </foreignObject>
  <text x="72" y="1045" class="mono label">${escapeHtml(album.files.length)} TRACKS / VOLHOLLA</text>
  <foreignObject x="72" y="1090" width="936" height="120">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font: 900 24px/1.2 Menlo, Consolas, 'Courier New', monospace; overflow-wrap: anywhere; color: #000;">${escapeHtml(pageUrl)}</div>
  </foreignObject>
  <line x1="30" y1="1242" x2="1050" y2="1242" stroke="#000" stroke-width="8"/>
  <text x="72" y="1304" class="mono small">SCAN TO OPEN ALBUM PAGE</text>
</svg>`;
    }

    function downloadText(filename, text, type) {
      const blob = new Blob([text], { type });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    }

    function downloadAlbumQrImage() {
      downloadText(`${album.pageSlug || album.key}-qr.svg`, albumQrSvg(), "image/svg+xml");
      if (els.topQrBtn) {
        els.topQrBtn.textContent = "✓ QR";
        setTimeout(() => { els.topQrBtn.textContent = "QR Image"; }, 1200);
      }
      if (els.headMenu) els.headMenu.open = false;
    }

    async function sharePage() {
      try {
        const mode = await copyOrShare(pageUrl, album.label);
        if (els.sendBtn) els.sendBtn.textContent = mode === "copied" ? "✓ Copied" : "✓ Sent";
        if (els.topShare) els.topShare.textContent = "✓";
      } catch (err) {
        if (!err || err.name !== "AbortError") {
          window.prompt("Copy album URL", pageUrl);
        } else {
          return;
        }
      }
      setTimeout(() => {
        if (els.sendBtn) els.sendBtn.textContent = "Send";
        if (els.topShare) els.topShare.textContent = "Send";
      }, 1200);
    }

    if (els.playBtn) els.playBtn.addEventListener("click", togglePlay);
    if (els.prevBtn) els.prevBtn.addEventListener("click", prevTrack);
    if (els.nextBtn) els.nextBtn.addEventListener("click", nextTrack);
    if (els.unitPlayBtn) els.unitPlayBtn.addEventListener("click", togglePlay);
    if (els.unitPrevBtn) els.unitPrevBtn.addEventListener("click", prevTrack);
    if (els.unitNextBtn) els.unitNextBtn.addEventListener("click", nextTrack);
    if (els.discTapTarget) {
      els.discTapTarget.addEventListener("click", togglePlay);
      els.discTapTarget.setAttribute("role", "button");
      els.discTapTarget.setAttribute("tabindex", "0");
      els.discTapTarget.setAttribute("aria-label", "Play or pause album");
      els.discTapTarget.addEventListener("keydown", (event) => {
        if (event.key !== "Enter" && event.key !== " ") return;
        event.preventDefault();
        togglePlay();
      });
    }
    if (els.sendBtn) els.sendBtn.addEventListener("click", sharePage);
    if (els.topShare) els.topShare.addEventListener("click", sharePage);
    if (els.topQrBtn) els.topQrBtn.addEventListener("click", downloadAlbumQrImage);
    if (els.topCopyBtn) {
      els.topCopyBtn.addEventListener("click", async () => {
        try {
          if (navigator.clipboard?.writeText) {
            await navigator.clipboard.writeText(pageUrl);
            els.topCopyBtn.textContent = "✓ Copied";
            setTimeout(() => { els.topCopyBtn.textContent = "Copy URL"; }, 1200);
          } else {
            window.prompt("Copy album URL", pageUrl);
          }
        } catch {
          window.prompt("Copy album URL", pageUrl);
        } finally {
          if (els.headMenu) els.headMenu.open = false;
        }
      });
    }
    if (els.copyBtn) {
      els.copyBtn.addEventListener("click", async () => {
        try {
          if (navigator.clipboard?.writeText) {
            await navigator.clipboard.writeText(pageUrl);
            els.copyBtn.textContent = "✓ Copied";
            setTimeout(() => { els.copyBtn.textContent = "Copy URL"; }, 1200);
          } else {
            sharePage();
          }
        } catch {
          sharePage();
        }
      });
    }
    if (els.retryBtn) {
      els.retryBtn.addEventListener("click", () => {
        if (currentIndex >= 0) loadTrack(currentIndex, true);
        else loadTrack(0, true);
      });
    }
    if (els.jumpTracksBtn) {
      els.jumpTracksBtn.addEventListener("click", () => {
        if (els.tracksPanel) els.tracksPanel.open = true;
        (els.tracksPanel || root.querySelector(".tracks-panel"))?.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    }
    if (els.unitOpenTracksBtn) {
      els.unitOpenTracksBtn.addEventListener("click", () => {
        if (els.tracksPanel) els.tracksPanel.open = true;
        (els.tracksPanel || root.querySelector(".tracks-panel"))?.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    }
    if (els.jumpVisualsBtn) {
      els.jumpVisualsBtn.addEventListener("click", () => {
        if (els.visualsPanel) els.visualsPanel.open = true;
        els.visualsPanel?.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    }

    els.trackBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const idx = Number(btn.getAttribute("data-track-index"));
        if (!Number.isFinite(idx)) return;
        if (idx === currentIndex) togglePlay();
        else loadTrack(idx, true);
      });
    });

    audio.addEventListener("play", updateNowUI);
    audio.addEventListener("pause", () => {
      if (transportState !== "error") setTransportState("ready");
      updateNowUI();
    });
    audio.addEventListener("timeupdate", updateNowUI);
    audio.addEventListener("loadstart", () => {
      if (hasPlaybackIntent) setTransportState("loading");
    });
    audio.addEventListener("loadedmetadata", () => {
      if (hasPlaybackIntent && audio.paused) setTransportState("ready");
      updateNowUI();
    });
    audio.addEventListener("canplay", () => {
      if (hasPlaybackIntent && audio.paused) setTransportState("ready");
    });
    audio.addEventListener("waiting", () => {
      if (hasPlaybackIntent) setTransportState("buffering");
    });
    audio.addEventListener("seeking", () => {
      if (hasPlaybackIntent) setTransportState("buffering");
    });
    audio.addEventListener("seeked", () => {
      if (!hasPlaybackIntent) return;
      setTransportState(audio.paused ? "ready" : "playing");
    });
    audio.addEventListener("playing", () => {
      setTransportState("playing");
      updateNowUI();
    });
    audio.addEventListener("ended", () => nextTrack(true));
    audio.addEventListener("error", () => {
      setTransportState("error");
      if (els.nowKicker) els.nowKicker.textContent = "Error";
      if (els.nowSub) els.nowSub.textContent = "Could not load track";
    });

    updateNowUI();
    scheduleWarmup(0);
    if (connection?.addEventListener) connection.addEventListener("change", updateNowUI);
    root.__albumPage = { album, tracks, audio, loadTrack, togglePlay, nextTrack, prevTrack, applyMediaManifest };
  }

  function copyOrShare(url, label) {
    const data = {
      title: `${label} · VOLHOLLA`,
      text: `${label} album page`,
      url
    };
    return (async () => {
      if (navigator.share) {
        await navigator.share(data);
        return "shared";
      }
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(url);
        return "copied";
      }
      window.prompt("Copy album URL", url);
      return "prompt";
    })();
  }

  function init() {
    const root = document.querySelector("[data-album-page]");
    if (!root) return;
    const params = new URLSearchParams(window.location.search);
    const pageSlug = window.location.pathname.split("/").pop()?.replace(/\.html$/i, "") || "";
    const key = normalizeAlbumKey(root.getAttribute("data-album-page") || params.get("album") || pageSlug);
    const album = ALBUMS[key] || ALBUMS.volholla;

    document.title = `${album.label} · Album Page`;
    document.body.style.setProperty("--accent-a", album.accentA);
    document.body.style.setProperty("--accent-b", album.accentB);

    const hallHref = `./index.html?album=${encodeURIComponent(album.hallKey)}`;
    const op2Href = `../op2.html?a=${encodeURIComponent(album.op2Key)}&b=${encodeURIComponent(album.op2Pair)}`;
    const pageUrl = window.location.href;

    root.innerHTML = `
      <div class="top-rack">
        <div class="top-rack-card">
          <div class="te-strip">
            <div class="left">
              <span class="te-led" aria-hidden="true"></span>
              <span class="mono">Send + Play</span>
            </div>
            <span class="tag">${escapeHtml(album.files.length)} Tracks</span>
          </div>
          <div class="head">
            <div class="brand">
              <div class="shield">${shieldSvg(album.accentA, album.accentB, "ring")}</div>
              <div class="title-wrap">
                <h1>${escapeHtml(album.label)}</h1>
              </div>
            </div>
            <div class="pills">
              <button class="btn primary" type="button" id="sharePageBtn" aria-label="Share this album page">Send</button>
              <details class="head-menu">
                <summary class="btn ghost" aria-label="More album actions">⋯</summary>
                <div class="head-menu-panel">
                  <a class="btn" href="${escapeHtml(hallHref)}" aria-label="Open library view for this album">Library</a>
                  <a class="btn" href="${escapeHtml(op2Href)}" aria-label="Open mix view for this album pair">Mix</a>
                  <a class="btn" href="./index.html" aria-label="All album pages">Albums</a>
                  <button class="btn" type="button" id="copyTopUrlBtn" aria-label="Copy album page URL">Copy URL</button>
                  <button class="btn" type="button" id="downloadAlbumQrBtn" aria-label="Download album QR image">QR Image</button>
                </div>
              </details>
            </div>
          </div>
        </div>
      </div>

      <div class="layout">
        <section class="panel hero-panel">
          <div class="hero-grid">
            <div class="cover-frame">
              <div class="cover-head" aria-label="Primary playback controls">
                <button class="cover-mini-btn" type="button" id="unitPrevTrackBtn">Prev</button>
                <button class="cover-mini-btn is-primary" type="button" id="unitPlayAlbumBtn">Play</button>
                <button class="cover-mini-btn" type="button" id="unitNextTrackBtn">Next</button>
              </div>
              <div class="cover-square">
                ${album.coverImage
                  ? `<img src="${escapeHtml(encodeURI(normalizeAssetPath(album.coverImage)))}" alt="${escapeHtml(album.label)} cover artwork">`
                  : `<div class="fallback">${shieldSvg(album.accentA, album.accentB, "tri")}</div>`}
              </div>
              <div class="cover-foot">
                <button class="track-shelf-open" type="button" id="unitOpenTracksBtn">
                  <span class="count">${String(album.files.length).padStart(2, "0")} tracks</span>
                  <span class="label">Track List</span>
                </button>
              </div>
            </div>
            <div class="hero-text">
              <div class="album-player" id="albumPlayerShell">
                <div class="album-player-head">
                  <div class="album-now">
                    <div class="album-now-kicker" id="albumNowKicker">${String(album.files.length).padStart(2, "0")} tracks</div>
                    <div class="album-now-title" id="albumNowTitle">${escapeHtml(album.label)}</div>
                    <div class="album-now-sub" id="albumNowSub"></div>
                  </div>
                  <div class="album-time">
                    <span id="albumTimeNow">0:00</span>
                    <span class="sep">/</span>
                    <span id="albumTimeTotal">0:00</span>
                  </div>
                </div>
                <div class="transport-strip" aria-live="polite">
                  <div class="transport-copy">
                    <span class="transport-dot" aria-hidden="true"></span>
                    <span class="transport-text" id="albumTransportText">Album ready. Choose a track or press Play.</span>
                  </div>
                  <div class="transport-badges">
                    <span class="transport-chip" id="albumTransportModeChip" hidden>Lite</span>
                    <span class="transport-chip" id="albumTransportSignalChip" hidden></span>
                    <button type="button" class="transport-chip transport-retry" id="albumRetryBtn" hidden>Retry</button>
                  </div>
                </div>
                <div class="transport-rail" aria-hidden="true"><div class="transport-rail-fill" id="albumTransportRailFill"></div></div>
                <div class="album-progress" aria-hidden="true">
                  <div class="album-progress-fill" id="albumProgressFill"></div>
                </div>
                <div class="disc-stage">
                  <div class="disc-wrap">
                    <div class="disc-shadow"></div>
                    <div class="disc">
                      <div class="disc-label">
                        <div class="disc-label-inner">
                          <div class="disc-track-no" id="discTrackNo">--</div>
                          <div class="disc-track-mark" id="discTrackMark">◎</div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="disc-readout">
                    <div class="mono">Disc Viz</div>
                    <div class="line" id="discLine">${escapeHtml(album.label)}</div>
                    <div class="subline" id="discSubline">idle</div>
                  </div>
                </div>
                <div class="album-controls">
                  <button class="btn icon-btn" type="button" id="prevTrackBtn" aria-label="Previous track">Prev</button>
                  <button class="btn primary play-btn" type="button" id="playAlbumBtn" aria-label="Play or pause album">Play Album</button>
                  <button class="btn icon-btn" type="button" id="nextTrackBtn" aria-label="Next track">Next</button>
                </div>
              </div>
            </div>
          </div>
        </section>

        <details class="panel tracks-panel" id="albumTracksPanel" open>
          <summary class="tracks-summary">
            <span class="left">
              <span class="title">Tracks</span>
              <span class="mono">${String(album.files.length)} items</span>
            </span>
            <span class="caret" aria-hidden="true">▾</span>
          </summary>
          <div class="section">
            <ol class="track-list" id="albumTrackList">
              ${renderTrackList(album)}
            </ol>
          </div>
        </details>

        <div style="grid-column: 1 / -1;">
          ${album.trackArtByTitle ? renderVisualPanel(album) : ""}
        </div>
      </div>
    `;
    mountAlbumPlayer(root, album, pageUrl);
    loadMediaManifest().then((manifest) => {
      root.__albumPage?.applyMediaManifest?.(manifest?.albums?.[album.key] || null);
    });
  }

  init();
})();
