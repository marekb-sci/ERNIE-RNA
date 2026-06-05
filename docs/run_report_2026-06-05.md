# ERNIE-RNA Setup And Execution Report

Date: 2026-06-05

## Scope

Completed:

- Created a minimal `uv` inference environment.
- Downloaded the required model checkpoints into the repository's expected paths.
- Executed the README inference examples.
- Patched runtime issues that blocked inference on this machine.

## Environment

Environment created with `uv`:

```bash
uv venv --python 3.9 .venv-uv-infer
uv pip install --python .venv-uv-infer/bin/python -r requirements-uv-inference.txt
```

Validation commands:

```bash
.venv-uv-infer/bin/python -c "import extract_embedding, predict_ss_rna, predict_3d_clossness, predict_MRL; print('imports-ok')"
.venv-uv-infer/bin/python extract_embedding.py --help
.venv-uv-infer/bin/python predict_ss_rna.py --help
.venv-uv-infer/bin/python predict_3d_clossness.py --help
.venv-uv-infer/bin/python predict_MRL.py --help
```

Outcome:

- `uv` environment created successfully.
- Initial import failed because `torch==1.10.0` expects `pkg_resources`.
- Fixed by adding `setuptools==68.2.2` to `requirements-uv-inference.txt`.
- All four entry points then imported and their CLIs started correctly.

## Weight Download

The Google Drive URLs in the checkpoint text files did not download correctly with `gdown --fuzzy`; that path returned HTML viewer pages instead of binaries.

Working pattern:

```bash
gdown FILE_ID -O target/path.pt
```

Downloaded checkpoints:

- `checkpoint/ERNIE-RNA_checkpoint/ERNIE-RNA_pretrain.pt`
- `checkpoint/ERNIE-RNA_ss_prediction_checkpoint/ERNIE-RNA_attn-map_ss_prediction_bpRNA-1m_checkpoint.pt`
- `checkpoint/ERNIE-RNA_ss_prediction_checkpoint/ERNIE-RNA_attn-map_frozen_ss_prediction_bpRNA-1m_checkpoint.pt`
- `checkpoint/ERNIE-RNA_ss_prediction_checkpoint/ERNIE-RNA_attn-map_ss_prediction_RIVAS_checkpoint.pt`
- `checkpoint/ERNIE-RNA_ss_prediction_checkpoint/ERNIE-RNA_attn-map_ss_prediction_RNA3DB_checkpoint.pt`
- `checkpoint/ERNIE-RNA_ss_prediction_checkpoint/ERNIE-RNA_attn-map_ss_prediction_RNAStralign_checkpoint.pt`
- `checkpoint/ERNIE-RNA_ss_prediction_checkpoint/ERNIE-RNA_attn-map_ss_prediction_bpRNA-1m-all_and_RNAStralign_checkpoint.pt`
- `checkpoint/ERNIE-RNA_3d_clossness_checkpoint/ERNIE-RNA_3D_closeness_attnmap_dp16_finetuned.pt`
- `checkpoint/ERNIE-RNA_UTR_MRL_checkpoint/ERNIE-RNA-UTR_ML_CNN_checkpoint.pt`

Outcome:

- All downloaded files were validated as binary archives with expected large sizes.

## Code Changes

Changed files:

- `requirements-uv-inference.txt`
- `src/utils.py`
- `extract_embedding.py`
- `predict_ss_rna.py`
- `predict_3d_clossness.py`
- `predict_MRL.py`

Rationale:

1. `requirements-uv-inference.txt`
   - Added `setuptools==68.2.2` because old Torch imports `pkg_resources` at runtime.

2. Device handling across inference scripts
   - Added shared device normalization in `src/utils.py`.
   - Scripts now accept device strings like `cpu`, `-1`, `0`, and `cuda:0`.
   - Scripts now fall back to CPU when CUDA is unavailable or unsupported by the installed PyTorch build.

