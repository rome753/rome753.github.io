
main()


function main() {
    const testFolder = './tests/';
    const fs = require('fs');

    fs.readdirSync(testFolder).forEach(file => {
        console.log(file);
    });
}
