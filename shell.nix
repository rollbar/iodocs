let pkgs  = import <nixpkgs> {};
    pkgs' = import pkgs.path { overlays = [ (import ../vagrant-dev-vm/nix) ]; };
in pkgs'.callPackage ({
  nodejs_0_10,
  stdenv,
  writeScriptBin,
  bash,
  devEnvs,
  moxLib,
}:

let
node = nodejs_0_10;
config = moxLib.projectConfig ./. {
  env = {
  };
};

in

stdenv.mkDerivation rec {
  name = "iodocs-env";

  buildInputs = [
    node
    moxUpdate
  ];

  projectDir = toString ./.;
  hardeningDisable = [ "all" ];

  moxUpdate = writeScriptBin "mox-update" ''
    #!${bash}/bin/bash
    set -x

    cd ${projectDir}
    unset NIX_ENFORCE_PURITY

    git submodule update --init

    npm install
  '';

  provision = devEnvs.ensureProvisioned ''
    mox-update
  '';

  shellHook = ''
    cd ${projectDir}

    ${devEnvs.withNodeBin}

    ${provision}
  '';
} // config.env

) {}
