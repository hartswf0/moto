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
        "Clinical Heat - Ibadan To Island - Sonauto (1).ogg",
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
      coverImage: "../NO SERVICE/Gemini_Generated_Image_g7u7pzg7u7pzg7u7.png",
      defaultTrackArt: "../NO SERVICE/Gemini_Generated_Image_g7u7pzg7u7pzg7u7.png",
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
      .replace(/^clinical heat\s*-\s*/i, "")
      .replace(/^the d\.c\.\s*pocket\s*&\s*afro-funk\s*-\s*/i, "")
      .replace(/^(?:canyon fog and silver strings|chiptune crossroads|crown on|piassa state of mind|remix of the burn of being|the sad god)\s*-\s*/i, "")
      .replace(/\s*-\s*Sonauto\s*\((\d+)\)$/i, " ($1)")
      .replace(/\s*-\s*Sonauto$/i, "")
      .replace(/_/g, " ")
      .trim();
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

  function fmtTime(sec) {
    if (!Number.isFinite(sec) || sec < 0) return "0:00";
    const s = Math.floor(sec);
    const m = Math.floor(s / 60);
    const r = s % 60;
    return `${m}:${String(r).padStart(2, "0")}`;
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

  function normalizeAlbumInput(rawValue) {
    const raw = String(rawValue || "volholla").toLowerCase();
    const key = raw === "river-bank-waiting" || raw === "river_bank_waiting" || raw === "rbw"
      ? "river"
      : raw === "crossroads-and-crown" || raw === "crossroads_and_crown" || raw === "cac"
        ? "crossroads"
        : raw === "solar-reveries" || raw === "solar_reveries" || raw === "solar"
          ? "solar"
          : raw === "jukebox-time-collapse" || raw === "jukebox_time_collapse" || raw === "jtc"
            ? "jukebox"
            : raw === "cybernetic-winter" || raw === "cybernetic_winter" || raw === "cyber"
              ? "cyber"
              : raw === "no-service" || raw === "no_service" || raw === "noservice"
                ? "noservice"
                : raw === "clinical-heat" || raw === "clinical_heat" || raw === "clinical"
                  ? "clinical"
            : raw;
    return ALBUMS[key] ? key : "volholla";
  }

  function getAlbumFromContext(root) {
    const dataAlbum = root?.getAttribute("data-album") || "";
    if (dataAlbum) return ALBUMS[normalizeAlbumInput(dataAlbum)] || ALBUMS.volholla;
    const params = new URLSearchParams(window.location.search);
    return ALBUMS[normalizeAlbumInput(params.get("album"))] || ALBUMS.volholla;
  }

  function getTrackIndexFromContext(root, album, tracks) {
    const dataTrack = root?.getAttribute("data-track");
    if (dataTrack !== null && dataTrack !== "") {
      const n = Number(dataTrack);
      if (Number.isFinite(n)) {
        if (n >= 1 && n <= tracks.length) return n - 1;
        if (n >= 0 && n < tracks.length) return n;
      }
    }
    return findTrackIndex(album, tracks);
  }

  function getSongPagePath(albumKey, trackIndex, opts = {}) {
    const num = String(trackIndex + 1).padStart(2, "0");
    const params = new URLSearchParams();
    Object.entries(opts).forEach(([k, v]) => {
      if (v === undefined || v === null || v === false) return;
      params.set(k, String(v));
    });
    const query = params.toString();
    return `./song-${albumKey}-${num}.html${query ? `?${query}` : ""}`;
  }

  function getAlbumFromParams() {
    const params = new URLSearchParams(window.location.search);
    return ALBUMS[normalizeAlbumInput(params.get("album"))] || ALBUMS.volholla;
  }

  function getLegacySongPagePath(albumKey, trackIndex, opts = {}) {
    const params = new URLSearchParams();
    params.set("album", albumKey);
    params.set("track", String(trackIndex + 1));
    Object.entries(opts).forEach(([k, v]) => {
      if (v === undefined || v === null || v === false) return;
      params.set(k, String(v));
    });
    return `./song.html?${params.toString()}`;
  }

  function getAbsoluteSongPagePath(albumKey, trackIndex, opts = {}) {
    return getSongPagePath(albumKey, trackIndex, opts);
  }

  function songUrl(albumKey, trackIndex, opts = {}) {
    return getAbsoluteSongPagePath(albumKey, trackIndex, opts);
  }

  function legacySongUrl(albumKey, trackIndex, opts = {}) {
    return getLegacySongPagePath(albumKey, trackIndex, opts);
  }

  function trackArtFor(album, title, index) {
    return album.trackArtByTitle?.[title] || album.trackArtByIndex?.[index] || album.defaultTrackArt || null;
  }

  function buildTracks(album) {
    return album.files.map((file, index) => ({
      index,
      file,
      title: titleFromFilename(file),
      src: encodeURI(`${album.basePath || ""}${file}`),
      art: trackArtFor(album, titleFromFilename(file), index)
    }));
  }

  function findTrackIndex(album, tracks) {
    const params = new URLSearchParams(window.location.search);
    const qTrack = params.get("track");
    const qSong = (params.get("song") || "").trim().toLowerCase();

    if (qTrack !== null) {
      const n = Number(qTrack);
      if (Number.isFinite(n)) {
        if (n >= 1 && n <= tracks.length) return n - 1;
        if (n >= 0 && n < tracks.length) return n;
      }
    }

    if (qSong) {
      const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
      const idx = tracks.findIndex((t) => slug(t.title) === qSong || t.title.toLowerCase() === qSong);
      if (idx >= 0) return idx;
    }

    return 0;
  }

  function copyOrShare(url, title, text) {
    const data = { title, text, url };
    return (async () => {
      if (navigator.share) {
        await navigator.share(data);
        return "shared";
      }
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(url);
        return "copied";
      }
      window.prompt("Copy URL", url);
      return "prompt";
    })();
  }

  function isEmbedMode() {
    const params = new URLSearchParams(window.location.search);
    const v = params.get("embed");
    return v === "1" || v === "true" || v === "yes";
  }

  function wantsAutoplay() {
    const params = new URLSearchParams(window.location.search);
    const v = params.get("autoplay");
    return v === "1" || v === "true" || v === "yes";
  }

  function mount() {
    const root = document.getElementById("songPageRoot");
    if (!root) return;
    const album = getAlbumFromContext(root);
    const tracks = buildTracks(album);
    let currentIndex = Math.max(0, Math.min(tracks.length - 1, getTrackIndexFromContext(root, album, tracks)));
    const embed = isEmbedMode();
    if (embed) document.body.classList.add("embed");

    document.body.style.setProperty("--accent-a", album.accentA);
    document.body.style.setProperty("--accent-b", album.accentB);

    const audio = new Audio();
    audio.preload = "metadata";
    let isSeeking = false;

    const hallHrefFor = () => `./index.html?album=${encodeURIComponent(album.hallKey)}`;
    const op2HrefFor = () => `../op2.html?a=${encodeURIComponent(album.op2Key)}&b=${encodeURIComponent(album.op2Pair)}`;
    const albumPageHref = () => `./${album.pageSlug || album.key}.html`;
    const currentTrack = () => tracks[currentIndex];
    const currentSongUrl = (opts = {}) => {
      const href = songUrl(album.key, currentIndex, opts);
      try {
        return new URL(href, window.location.href).toString();
      } catch {
        return href;
      }
    };

    function renderTrackRows() {
      return tracks.map((track, index) => `
        <li class="track-row">
          <button class="track-btn${index === currentIndex ? " is-current" : ""}" type="button" data-track-index="${index}" aria-label="Play ${escapeHtml(track.title)}">
            <div class="track-no">${String(index + 1).padStart(2, "0")}</div>
            <div class="track-title">${escapeHtml(track.title)}</div>
            <div class="track-cta" aria-hidden="true">▶</div>
          </button>
          <a class="track-link" href="${escapeHtml(songUrl(album.key, index))}" aria-label="Open song page for ${escapeHtml(track.title)}">↗</a>
        </li>
      `).join("");
    }

    const firstTrack = currentTrack();
    const art = firstTrack?.art || album.coverImage || null;

    root.innerHTML = `
      <div class="shell">
        <header class="top">
          <div class="top-card">
            <div class="te-strip">
              <div class="te-left">
                <span class="led" aria-hidden="true"></span>
                <span class="mono">${embed ? "Embed" : "Listen"}</span>
              </div>
              <span class="te-tag">Track ${String(currentIndex + 1).padStart(2, "0")} / ${tracks.length}</span>
            </div>
            <div class="head">
              <div class="head-main">
                <div class="eyebrow">${escapeHtml(album.label)}</div>
                <h1 class="song-title" id="headSongTitle">${escapeHtml(firstTrack.title)}</h1>
                <div class="album-sub">${escapeHtml(album.subtitle)}</div>
              </div>
              <div class="head-actions">
                <button type="button" class="btn primary" id="sendBtn">↗ Send</button>
              </div>
            </div>
            <nav class="layer-map hide-in-embed" aria-label="Media layers and linked views">
              <a class="layer-node" href="${escapeHtml(hallHrefFor())}" title="Library view (all songs / shield hall)">
                <span class="dir" aria-hidden="true">↑</span><span class="label">Library</span>
              </a>
              <span class="layer-edge" aria-hidden="true"></span>
              <a class="layer-node" href="${escapeHtml(albumPageHref())}" title="Album object page">
                <span class="dir" aria-hidden="true">↑</span><span class="label">Album</span>
              </a>
              <span class="layer-edge active" aria-hidden="true"></span>
              <span class="layer-node is-current" aria-current="page" title="Current song page">
                <span class="dir" aria-hidden="true">•</span><span class="label">Song</span>
              </span>
              <span class="layer-edge alt" aria-hidden="true"></span>
              <a class="layer-node" href="${escapeHtml(op2HrefFor())}" title="Paired album mixer (OP2)">
                <span class="dir" aria-hidden="true">⇄</span><span class="label">Mix</span>
              </a>
            </nav>
          </div>
        </header>

        <div class="grid">
          <section class="panel art-panel">
            <div class="cover-frame">
              <div class="cover-head">
                <span class="mono">Song Unit</span>
                <span class="mono">${escapeHtml(album.key)} / ${String(currentIndex + 1).padStart(2, "0")}</span>
              </div>
              <div class="art-square" id="artSquare">
                ${art ? `<img id="songArtImg" src="${escapeHtml(encodeURI(art))}" alt="${escapeHtml(firstTrack.title)} artwork">` : `<div class="fallback">${shieldSvg(album.accentA, album.accentB, "tri")}</div>`}
              </div>
              <div class="cover-foot">
                <div class="main" id="lcdTrackTitle">${escapeHtml(firstTrack.title)}</div>
                <div class="meta">track</div>
              </div>
            </div>
          </section>

          <section class="panel player-panel" id="playerPanel">
            <div class="now-card">
              <div class="now-head">
                <div>
                  <div class="now-kicker" id="nowKicker">Ready</div>
                  <div class="now-line" id="nowLine">${escapeHtml(firstTrack.title)}</div>
                  <div class="now-subline" id="nowSubline">Tap Play</div>
                </div>
                <div class="time-box">
                  <span id="timeNow">0:00</span>
                  <span class="sep">/</span>
                  <span id="timeTotal">0:00</span>
                </div>
              </div>
              <div class="progress" aria-hidden="true"><div class="progress-fill" id="progressFill"></div></div>
              <div class="seek-row">
                <div class="seek-time" id="seekNow">0:00</div>
                <input id="seekBar" type="range" min="0" max="1000" value="0" step="1" aria-label="Seek playback" />
                <div class="seek-time" id="seekTotal">0:00</div>
              </div>
            </div>

            <div class="disc-stage" aria-hidden="true">
              <div class="disc-wrap">
                <div class="disc-shadow"></div>
                <div class="disc">
                  <div class="disc-label">
                    <div class="disc-label-inner">
                      <div class="disc-track-no" id="discTrackNo">${String(currentIndex + 1).padStart(2, "0")}</div>
                      <div class="disc-track-mark" id="discTrackMark">◎</div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="disc-readout">
                <div class="mono">Now</div>
                <div class="line" id="discLine">${escapeHtml(firstTrack.title)}</div>
                <div class="subline" id="discSubline">Tap Play</div>
              </div>
            </div>

            <div class="controls">
              <button type="button" class="btn icon-btn" id="prevBtn" aria-label="Previous song">⏮</button>
              <button type="button" class="btn primary play-btn" id="playBtn" aria-label="Play or pause"><span aria-hidden="true">▶</span><span>Play</span></button>
              <button type="button" class="btn icon-btn" id="nextBtn" aria-label="Next song">⏭</button>
            </div>

            <div class="actions">
              <button type="button" class="btn" id="copyUrlBtn">Copy URL</button>
              <button type="button" class="btn" id="copyEmbedBtn">Embed</button>
            </div>

            <div class="embed-code">
              <details>
                <summary><span>Embed</span><span class="mono">iframe</span></summary>
                <div class="code-box" id="embedCodeBox"></div>
              </details>
            </div>

          </section>
        </div>

        <details class="panel queue-panel">
          <summary class="queue-summary">
            <span class="left">
              <span class="title">Tracks</span>
              <span class="mono">${tracks.length} / tap to play</span>
            </span>
            <span class="caret" aria-hidden="true">▾</span>
          </summary>
          <div style="padding:10px">
            <ol class="track-list" id="queueTrackList">${renderTrackRows()}</ol>
          </div>
        </details>
      </div>
    `;

    const els = {
      topCard: root.querySelector(".top-card"),
      layerMap: root.querySelector(".layer-map"),
      coverFrame: root.querySelector(".cover-frame"),
      panel: document.getElementById("playerPanel"),
      headSongTitle: document.getElementById("headSongTitle"),
      lcdTrackTitle: document.getElementById("lcdTrackTitle"),
      songArtImg: document.getElementById("songArtImg"),
      artSquare: document.getElementById("artSquare"),
      sendBtn: document.getElementById("sendBtn"),
      copyUrlBtn: document.getElementById("copyUrlBtn"),
      copyEmbedBtn: document.getElementById("copyEmbedBtn"),
      embedCodeBox: document.getElementById("embedCodeBox"),
      prevBtn: document.getElementById("prevBtn"),
      playBtn: document.getElementById("playBtn"),
      nextBtn: document.getElementById("nextBtn"),
      nowKicker: document.getElementById("nowKicker"),
      nowLine: document.getElementById("nowLine"),
      nowSubline: document.getElementById("nowSubline"),
      timeNow: document.getElementById("timeNow"),
      timeTotal: document.getElementById("timeTotal"),
      seekNow: document.getElementById("seekNow"),
      seekTotal: document.getElementById("seekTotal"),
      progressFill: document.getElementById("progressFill"),
      seekBar: document.getElementById("seekBar"),
      discTrackNo: document.getElementById("discTrackNo"),
      discTrackMark: document.getElementById("discTrackMark"),
      discLine: document.getElementById("discLine"),
      discSubline: document.getElementById("discSubline"),
      trackBtns: Array.from(root.querySelectorAll(".track-btn"))
    };
    let trackPulseTimer = 0;
    let lastSeekBuzzAt = 0;

    function vibrate(ms = 8) {
      if (!embed && navigator.vibrate) navigator.vibrate(ms);
    }

    function pulseControlSurface() {
      const nodes = [els.topCard, els.layerMap, els.coverFrame, els.panel].filter(Boolean);
      nodes.forEach((node) => node.classList.remove("surface-pulse"));
      if (trackPulseTimer) clearTimeout(trackPulseTimer);
      requestAnimationFrame(() => nodes.forEach((node) => node.classList.add("surface-pulse")));
      trackPulseTimer = setTimeout(() => {
        nodes.forEach((node) => node.classList.remove("surface-pulse"));
        trackPulseTimer = 0;
      }, 260);
    }

    function setSeekPct(rawPct) {
      if (!els.seekBar) return;
      const pct = Math.max(0, Math.min(100, Number(rawPct) || 0));
      els.seekBar.style.setProperty("--seek-pct", `${pct}%`);
    }

    function getTrackArt(track) {
      return track.art || album.coverImage || null;
    }

    function absoluteSongUrl(opts = {}) {
      try {
        return new URL(songUrl(album.key, currentIndex, opts), window.location.href).toString();
      } catch {
        return songUrl(album.key, currentIndex, opts);
      }
    }

    function ensureMeta(selector, attr, value) {
      if (!value) return;
      let el = document.head.querySelector(selector);
      if (!el) {
        el = document.createElement("meta");
        el.setAttribute(attr, selector.includes('property="') ? selector.match(/property="([^"]+)"/)?.[1] || "" : selector.match(/name="([^"]+)"/)?.[1] || "");
        if (!el.getAttribute(attr)) return;
        document.head.appendChild(el);
      }
      el.setAttribute("content", value);
    }

    function ensureFavicon(href) {
      if (!href) return;
      let link = document.head.querySelector('link[rel="icon"]');
      if (!link) {
        link = document.createElement("link");
        link.setAttribute("rel", "icon");
        document.head.appendChild(link);
      }
      link.setAttribute("href", href);
    }

    function updateDocumentMeta(track) {
      const artSrc = getTrackArt(track);
      const absArt = artSrc ? (() => {
        try { return new URL(encodeURI(artSrc), window.location.href).toString(); }
        catch { return encodeURI(artSrc); }
      })() : "";
      const pageUrl = absoluteSongUrl();
      const title = `${track.title} · ${album.label}`;
      const desc = `${album.label} · Track ${String(currentIndex + 1).padStart(2, "0")} of ${tracks.length}`;

      document.title = title;
      ensureMeta('meta[property="og:title"]', "property", title);
      ensureMeta('meta[name="twitter:title"]', "name", title);
      ensureMeta('meta[property="og:description"]', "property", desc);
      ensureMeta('meta[name="twitter:description"]', "name", desc);
      ensureMeta('meta[property="og:url"]', "property", pageUrl);
      if (absArt) {
        ensureMeta('meta[property="og:image"]', "property", absArt);
        ensureMeta('meta[name="twitter:image"]', "name", absArt);
      }
      ensureFavicon(artSrc ? encodeURI(artSrc) : "");
    }

    function currentEmbedCode() {
      const src = absoluteSongUrl({ embed: 1 });
      return [
        `<iframe`,
        `  src="${src}"`,
        `  title="${album.label} — ${currentTrack().title}"`,
        `  width="100%"`,
        `  height="640"`,
        `  style="max-width:100%; border:0; border-radius:12px; overflow:hidden;"`,
        `  allow="autoplay; clipboard-write"`,
        `></iframe>`
      ].join("\n");
    }

    function updateTrackListUI() {
      els.trackBtns.forEach((btn) => {
        const idx = Number(btn.getAttribute("data-track-index"));
        const isCurrent = idx === currentIndex;
        const isPlaying = isCurrent && !audio.paused;
        btn.classList.toggle("is-current", isCurrent);
        btn.classList.toggle("is-playing", isPlaying);
        const cta = btn.querySelector(".track-cta");
        if (cta) cta.textContent = isPlaying ? "⏸" : "▶";
      });
    }

    function updateArt(track) {
      const artSrc = getTrackArt(track);
      if (els.songArtImg && artSrc) {
        els.songArtImg.src = encodeURI(artSrc);
        els.songArtImg.alt = `${track.title} artwork`;
        return;
      }
      if (!artSrc && els.songArtImg && els.songArtImg.parentNode) {
        els.songArtImg.remove();
      }
      if (!artSrc && els.artSquare && !els.artSquare.querySelector(".fallback")) {
        els.artSquare.insertAdjacentHTML("beforeend", `<div class="fallback">${shieldSvg(album.accentA, album.accentB, "tri")}</div>`);
      }
    }

    function setPlayButton(playing) {
      if (!els.playBtn) return;
      els.playBtn.innerHTML = `<span aria-hidden="true">${playing ? "⏸" : "▶"}</span><span>${playing ? "Pause" : "Play"}</span>`;
    }

    function updateNowUI() {
      const track = currentTrack();
      const playing = !audio.paused && !!audio.src;
      const pct = Number.isFinite(audio.duration) && audio.duration > 0
        ? Math.max(0, Math.min(100, (audio.currentTime / audio.duration) * 100))
        : 0;

      updateDocumentMeta(track);
      if (els.panel) els.panel.classList.toggle("is-playing", playing);
      if (els.headSongTitle) els.headSongTitle.textContent = track.title;
      if (els.lcdTrackTitle) els.lcdTrackTitle.textContent = track.title;
      if (els.nowKicker) els.nowKicker.textContent = `${playing ? "Playing" : "Paused"} ${String(currentIndex + 1).padStart(2, "0")} / ${tracks.length}`;
      if (els.nowLine) els.nowLine.textContent = track.title;
      if (els.nowSubline) els.nowSubline.textContent = playing ? album.subtitle : "Tap Play";
      if (els.timeNow) els.timeNow.textContent = fmtTime(audio.currentTime);
      if (els.timeTotal) els.timeTotal.textContent = fmtTime(audio.duration);
      if (els.seekNow) els.seekNow.textContent = fmtTime(audio.currentTime);
      if (els.seekTotal) els.seekTotal.textContent = fmtTime(audio.duration);
      if (els.progressFill) els.progressFill.style.width = `${pct}%`;
      setSeekPct(pct);
      if (!isSeeking && els.seekBar) {
        els.seekBar.value = Number.isFinite(audio.duration) && audio.duration > 0
          ? String(Math.round((audio.currentTime / audio.duration) * 1000))
          : "0";
      }
      if (els.discTrackNo) els.discTrackNo.textContent = String(currentIndex + 1).padStart(2, "0");
      if (els.discTrackMark) els.discTrackMark.textContent = playing ? "◉" : "◎";
      if (els.discLine) els.discLine.textContent = track.title;
      if (els.discSubline) els.discSubline.textContent = playing ? "spinning" : "paused";
      if (els.embedCodeBox) els.embedCodeBox.textContent = currentEmbedCode();
      setPlayButton(playing);
      updateTrackListUI();
      updateArt(track);
      try {
        const nextUrl = songUrl(album.key, currentIndex, embed ? { embed: 1 } : {});
        window.history.replaceState({}, "", nextUrl);
      } catch {
        // ignore
      }
    }

    async function loadTrack(index, autoplay = false) {
      if (index < 0 || index >= tracks.length) return;
      currentIndex = index;
      audio.src = currentTrack().src;
      audio.load();
      pulseControlSurface();
      updateNowUI();
      if (autoplay) await playCurrent();
    }

    async function playCurrent() {
      try {
        await audio.play();
      } catch (err) {
        console.warn("Song page playback blocked", err);
      }
      updateNowUI();
    }

    function togglePlay() {
      if (!audio.src) {
        loadTrack(currentIndex, true);
        return;
      }
      if (audio.paused) playCurrent();
      else audio.pause();
    }

    function nextTrack(fromEnded = false) {
      if (fromEnded && currentIndex >= tracks.length - 1) {
        audio.pause();
        updateNowUI();
        return;
      }
      const next = currentIndex < tracks.length - 1 ? currentIndex + 1 : 0;
      loadTrack(next, true);
    }

    function prevTrack() {
      if (audio.currentTime > 3) {
        audio.currentTime = 0;
        updateNowUI();
        return;
      }
      const prev = currentIndex > 0 ? currentIndex - 1 : tracks.length - 1;
      loadTrack(prev, true);
    }

    async function sendSong() {
      const track = currentTrack();
      try {
        const mode = await copyOrShare(absoluteSongUrl(), `${track.title} · ${album.label}`, `${track.title} — ${album.label}`);
        if (els.sendBtn) els.sendBtn.textContent = mode === "copied" ? "✓ Copied" : "✓ Sent";
      } catch (err) {
        if (!err || err.name !== "AbortError") window.prompt("Copy song URL", absoluteSongUrl());
        else return;
      }
      setTimeout(() => { if (els.sendBtn) els.sendBtn.textContent = "↗ Send"; }, 1200);
    }

    async function copyText(text, btn, reset) {
      try {
        if (navigator.clipboard?.writeText) {
          await navigator.clipboard.writeText(text);
          if (btn) btn.textContent = "✓ Copied";
          if (btn) setTimeout(() => { btn.textContent = reset; }, 1200);
          return;
        }
      } catch {
        // fallback prompt below
      }
      window.prompt("Copy", text);
    }

    if (els.sendBtn) els.sendBtn.addEventListener("click", sendSong);
    if (els.copyUrlBtn) els.copyUrlBtn.addEventListener("click", () => { vibrate(8); copyText(absoluteSongUrl(), els.copyUrlBtn, "Copy URL"); });
    if (els.copyEmbedBtn) els.copyEmbedBtn.addEventListener("click", () => { vibrate(8); copyText(currentEmbedCode(), els.copyEmbedBtn, "Embed"); });
    if (els.playBtn) els.playBtn.addEventListener("click", () => { vibrate(10); togglePlay(); });
    if (els.prevBtn) els.prevBtn.addEventListener("click", () => { vibrate(8); prevTrack(); });
    if (els.nextBtn) els.nextBtn.addEventListener("click", () => { vibrate(8); nextTrack(false); });

    els.trackBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        vibrate(8);
        const idx = Number(btn.getAttribute("data-track-index"));
        if (!Number.isFinite(idx)) return;
        if (idx === currentIndex) togglePlay();
        else loadTrack(idx, true);
      });
    });

    if (els.seekBar) {
      els.seekBar.addEventListener("pointerdown", () => { isSeeking = true; vibrate(6); });
      els.seekBar.addEventListener("pointerup", () => { isSeeking = false; vibrate(4); });
      els.seekBar.addEventListener("input", () => {
        isSeeking = true;
        setSeekPct(Number(els.seekBar.value) / 10);
        const now = performance.now();
        if (now - lastSeekBuzzAt > 85) {
          vibrate(2);
          lastSeekBuzzAt = now;
        }
        if (!Number.isFinite(audio.duration) || audio.duration <= 0) return;
        const target = (Number(els.seekBar.value) / 1000) * audio.duration;
        if (els.seekNow) els.seekNow.textContent = fmtTime(target);
      });
      els.seekBar.addEventListener("change", () => {
        if (!Number.isFinite(audio.duration) || audio.duration <= 0) {
          isSeeking = false;
          return;
        }
        audio.currentTime = (Number(els.seekBar.value) / 1000) * audio.duration;
        isSeeking = false;
        vibrate(6);
        updateNowUI();
      });
    }

    audio.addEventListener("play", updateNowUI);
    audio.addEventListener("pause", updateNowUI);
    audio.addEventListener("timeupdate", updateNowUI);
    audio.addEventListener("loadedmetadata", updateNowUI);
    audio.addEventListener("ended", () => nextTrack(true));
    audio.addEventListener("error", () => {
      if (els.nowKicker) els.nowKicker.textContent = "Error";
      if (els.nowSubline) els.nowSubline.textContent = "Could not load track";
    });

    updateNowUI();
    if (wantsAutoplay()) {
      loadTrack(currentIndex, true);
    }
  }

  mount();
})();
