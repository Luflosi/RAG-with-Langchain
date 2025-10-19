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
      pkgs = import nixpkgs {
        inherit system;
        overlays = [
          (import ./nix/overlays.nix)
        ];
      };

      pythonEnv = pkgs.python3.withPackages (ps: with ps; [
        chromadb
        deepeval
        jupyterlab
        langchain
        langchain-community
        langchain-huggingface
        langchain-ollama
        langchain-openai
        # langchainhub
        sentence-transformers
        streamlit
        streamlit-jupyter
        ragas
      ]);
    in {
      default = pkgs.mkShellNoCC {
        packages = with pkgs; [
          pythonEnv
          nix-init
          git
          lix
        ];

        shellHook = ''
          export PYTHONPATH="${lib.getExe pythonEnv}"

          # Load OpenAI API key if this file exists
          source .OpenAI-API-Key.sh || true
        '';
      };
    });
  };
}
