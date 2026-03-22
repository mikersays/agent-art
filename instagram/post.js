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

// ── Caption generator ─────────────────────────────────────────────────────
function generateCaption(index, title) {
  const hashtags = '#bauhaus #generativeart #geometricart #abstractart #svgart #agentart #bauhausmachina #dailyart #constructivism #modernism';
  return `${title}\n\n${hashtags}`;
}

// ── SVG → PNG ─────────────────────────────────────────────────────────────
// Output: 1080×1350 (4:5 Instagram portrait ratio)
// Layout: artwork centered at 980×980 on black canvas, 50px black border all sides
async function convertSvgToPng(svgPath, outPath) {
  const CANVAS_W = 1080;
  const CANVAS_H = 1350;
  const ART_SIZE = 980; // artwork area (square, centered horizontally)
  const ART_TOP  = Math.floor((CANVAS_H - ART_SIZE) / 2); // vertically centered
  const ART_LEFT = Math.floor((CANVAS_W - ART_SIZE) / 2);
  const BORDER   = '#000000';

  // Render SVG into ART_SIZE square, then composite onto black canvas
  const artBuffer = await sharp(svgPath)
    .resize(ART_SIZE, ART_SIZE, { fit: 'contain', background: BORDER })
    .flatten({ background: BORDER })
    .png()
    .toBuffer();

  await sharp({
    create: { width: CANVAS_W, height: CANVAS_H, channels: 3, background: BORDER }
  })
    .composite([{ input: artBuffer, top: ART_TOP, left: ART_LEFT }])
    .png()
    .toFile(outPath);

  console.log(`✅ PNG written to ${outPath} (${CANVAS_W}×${CANVAS_H}, black border)`);
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
