# CUTBASTARD-1 — PATCH EXTRACTION & REFORGE
**Source:** 6 × 8.000s / 1280×720 / 24fps / h264 reels (V1–V6). Total raw: 48.000s.
**Conform target:** 2 trailers, 1920×1080, 2.39:1 scope, 24fps.
**Reel timecode:** each reel estimated from `01:00:00:00`.

---

# MATRIX O — OLOG STRUCTURAL MAP

## Brutal Structural Diagnosis

- **The source is not six shots. It is sixteen.** Five of six reels are pre-cut internal montages. V2 is four unrelated 2.000s locations welded end-to-end with no transitional logic; V1 carries six sub-shots in eight seconds. Only V5 is a single unbroken take. Anyone treating these files as atomic clips is cutting blind.
- **PATCH LAW cannot hold at 8–10s here and the material is why.** Location, camera distance and entity change every 1.5–2.0s. Honoring the trigger list produces patches of 0.83–3.04s. The law is overridden by the source, not by preference. Stated, not hidden.
- **V2 has no diegesis, it has an index.** Gallery → mocap lab → lecture theatre → concert stage, 2s each, same entity class, zero causal thread. It is a capability reel pretending to be a scene. Useful as a *category* generator; useless as continuity.
- **The only real continuity in 48 seconds is V5.** A single POV dolly down a server aisle, paws entering frame at 2.6s, contact with the table at 4.4s. It is the only patch with an uninterrupted causal chain, so it carries every act-opening in Trailer B.
- **V3's first cut is a lie of omission.** 00:00–03:01 reads as two shots but is one: the bear's head sinks out of the bottom of frame and the gallery is *revealed by subtraction*, not by a cut. Scene detection at 0.25 misses it, at 0.12 still misses it. Only frame-stepping exposes it.
- **V4 ships with burned-in text.** A lower-third caption — `"Puddle-Soot" / Pooh's depraved cousin` — lives in the first 1.5s. That is a source graphic, not an authored one. It must either be featured deliberately or cropped out. Trailer B features it; it is the only naming device in either cut that came free.
- **Sound is unusable as a bed.** Each reel carries its own 128kbps AAC generated stem with no shared acoustic space. Cross-cut at 0.3s intervals it becomes noise. Both conforms are scored to the song and the source audio is discarded.

## Olog Map

- `<Reel V1>` [contains] `<6 sub-shots>`
- `<Reel V2>` [contains] `<4 sub-shots, hard-cut on 2.000s grid>`
- `<Reel V5>` [contains] `<1 continuous take>`
- `<Bear-Scholar>` [wears] `<star-map mortarboard + gown>`
- `<Bear-Scholar>` [occupies] `<lecture hall / lectern / MacBook>`
- `<Honey>` [transfers from] `<jar>` [to] `<keyboard, book, lectern edge>`
- `<Honey>` [functions as] `<threshold marker: every V1 patch is honey-wet>`
- `<Projection screen>` [displays] `<portrait grid + terminal log>`
- `<Portrait grid>` [instantiates] `<archive, the obstacle the bear is answering>`
- `<Puddle-Soot (plush)>` [inhabits] `<data centre>` [and destroys] `<server racks>`
- `<Bear-POV (V5)>` [advances along] `<symmetric rack aisle>` [toward] `<lit wooden table>`
- `<Paws (V5)>` [cross] `<frame threshold at 01:00:02:14>`
- `<Framed drawing (V3)>` [is crushed by] `<bear paw>` [producing] `<glass field>`
- `<Shovel (V3)>` [scrapes] `<black soil across gallery floor>` [after] `<glass field>`
- `<Shovel>` [implies] `<a cleanup agent off-screen — the only unseen entity in the source>`
- `<Camera (V5)>` [holds] `<one-point perspective, no cut, 8.000s>`
- `<Camera (V2)>` [holds] `<wide, static-ish, 4 locations>` [and therefore] `<refuses coverage>`
- `<Light state (V1)>` [is] `<blown tungsten backlight + practical screen glow>`
- `<Light state (V3)>` [is] `<sepia gallery flood>`
- `<Light state (V4)>` [is] `<magenta/cyan rack light + weld-arc>`
- `<Light state divergence>` [enables] `<two-grade split: amber reel-set vs steel reel-set>`
- `<Beat A3 (burst)>` [compresses] `<patch duration to 0.291s>` [via] `<punch-in reframe of already-used patches>`
- `<Punch-in reframe>` [manufactures] `<new coverage from exhausted material>`
- `<Song s34 downbeat 0.817s>` [anchors] `<Trailer A act boundaries>`
- `<Song s02 breakdown 50.2–57.8s>` [hosts] `<Trailer B title card>`
- `<Pressure shift>` [is triggered by] `<threshold crossing, object transfer, or light-state change>` [never by] `<dialogue — there is none>`

## Structural Consequences

**Segmentation logic revealed.** The material segments on *institution*, not on story. Five institutional fields recur: the lecture hall (V1, V2c), the museum/gallery (V2a, V3), the machine room (V2b, V4, V5), the control/edit suite (V6), the concert stage (V2d). Every reel is a raid on one of them. This is the only through-line the footage actually supports, so both conforms are built as institution-cycles rather than as narratives.

**Most important patch triggers, ranked by frequency in the source:**
1. **Camera distance change** — dominant. Drives 9 of 16 patch starts.
2. **Location change** — hard, unmotivated, on a 2.000s grid in V2.
3. **Light state change** — the only trigger that is also a *grading* boundary; it splits the reels into a warm set (V1, V3, V2c) and a cold set (V4, V5, V6, V2b).
4. **Threshold crossing** — rare but load-bearing: paws entering frame (V5 @ 02:14), paw onto framed art (V3 @ 03:01).
5. **Object transfer** — honey (V1), cable (V4), soil (V3). The only trigger that survives being cut to 7 frames.

---

# MATRIX A — YAML PATCH GENOME

