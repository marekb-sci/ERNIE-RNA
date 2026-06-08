from pathlib import Path
from genomic_benchmarks.loc2seq import download_dataset

# 1. Download the dataset (data/genomic_benchmarks)
dataset_name = "demo_human_or_worm"
dest_path = "data/genomic_benchmarks"
download_dataset(dataset_name, dest_path=dest_path)

# 2. Define paths
dataset_path = Path(dest_path) / dataset_name


def write_split_fastas(split_name: str) -> None:
    split_path = dataset_path / split_name
    label_fastas = {}

    for class_dir in sorted(split_path.iterdir()):
        if not class_dir.is_dir():
            continue

        class_name = class_dir.name
        label_fasta_path = dataset_path / f"{split_name}_{class_name}.fasta"
        label_fastas[class_name] = open(label_fasta_path, "w")

        for seq_file in sorted(class_dir.iterdir()):
            if not seq_file.is_file():
                continue

            sequence = seq_file.read_text().strip()
            fasta_entry = f">{seq_file.stem} label={class_name}\n{sequence}\n"
            label_fastas[class_name].write(fasta_entry)

    for label_fasta_file in label_fastas.values():
        label_fasta_file.close()


# 3. Parse text files and write FASTA files for train/test and per-label splits
write_split_fastas("train")
write_split_fastas("test")