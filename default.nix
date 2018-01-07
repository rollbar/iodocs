{ pkgs, writeScript, moxLib }:

let

config = moxLib.projectConfig ./. {
  enabled = {};
};

in

config.serviceInEnv "servers" "iodocs" ''
  exec node app.js
''