```yaml
title: "Bear raids five institutions, honey everywhere"
seed: "A bear in academic regalia and its plush counterpart destroy a lecture hall, a gallery, a data centre and a control room."
diegesis:
  premise: "Ursine entities occupy and dismantle human institutional spaces while equipment continues to run."
  world_rules:
    - "Bears operate human interfaces (keyboards, lecterns, mixing desks) without explanation."
    - "Humans are present but never intervene; they flee, watch, or continue seated."
    - "Every surface the bear touches becomes wet, broken, or burning."
    - "Screens keep displaying valid content after their room is destroyed."
  core_entities:
    - "Bear-Scholar (brown, star-map mortarboard, gown)"
    - "Bear-Black (gallery/lab/stage aggressor)"
    - "Puddle-Soot (yellow plush bear, red shirt, soot-and-honey face)"
    - "Bear-POV (first-person, ash-grey paws)"
    - "Human bystanders (fleeing, seated, running)"
    - "Honey / soil / glass / cable (transfer objects)"
  core_locations:
    - "Lecture hall with lectern, MacBook, projection screen"
    - "Museum gallery, sepia flood, framed charcoal works"
    - "Data centre / server aisle"
    - "Control-and-edit suite with waveform wall"
    - "Concert stage"

macro_structure:
  - unit_id: "U1"
    kind: "sequence"
    function: "Scholar occupies the lecture hall; honey saturates the apparatus."
  - unit_id: "U2"
    kind: "sequence"
    function: "Institutional index: four spaces breached in four cuts."
  - unit_id: "U3"
    kind: "sequence"
    function: "Gallery is entered, art is crushed underfoot, floor is scraped clean."
  - unit_id: "U4"
    kind: "sequence"
    function: "Plush entity dismantles the data centre from outside; POV entity dismantles it from inside."
  - unit_id: "U5"
    kind: "sequence"
    function: "Control suite runs unattended-but-operated; signal survives the operator."

beat_structure:
  - beat_id: "B1"
    parent_unit: "U1"
    syntagma_type: "accumulative"
    pressure_shift: "feeding -> presenting"
  - beat_id: "B2"
    parent_unit: "U1"
    syntagma_type: "alternating"
    pressure_shift: "presenting -> archive answers back"
  - beat_id: "B3"
    parent_unit: "U2"
    syntagma_type: "parallel"
    pressure_shift: "one room breached -> all rooms breached"
  - beat_id: "B4"
    parent_unit: "U3"
    syntagma_type: "continuous"
    pressure_shift: "looking at art -> standing on art"
  - beat_id: "B5"
    parent_unit: "U3"
    syntagma_type: "insertive"
    pressure_shift: "breakage -> removal of evidence"
  - beat_id: "B6"
    parent_unit: "U4"
    syntagma_type: "alternating"
    pressure_shift: "racks intact -> racks arcing"
  - beat_id: "B7"
    parent_unit: "U4"
    syntagma_type: "continuous"
    pressure_shift: "approach -> contact -> impact"
  - beat_id: "B8"
    parent_unit: "U5"
    syntagma_type: "accumulative"
    pressure_shift: "operating the desk -> becoming the signal"

patch_timeline:
  - patch_id: "P1A"
    start_time: "01:00:00:00"
    end_time: "01:00:01:11"
    location: "Lecture hall, behind lectern"
    entities_present: ["Bear-Scholar", "MacBook", "honey", "projection screen"]
    action_summary: "ECU bear face in honey-smeared star-map mortarboard, jaw working, paper flecks and honey droplets flying toward lens."
    camera_relation: "ECU, eye-level, locked, shallow depth"
    light_sound_state: "Hard tungsten key from screen-left, blown highlights; screen glow behind. Source audio: chewing, room tone."
    patch_trigger: "Reel head."
    rehydration_seed: "Extreme close-up of a brown bear wearing a honey-drenched academic mortarboard painted with a star chart, chewing, honey and torn paper suspended in the air, a network diagram glowing on a projection screen behind."
  - patch_id: "P1B"
    start_time: "01:00:01:11"
    end_time: "01:00:02:23"
    location: "Lecture hall, lectern"
    entities_present: ["Bear-Scholar", "honey jar", "MacBook"]
    action_summary: "Bear seated at open MacBook lifts a honey jar in one paw; honey strings onto the keyboard."
    camera_relation: "Medium shot, eye-level, slight push"
    light_sound_state: "Backlight blown to white; silhouette edges. Room tone."
    patch_trigger: "Camera distance change ECU -> MS; object (jar) enters."
    rehydration_seed: "Medium shot, a robed bear at a laptop lifting a glass honey jar, honey strands falling across the keys, window light blown out white behind it."
  - patch_id: "P1C"
    start_time: "01:00:02:23"
    end_time: "01:00:04:11"
    location: "Lecture hall, projection screen only"
    entities_present: ["projection screen", "portrait grid", "terminal text"]
    action_summary: "Screen fills frame: a 5×3 grid of Renaissance and Baroque portraits, two lines of terminal log text running beneath."
    camera_relation: "Medium-wide on screen surface, static, darkened room"
    light_sound_state: "Screen is the only source; room falls to black. Low hum."
    patch_trigger: "Entity exit — the bear leaves frame entirely; light state inverts."
    rehydration_seed: "A darkened lecture hall projection screen showing a grid of fifteen Renaissance portrait paintings with two lines of small terminal log text beneath, the room black around it."
  - patch_id: "P1D"
    start_time: "01:00:04:11"
    end_time: "01:00:05:22"
    location: "Lecture hall, lectern"
    entities_present: ["Bear-Scholar", "open book", "MacBook", "paper scraps"]
    action_summary: "Bear leans over a large open book beside the laptop, paws flat on the lectern, torn paper drifting."
    camera_relation: "Medium shot, slightly low, static"
    light_sound_state: "Same blown backlight; honey specular on fur. Page rustle."
    patch_trigger: "New object (book) enters; entity re-enters frame."
    rehydration_seed: "A bear in academic dress leaning over a large open book on a wooden lectern next to a laptop, torn paper scraps floating, hard white backlight."
  - patch_id: "P1E"
    start_time: "01:00:05:22"
    end_time: "01:00:07:04"
    location: "Lecture hall, lectern"
    entities_present: ["Bear-Scholar", "MacBook", "portrait grid behind"]
    action_summary: "Bear rears at the laptop with jaw wide open, honey and debris thrown outward; portrait grid now visible on the screen behind."
    camera_relation: "MCU, eye-level, static"
    light_sound_state: "Screen behind now carries the portrait grid — background content changed. Roar."
    patch_trigger: "Kinetic vector change: presenting -> vocalising; background content swap."
    rehydration_seed: "Medium close-up of a bear in a mortarboard roaring over a laptop, honey flying, a grid of old master portraits glowing on the screen behind it."
  - patch_id: "P1F"
    start_time: "01:00:07:04"
    end_time: "01:00:08:00"
    location: "Lectern edge"
    entities_present: ["honey", "gowned forearm", "wooden lectern"]
    action_summary: "ECU honey sheets over the front edge of the lectern past a gowned arm; long vertical light streaks."
    camera_relation: "ECU, macro, static, very shallow"
    light_sound_state: "Backlit honey, amber specular, vertical flare bars. Drip."
    patch_trigger: "Camera scale collapse to macro; entity reduced to fragment."
    rehydration_seed: "Macro shot of honey pouring over the edge of a wooden lectern beside a dark academic sleeve, backlit amber, long vertical lens flares."
  - patch_id: "P2A"
    start_time: "01:00:00:00"
    end_time: "01:00:02:00"
    location: "Museum gallery, white walls"
    entities_present: ["Bear-Black", "framed works", "fleeing humans"]
    action_summary: "Black bear charges through a white gallery tearing a framed drawing from the wall; two people in black flee and fall; red splatter on the wall."
    camera_relation: "Wide, low, static"
    light_sound_state: "Flat white gallery light. Impact and shouting."
    patch_trigger: "Reel head."
    rehydration_seed: "Wide shot of a black bear charging through a white-walled museum gallery, ripping a framed drawing off the wall, two people in black falling as they flee, red splatter across the wall."
  - patch_id: "P2B"
    start_time: "01:00:02:00"
    end_time: "01:00:04:00"
    location: "Motion-capture / server lab"
    entities_present: ["Bear-Black with green mocap markers", "technician", "server racks", "anatomy monitors"]
    action_summary: "Bear studded with green tracking markers pulls free of cabling; a technician runs; sparks burst from a rack; wall monitors show blue holographic human figures."
    camera_relation: "Wide, eye-level, static"
    light_sound_state: "Cold fluorescent + blue monitor glow. Electrical crack."
    patch_trigger: "Hard cut, location change (2.000s grid)."
    rehydration_seed: "Wide shot of a bear covered in green motion-capture markers tearing loose in a server lab, a technician running, sparks bursting from a rack, blue holographic anatomy figures on the wall monitors."
  - patch_id: "P2C"
    start_time: "01:00:04:00"
    end_time: "01:00:06:00"
    location: "Lecture theatre, raked seating"
    entities_present: ["Bear-Black", "seated academics", "broadcast camera", "charts", "laptop"]
    action_summary: "Bear rears at a lecture podium hurling printed charts into the air; academics remain seated; a broadcast camera and a laptop showing a video call sit in the foreground."
    camera_relation: "Wide, slightly low, static"
    light_sound_state: "Warm theatre spots. Paper and roar."
    patch_trigger: "Hard cut, location change."
    rehydration_seed: "Wide shot of a bear rearing at a lecture theatre podium, printed charts flying, rows of seated academics unmoving, a broadcast camera and an open laptop on a video call in the foreground."
  - patch_id: "P2D"
    start_time: "01:00:06:00"
    end_time: "01:00:08:00"
    location: "Concert stage"
    entities_present: ["Bear-Black", "upright bass", "conductor figure", "waveform LED wall", "pyro"]
    action_summary: "Bear plays an upright bass centre stage; a small conductor figure gestures at frame-left; a coloured waveform wall runs behind; pyrotechnic bursts fire on both sides."
    camera_relation: "Wide, eye-level, static"
    light_sound_state: "Stage dark, LED wall as key, sparks. Low string tone."
    patch_trigger: "Hard cut, location change."
    rehydration_seed: "Wide shot of a bear bowing an upright bass on a dark concert stage, a small conductor gesturing at the edge of frame, a coloured audio waveform wall behind, pyrotechnic fountains firing either side."
  - patch_id: "P3A"
    start_time: "01:00:00:00"
    end_time: "01:00:03:01"
    location: "Museum gallery, sepia"
    entities_present: ["Bear-Ranger (wet fur, ranger hat)", "framed charcoal works"]
    action_summary: "ECU wet bear face in a ranger hat holds, then sinks straight down out of frame, uncovering a symmetric gallery corridor with ceiling floods."
    camera_relation: "ECU locked; reveal by subject exit, NOT by cut"
    light_sound_state: "Warm sepia flood, heavy ceiling practicals, dust in beam. Breath."
    patch_trigger: "Reel head."
    rehydration_seed: "Locked extreme close-up of a wet black bear in a ranger hat that slowly sinks down out of frame, revealing a symmetrical sepia gallery corridor with bright ceiling lights and framed charcoal drawings."
  - patch_id: "P3B"
    start_time: "01:00:03:01"
    end_time: "01:00:05:00"
    location: "Gallery floor"
    entities_present: ["bear paw", "framed charcoal drawing", "glass"]
    action_summary: "A bear paw presses down onto a framed charcoal drawing lying on the floor; the glass fractures outward and scatters."
    camera_relation: "Low, close, static"
    light_sound_state: "Sepia flood, glass specular. Glass break."
    patch_trigger: "Threshold crossing — paw makes contact with the artwork plane."
    rehydration_seed: "Low close shot of a heavy bear paw pressing onto a framed charcoal drawing flat on a gallery floor, the glass fracturing and scattering outward."
  - patch_id: "P3C"
    start_time: "01:00:05:00"
    end_time: "01:00:08:00"
    location: "Gallery floor, wood"
    entities_present: ["shovel", "black soil", "glass shards", "bear feet at frame edge"]
    action_summary: "A shovel blade drags black soil and glass shards across a polished wood gallery floor; bear feet stand at the frame edge."
    camera_relation: "Low, close, slow drift"
    light_sound_state: "Sepia, reflective floor. Scrape."
    patch_trigger: "Object transfer — destruction becomes removal; new entity (shovel) enters."
    rehydration_seed: "Low shot of a shovel blade dragging black soil and broken glass across a polished wooden gallery floor, dark animal feet standing at the edge of frame."
  - patch_id: "P4A"
    start_time: "01:00:00:00"
    end_time: "01:00:01:12"
    location: "Data centre"
    entities_present: ["Puddle-Soot (yellow plush bear)", "burned-in caption"]
    action_summary: "ECU yellow plush bear face smeared with honey and soot, mouth open, red shirt; a lower-third caption reads \"Puddle-Soot\" / Pooh's depraved cousin."
    camera_relation: "ECU, eye-level, static, heavy bokeh"
    light_sound_state: "Cool practicals, teal monitor bokeh. Breath/hum."
    patch_trigger: "Reel head."
    rehydration_seed: "Extreme close-up of a filthy yellow plush bear in a red shirt, face smeared with honey and soot, mouth open, standing in a data centre with teal monitor bokeh behind."
  - patch_id: "P4B"
    start_time: "01:00:01:12"
    end_time: "01:00:05:11"
    location: "Data centre, rack face"
    entities_present: ["Puddle-Soot", "server racks", "cables", "anatomy monitors"]
    action_summary: "Plush paws grip and tear cabling from a rack face; a hard flare blooms; the room widens to magenta and violet light with holographic human figures on the monitors and a laser streak across frame."
    camera_relation: "MS on rack, then wide; bear eye holds at frame right"
    light_sound_state: "Rack LEDs, then magenta/violet wash and lens streak. Servo and tearing."
    patch_trigger: "Object transfer (cable) and light-state change to magenta."
    rehydration_seed: "Plush bear paws ripping cable bundles out of a server rack, a hard white flare, the room washing into magenta and violet with holographic human anatomy figures glowing on the monitors."
  - patch_id: "P4C"
    start_time: "01:00:05:11"
    end_time: "01:00:08:00"
    location: "Data centre floor"
    entities_present: ["torn monitor", "cable bundle", "weld-arc sparks", "Puddle-Soot eye"]
    action_summary: "A monitor lies torn open on the floor; cables arc and throw welding-bright sparks; smoke rolls; the plush bear's eye watches from frame right."
    camera_relation: "Low, close, static; bear eye in extreme foreground right"
    light_sound_state: "Arc light as key, everything else falls off. Electrical arc."
    patch_trigger: "Camera scale change and light state change to arc."
    rehydration_seed: "A torn-open monitor on a data centre floor with cables throwing welding-bright sparks and smoke, an out-of-focus plush bear eye watching from the right edge of frame."
  - patch_id: "P5A"
    start_time: "01:00:00:00"
    end_time: "01:00:02:14"
    location: "Server aisle"
    entities_present: ["Bear-POV", "server racks", "lit wooden table", "ash"]
    action_summary: "First-person push down a perfectly symmetrical server aisle toward a small lit wooden table; ash and steam drift through frame."
    camera_relation: "POV, one-point perspective, steady dolly-in"
    light_sound_state: "Single hard overhead lamp at the vanishing point; racks in shadow. Hum."
    patch_trigger: "Reel head."
    rehydration_seed: "First-person point-of-view pushing slowly down a symmetrical server room aisle toward a small wooden table under a single hanging lamp, ash and steam drifting through the frame."
  - patch_id: "P5B"
    start_time: "01:00:02:14"
    end_time: "01:00:04:10"
    location: "Server aisle, at the table"
    entities_present: ["Bear-POV paws", "table", "network gear"]
    action_summary: "Ash-grey bear paws swing into frame from the bottom edge and sweep across the tabletop, scattering small hardware."
    camera_relation: "POV, continuous, same lens"
    light_sound_state: "Same lamp; motion blur on paws. Clatter."
    patch_trigger: "Threshold crossing — the operator's own limbs enter frame for the first time."
    rehydration_seed: "First-person view as two ash-covered bear paws swing up into frame and sweep small network hardware off a lit wooden table in a server aisle."
  - patch_id: "P5C"
    start_time: "01:00:04:10"
    end_time: "01:00:06:07"
    location: "Server aisle, rack face"
    entities_present: ["Bear-POV paws", "keyboard", "switch gear", "cables"]
    action_summary: "Paws strike down onto a keyboard set into the rack face; cables whip; debris scatters across the white floor."
    camera_relation: "POV, continuous, slight drop"
    light_sound_state: "Overhead lamp, cold floor bounce. Impact."
    patch_trigger: "Kinetic vector change: sweeping -> striking; new object (keyboard)."
    rehydration_seed: "First-person view of heavy ash-covered bear paws slamming down onto a keyboard mounted in a server rack, cables whipping, debris scattering on a white floor."
  - patch_id: "P5D"
    start_time: "01:00:06:07"
    end_time: "01:00:08:00"
    location: "Server aisle, at the table"
    entities_present: ["Bear-POV paws", "table", "steam"]
    action_summary: "Steam bursts across frame; both paws come down flat on the table edge and hold."
    camera_relation: "POV, continuous, settles"
    light_sound_state: "Steam diffuses the lamp into a bloom. Hiss."
    patch_trigger: "Environmental change (steam) and motion arrest."
    rehydration_seed: "First-person view as steam bursts across a server aisle and two ash-covered bear paws come down flat on a wooden table edge and stop."
  - patch_id: "P6A"
    start_time: "01:00:00:00"
    end_time: "01:00:01:23"
    location: "Control suite, oversized console"
    entities_present: ["Bear-Black", "oversized keyboard", "kaleidoscope wall"]
    action_summary: "Bear hammers an oversized keyboard; keycaps and debris fly; a symmetrical kaleidoscopic laser wall pulses behind."
    camera_relation: "MCU, low, static, wide lens"
    light_sound_state: "Screen wall is the only key; hard rim on fur. Key impacts."
    patch_trigger: "Reel head."
    rehydration_seed: "Medium close-up from below of a black bear hammering an oversized keyboard, keycaps flying, a symmetrical white kaleidoscopic laser pattern pulsing on the wall behind."
  - patch_id: "P6B"
    start_time: "01:00:01:23"
    end_time: "01:00:04:11"
    location: "Edit suite"
    entities_present: ["Bear-Black", "colour-bar monitors", "quadcopter drone", "code projection"]
    action_summary: "Wide of an edit bay: bear hunched at a desk of colour-bar monitors, a quadcopter hovering above it, a code-and-window projection filling the back wall; a puff of smoke rises."
    camera_relation: "Wide, eye-level, static"
    light_sound_state: "Monitor glow only, deep black surround. Rotor whine."
    patch_trigger: "Camera distance change MCU -> WS; new entity (drone)."
    rehydration_seed: "Wide shot of a dark edit suite, a bear hunched over a desk of colour-bar monitors, a small quadcopter hovering above, a wall-sized projection of code windows behind, smoke rising."
  - patch_id: "P6C"
    start_time: "01:00:04:11"
    end_time: "01:00:06:12"
    location: "Control suite, light table"
    entities_present: ["Bear-Black", "illuminated light table", "waveform screens", "tungsten lamps"]
    action_summary: "Bear's head and both paws come down over a glowing light table; waveform and geometric graphics on the screens behind; a steam plume rises from the surface."
    camera_relation: "ECU/MCU, low, symmetrical, static"
    light_sound_state: "Underlit from the table, tungsten kickers either side. Steam hiss."
    patch_trigger: "Camera distance change and light direction inversion (underlight)."
    rehydration_seed: "Low symmetrical close-up of a bear's head and paws over a glowing white light table, audio waveform and geometric graphics on the screens behind, tungsten lamps either side, steam rising off the surface."
  - patch_id: "P6D"
    start_time: "01:00:06:12"
    end_time: "01:00:08:00"
    location: "Stage / edit bay, wooden deck"
    entities_present: ["Bear-Black", "low desk", "waveform projection", "cables"]
    action_summary: "Wide of a wooden stage deck; the bear crouches over a low desk trailing cables; a large waveform projection fills the wall; red curtain at the frame edge."
    camera_relation: "Wide, eye-level, static, symmetrical"
    light_sound_state: "Projection as key, stage otherwise dark. Room tone."
    patch_trigger: "Location/scale change to wide stage."
    rehydration_seed: "Wide symmetrical shot of a bear crouched over a low desk on a wooden stage deck, cables trailing across the floor, a large white audio waveform projected on the wall behind, red curtain at the edge of frame."
```

