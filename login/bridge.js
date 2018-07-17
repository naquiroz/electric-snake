const childProcess = require('child_process')
const buffer = require('buffer')
const net = require('net')

const PORT = 9999
const HOST = '0'
var pythonProcess = null
var connected = null
var sock = net.Socket()
function spawnPython () {
  pythonProcess = childProcess.spawn('./venv/bin/python3', ['./back.py'])

  pythonProcess.stdout.on('data', (data) => {
    if (connected === null) {
      connected = false
      connectSocket()
    }
    console.log('[Python] ' + data)
  })

  pythonProcess.stderr.on('data', (data) => {
    console.log('[Python]' + data)
  })
  pythonProcess.on('exit', (code, number, signal) => {
    collectGrabageAndKill()
  })

  return pythonProcess
}
function sendRequest (request) {
  console.log('[Javascript] Request recieved, sending ' + request.toString())
  var string = JSON.stringify(request)
  var size = buffer.Buffer.byteLength(string)
  var chunkSize = buffer.Buffer.allocUnsafe(4)
  chunkSize.writeUInt32BE(size)
  sock.write(buffer.Buffer.concat([chunkSize, buffer.Buffer.from(string)]))
}

function connectSocket () {
  sock.connect(PORT, HOST, () => {
    console.log('[Javascript] Successfully connected')
    connected = true
  })
}
function collectGrabageAndKill () {
  sock.end()
  pythonProcess.kill()
  console.log('Garbage collected')
  process.exit()
}
function killPython () {
  if (pythonProcess === null) {
    console.log('[Javascript] Python backend not instantiated!')
  } else {
    console.log('[Javascript] Killing process...')
    sendRequest({command: 'kill'})
  }
}
exports.killPython = killPython
exports.spawnPython = spawnPython
