const qrcode = require('qrcode-terminal');
const ip = '169.254.8.1';
const url = `exp://${ip}:8081`;
console.log('\n\n=== Expo Go QR Code ===\n');
console.log(`Scan this QR code with Expo Go app:\n`);
qrcode.generate(url, {small: false}, function(qrcode) {
    console.log(qrcode);
    console.log(`\nDirect URL: ${url}`);
    console.log('\nInstructions:');
    console.log('1. Install Expo Go app on your phone');
    console.log('2. Scan the QR code above with Expo Go');
    console.log('3. Make sure your phone is on the same network\n');
});