---

# MATRIX B — MARKDOWN STORY MAP

# Diegesis
Ursine entities occupy five human institutions — lecture hall, gallery, data centre, control suite, concert stage — and dismantle the apparatus while it keeps running. No dialogue. Pressure is carried entirely by threshold crossings and object transfer: honey, cable, soil, glass.

# Macro Structure

## U1 — THE LECTURE HALL (Reel V1)
### B1 — Feeding becomes presenting
#### P1A - 01:00:00:00 → 01:00:01:11
- **Action**: ECU bear in honey-drenched star-map mortarboard, jaw working, debris toward lens.
- **Camera/Environment**: ECU locked, blown tungsten key, network diagram on screen behind.
- **Pressure Shift**: consuming -> being watched
- **Seed**: Extreme close-up of a brown bear in a honey-covered star-chart mortarboard chewing, honey and torn paper in the air, a glowing network diagram behind.
#### P1B - 01:00:01:11 → 01:00:02:23
- **Action**: Bear lifts a honey jar over an open MacBook; honey strings onto the keys.
- **Camera/Environment**: MS, backlight blown white.
- **Pressure Shift**: eating -> contaminating the instrument
- **Seed**: Medium shot of a robed bear lifting a glass honey jar over a laptop keyboard, honey falling across the keys.
#### P1D - 01:00:04:11 → 01:00:05:22
- **Action**: Bear leans over a large open book beside the laptop, paper drifting.
- **Camera/Environment**: MS slightly low, static.
- **Pressure Shift**: contaminating -> consulting
- **Seed**: A bear in academic dress leaning over a large open book on a lectern next to a laptop, torn paper drifting.

