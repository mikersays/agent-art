#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const axios = require('axios');
const sharp = require('sharp');
const { execSync } = require('child_process');

// ── Paths ──────────────────────────────────────────────────────────────────
const DIR          = __dirname;
const REPO_ROOT    = path.resolve(DIR, '..');
const BAUHAUS_DIR  = path.join(REPO_ROOT, 'bauhaus');
const STATE_FILE   = path.join(DIR, 'state.json');
const LOG_FILE     = path.join(DIR, 'log.json');
const TMP_PNG      = path.join(DIR, 'tmp_post.png');
const ARCHIVE_DIR  = path.join(DIR, 'archive');
const CREDS_FILE   = '/home/momo/.openclaw/workspace/secrets/bauhaus-ig.json';

// ── Titles (1-indexed) ────────────────────────────────────────────────────
const TITLES = [
  null, // index 0 unused
  "Composition with Circles","Grid Study","Triangle Harmony","Concentric Forms",
  "Diagonal Tension","Staircase","Radial Burst","Color Blocks","Arch Study",
  "Point and Line to Plane","Weaving Pattern","Mechanical Ballet","Typography Grid",
  "Golden Section","Shadow Play","Clock Tower","Suprematist Homage","Industrial Rhythm",
  "Color Theory","Architectural Plan","Tessellation","Suspension Bridge","Dance Notation",
  "Spectrum Analysis","Nested Frames","Photomontage Abstract","Furniture Study",
  "Rhythm and Blues","Eye of the Bauhaus","Final Composition","Pendulum Motion",
  "Cityscape","Spiral Staircase","Chess Board","Signal Flags","Counterweight",
  "Map Fragment","Propeller","Domino Effect","Kaleidoscope","Orbit","Brick Wall",
  "Sound Wave","Compass Rose","Totem","Scaffolding","Abacus","Labyrinth","Semaphore",
  "Prism","Molecule","Venetian Blinds","Target Practice","Origami","Metronome",
  "Typewriter Keys","Windmill","Circuit Board","Hourglass","Grand Finale",
  "Rotating Squares","Bauhaus Poster","Piano Keys","Sundial","Suspension","Elevation",
  "Gears Interlocking","Ripple","Flagpole","Cross Section","Lattice","Lighthouse",
  "Pulse","Bookshelf","Canopy","Pinwheel","Amphitheater","Periscope","Dominos Arranged",
  "Bauhaus Garden","Trapeze","Honeycomb","Lever and Fulcrum","Crown","Wavelength",
  "Drawbridge","Pixel Grid","Gyroscope","Lantern","Erosion","Pendulums in Sync",
  "Mosaic","Antenna Array","Tightrope","Stained Glass","Parachute","Dice","Viaduct",
  "Carousel","Century Mark","Ziggurat","Pulley System","Aqueduct","Barcode",
  "Constellation","Ferris Wheel","Guilloche","Drawers","Rocket","Opus Finale",
  "Watchtower","Pendulum Clock","Butterfly Wings","Rail Yard","Sundial Shadow",
  "Venetian Mask","Turbine","Torii Gate","Puzzle Pieces","Pendulum Wave","Amphora",
  "Crossroads","Chandelier","Fortress Wall","Dandelion","Accordion","Satellite Dish",
  "Candelabra","Domino Chain","Mosaic Floor","Seismograph","Kite","DNA Helix",
  "Bell Tower","Nautilus","Telescope","Catapult","Abacus Frame","Flower Press",
  "Marionette","Suspension Cable","Snowflake","Kaleidoscope II","Paper Airplane",
  "Scaffold Grid","Metronome Row","Flame","Anvil","Chevron Stack","Ship Hull",
  "Perforated Screen","Zigzag Path","Canopy Tent","Torus","Rowing Oars","Megaphone",
  "Atomic Model","Drawbridge Up","Tessellated Fish","Ventilation Grid","Waterfall",
  "Panopticon","Crown Jewels","Tuning Fork","Tree Rings","Crane","Iris","Waffle Grid",
  "Compass Needle","Hammock","Pinball","Rope Knot","Terrarium","Semaphore Tower",
  "Tangram","Escalator","Zodiac Wheel","Plumb Line","Xylophone","Funicular",
  "Drawers Open","Heliostat","Woven Basket","Signal Light","Fractal Tree","Portcullis",
  "Gyroscope II","Shield","Sextant","Quilt","Typeface Study","Oil Derrick",
  "Vinyl Record","Trebuchet","Mosaic Star","Astrolabe","Organ Pipes",
  "Drawbridge Chains","Pagoda","Bicentennial","Armillary Sphere","Basket Weave",
  "Cog Railway","Mandala","Pennant String","Orrery","Stacking Rings","Weather Vane",
  "Scaffolding II","Prism Rainbow","Perforated Facade","Aerial View","Silo Cluster",
  "Gear Train","Fan Vaulting","Drawloom","Amphitheater II","Moebius Strip",
  "Semaphore Grid","Parquet Floor","Hot Air Balloon","Resonance","Totem Pole II",
  "Trebuchet II","Crystalline","Cuckoo Clock","Anchor","Panopticon II","Spirograph",
  "Rampart","Anemometer","Rosette","Abacus III","Stairwell","Trident",
  "Suspension Bridge II","Dartboard","Venetian Window","Mill Wheel","Op Art Squares",
  "Coat of Arms","Plumbing","Maypole","Geode","Ballast","Kaleidoscope III",
  "Siege Tower","Magnetic Field","Crown Finale","Magnum Opus"
];

