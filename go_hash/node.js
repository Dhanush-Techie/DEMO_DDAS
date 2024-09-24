const http = require('http');
const fs = require('fs');

// File path to be chunked and sent
const filePath = "C:\\Users\\donha\\OneDrive\\Desktop\\Code_Surge_sih_NOMINATION_LETTER.docx";
//const filePath = "C:\\Users\\donha\\OneDrive\\Desktop\\Code_Surge.docx";
// const filePaath = path.join('C:', 'Users', 'rajku', 'OneDrive', 'Desktop', 'SIH', 'update ppt.pptx');

// Chunk size (adjust as per requirement)
const CHUNK_SIZE = 1024 * 1024; // 1MB chunk size
const options = {
  hostname: 'localhost',
  port: 8080, // The port Go server is running on
  path: '/upload',
  method: 'POST',
  headers: {
    'Content-Type': 'application/octet-stream',
  },
};

const req = http.request(options, (res) => {
  res.on('data', (chunk) => {
    console.log(`Response:${chunk}`);
  });
});

// Read file and send chunks
fs.createReadStream(filePath, { highWaterMark: CHUNK_SIZE })
  .on('data', (chunk) => {
    console.log(`Sending chunk: ${chunk.length} bytes`);
    req.write(chunk);
  })
  .on('end', () => {
    req.end();
  });