### B2 — The archive answers back
#### P1C - 01:00:02:23 → 01:00:04:11
- **Action**: Screen fills frame — grid of fifteen old-master portraits over two lines of terminal log.
- **Camera/Environment**: MW on screen, room falls to black.
- **Pressure Shift**: bear present -> bear absent, archive speaking
- **Seed**: A darkened lecture hall screen showing a grid of Renaissance portraits with terminal log text beneath.
#### P1E - 01:00:05:22 → 01:00:07:04
- **Action**: Bear rears at the laptop, jaw wide, honey thrown outward; portrait grid now behind.
- **Camera/Environment**: MCU, static; background content has swapped.
- **Pressure Shift**: consulting -> declaring
- **Seed**: Medium close-up of a bear in a mortarboard roaring over a laptop, old-master portraits glowing behind.
#### P1F - 01:00:07:04 → 01:00:08:00
- **Action**: Honey sheets over the lectern edge past a gowned arm.
- **Camera/Environment**: Macro, backlit amber, vertical flare bars.
- **Pressure Shift**: declaring -> residue
- **Seed**: Macro of honey pouring over a wooden lectern edge beside a dark academic sleeve, backlit amber.

## U2 — THE INDEX (Reel V2)
### B3 — One room breached becomes all rooms breached
#### P2A - 01:00:00:00 → 01:00:02:00
- **Action**: Bear charges a white gallery, tears a framed drawing down; people fall fleeing; red splatter.
- **Camera/Environment**: WS low static, flat gallery light.
- **Pressure Shift**: institution intact -> institution breached
- **Seed**: Wide shot of a black bear tearing a framed drawing off a white gallery wall as two people in black fall while fleeing.
#### P2B - 01:00:02:00 → 01:00:04:00
- **Action**: Mocap-markered bear pulls free of cabling; technician runs; rack sparks.
- **Camera/Environment**: WS, cold fluorescent and blue monitor glow.
- **Pressure Shift**: measured -> unmeasurable
- **Seed**: Wide shot of a bear covered in green motion-capture markers tearing loose in a server lab, sparks from a rack, blue anatomy holograms on the monitors.
#### P2C - 01:00:04:00 → 01:00:06:00
- **Action**: Bear rears at a lecture podium; charts fly; academics stay seated; broadcast camera rolls.
- **Camera/Environment**: WS slightly low, warm theatre spots.
- **Pressure Shift**: disruption -> disruption being recorded
- **Seed**: Wide shot of a bear rearing at a lecture podium, printed charts flying, seated academics unmoving, a broadcast camera in the foreground.
#### P2D - 01:00:06:00 → 01:00:08:00
- **Action**: Bear plays upright bass centre stage; conductor gestures; pyro fires.
- **Camera/Environment**: WS, LED waveform wall as key.
- **Pressure Shift**: breaking the instrument -> playing the instrument
- **Seed**: Wide shot of a bear bowing an upright bass on a dark stage, a coloured waveform wall behind, pyrotechnics firing either side.