// ── Bauhaus principles (rotate by index) ─────────────────────────────────
const PRINCIPLES = [
  "Form follows function.",
  "Art and craft are one.",
  "Less is more.",
  "The eye is the window to the mind.",
  "Structure is freedom.",
];

// ── Evocative descriptions keyed loosely to title themes ─────────────────
// We generate these dynamically based on the title.
function getDescription(index, title) {
  // Deterministic but varied short descriptions
  const descriptions = {
    "Composition with Circles": "Circles nest and orbit in silent dialogue, each radius a deliberate decision. Pure geometry, pure intention.",
    "Grid Study": "The grid is not a cage — it is a compass. Every intersection a choice, every line a commitment.",
    "Triangle Harmony": "Three points in perfect tension, a form that cannot be simplified further. The triangle speaks in absolutes.",
    "Concentric Forms": "Ring within ring, each layer a deeper truth. The center holds still while the world radiates outward.",
    "Diagonal Tension": "The diagonal refuses to rest. It cuts across the static world and introduces kinetic energy into still space.",
    "Staircase": "Each step is both destination and departure. Rhythm made physical, ascent made visible.",
    "Radial Burst": "From a single origin, all lines flee toward the infinite — a controlled explosion of pure direction.",
    "Color Blocks": "Primary masses in conversation. The colors do not blend; they argue, agree, and coexist.",
    "Arch Study": "The arch resolves opposing forces into a single elegant gesture. Compression becomes grace.",
    "Point and Line to Plane": "Klee's lesson made manifest: from the smallest mark, entire worlds unfold.",
    "Weaving Pattern": "Over and under, warp and weft — the loom as logic, the textile as theorem.",
    "Mechanical Ballet": "Gears perform their choreography without rehearsal. Every rotation is a pas de deux of cause and effect.",
    "Typography Grid": "Letters submit to the grid and gain power from it. The page becomes architecture.",
    "Golden Section": "Nature's own proportion, borrowed by the workshop. Beauty with a mathematical spine.",
    "Shadow Play": "Light defines the form; shadow reveals the volume. The unseen half completes the whole.",
    "Clock Tower": "Time given a body. Each hand a vector, each face a plane awaiting its moment.",
    "Suprematist Homage": "After Malevich, the square floats free. Color liberated from representation.",
    "Industrial Rhythm": "The factory floor has its own music — stamping, turning, repeating in faithful time.",
    "Color Theory": "Itten's wheel made manifest. Contrast, harmony, and temperature dance in measured steps.",
    "Architectural Plan": "The building before the building. Lines that will one day hold sky.",
    "Tessellation": "No space wasted, no gap permitted. The plane is conquered by a single repeating truth.",
    "Suspension Bridge": "Cables sing under tension, towers rise from bedrock. Engineering as lyric poetry.",
    "Dance Notation": "Movement frozen into symbol — the body's arc rendered as line and angle.",
    "Spectrum Analysis": "The invisible made visible, frequency by frequency. Light confesses its hidden structure.",
    "Nested Frames": "Frame within frame, each boundary a new context. Where does the picture end?",
    "Photomontage Abstract": "Reality cut apart and reassembled more honestly than it ever was whole.",
    "Furniture Study": "The chair is not decoration — it is a problem solved in three dimensions.",
    "Rhythm and Blues": "Two forces in counterpoint. The blue retreats; the rhythm advances. Neither wins.",
    "Eye of the Bauhaus": "The school watches back. A lens focused on the intersection of seeing and making.",
    "Final Composition": "Every element earned its place. Nothing more to add; nothing left to remove.",
    "Pendulum Motion": "The arc of the pendulum inscribes certainty. Physics made geometric, time made visible.",
    "Cityscape": "Rectangles stack into skyline. The city is a composition only altitude can read.",
    "Spiral Staircase": "Ascent as rotation. The eye climbs in a helix toward a vanishing point of light.",
    "Chess Board": "The battlefield of pure logic. Sixty-four squares, infinite possibility, absolute rules.",
    "Signal Flags": "Color at a distance is language. The semaphore alphabet speaks in bold primary strokes.",
    "Counterweight": "Balance achieved not by sameness but by exact opposition. Mass speaks to mass across a fulcrum.",
    "Map Fragment": "A piece of the territory — borders, contours, the geometry of somewhere specific.",
    "Propeller": "The spiral blade converts rotation to thrust. Motion made purposeful through form.",
    "Domino Effect": "One fall initiates all falls. Causality made tangible and beautiful.",
    "Kaleidoscope": "Symmetry multiplied until it becomes hypnotic. The fragment becomes the whole.",
    "Orbit": "The ellipse of inevitability. Gravity described as a path, attraction as geometry.",
    "Brick Wall": "Each unit identical; the whole, irreducible. The wall is more than the sum of its bricks.",
    "Sound Wave": "Pressure made visible — the ear's experience translated for the eye to understand.",
    "Compass Rose": "All directions at once, emanating from a single still center. Navigation made beautiful.",
    "Totem": "Stacked symbols ascending toward meaning. Vertical accumulation as cultural grammar.",
    "Scaffolding": "The structure beneath the structure. Temporary geometry that makes permanence possible.",
    "Abacus": "The original digital computer — beads in binary, calculation made tangible.",
    "Labyrinth": "One path, infinite confusion. The maze is a meditative argument with direction.",
    "Semaphore": "The body becomes code. Arms extended at angles transmit meaning across vast distances.",
    "Prism": "White light confesses its components. The prism is an honest instrument.",
    "Molecule": "Bonds between atoms, angles of attachment — chemistry drawn as a diagram of belonging.",
    "Venetian Blinds": "Horizontal slats parse the light into measured intervals. The window becomes a rhythm.",
    "Target Practice": "Concentric rings converging on a center — the geometry of intention and precision.",
    "Origami": "The fold as construction method. A single sheet, transformed without addition or subtraction.",
    "Metronome": "The tick is the teacher. Time divided into equal, democratic intervals.",
    "Typewriter Keys": "A grid of letters, each in its fixed place, awaiting the finger's command.",
    "Windmill": "The wind made workable. Rotation harvested from the invisible and put to use.",
    "Circuit Board": "Copper pathways carry invisible current. The board is a map of electrical intention.",
    "Hourglass": "Sand as clock. The narrow neck is the present — everything else is past or future.",
    "Grand Finale": "All the forms return for their final bow. The composition resolves into silence.",
    "Rotating Squares": "The square spins and becomes something else. Rotation reveals hidden symmetries.",
    "Bauhaus Poster": "The manifesto compressed into a single image. Typography, geometry, purpose.",
    "Piano Keys": "Black and white in strict alternation, each gap precisely measured. Music before sound.",
    "Sundial": "The shadow is the hand. Light becomes clock; the gnomon points toward noon.",
    "Suspension": "Gravity acknowledged and elegantly deferred. The hanging form is a negotiation.",
    "Elevation": "The building seen from the side, all depth removed. Architecture as pure drawing.",
    "Gears Interlocking": "Tooth meets tooth in perfect mechanical sympathy. Torque transfers through geometry.",
    "Ripple": "One point of contact, infinite rings of consequence. Disturbance made visible.",
    "Flagpole": "The vertical absolute. A line drawn between earth and sky, claiming the space between.",
    "Cross Section": "The interior revealed. The cut exposes what enclosure hides.",
    "Lattice": "The grid made three-dimensional, projected flat. Depth implied by diagonal.",
    "Lighthouse": "A point of light that defines the darkness around it. The beacon is a form.",
    "Pulse": "The heartbeat as waveform. Life's rhythm abstracted into peaks and valleys.",
    "Bookshelf": "Rectangles ranked by height. The library is a composition waiting to be read.",
    "Canopy": "The curve that shelters. Geometry in service of protection.",
    "Pinwheel": "Wind made visible in rotation. The playful cousin of the turbine and the fan.",
    "Amphitheater": "The semicircle of attention. All sight lines converge on a single point of presence.",
    "Periscope": "Mirrors redirect the eye around obstacles. The invisible becomes navigable.",
    "Dominos Arranged": "The patience of arrangement before the cascade. Potential energy given beautiful form.",
    "Bauhaus Garden": "Nature submitted to the grid, then set gently free. Order and growth in dialogue.",
    "Trapeze": "The arc of trust. A body suspended between two fixed points, momentarily free.",
    "Honeycomb": "The hexagon is nature's most efficient answer. The bee solved the packing problem first.",
    "Lever and Fulcrum": "One point transforms all force. Archimedes' diagram made permanent.",
    "Crown": "Radial points ascending from a base ring. Authority made geometric.",
    "Wavelength": "Distance between crests — the measure of light, sound, water. Energy has a period.",
    "Drawbridge": "The hinge as drama. A road that chooses when to be a road.",
    "Pixel Grid": "The raster reveals itself. Zoomed to its atomic unit, the image becomes pure geometry.",
    "Gyroscope": "Rotation that resists change of direction. Stability achieved through spinning.",
    "Lantern": "Light contained and directed by form. The shade is not decoration — it is function.",
    "Erosion": "Time's mark on form. Subtraction as creative force; the worn edge as truth.",
    "Pendulums in Sync": "Individual periods finding common rhythm. Synchrony emerging from chaos.",
    "Mosaic": "A thousand small truths composing a single large image. The fragment serves the whole.",
    "Antenna Array": "Receivers arrayed for maximum gain. The geometry of listening.",
    "Tightrope": "One dimension of travel, the rest negotiated through balance. The line between.",
    "Stained Glass": "Color held in lead tracery. The window as painting painted with light.",
    "Parachute": "The canopy that slows descent. Fabric geometry engineered for controlled falling.",
    "Dice": "Six faces, each a claim. The cube democratizes chance.",
    "Viaduct": "Arches multiplied into infrastructure. Roman logic extended across the valley.",
    "Carousel": "Rotation with cargo. The circle carries and returns what it takes.",
    "Century Mark": "One hundred — the decimal milestone. The grid counts its own accomplishment.",
    "Ziggurat": "Platforms stacked in diminishing sequence toward the sky. Sacred geometry in clay.",
    "Pulley System": "Rope over wheel, force redirected. Mechanical advantage made elegant.",
    "Aqueduct": "Gradient engineered across distance. Water finds its level through human patience.",
    "Barcode": "Data encoded in the width of silence between lines. The machine reads what the eye misses.",
    "Constellation": "Dots joined by imagination into myth. The map we drew across the night.",
    "Ferris Wheel": "The circle made inhabitable. Rotation offers vantage in exchange for surrender.",
    "Guilloche": "Engraved interlocking curves that defeat duplication. Security through complexity.",
    "Drawers": "The rectangle repeated and stacked. Storage as architecture; organization as form.",
    "Rocket": "Mass concentrated into a point, aimed at escape velocity. Geometry as ambition.",
    "Opus Finale": "The great work completed. Form and function, reconciled at last.",
    "Watchtower": "Height as strategy. The elevated point commands its radius of vision.",
    "Pendulum Clock": "Oscillation counted and accumulated into hours. The swing of certainty.",
    "Butterfly Wings": "Bilateral symmetry in flight. Nature's Rorschach, engineered for lift.",
    "Rail Yard": "Parallel lines branching at precise angles. The grammar of directed motion.",
    "Sundial Shadow": "The shadow moves; the stone does not. The sun writes its diary in dark lines.",
    "Venetian Mask": "Symmetry conceals identity while revealing character. The mask is an honest face.",
    "Turbine": "Curved blades extract energy from flow. The wind's work, geometrically harvested.",
    "Torii Gate": "Two uprights, two crossbeams — a threshold between the mundane and the sacred.",
    "Puzzle Pieces": "Interlocking forms that know exactly where they belong. Geometry as belonging.",
    "Pendulum Wave": "Multiple pendulums, different periods, generating collective patterns from individual motion.",
    "Amphora": "The vessel that remembers its contents. Form evolved over millennia through use.",
    "Crossroads": "The X at the center of everything. Where all paths intersect, all choices collapse.",
    "Chandelier": "Light distributed downward from a radial center. Illumination made ceremonial.",
    "Fortress Wall": "Thick, low, and patient. The wall is a form that believes in duration.",
    "Dandelion": "Radial seeds awaiting wind. Dispersal designed as a perfect sphere.",
    "Accordion": "Folded air made musical. The bellows expand and contract like mechanical breathing.",
    "Satellite Dish": "The parabola focuses signal from the sky. Geometry that listens.",
    "Candelabra": "Branches of light ascending from a common trunk. The family tree of flame.",
    "Domino Chain": "Topology of cause and effect. The line between standing and fallen.",
    "Mosaic Floor": "Ten thousand tiles beneath ten thousand feet, patiently holding their pattern.",
    "Seismograph": "The earth's trembling transcribed. Geology made legible through the moving needle.",
    "Kite": "Diamond balanced against the wind. Flight without wings, tethered to ground.",
    "DNA Helix": "The blueprint coiled around itself. Information stored in the geometry of the spiral.",
    "Bell Tower": "Height and hollow, together producing resonance. The tower is an instrument.",
    "Nautilus": "The living logarithm. Growth that never forgets its own proportion.",
    "Telescope": "Lenses aligned to bring the distant close. Geometry as a tool for curiosity.",
    "Catapult": "Potential energy stored in tension, released in an arc. Physics made wood and rope.",
    "Abacus Frame": "The empty frame awaits calculation. Structure before function.",
    "Flower Press": "The specimen between two planes, dried to perfect flatness. Nature made archivable.",
    "Marionette": "Joints and strings, geometry in motion. The puppet's dance is a kinematic diagram.",
    "Suspension Cable": "The catenary curve, loaded and patient. Math made structural.",
    "Snowflake": "Hexagonal symmetry that never repeats. Six-fold form, infinitely varied.",
    "Kaleidoscope II": "The second mirror changes everything. Symmetry doubled is not merely symmetry — it transcends.",
    "Paper Airplane": "One fold at a time, the flat sheet learns to glide. Origami's utilitarian cousin.",
    "Scaffold Grid": "The temporary skeleton of construction. Order imposed before beauty begins.",
    "Metronome Row": "A line of tickers, each at its own tempo, together generating complex rhythm.",
    "Flame": "The teardrop of combustion. A form with no hard edge, always consuming itself.",
    "Anvil": "Mass concentrated into service. The anvil's geometry is the geometry of resistance.",
    "Chevron Stack": "The V repeated until it becomes a forest of arrows, all pointing the same direction.",
    "Ship Hull": "The form that parts water with minimum resistance. Beauty born of hydrodynamics.",
    "Perforated Screen": "The surface that is also an absence. Pattern through subtraction.",
    "Zigzag Path": "The path that refuses the straight line but still arrives. Deviation as method.",
    "Canopy Tent": "The tensioned membrane overhead. Geometry sheltering geometry.",
    "Torus": "The donut of mathematics. A closed surface with no inside, no outside — only through.",
    "Rowing Oars": "Parallel levers in the hands of synchronized bodies. Propulsion through coordination.",
    "Megaphone": "The cone that amplifies. Form borrowed from acoustics to serve communication.",
    "Atomic Model": "Nucleus and orbiting shell — Bohr's diagram as clean geometry.",
    "Drawbridge Up": "The road in its vertical state. Infrastructure that changes its own topology.",
    "Tessellated Fish": "Escher's lesson: one form can tile the world if it knows its neighbors.",
    "Ventilation Grid": "The grid that breathes. Regularity in service of invisible circulation.",
    "Waterfall": "The vertical river. Gravity made visible as cascading form.",
    "Panopticon": "The circle of surveillance. Bentham's architecture of the seen.",
    "Crown Jewels": "Facets cut to maximize brilliance. Geometry in service of radiance.",
    "Tuning Fork": "Two tines vibrating in sympathy. Resonance given a handle.",
    "Tree Rings": "Concentric time. Each ring a year, each year a circle grown outward.",
    "Crane": "The cantilever that reaches. Engineering's long arm, balanced by counterweight.",
    "Iris": "The aperture of the eye — concentric muscle controlling the admission of light.",
    "Waffle Grid": "The grid made three-dimensional and edible. Structure and surface, unified.",
    "Compass Needle": "The form that knows north. A pointer of magnetic certainty.",
    "Hammock": "The catenary at rest. Two trees, one curve, the body in the center.",
    "Pinball": "Gravity and bumpers in negotiation. Chance made kinetic and geometric.",
    "Rope Knot": "Topology made tangible. The trefoil knot is a form that cannot be undone.",
    "Terrarium": "A small ecosystem in a geometric container. Nature bounded by glass and intention.",
    "Semaphore Tower": "High on the hill, arms extended. The visual telegraph predated electricity.",
    "Tangram": "Seven pieces, infinite arrangements. The ancient puzzle of form and fit.",
    "Escalator": "The staircase set in continuous motion. Steps that carry the patient traveler.",
    "Zodiac Wheel": "Twelve sectors of the ecliptic circle. The sky divided for human narrative.",
    "Plumb Line": "The weight on a string that defines true vertical. Gravity as instrument.",
    "Xylophone": "Graduated bars in a row — the keyboard of the percussion world.",
    "Funicular": "Two cars on one cable, ascending and descending in perfect counterbalance.",
    "Drawers Open": "The interior made exterior. The closed rectangle reveals its hidden compartments.",
    "Heliostat": "The mirror that tracks the sun. Reflection engineered to follow the source.",
    "Woven Basket": "Over, under, over, under — the logic of weaving, enacted in three dimensions.",
    "Signal Light": "The semaphore of the rails. Color and position communicate passage and danger.",
    "Fractal Tree": "Branches that contain their own branching. Self-similarity at every scale.",
    "Portcullis": "The iron grid that falls to bar the gate. Defense encoded in vertical bars.",
    "Gyroscope II": "Still spinning, still stable. The second gyroscope confirms the first law.",
    "Shield": "The geometry of protection. Heraldic form hardened against impact.",
    "Sextant": "Angles measured against the horizon. Navigation by the geometry of sky and sea.",
    "Quilt": "Fragments arranged into warmth. The pattern is both practical and profound.",
    "Typeface Study": "The letterform under examination. Serif, counter, bowl — anatomy of the written word.",
    "Oil Derrick": "The lattice tower over the hidden resource. Industrial geometry piercing the earth.",
    "Vinyl Record": "Concentric grooves carrying compressed sound. The circle that sings.",
    "Trebuchet": "Counterweight, arm, sling — the physics of siege rendered in elegant leverage.",
    "Mosaic Star": "Points radiating from a center, tiled outward. The star repeated until it becomes pavement.",
    "Astrolabe": "The sky folded flat. Circles within circles mapping the celestial sphere.",
    "Organ Pipes": "Columns of air at precise lengths. Pitch is the physics of the vertical.",
    "Drawbridge Chains": "The links that hold the road suspended. Each chain a line of controlled force.",
    "Pagoda": "Tiered roofs ascending in diminishing sequence. The sky met gradually, respectfully.",
    "Bicentennial": "Two hundred — the double century marked in form. The grid honors its own milestone.",
    "Armillary Sphere": "Rings nested at angles, modeling the celestial mechanics. A universe in wire.",
    "Basket Weave": "The classic interlace, flat and infinite. Weaving reduced to its essential pattern.",
    "Cog Railway": "The toothed rail that makes the impossible grade possible. The mountain yields to the gear.",
    "Mandala": "The sacred circle, filled with symmetrical meaning. Meditation made visible.",
    "Pennant String": "Triangles on a line, fluttering between poles. Celebration made geometric.",
    "Orrery": "The solar system in miniature. Planetary motion mechanized and made holdable.",
    "Stacking Rings": "Each ring smaller than the last. The tower narrows toward its inevitable point.",
    "Weather Vane": "The arrow that finds the wind's direction. The pivot makes all angles equal.",
    "Scaffolding II": "The second scaffold, more elaborate. Structure supporting structure in recursive patience.",
    "Prism Rainbow": "The spectrum extracted from white. Seven colors hidden in one, revealed by glass.",
    "Perforated Facade": "The building that is also a screen. The hole is as important as the wall.",
    "Aerial View": "The city from above — all depth removed, all plan revealed. Geometry unmasked.",
    "Silo Cluster": "Cylinders gathered in productive proximity. Storage made monumental.",
    "Gear Train": "A sequence of gears transmitting and transforming torque. Mechanical logic in chain.",
    "Fan Vaulting": "Gothic ribs spreading from capital to ceiling. Structure as exuberant geometry.",
    "Drawloom": "The mechanized weaver's tool. Pattern punched in advance and then patiently executed.",
    "Amphitheater II": "The second bowl of attention. More rows, wider arcs, a larger audience for the form.",
    "Moebius Strip": "One surface, one edge — the topology that cannot be oriented. The inside is the outside.",
    "Semaphore Grid": "Multiple semaphores in array. The message multiplied across the visual field.",
    "Parquet Floor": "Geometric tile laid in interlocking herringbone. The floor as composition.",
    "Hot Air Balloon": "The envelope of heated air, lifting its basket. Buoyancy through containment.",
    "Resonance": "Frequencies finding their matching forms. The bridge and the note that unmade it.",
    "Totem Pole II": "The second column of carved meaning rises. Each face a chapter of the story.",
    "Trebuchet II": "The second siege engine, refined. The arc of the arm is longer, the counterweight heavier.",
    "Crystalline": "The lattice of atoms made visible. Crystal structure as geometry at molecular scale.",
    "Cuckoo Clock": "The clockwork that rewards punctuality with a small wooden bird.",
    "Anchor": "The heavy form that holds the floating form in place. Resistance as purpose.",
    "Panopticon II": "The second circle of surveillance. The eye in the center sees further now.",
    "Spirograph": "Circles rolling inside circles, tracing curves too complex for a free hand.",
    "Rampart": "The defensive embankment, geometric in plan. The angle of deflection calculated in advance.",
    "Anemometer": "Cups rotating in the wind, measuring what they catch. Speed made angular.",
    "Rosette": "Petals arrayed in radial symmetry. The flower as geometric proof.",
    "Abacus III": "The third abacus — more columns, more beads, more precision. Calculation deepened.",
    "Stairwell": "The staircase viewed from above — a spiral that organizes vertical travel.",
    "Trident": "Three tines from one handle. The sea's weapon is also a geometric argument.",
    "Suspension Bridge II": "The second span. More cable, more tower, more distance held in tension.",
    "Dartboard": "Concentric rings scored by proximity to center. The target as pure geometry.",
    "Venetian Window": "The arched window divided by a column into three lights. Light regulated by form.",
    "Mill Wheel": "Water turns wood turns stone turns grain. The circle in service of transformation.",
    "Op Art Squares": "Squares that vibrate. The eye cannot hold them still — they insist on motion.",
    "Coat of Arms": "Heraldic geometry encoding lineage and claim. The shield as visual biography.",
    "Plumbing": "Pipes joining at angles, carrying water through the wall's hidden logic.",
    "Maypole": "Ribbons braiding around the vertical axis. Dance made into textile.",
    "Geode": "Crystal interior hidden in dull exterior. The hollow rock's secret geometry.",
    "Ballast": "The heavy thing in the bottom of the boat that makes stability possible.",
    "Kaleidoscope III": "The third mirror added. Now the symmetry has no edge — it tiles infinity.",
    "Siege Tower": "The mobile scaffold that brings the attacker level with the defender.",
    "Magnetic Field": "Iron filings reveal the invisible lines of force. The field made seeable.",
    "Crown Finale": "The final crown. Points ascending in the last regal gesture before the end.",
    "Magnum Opus": "Two hundred and fifty compositions. The great work, complete at last — form, function, and beauty made whole."
  };

  return descriptions[title] || `A study in geometric form, exploring the visual language of ${title.toLowerCase()} through Bauhaus principles of clarity and purpose.`;
}