3. `predict_MRL.py`
   - Fixed CPU inference path.
   - Removed the unconditional GPU-only wrapping assumption in practice by loading on the resolved device.
   - Added checkpoint key translation from:
     - `head.reductio_weight` -> `head.reductio_module.weight`
     - `head.reductio_bias` -> `head.reductio_module.bias`
   - This was necessary because the published checkpoint uses older parameter names.

## Executed README Examples

### 1. Embedding extraction

Command:

```bash
.venv-uv-infer/bin/python extract_embedding.py --seqs_path ./data/test_seqs.txt --save_path ./results/ernie_rna_representations/test_seqs_uv/ --device 0
```

First outcome:

- Failed with `RuntimeError: CUDA error: no kernel image is available for execution on the device`

Fix:

- Added CPU fallback device normalization.

Final outcome:

- Succeeded.
- Generated:
  - `results/ernie_rna_representations/test_seqs_uv/cls_embedding.npy`
  - `results/ernie_rna_representations/test_seqs_uv/all_embedding.npy`
  - `results/ernie_rna_representations/test_seqs_uv/attnmap.npy`

### 2. Secondary structure prediction

Commands:

```bash
.venv-uv-infer/bin/python predict_ss_rna.py --dataset_name bpRNA-1m --device 0 --seqs_path ./data/ss_prediction/bpRNA-1m_testseqs.fasta --save_path ./results/ernie_rna_ss_prediction/bpRNA-1m_test_results_uv/
.venv-uv-infer/bin/python predict_ss_rna.py --dataset_name RNA3DB --device 0 --seqs_path ./data/ss_prediction/rna3db_testseqs.fasta --save_path ./results/ernie_rna_ss_prediction/rna3db_test_results_uv/
.venv-uv-infer/bin/python predict_ss_rna.py --dataset_name bpRNA-new --device 0 --seqs_path ./data/ss_prediction/bpRNA-new_testseqs.fasta --save_path ./results/ernie_rna_ss_prediction/bpRNA-new_test_results_uv/
```

Outcome:

- All three commands succeeded.
- Generated CT outputs for finetuned and zeroshot predictions in the corresponding `_uv` result directories.

### 3. 3D closeness prediction

Command:

```bash
.venv-uv-infer/bin/python predict_3d_clossness.py --input_rna_file ./results/ernie_rna_3d_clossness/example.fasta --device 0 --visualize --output_dir ./results/ernie_rna_3d_clossness_uv --plot_dir ./results/ernie_rna_3d_clossness_uv/closeness_plots/
```

Outcome:

- Succeeded.
- Generated:
  - `results/ernie_rna_3d_clossness_uv/1gax_D_closeness_pred.npy`
  - `results/ernie_rna_3d_clossness_uv/5gup_EC_closeness_pred.npy`
  - `results/ernie_rna_3d_clossness_uv/closeness_plots/1gax_D_closeness_pred.png`
  - `results/ernie_rna_3d_clossness_uv/closeness_plots/5gup_EC_closeness_pred.png`

### 4. UTR MRL prediction

Command:

```bash
.venv-uv-infer/bin/python predict_MRL.py --data_roots ./data/MRL_data/seqs.fasta --device 0 --output_dir ./results/ernie_rna_utr_mrl_uv
```

First outcome:

- Failed while loading the published checkpoint because parameter names in the checkpoint did not match the current code.

Fix:

- Added checkpoint key translation in `predict_MRL.py`.

Final outcome:

- Succeeded.
- Generated `results/ernie_rna_utr_mrl_uv/prediction.txt`

## Warnings And Residual Notes

- This machine has an RTX 3060, but the installed `torch==1.10.0` build does not support `sm_86`; inference therefore ran on CPU by design after the fallback patch.
- `predict_MRL.py` emitted a scikit-learn version warning when loading `scaler.save`:
  - checkpoint scaler was serialized with scikit-learn `0.23.1`
  - current environment uses scikit-learn `1.3.0`
  - inference still completed and produced outputs

## Final Validation

- Language/tooling diagnostics on edited files reported no errors.
- All README inference examples completed successfully in the `uv` environment after the fixes above.