## U3 — THE GALLERY (Reel V3)
### B4 — Looking at art becomes standing on art
#### P3A - 01:00:00:00 → 01:00:03:01
- **Action**: ECU wet bear in ranger hat sinks out of frame, revealing the gallery corridor by subtraction.
- **Camera/Environment**: ECU locked; reveal without a cut; sepia flood, ceiling practicals.
- **Pressure Shift**: face fills the world -> the room is empty
- **Seed**: Locked close-up of a wet bear in a ranger hat sinking out of frame to reveal a symmetrical sepia gallery with bright ceiling lights.
#### P3B - 01:00:03:01 → 01:00:05:00
- **Action**: Paw presses a framed charcoal drawing on the floor; glass fractures outward.
- **Camera/Environment**: Low close static, glass specular.
- **Pressure Shift**: art on the wall -> art underfoot
- **Seed**: Low close shot of a bear paw pressing a framed charcoal drawing flat on the floor, glass fracturing outward.

### B5 — Breakage becomes removal
#### P3C - 01:00:05:00 → 01:00:08:00
- **Action**: A shovel drags black soil and glass across polished wood; bear feet at frame edge.
- **Camera/Environment**: Low, slow drift, reflective floor.
- **Pressure Shift**: evidence made -> evidence moved
- **Seed**: Low shot of a shovel dragging black soil and broken glass across a polished wooden gallery floor, dark animal feet at the edge of frame.