// ── Caption generator ─────────────────────────────────────────────────────
function generateCaption(index, title) {
  const principle = PRINCIPLES[(index - 1) % PRINCIPLES.length];
  const description = getDescription(index, title);
  const hashtags = '#bauhaus #generativeart #geometricart #abstractart #svgart #agentart #bauhaus.machina #dailyart #constructivism #modernism';

  const body = `${principle} No. ${index} — ${title}. ${description}`;
  return `${body}\n\n${hashtags}`;
}

// ── SVG → PNG ─────────────────────────────────────────────────────────────
async function convertSvgToPng(svgPath, outPath) {
  const paddedIndex = String(TITLES.indexOf(TITLES.find((_, i) => i > 0 && svgPath.includes(String(i).padStart(3, '0'))))).padStart(3, '0');
  
  await sharp(svgPath)
    .resize(800, 800, { fit: 'contain', background: '#FEFAE0' })
    .extend({ top: 140, bottom: 140, left: 140, right: 140, background: '#FEFAE0' })
    .flatten({ background: '#FEFAE0' })
    .png()
    .toFile(outPath);

  console.log(`✅ PNG written to ${outPath}`);
}

// ── Upload to Imgur ───────────────────────────────────────────────────────
async function uploadToImgur(pngPath) {
  const imageData = fs.readFileSync(pngPath).toString('base64');
  
  console.log('📤 Uploading to Imgur...');
  const response = await axios.post('https://api.imgur.com/3/image', {
    image: imageData,
    type: 'base64',
    name: path.basename(pngPath),
  }, {
    headers: {
      'Authorization': 'Client-ID 546c25a59c58ad7',
      'Content-Type': 'application/json',
    },
    timeout: 30000,
  });

  if (!response.data.success) {
    throw new Error(`Imgur upload failed: ${JSON.stringify(response.data)}`);
  }

  const url = response.data.data.link;
  console.log(`✅ Imgur URL: ${url}`);
  return url;
}

