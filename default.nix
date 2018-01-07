{ pkgs, writeScript, moxLib }:

let

config = moxLib.projectConfig ./. {
  enabled = true;
};

in

config.serviceInEnv "servers" "iodocs" ''
  exec node app.js
''