## U4 — THE MACHINE ROOM (Reels V4, V5)
### B6 — Racks intact becomes racks arcing
#### P4A - 01:00:00:00 → 01:00:01:12
- **Action**: ECU yellow plush bear, honey-and-soot face, red shirt; burned-in caption names it.
- **Camera/Environment**: ECU static, teal monitor bokeh.
- **Pressure Shift**: anonymous -> named
- **Seed**: Extreme close-up of a filthy yellow plush bear in a red shirt in a data centre, teal bokeh behind.
#### P4B - 01:00:01:12 → 01:00:05:11
- **Action**: Plush paws tear cable from a rack; flare; room washes magenta with anatomy holograms.
- **Camera/Environment**: MS to WS, magenta/violet, laser streak.
- **Pressure Shift**: touching the machine -> gutting the machine
- **Seed**: Plush bear paws ripping cables from a server rack, the room washing magenta with holographic human figures on the monitors.
#### P4C - 01:00:05:11 → 01:00:08:00
- **Action**: Torn monitor on the floor; cables throw weld-bright sparks; smoke; the bear's eye watches.
- **Camera/Environment**: Low close static, arc as sole key.
- **Pressure Shift**: gutting -> burning
- **Seed**: A torn-open monitor on a data centre floor throwing welding-bright sparks, an out-of-focus plush bear eye at the right edge.

### B7 — Approach, contact, impact
#### P5A - 01:00:00:00 → 01:00:02:14
- **Action**: POV push down a symmetric server aisle toward a lit table; ash drifts.
- **Camera/Environment**: POV one-point dolly-in, single vanishing-point lamp.
- **Pressure Shift**: distance -> approach
- **Seed**: First-person push down a symmetrical server aisle toward a small wooden table under a single lamp, ash drifting.
#### P5B - 01:00:02:14 → 01:00:04:10
- **Action**: Ash-grey paws swing in from the bottom edge and sweep the tabletop clear.
- **Camera/Environment**: POV continuous, motion blur.
- **Pressure Shift**: observer -> participant
- **Seed**: First-person view as ash-covered bear paws sweep hardware off a lit wooden table in a server aisle.
#### P5C - 01:00:04:10 → 01:00:06:07
- **Action**: Paws strike a rack-mounted keyboard; cables whip; debris scatters.
- **Camera/Environment**: POV continuous, slight drop.
- **Pressure Shift**: sweeping -> striking
- **Seed**: First-person view of bear paws slamming onto a keyboard in a server rack, cables whipping, debris across a white floor.
#### P5D - 01:00:06:07 → 01:00:08:00
- **Action**: Steam bursts; both paws land flat on the table edge and hold.
- **Camera/Environment**: POV settles, lamp blooms through steam.
- **Pressure Shift**: striking -> arrest
- **Seed**: First-person view as steam bursts and two bear paws come down flat on a wooden table edge and stop.

## U5 — THE CONTROL SUITE (Reel V6)
### B8 — Operating the desk becomes being the signal
#### P6A - 01:00:00:00 → 01:00:01:23
- **Action**: Bear hammers an oversized keyboard; keycaps fly; kaleidoscope wall pulses.
- **Camera/Environment**: MCU low wide-lens, screen wall as only key.
- **Pressure Shift**: interface offered -> interface overloaded
- **Seed**: Low medium close-up of a bear hammering an oversized keyboard, keycaps flying, a kaleidoscopic laser pattern behind.
#### P6B - 01:00:01:23 → 01:00:04:11
- **Action**: Wide edit bay; bear at colour-bar monitors, drone hovering, code projection, smoke.
- **Camera/Environment**: WS static, monitor glow only.
- **Pressure Shift**: one operator -> a whole facility running itself
- **Seed**: Wide shot of a dark edit suite with a bear at colour-bar monitors, a quadcopter above, a wall of projected code.
#### P6C - 01:00:04:11 → 01:00:06:12
- **Action**: Head and paws come down over a glowing light table; steam rises.
- **Camera/Environment**: Low symmetric ECU, underlit, tungsten kickers.
- **Pressure Shift**: operating -> being lit from beneath by the work
- **Seed**: Low symmetrical close-up of a bear over a glowing light table, waveform graphics behind, steam rising.
#### P6D - 01:00:06:12 → 01:00:08:00
- **Action**: Wide wooden stage deck; bear crouched over a low desk; waveform fills the wall.
- **Camera/Environment**: WS symmetric static, projection as key.
- **Pressure Shift**: room -> stage; private work -> broadcast
- **Seed**: Wide symmetrical shot of a bear crouched over a low desk on a wooden stage, a large waveform projected behind, cables across the floor.

---

# MATRIX E — JSON SCENE BLUEPRINT