// ── Upload to tmpfiles.org (fallback) ─────────────────────────────────────
async function uploadToTmpfiles(pngPath) {
  const FormData = require('form-data');
  const form = new FormData();
  form.append('file', fs.createReadStream(pngPath));

  console.log('📤 Uploading to tmpfiles.org (fallback)...');
  const response = await axios.post('https://tmpfiles.org/api/v1/upload', form, {
    headers: form.getHeaders(),
    timeout: 30000,
  });

  if (!response.data || !response.data.data || !response.data.data.url) {
    throw new Error(`tmpfiles upload failed: ${JSON.stringify(response.data)}`);
  }

  // tmpfiles returns /tmp/XXXX path, convert to direct URL
  const url = response.data.data.url.replace('tmpfiles.org/', 'tmpfiles.org/dl/');
  console.log(`✅ tmpfiles URL: ${url}`);
  return url;
}

// ── Post to Instagram via Meta Graph API ─────────────────────────────────
async function postToInstagram(igUserId, token, imageUrl, caption) {
  const BASE = 'https://graph.facebook.com/v21.0';

  // Step 1: Create media container
  console.log('📸 Creating Instagram media container...');
  const containerRes = await axios.post(`${BASE}/${igUserId}/media`, null, {
    params: {
      image_url: imageUrl,
      caption: caption,
      access_token: token,
    },
    timeout: 30000,
  });

  const creationId = containerRes.data.id;
  if (!creationId) throw new Error(`No creation_id returned: ${JSON.stringify(containerRes.data)}`);
  console.log(`✅ Media container created: ${creationId}`);

  // Brief pause before publishing (Meta recommends a short delay)
  await new Promise(r => setTimeout(r, 3000));

  // Step 2: Publish
  console.log('🚀 Publishing to Instagram...');
  const publishRes = await axios.post(`${BASE}/${igUserId}/media_publish`, null, {
    params: {
      creation_id: creationId,
      access_token: token,
    },
    timeout: 30000,
  });

  const postId = publishRes.data.id;
  if (!postId) throw new Error(`No post id returned: ${JSON.stringify(publishRes.data)}`);
  console.log(`✅ Published! Post ID: ${postId}`);
  return postId;
}

