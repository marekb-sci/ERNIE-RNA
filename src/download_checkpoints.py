import argparse
from pathlib import Path

import gdown


CHECKPOINTS = {
    "checkpoint/ERNIE-RNA_checkpoint/ERNIE-RNA_pretrain.pt": "1CmNxJxgjDhRoBdlDODFFjDNNzJMHVzmO",
    "checkpoint/ERNIE-RNA_ss_prediction_checkpoint/ERNIE-RNA_attn-map_ss_prediction_bpRNA-1m_checkpoint.pt": "1tvoHc66uQ796mqlbKgJrl-MiRPQGylR5",
    "checkpoint/ERNIE-RNA_ss_prediction_checkpoint/ERNIE-RNA_attn-map_frozen_ss_prediction_bpRNA-1m_checkpoint.pt": "1ii6XDkAsfVC--ZN2o3uiOcF5j9TTcvm7",
    "checkpoint/ERNIE-RNA_ss_prediction_checkpoint/ERNIE-RNA_attn-map_ss_prediction_RIVAS_checkpoint.pt": "1_0skCEMLWPxslnneDskTxgfBwkWlhZBe",
    "checkpoint/ERNIE-RNA_ss_prediction_checkpoint/ERNIE-RNA_attn-map_ss_prediction_RNA3DB_checkpoint.pt": "1CRuc1mo2wqfKxbv9UTlaXMWBZjuBAxDE",
    "checkpoint/ERNIE-RNA_ss_prediction_checkpoint/ERNIE-RNA_attn-map_ss_prediction_RNAStralign_checkpoint.pt": "1uyJJ48BG4Kw-D8tdSbH-K85i5qrqvSFm",
    "checkpoint/ERNIE-RNA_ss_prediction_checkpoint/ERNIE-RNA_attn-map_ss_prediction_bpRNA-1m-all_and_RNAStralign_checkpoint.pt": "1BQbXYXAQYpjm432zwJ_WoQHbivs093tx",
    "checkpoint/ERNIE-RNA_3d_clossness_checkpoint/ERNIE-RNA_3D_closeness_attnmap_dp16_finetuned.pt": "1YQ-FJXFnP0BzW-gJZGohHFlRCKM-jO5b",
    "checkpoint/ERNIE-RNA_UTR_MRL_checkpoint/ERNIE-RNA-UTR_ML_CNN_checkpoint.pt": "1YuI1oToq0b70hV5H7wgZ-FaObaxClHlf",
}


def main():
    parser = argparse.ArgumentParser(description="Download ERNIE-RNA checkpoints from Google Drive.")
    parser.add_argument("--force", action="store_true", help="Redownload files even if they already exist.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent

    for relative_path, file_id in CHECKPOINTS.items():
        output_path = repo_root / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if output_path.exists() and not args.force:
            print(f"Skipping existing file: {output_path}")
            continue

        print(f"Downloading {output_path.name}...")
        gdown.download(id=file_id, output=str(output_path), quiet=False)


if __name__ == "__main__":
    main()