```json
{
  "Scene_Blueprint": {
    "Bear-Scholar": {
      "Previous_Scene": {
        "who": "An unranked animal outside the credentialing apparatus",
        "what": "Obtained honey and academic regalia; both arrive already damaged and smeared",
        "when": "Before reel head; inferred from the state of the cap and gown at 01:00:00:00",
        "where": "Outside the lecture hall",
        "why": "Access to the lectern requires the costume; the honey is what it actually came for",
        "how": "Not shown. Only its residue is on screen — honey saturating cap, fur, keys and book"
      },
      "Current_Scene": {
        "who": "Occupant of the lectern, operating the hall's apparatus",
        "what": "Chews, lifts a honey jar over the laptop, consults an open book, rears and roars at the screen",
        "when": "V1 01:00:00:00 → 01:00:08:00, continuous within the hall",
        "where": "Lecture hall: lectern, MacBook, projection screen",
        "why": "The screen changes from a network diagram to a grid of old-master portraits between P1A and P1E — the apparatus answers, and the bear escalates to vocalising at it",
        "how": "Blown tungsten backlight, honey specular on fur, paper flecks in the air, jaw open, honey finally sheeting over the lectern edge"
      },
      "Update_Scene": {
        "who": "Residue — the entity has left, the surface has not",
        "what": "Honey continues pouring over the lectern edge after the body exits the frame",
        "when": "V1 01:00:07:04 → 01:00:08:00",
        "where": "Lectern edge, macro",
        "why": "Gravity; the jar was tipped in P1B and nothing stopped it",
        "how": "Amber backlit sheet, vertical flare bars, no motion but the fall"
      }
    },
    "Puddle-Soot": {
      "Previous_Scene": {
        "who": "A plush toy that has already been through fire and honey",
        "what": "Acquired soot and honey coating; entered a secured data centre",
        "when": "Before V4 reel head",
        "where": "Outside the data centre",
        "why": "Inferred only from the coating on its face at 01:00:00:00 — it arrives already contaminated",
        "how": "Not shown; teal monitor bokeh establishes the room it has already reached"
      },
      "Current_Scene": {
        "who": "The agent tearing the facility apart by hand",
        "what": "Grips and rips cable bundles from a rack face; the room floods magenta; a monitor ends up torn open and arcing on the floor",
        "when": "V4 01:00:00:00 → 01:00:08:00",
        "where": "Data centre: rack face, floor, monitor wall",
        "why": "The racks are the only thing in the room that resists; it goes at the cabling first, which is the part that comes away",
        "how": "Plush paws against metal, hard flare, magenta and violet wash, laser streak, then weld-bright arc and smoke"
      },
      "Update_Scene": {
        "who": "A watcher at the edge of its own damage",
        "what": "Holds at frame right, out of focus, while the torn monitor arcs and smokes",
        "when": "V4 01:00:05:11 → 01:00:08:00",
        "where": "Data centre floor",
        "why": "The destruction is now self-sustaining — the arcing needs no further contact",
        "how": "Arc light is the only key; the bear's eye is a dark unfocused mass in the foreground"
      }
    },
    "Bear-POV": {
      "Previous_Scene": {
        "who": "An unseen body already inside the facility",
        "what": "Reached the head of a server aisle; acquired an ash coating",
        "when": "Before V5 reel head",
        "where": "Server room, upstream of the aisle",
        "why": "Ash on the paws at first contact indicates it passed through fire or debris to get here",
        "how": "Not shown — the camera is its eyes and the eyes are already in the corridor"
      },
      "Current_Scene": {
        "who": "The operator, seen only as its own two paws",
        "what": "Pushes down the aisle, sweeps a table clear, strikes a rack keyboard, lands both paws flat as steam bursts",
        "when": "V5 01:00:00:00 → 01:00:08:00, one unbroken take",
        "where": "Symmetrical server aisle, lit wooden table at the vanishing point",
        "why": "The lit table at the end of the corridor is the only illuminated object; the movement is toward it and stops on it",
        "how": "One-point perspective, steady dolly-in, single overhead lamp, ash and steam through frame, paws entering from the bottom edge at 01:00:02:14"
      },
      "Update_Scene": {
        "who": "A stopped body with both hands on the target",
        "what": "Both paws rest flat on the table edge; steam blooms the lamp",
        "when": "V5 01:00:06:07 → 01:00:08:00",
        "where": "At the table",
        "why": "The approach is complete; there is nothing further down the aisle",
        "how": "Motion arrest, diffused key, hiss"
      }
    },
    "The Gallery": {
      "Previous_Scene": {
        "who": "A hung, lit, intact exhibition",
        "what": "Framed charcoal works on the wall under ceiling floods",
        "when": "Before V3 01:00:03:01; visible intact in the reveal at 01:00:02:00",
        "where": "Sepia gallery corridor",
        "why": "It is a gallery; the works are on the wall because that is where they are kept",
        "how": "Symmetrical corridor, bright ceiling practicals, dust in the beams"
      },
      "Current_Scene": {
        "who": "A room being converted into debris",
        "what": "A framed drawing lies on the floor; a paw presses it; the glass fractures and scatters",
        "when": "V3 01:00:03:01 → 01:00:05:00",
        "where": "Gallery floor",
        "why": "The work came off the wall before this patch — the frame is already down when the paw arrives",
        "how": "Low static close shot, glass specular, fracture propagating outward from the point of contact"
      },
      "Update_Scene": {
        "who": "A crime scene being cleared",
        "what": "A shovel drags black soil and glass across the polished wood",
        "when": "V3 01:00:05:00 → 01:00:08:00",
        "where": "Gallery floor, wood",
        "why": "Someone off-screen is holding the shovel — the only entity in 48 seconds that is inferred and never shown",
        "how": "Slow drift, scrape, dark feet standing at the frame edge"
      }
    }
  }
}
```

---

# MATRIX F — PATCH REFORGE STACK

## P1A — 01:00:00:00 to 01:00:01:11
- **Patch Event**: ECU bear in honey-soaked star-map mortarboard, jaw working, debris toward lens.
- **Base Patch Prompt**: Close-up of a bear wearing a graduation cap, chewing.
- **Clarified Prompt**: Extreme close-up of a brown bear's face filling frame, wearing a wide academic mortarboard painted with a dark blue star chart and drenched in honey; jaw working; honey droplets and torn paper flecks suspended between the face and the lens.
- **Cinematic Prompt**: 85mm, T2.0, extreme close-up, locked off, eye-level. Hard tungsten key from screen-left blowing the left edge of the frame; practical glow from a projection screen behind rimming the ears. Shallow focus holding the muzzle, falling off by the cap brim. Amber specular on wet fur.
- **Director Prompt**: Hold the frame absolutely still and let the animal be the only motion. The chew is continuous and unhurried — it does not know it is being watched. Debris must cross the lens plane at least twice so the audience feels the distance is unsafe. No reaction, no glance to camera.
- **Stress-Test Prompt**: Single 1.5-second take, no cut, no camera move, 24fps. Cap must remain within frame at all times; muzzle must never leave the centre third. Honey must be visibly *dripping*, not static. Background screen legible but out of focus. No human in frame. No blink.
- **Master Patch Prompt**: Locked-off 85mm extreme close-up, eye-level, of a brown bear's face filling the frame in a honey-drenched academic mortarboard painted with a blue star chart; jaw working slowly and continuously; honey droplets and torn paper crossing the lens plane; hard tungsten key from screen-left blowing out the frame edge, a defocused network diagram glowing on a projection screen behind; shallow focus on the muzzle, amber specular on wet fur; 1.5s, no cut, no camera move.

## P1F — 01:00:07:04 to 01:00:08:00
- **Patch Event**: Honey sheets over the front edge of a lectern past a gowned forearm.
- **Base Patch Prompt**: Close-up of honey pouring over a wooden edge.
- **Clarified Prompt**: Macro shot of honey sheeting over the front edge of a wooden lectern, a dark academic sleeve just behind it, the honey falling in a continuous unbroken curtain.
- **Cinematic Prompt**: 100mm macro, T2.8, extreme close-up, static, backlit. Long vertical lens-flare bars from a hard source behind. Amber transmission through the honey; wood grain in the near field; everything past the sleeve falls to black.
- **Director Prompt**: This is the residue shot — the body has already left. Nothing acts. Let gravity be the only performer and hold long enough that the audience registers that no one is stopping it. The sleeve must be still.
- **Stress-Test Prompt**: 0.8-second take, no camera move, no cut. Honey must be continuous, not droplets. At least three vertical flare bars. No face, no eye, no full body — fragment only. Focus plane on the honey curtain, not the wood.
- **Master Patch Prompt**: Static 100mm macro, backlit, of honey sheeting in a continuous curtain over the front edge of a wooden lectern past a still dark academic sleeve; long vertical lens-flare bars from a hard rear source; amber transmission through the honey, wood grain in the near field, black falloff behind; no body, no motion but the fall; 0.8s, locked.

