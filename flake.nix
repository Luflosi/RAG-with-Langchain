{
  description = "Python shell flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, ... }: let
    lib = nixpkgs.lib;
    forAllSystems = function: lib.genAttrs [
      "aarch64-linux"
      "x86_64-linux"
    ] function;
  in {
    devShells = forAllSystems (system: let
      pkgs = nixpkgs.legacyPackages.${system};

      pythonEnv = pkgs.python3.withPackages (ps: with ps; [
        jupyterlab
        pandas
      ]);
    in {
      default = pkgs.mkShellNoCC {
        packages = [
          pythonEnv
        ];

        shellHook = ''
          export PYTHONPATH="${lib.getExe pythonEnv}"
        '';
      };
    });
  };
}
