const bridge = require('./login/bridge')
const electron = require('electron')

/** @description Makes e user window.
 */
function createWindow () {
  // Create the browser window.
  var win = new electron.BrowserWindow({width: 800,
    height: 600})
  // and load the index.html of the app.
  win.loadFile('index.html')
  // ESLint will warn about any use of eval(), even this one
  // eslint-disable-next-line
  win.eval = global.eval = function () {
    throw new Error(`Sorry, this app does not support window.eval().`)
  }
}

// function killBackend () {
// python.kill('SIGINT')
// }
electron.app.on('ready', createWindow)
electron.app.on('ready', bridge.spawnPython)
electron.app.on('window-all-closed', bridge.killPython)