## P3A — 01:00:00:00 to 01:00:03:01
- **Patch Event**: ECU wet bear in a ranger hat sinks out of frame, uncovering the gallery corridor.
- **Base Patch Prompt**: A bear in a hat moves down out of frame revealing a gallery.
- **Clarified Prompt**: Locked extreme close-up of a wet black bear wearing a wide flat-brimmed ranger hat; it descends vertically out of the bottom of frame, uncovering a symmetrical sepia gallery corridor with bright ceiling floods and framed charcoal drawings on both walls.
- **Cinematic Prompt**: 35mm, T2.8, locked off, eye-level, centred. Warm sepia flood; hard ceiling practicals flaring into the lens once uncovered; visible dust in the beams. Deep focus so the corridor resolves the instant the head clears frame.
- **Director Prompt**: The reveal is by subtraction, not by a cut and not by a camera move — the camera never touches this. The descent is slow and even, no dip, no bounce. The audience should realise the room was always there and the animal was simply in the way.
- **Stress-Test Prompt**: One continuous 3-second take. Camera absolutely locked — no pan, tilt, dolly or zoom. Bear must exit frame bottom only, at constant speed, fully clearing by 2.6s. Corridor must be perfectly symmetrical about the vertical centre line. No cut anywhere in the take.
- **Master Patch Prompt**: One continuous locked-off 35mm shot, eye-level and centred: a wet black bear in a wide flat-brimmed ranger hat fills frame, then descends vertically out of the bottom at constant speed, uncovering a perfectly symmetrical sepia gallery corridor with hard ceiling floods flaring into the lens, dust visible in the beams, framed charcoal drawings on both walls; deep focus, no camera move, no cut, 3s.

## P4B — 01:00:01:12 to 01:00:05:11
- **Patch Event**: Plush paws tear cable from a rack; hard flare; the room washes magenta with anatomy holograms.
- **Base Patch Prompt**: A teddy bear pulls cables out of a server.
- **Clarified Prompt**: A filthy yellow plush bear's paws grip and tear bundled cables out of the face of a server rack; a hard white flare blooms across frame; the shot widens to a data centre lit magenta and violet, holographic human anatomy figures glowing on the wall monitors, a laser streak crossing the frame.
- **Cinematic Prompt**: 24mm, T2.8, medium on the rack face widening to a wide. Rack LEDs as near key; magenta and violet wash from the monitor wall; anamorphic streak across frame; hard flare bloom at the transition. Plush fibre catching every light source.
- **Director Prompt**: The tearing must be two-handed and effortful — the cable resists, then gives all at once. Let the flare hide the scale change so the widening reads as the room revealing itself rather than as a camera move. Keep the bear's eye at frame right through the wide so the audience knows who is still in the room.
- **Stress-Test Prompt**: 4-second take. Cable must visibly detach — a pull with no separation fails the shot. Colour must transition from neutral rack light to magenta/violet within the take, not before it. Exactly one laser streak. Bear eye must remain in the right third of the wide. No human.
- **Master Patch Prompt**: 24mm handheld-steady take starting medium on a server rack face: a filthy yellow plush bear's paws grip a bundled cable two-handed, strain, and tear it free; a hard white flare blooms and the frame widens to a data centre washed magenta and violet, holographic human anatomy figures on the wall monitors, a single anamorphic laser streak crossing frame, the bear's out-of-focus eye holding the right third; plush fibre catching every source; 4s, one take.

## P5A — 01:00:00:00 to 01:00:02:14
- **Patch Event**: First-person push down a symmetrical server aisle toward a lit wooden table.
- **Base Patch Prompt**: POV walking down a server room aisle.
- **Clarified Prompt**: First-person point-of-view moving steadily down a perfectly symmetrical server aisle toward a small wooden table at the far end lit by a single hanging lamp; ash and steam drifting through the frame.
- **Cinematic Prompt**: 21mm, T2.8, POV, steady dolly-in at walking pace, exact one-point perspective. Single hard overhead practical at the vanishing point as the only key; rack faces falling to black either side with scattered status LEDs. Ash particles catching the lamp.
- **Director Prompt**: The camera is the animal's eyes and must move like a body, not a dolly — slight vertical rhythm, no lateral drift. The vanishing point must stay dead centre for the whole move so the corridor reads as a barrel pointed at the table. Do not reveal the paws in this patch; the body stays unseen.
- **Stress-Test Prompt**: 2.6-second continuous take. Vanishing point locked to frame centre within a few pixels. No paws, no limbs, no body in frame at any point. Only one light source. Ash must drift through at least two depth planes. No cut, no whip, no rack focus.
- **Master Patch Prompt**: Continuous 21mm first-person point-of-view pushing at walking pace down a perfectly symmetrical server aisle in exact one-point perspective, vanishing point locked dead centre, toward a small wooden table lit by a single hard overhead lamp; rack faces falling to black either side with scattered status LEDs; ash and steam drifting across two depth planes; slight vertical body rhythm, no lateral drift, no limbs in frame; 2.6s, one take.

## P6C — 01:00:04:11 to 01:00:06:12
- **Patch Event**: Bear's head and paws come down over a glowing light table; steam rises off the surface.
- **Base Patch Prompt**: A bear leans over a glowing table.
- **Clarified Prompt**: Low symmetrical close shot of a bear's head and both front paws coming down over an illuminated white light table; audio waveform and geometric graphics on the screens behind; a plume of steam rising off the table surface.
- **Cinematic Prompt**: 40mm, T2.0, low, dead-centre symmetrical, static. Key comes from *below* — the light table underlighting the muzzle and the undersides of the paws; tungsten kicker lamps either side rimming the shoulders; screens behind supplying cool fill. Steam catching the underlight.
- **Director Prompt**: Underlight is the whole shot — stage the head so the table throws the light up into the muzzle and the eyes stay in shadow. Both paws land at the same moment, framing the light source symmetrically. The steam must rise *after* the paws land, so it reads as a consequence.
- **Stress-Test Prompt**: 2-second take, camera locked, perfectly symmetrical about the vertical centre. Dominant key must come from below — any top-light fails the shot. Both paws in frame, equidistant from centre. Steam must begin after the paws contact. Waveform graphics legible behind.
- **Master Patch Prompt**: Locked 40mm low shot, perfectly symmetrical about the vertical centre: a bear's head and both front paws come down together over an illuminated white light table that underlights the muzzle from below and leaves the eyes in shadow; tungsten kicker lamps either side rimming the shoulders; audio waveform and geometric graphics legible on the screens behind; a steam plume rising off the surface after the paws contact; 2s, static.
