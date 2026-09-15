import json, os, yaml

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--source")
    args = parser.parse_args()

    with open(args.source) as f:
        manifest = yaml.safe_load(f)

    outdir = f"corpus/{manifest['source_id']}"
    os.makedirs(f"{outdir}/original", exist_ok=True)

    # Placeholder: you will later add real fetching logic
    with open(f"{outdir}/source.json", "w") as f:
        json.dump(manifest, f, indent=2)

    with open(f"{outdir}/fetch-log.json", "w") as f:
        f.write("{}")

if __name__ == "__main__":
    main()
