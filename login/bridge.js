const childProcess = require('child_process')

function spawnPython () {
  var process = childProcess.spawn('./venv/bin/python3', ['./back.py'])

  process.stdout.on('data', (data) => {
    console.log('[Python] ' + data)
  })

  process.stderr.on('data', (data) => {
    console.log('[Python]' + data)
  })

  return process
}

exports.spawnPython = spawnPython
