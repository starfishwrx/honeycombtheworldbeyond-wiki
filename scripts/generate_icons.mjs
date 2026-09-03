import { deflateSync } from 'node:zlib';
import { writeFileSync } from 'node:fs';
import { join } from 'node:path';

function crc32(buf) {
  let table = [];
  for (let i = 0; i < 256; i++) {
    let c = i;
    for (let k = 0; k < 8; k++) {
      c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
    }
    table[i] = c;
  }
  let c = 0xFFFFFFFF;
  for (let i = 0; i < buf.length; i++) {
    c = table[(c ^ buf[i]) & 0xFF] ^ (c >>> 8);
  }
  return (c ^ 0xFFFFFFFF) >>> 0;
}

function makeChunk(type, data) {
  const len = data.length;
  const chunk = Buffer.alloc(12 + len);
  chunk.writeUInt32BE(len, 0);
  chunk.write(type, 4, 4, 'ascii');
  data.copy(chunk, 8);
  const typeAndData = chunk.subarray(4, 8 + len);
  chunk.writeUInt32BE(crc32(typeAndData), 8 + len);
  return chunk;
}

function createPng(width, height, drawFn) {
  const sig = Buffer.from([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]);
  
  // IHDR
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(width, 0);
  ihdr.writeUInt32BE(height, 4);
  ihdr[8] = 8; // bit depth
  ihdr[9] = 6; // RGBA
  ihdr[10] = 0; // compression
  ihdr[11] = 0; // filter
  ihdr[12] = 0; // interlace
  const ihdrChunk = makeChunk('IHDR', ihdr);

  // Raw image data with filter byte 0 at each scanline
  const raw = Buffer.alloc(height * (1 + width * 4));
  for (let y = 0; y < height; y++) {
    const rowOffset = y * (1 + width * 4);
    raw[rowOffset] = 0; // filter None
    for (let x = 0; x < width; x++) {
      const pixelOffset = rowOffset + 1 + x * 4;
      const [r, g, b, a] = drawFn(x, y, width, height);
      raw[pixelOffset] = r;
      raw[pixelOffset + 1] = g;
      raw[pixelOffset + 2] = b;
      raw[pixelOffset + 3] = a;
    }
  }

  const idatData = deflateSync(raw);
  const idatChunk = makeChunk('IDAT', idatData);
  const iendChunk = makeChunk('IEND', Buffer.alloc(0));

  return Buffer.concat([sig, ihdrChunk, idatChunk, iendChunk]);
}

// Draw Honeycomb brand icon: deep teal background (#091c18), cyan hexagon ring (#4ecdc4), amber center (#f7d060)
function drawHoneycomb(x, y, w, h) {
  const cx = w / 2;
  const cy = h / 2;
  const dx = x - cx;
  const dy = y - cy;
  const dist = Math.sqrt(dx * dx + dy * dy);

  // Background rounded rect
  const cornerR = w * 0.18;
  const inCorner = (Math.abs(dx) > (w/2 - cornerR) && Math.abs(dy) > (h/2 - cornerR));
  if (inCorner) {
    const cdx = Math.abs(dx) - (w/2 - cornerR);
    const cdy = Math.abs(dy) - (h/2 - cornerR);
    if (Math.sqrt(cdx * cdx + cdy * cdy) > cornerR) {
      return [0, 0, 0, 0]; // transparent outside rounded corner
    }
  }

  // Hexagon distance approximation
  const qx = Math.abs(dx);
  const qy = Math.abs(dy);
  const hexDist = Math.max(qx * 0.866025 + qy * 0.5, qy);
  const hexR = w * 0.38;
  const hexW = Math.max(2, w * 0.06);

  // Amber center dot
  const centerR = w * 0.12;
  if (dist <= centerR) {
    return [247, 208, 96, 255]; // #f7d060
  }

  // Hexagon outline
  if (Math.abs(hexDist - hexR) <= hexW / 2) {
    return [78, 205, 196, 255]; // #4ecdc4
  }

  // Dark background #091c18
  return [9, 28, 24, 255];
}

const dir = 'd:/workspace/context-infrastructure/adhoc_jobs/honeycombtheworldbeyond_wiki';

const png48 = createPng(48, 48, drawHoneycomb);
writeFileSync(join(dir, 'icon-48.png'), png48);

const png192 = createPng(192, 192, drawHoneycomb);
writeFileSync(join(dir, 'icon-192.png'), png192);
writeFileSync(join(dir, 'apple-touch-icon.png'), png192);

console.log('Successfully generated icon-48.png, icon-192.png, apple-touch-icon.png');
