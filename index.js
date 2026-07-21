const packageJson = require('./package.json');

module.exports = {
  version: packageJson.version,
  name: packageJson.name,
  description: packageJson.description
};
