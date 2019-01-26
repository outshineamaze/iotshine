const ghpages = require('gh-pages')
const execSync = require('child_process').execSync;

// Makes the script crash on unhandled rejections instead of silently
// ignoring them. In the future, promise rejections that are not handled will
// terminate the Node.js process with a non-zero exit code.
process.on('unhandledRejection', err => {
  throw err;
});

function genDocs() {
  try {
    execSync('gitbook build', { stdio: 'ignore' });
    return true;
  } catch (e) {
    return false;
  }
}

function uploadDocs() {
  try {
    ghpages.publish('_book', {
      branch: 'gh-pages',
      message: 'Auto-generated commit',
      repo: 'https://github.com/outshineamaze/iotshine.git'
    }, () => {});
  } catch (e) {
    return false;
  }
}
genDocs()
uploadDocs()

