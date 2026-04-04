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
        "USB Legacy - Blood & Iron Debt - Sonauto.ogg",
        "USB Legacy - Chemical Ignition - Sonauto.ogg",
        "USB Legacy - Corazoncito (Stadium Love) - Sonauto.ogg",
        "USB Legacy - Extraction Ceremony - Sonauto.ogg",
        "USB Legacy - Grace Through Erosion - Sonauto.ogg",
        "USB Legacy - Hull Creak Ritual - Sonauto.ogg",
        "USB Legacy - Hull Creaks and Healing - Sonauto.ogg",
        "USB Legacy - Icaro of the Shipyard - Sonauto.ogg",
        "USB Legacy - Iron Into Dust - Sonauto.ogg",
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
      .replace(/^the cybernetic winter\s*-\s*/i, "")
      .replace(/^the cathedral of iv drips\s*-\s*/i, "")
      .replace(/^silence in the 757\s*-\s*/i, "")
      .replace(/^gole yakh memory\s*-\s*/i, "")
      .replace(/^clinical heat\s*-\s*/i, "")
      .replace(/^concreto y cyphers\s*-\s*/i, "")
      .replace(/^usb legacy\s*-\s*/i, "")
      .replace(/^ferrous lament\s*-\s*/i, "")
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
    return album.files.map((file, i) => `
      <li class="track-row">
        <button class="track" type="button" data-track-index="${i}" aria-label="Play ${escapeHtml(titleFromFilename(file))}">
          <div class="track-no">${String(i + 1).padStart(2, "0")}</div>
          <div class="track-title">${escapeHtml(titleFromFilename(file))}</div>
          <div class="track-cta" aria-hidden="true">Play</div>
        </button>
        <a class="track-link" href="${escapeHtml(songPageHref(album, i))}" aria-label="Open song page for ${escapeHtml(titleFromFilename(file))}">Open</a>
      </li>
    `).join("");
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
    const key = root.getAttribute("data-album-page");
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