// ── Main ──────────────────────────────────────────────────────────────────
async function main() {
  const dryRun = process.argv.includes('--dry-run');
  if (dryRun) console.log('🔍 DRY RUN MODE — no actual Instagram post will be made\n');

  // Load state
  const state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  const nextIndex = state.last_posted_index + 1;

  if (nextIndex > state.total_pieces) {
    console.log('🎉 All 250 pieces have been posted!');
    process.exit(0);
  }

  // Load credentials
  const creds = JSON.parse(fs.readFileSync(CREDS_FILE, 'utf8'));
  const { long_lived_token, bauhaus_machina_ig_id } = creds;

  // Determine SVG path
  // Files use: 01-09 (2-digit), 10-99 (no padding), 100+ (3-digit)
  function getSvgFilename(idx) {
    if (idx < 10) return `bauhaus_${String(idx).padStart(2, '0')}.svg`;
    return `bauhaus_${idx}.svg`;
  }
  let svgPath = path.join(BAUHAUS_DIR, getSvgFilename(nextIndex));
  if (!fs.existsSync(svgPath)) {
    throw new Error(`SVG not found: ${getSvgFilename(nextIndex)} in ${BAUHAUS_DIR}`);
  }

  const title = TITLES[nextIndex];
  if (!title) throw new Error(`No title for index ${nextIndex}`);

  console.log(`\n📋 Next post: #${nextIndex} — ${title}`);
  console.log(`📁 SVG: ${svgPath}\n`);

  // Generate caption
  const caption = generateCaption(nextIndex, title);
  console.log('📝 Caption:');
  console.log('─'.repeat(60));
  console.log(caption);
  console.log('─'.repeat(60));
  console.log(`\nCaption length (body only): ${caption.split('\n\n')[0].length} chars\n`);

  // Convert SVG → PNG
  await convertSvgToPng(svgPath, TMP_PNG);

  if (dryRun) {
    console.log('\n✅ DRY RUN complete. PNG is at:', TMP_PNG);
    console.log('   Run without --dry-run to post for real.');
    return;
  }

  // Upload image
  let imageUrl;
  try {
    imageUrl = await uploadToImgur(TMP_PNG);
  } catch (err) {
    console.warn(`⚠️  Imgur upload failed: ${err.message}`);
    console.log('   Trying tmpfiles.org fallback...');
    imageUrl = await uploadToTmpfiles(TMP_PNG);
  }

  // Post to Instagram
  const postId = await postToInstagram(bauhaus_machina_ig_id, long_lived_token, imageUrl, caption);

  // Archive PNG
  if (!fs.existsSync(ARCHIVE_DIR)) fs.mkdirSync(ARCHIVE_DIR, { recursive: true });
  const today = new Date().toISOString().split('T')[0];
  const archivePath = path.join(ARCHIVE_DIR, `${today}_bauhaus_${String(nextIndex).padStart(3, '0')}.png`);
  fs.copyFileSync(TMP_PNG, archivePath);
  console.log(`📦 Archived to: ${archivePath}`);

  // Update state
  state.last_posted_index = nextIndex;
  state.last_posted_date = today;
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
  console.log('💾 state.json updated');

  // Append to log
  let log = [];
  if (fs.existsSync(LOG_FILE)) {
    try { log = JSON.parse(fs.readFileSync(LOG_FILE, 'utf8')); } catch {}
  }
  log.push({ date: today, index: nextIndex, title, caption, ig_post_id: postId, image_url: imageUrl });
  fs.writeFileSync(LOG_FILE, JSON.stringify(log, null, 2));
  console.log('📒 log.json updated');

  // Git commit and push
  console.log('\n🔄 Committing and pushing...');
  try {
    execSync(`cd "${REPO_ROOT}" && git add -A && git commit -m "Posted bauhaus #${String(nextIndex).padStart(3, '0')} - ${title}" && git push`, {
      stdio: 'inherit'
    });
    console.log('✅ Pushed to git');
  } catch (err) {
    console.warn('⚠️  Git push failed (non-fatal):', err.message);
  }

  console.log(`\n🎨 Successfully posted bauhaus #${nextIndex} — ${title}`);
  console.log(`   Post ID: ${postId}`);
}

main().catch(err => {
  console.error('\n❌ Error:', err.message);
  if (err.response) {
    console.error('   API response:', JSON.stringify(err.response.data, null, 2));
  }
  process.exit(1);
});
