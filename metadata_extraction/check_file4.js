const https = require('https');
const fs = require('fs');
const crypto = require('crypto');

function downloadAndHash(url, outputPath) {
    return new Promise((resolve, reject) => {
        const hash = crypto.createHash('blake2b');  // Create SHA-256 hash object
        const file = fs.createWriteStream(outputPath);  // Create write stream for saving file

        https.get(url, (response) => {
            if (response.statusCode !== 200) {
                reject(new Error(`Failed to download file: ${response.statusCode}`));
                return;
            }

            response.on('data', (chunk) => {
                hash.update(chunk);  // Update hash with chunk data
                file.write(chunk);  // Write chunk to file
            });

            response.on('end', () => {
                file.end();  // Close the write stream
                const hashValue = hash.digest('hex');  // Finalize the hash
                resolve(hashValue);
            });

            response.on('error', (err) => {
                reject(err);
            });
        }).on('error', (err) => {
            reject(err);
        });
    });
}

// Example usage
const url = 'https://web.mit.edu/16.070/www/lecture/hashing.pdf';
const outputPath = 'D:/Games/downloaded_again_file.pdf';  // Specify the local storage path
downloadAndHash(url, outputPath)
    .then(hashValue => {
        console.log(`SHA-256 Hash: ${hashValue}`);
    })
    .catch(err => {
        console.error(`Error: ${err.message}`);
    });
