# https://github.com/nix-community/nix-direnv#usage-example
{ pkgs ? import <nixpkgs> { } }:

let
  python-packages = ps: with ps; [
    beautifulsoup4
    requests
    qrcode
  ];
in

pkgs.mkShell {
  packages = with pkgs; [
    (python3.withPackages python-packages)
  ];
}
